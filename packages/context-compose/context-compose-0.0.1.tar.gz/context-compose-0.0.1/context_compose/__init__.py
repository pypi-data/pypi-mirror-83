from contextlib import contextmanager, ExitStack
from typing import List, ContextManager

@contextmanager
def compose(managers: List[ContextManager]):
    """
    Enter each context manager in the list `managers`, in order,
    and exit them in order
    """
    with ExitStack() as stack:
        for manager in managers:
            stack.enter_context(manager)
        yield


@contextmanager
def impotent_manager():
    """
    Context manager that does nothing. Useful for the negative branch
    when conditionally setting up context managers e.g.:

    profiler = profile_manager() if PROFILING else impotent_manager()
    with compose([profiler, ...]):
        ...
    """
    yield

