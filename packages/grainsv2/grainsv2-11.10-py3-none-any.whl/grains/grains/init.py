# Import python libs
import asyncio
import re
import threading
import traceback
from typing import Coroutine, List


def __init__(hub):
    # Variables for use within this module only
    hub.grains.init.WAIT = {}
    hub.grains.init.NUM_WAITING = 0
    hub.grains.init.LAST_CORO = False

    # Set up the central location to collect all of the grain data points
    hub.grains.GRAINS = hub.pop.data.omap()
    hub.pop.sub.add(dyne_name="idem")
    hub.pop.sub.load_subdirs(hub.grains, recurse=True)


def _timeout():
    """
    signal.SIGALRM/signal.alarm doesn't work on windows, this is a way around it
    """
    raise TimeoutError("Timeout while collecting grain")


def cli(hub):
    hub.pop.config.load(["grains", "rend"], "grains")
    hub.grains.init.standalone()

    outputter = getattr(hub, f"output.{hub.OPT.rend.output}.display")
    if hub.OPT.grains.get("grains"):
        print(
            outputter(
                {item: hub.grains.GRAINS.get(item) for item in hub.OPT.grains.grains}
            )
        )
    else:
        # Print all the grains sorted by dict key
        sorted_keys = sorted(hub.grains.GRAINS.keys(), key=lambda x: x.lower())
        sorted_grains = {key: hub.grains.GRAINS[key] for key in sorted_keys}

        print(outputter(sorted_grains))


def standalone(hub):
    """
    Run the grains sequence in a standalone fashion, useful for projects without
    a loop that want to make a temporary loop or from cli execution
    """
    hub.pop.loop.start(hub.grains.init.collect())


async def collect(hub):
    """
    Collect the grains that are presented by all of the app-merge projects that
    present grains.
    """
    # Load up the subs with specific grains
    await hub.grains.init.process_subs()


def release(hub):
    """
    After a grain collection function runs, see if any waiting functions can continue
    """
    for grain in hub.grains.init.WAIT:
        if grain in hub.grains.GRAINS and not hub.grains.init.WAIT[grain].is_set():
            hub.log.debug(f"Done waiting for '{grain}'")
            hub.grains.init.WAIT[grain].set()


def release_all(hub):
    """
    Open all the gates!!!
    All grains collection coroutines are finished
    Ready or not let all waiting collection functions finish
    """
    for grain in hub.grains.init.WAIT.keys():
        if not hub.grains.init.WAIT[grain].is_set():
            hub.log.info(f"Still waiting for grain '{grain}'")
            hub.grains.init.WAIT[grain].set()


def run_sub(hub, sub) -> List[Coroutine]:
    """
    Execute the contents of a specific sub, all modules in a sub are executed
    in parallel if they are coroutines
    """
    coros = []
    for mod in sub:
        if mod.__name__ == "init":
            continue
        hub.log.trace(f"Loading grains module {mod.__file__}")
        for func in mod:
            hub.log.trace(f"Loading grain in {func.__name__}()")
            # Ignore all errors in grain collection
            try:
                # timeout on the function if it takes too long
                alarm = threading.Timer(float(hub.OPT.grains.timeout), _timeout)
                alarm.start()
                ret = func()
                alarm.cancel()
                if asyncio.iscoroutine(ret):
                    coros.append(ret)
                else:
                    hub.log.trace(
                        f"Grains collection function is not asynchronous: {func}"
                    )
            except:  # pylint: disable=broad-except
                hub.log.critical(
                    f"Exception raised while collecting grains:\n{traceback.format_exc()}"
                )
            finally:
                hub.grains.init.release()

    return coros


