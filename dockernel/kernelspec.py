"""Kernelspec installation facilities

Where term "kernelspec dir" is used, it references the directory in which
kernel.json file is present.
Where term "kernelspec store" is used, it references the directory where
jupyter will look for kernelspec dirs.
"""
import json
import string
from typing import List, Dict, Optional
from enum import Enum
from pathlib import Path


KERNELSPEC_FILENAME = 'kernel.json'
KERNELSPEC_STORE_DIRNAME = 'kernels'


class InterruptMode(str, Enum):
    signal = 'signal'
    message = 'message'


class Kernelspec:
    """Represents generic kernelspec for a kernel

    See jupyter-client docs on kernelspec files for explanation of arguments
    taken by the __init__ of this class.

    Use str() on objects of this class to render the kernelspec file contents.
    """
    def __init__(self,
                 argv: List[str], display_name: str, language: str,
                 interrupt_mode: Optional[InterruptMode] = None,
                 env: Optional[str] = None,
                 metadata: Optional[Dict[str, str]] = None
                 ) -> None:
        self._spec = {}
        self._spec['argv'] = argv
        self._spec['display_name'] = display_name
        self._spec['language'] = language

        if interrupt_mode is not None:
            self._spec['interrupt_mode'] = interrupt_mode
        if env is not None:
            self._spec['env'] = env
        if metadata is not None:
            self._spec['metadata'] = metadata

    def json(self):
        return json.dumps(self._spec)


# TODO: make sure windows path is expanded properly
def user_kernelspec_store(system_type: str) -> Path:
    """Return path to the place where user's kernelspecs are stored on given OS.

    Parameters
    ----------
    system_type
        Output of the builtin ``platform.system()``.
    kernel_id
        Internal identifier of the kernel to instal. Should be short and
        URL-friendly. Should contain only ASCII numbers, ASCII letters, hyphen,
        period, underscore.

    Raises
    ------
    ValueError
        If `system_type` is not one of the supported types.

    Returns
    -------
    Path
        Path object to the per-user directory where kernelspec dirs are stored.
    """

    if system_type == "Linux":
        kernelspec_dir_path = "~/.local/share/jupyter/kernels"
    elif system_type == "Windows":
        kernelspec_dir_path = r"%APPDATA%\jupyter\kernels"
    elif system_type == "Darwin":
        kernelspec_dir_path = "~/Library/Jupyter/kernels"
    else:
        raise ValueError(f'unknown system type: {system_type}')

    return Path(kernelspec_dir_path).expanduser()


def kernelspec_dir(kernelspec_store: Path, kernel_id: str) -> Path:
    """Return path to the kernelspec directory for a kernel with a given ID

    Parameters
    ----------
    kernelspec_store
        Path to the place kernelspec store where kernelspec dir should be
        placed.
    kernel_id
        Internal identifier of the kernel to instal. Should be short and
        URL-friendly. Must contain only ASCII numbers, ASCII letters, hyphen,
        period, underscore.

    Raises
    ------
    ValueError
        If `kernel_id` contains improper characters.

    Returns
    -------
    Path
        Path object to the directory where kernelspec should be installed.
    """
    allowed_characters = set(string.ascii_letters + string.digits + '_.-')
    if not set(kernel_id) <= allowed_characters:
        raise ValueError("kernel_id contains forbidden characters")

    return kernelspec_store / kernel_id


def ensure_kernelspec_store_exists(kernelspec_store: Path) -> None:
    """Creates the kernel store directory if one doesn't exist.

    Parameters
    ----------
    kernelspec_store
        Path object to the store. The directory must be named "kernels".

    Raises
    ------
    ValueError
        If given path is not a valid store path, i.e. it doesn't end with
        "kernels".
    """
    if kernelspec_store.name != KERNELSPEC_STORE_DIRNAME:
        raise ValueError("not a valid kernelspec store name: "
                         f"{repr(kernelspec_store.name)} "
                         "- should be 'kernels'.")
    if not kernelspec_store.exists():
        kernelspec_store.mkdir()


def install_kernelspec(kernelspec_dir: Path, kernelspec: Kernelspec) -> None:
    """Generate appropriate kernelspec under the specified path.

    Creates a directory for the kernelspec and populates it with the spec
    files.

    Parameters
    ----------
    kernelspec_dir
        Path object to the store where the kernel should be installed.
    kernelspec:
        Kernelspec to render.

    Raises
    ------
    ValueError
        If a kernelspec already exists, i.e. the kernelspec directory is
        present.
    """
    if kernelspec_dir.exists():
        raise ValueError(f"kernelspec already exists: {kernelspec_dir}.")

    kernelspec_dir.mkdir()
    kernelspec_file = kernelspec_dir/KERNELSPEC_FILENAME
    kernelspec_file.write_text(kernelspec.json())
