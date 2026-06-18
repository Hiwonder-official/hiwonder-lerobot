"""CLI entry points that delegate to the underlying lerobot commands."""

import sys


def _run(cmd: str) -> None:
    """Replace the current process with the given lerobot CLI command."""
    from importlib import import_module

    module_path, func_name = cmd.rsplit(":", 1)
    module = import_module(module_path)
    getattr(module, func_name)()


def calibrate() -> None:
    _run("lerobot.scripts.lerobot_calibrate:main")


def teleoperate() -> None:
    _run("lerobot.scripts.lerobot_teleoperate:main")


def record() -> None:
    _run("lerobot.scripts.lerobot_record:main")


def replay() -> None:
    _run("lerobot.scripts.lerobot_replay:main")


def train() -> None:
    _run("lerobot.scripts.lerobot_train:main")


def eval() -> None:
    _run("lerobot.scripts.lerobot_eval:main")


def find_port() -> None:
    _run("lerobot.scripts.lerobot_find_port:main")


def setup_motors() -> None:
    _run("lerobot.scripts.lerobot_setup_motors:main")


if __name__ == "__main__":
    print("Use 'hiwonder-<command>' — run 'hiwonder-calibrate --help' to get started.")
    sys.exit(0)
