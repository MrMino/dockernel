from typing import List, Dict, Optional
from enum import Enum
import json


class InterruptMode(str, Enum):
    signal = 'signal'
    message = 'message'


class Kernelspec:
    """ Represents generic kernelspec for a kernel

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
        self.spec = {}
        self.spec['argv'] = argv
        self.spec['display_name'] = display_name
        self.spec['language'] = language

        if interrupt_mode is not None:
            self.spec['interrupt_mode'] = interrupt_mode
        if env is not None:
            self.spec['env'] = env
        if metadata is not None:
            self.spec['metadata'] = metadata

    def __str__(self):
        return json.dumps(self.spec)
