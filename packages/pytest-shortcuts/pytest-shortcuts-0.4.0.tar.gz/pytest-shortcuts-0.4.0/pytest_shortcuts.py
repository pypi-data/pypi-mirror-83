import shlex

import pytest


def pytest_addoption(parser):
    parser.addini(
        "shortcuts",
        default=[],
        type="linelist",
        help=(
            "A colon-separated list of extra shortcut options "
            "and their expanded list of args"
        ),
    )


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(early_config, parser, args):
    """Expand any shortcuts in the command line arguments.

    The shortcuts are expanded very early so as to allow the edited options to be
    processed by other plugins/parts of pytest.
    """
    shortcuts = dict(parse_shortcut(item) for item in early_config.getini("shortcuts"))
    add_command_line_options(shortcuts, parser)
    expand_shortcuts(shortcuts, args)


def add_command_line_options(shortcuts, parser):
    for shortcut, new_args in shortcuts.items():
        parser.addoption(
            shortcut,
            action="store_true",
            help="Shortcut for {}".format(" ".join(new_args)),
        )


def expand_shortcuts(shortcuts, raw_args):
    for shortcut, new_args in shortcuts.items():
        if shortcut in raw_args:
            pos = raw_args.index(shortcut)
            raw_args[pos : pos + 1] = new_args


def parse_shortcut(item):
    assert ":" in item, "Invalid shortcut definition"
    key, val = item.split(":", 1)
    assert key.startswith("--"), "Invalid shortcut definition"
    shortcut = key.strip()
    args = shlex.split(val.strip())
    return (shortcut, args)