async def process_subs(hub):
    """
    Process all of the nested subs found in hub.grains
    Each discovered sub is hit in lexicographical order and all plugins and functions
    exposed therein are executed in parallel if they are coroutines or as they
    are found if they are natural functions
    """
    coros = hub.grains.init.run_sub(hub.grains)
    for sub in hub.pop.sub.iter_subs(hub.grains, recurse=True):
        coros.extend(hub.grains.init.run_sub(sub))

    futures = asyncio.as_completed(
        coros, timeout=float(hub.OPT.grains.timeout), loop=hub.pop.Loop
    )

    def iter_futures(fs):
        """
        Iterate over futures and set a flag if we are on the last one, otherwise it could potentially wait forever
        """
        try:
            first = next(fs)
        except StopIteration:
            return

        try:
            yield next(fs)
            yield first
        except StopIteration:
            # There was only one
            print("asdf")
            hub.log.debug("Not waiting for any more grains")
            hub.grains.init.LAST_CORO = True
            yield first

        while True:
            yield next(fs)

    async def run_futures(fs, num_completed: int = 0):
        """
        Handle the incoming futures as they finish
        """
        for fut in iter_futures(fs):
            num_completed += 1
            if num_completed + hub.grains.init.NUM_WAITING >= len(coros):
                hub.grains.init.release_all()
            try:
                # timeout on the function if it takes too long
                alarm = threading.Timer(float(hub.OPT.grains.timeout), _timeout)
                alarm.start()
                await fut
                alarm.cancel()
            except (Exception, TimeoutError):  # pylint: disable=broad-except
                hub.log.critical(
                    f"Exception raised while collecting grains:\n{traceback.format_exc()}"
                )
            finally:
                # We're waiting forever for a grain, break out and reset
                if num_completed + hub.grains.init.NUM_WAITING >= len(coros):
                    return num_completed
                else:
                    hub.grains.init.release()
        return None

    num = await run_futures(futures)
    while num is not None:
        hub.log.debug("releasing all waiting coros")
        hub.grains.init.release_all()
        num = await run_futures(futures, num)
    await run_futures(futures)


async def wait_for(hub, grain: str) -> bool:
    """
    Wait for the named grain to be available
    Return True if waiting was successful
    False if all coroutines have been awaited and the waited for grain was never created
    """
    if hub.grains.init.LAST_CORO:
        return grain in hub.grains.GRAINS
    if grain not in hub.grains.GRAINS:
        hub.log.debug(f"Waiting for grain '{grain}'")
        if grain not in hub.grains.init.WAIT:
            hub.grains.init.WAIT[grain] = asyncio.Event()
        hub.grains.init.NUM_WAITING += 1
        await hub.grains.init.WAIT[grain].wait()
        hub.grains.init.NUM_WAITING -= 1
    return grain in hub.grains.GRAINS


async def clean_value(hub, key: str, val: str) -> str or None:
    """
    Clean out well-known bogus values.
    If it isn't clean (for example has value 'None'), return None.
    Otherwise, return the original value.
    """
    if val is None or not val or re.match("none", val, flags=re.IGNORECASE):
        return None
    elif re.search("serial|part|version", key):
        # 'To be filled by O.E.M.
        # 'Not applicable' etc.
        # 'Not specified' etc.
        # 0000000, 1234567 etc.
        # begone!
        if (
            re.match(r"^[0]+$", val)
            or re.match(r"[0]?1234567[8]?[9]?[0]?", val)
            or re.search(
                r"sernum|part[_-]?number|specified|filled|applicable",
                val,
                flags=re.IGNORECASE,
            )
        ):
            return None
    elif re.search("asset|manufacturer", key):
        # AssetTag0. Manufacturer04. Begone.
        if re.search(
            r"manufacturer|to be filled|available|asset|^no(ne|t)",
            val,
            flags=re.IGNORECASE,
        ):
            return None
    else:
        # map unspecified, undefined, unknown & whatever to None
        if re.search(r"to be filled", val, flags=re.IGNORECASE) or re.search(
            r"un(known|specified)|no(t|ne)? (asset|provided|defined|available|present|specified)",
            val,
            flags=re.IGNORECASE,
        ):
            return None
    return val
