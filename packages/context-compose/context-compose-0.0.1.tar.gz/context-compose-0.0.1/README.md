# context_compose

### Python utility library to compose context managers

## Motivation

When you want to use a dynamic combination of context managers together, and the builtin ways are too ugly or inflexible.

Turn this:

```python
import os

if __name__ == "__main__":
    if os.environ.get("DEBUG") and os.environ.get("PROFILE":
        with debugger(), profile():
            main()
    elif os.environ.get("DEBUG"):
        with debugger():
            main()
    elif os.environ.get("DEBUG"):
        with debugger():
            main()
```

Into this:

```python
import os

from context_compose import compose, impotent_manager


if __name__ == "__main__":
    managers = [
        debugger() if os.environ.get("DEBUG") else impotent_manager(),
        profile() if os.environ.get("PROFILE") else impotent_manager(),
    ]
    with compose(managers):
        main()

```

`impotent_manager` is a useful substitute when your code has a `with` block, you'd rather keep to a single pattern so a context manager _must_ be provided to it.

## How it works

Under the hood it uses [contextlib.ExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack) to layer context managers in list order.
