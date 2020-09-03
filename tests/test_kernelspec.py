from dockernel.kernelspec import Kernelspec, InterruptMode
import json
import pytest


def test_InterruptMode_has_proper_values():
    for mode in InterruptMode:
        assert mode.name == mode.value


class TestKernelspec:
    def test_kernelspec(self):
        data_given = {
            'argv': ['some', 'argument', 'vector'],
            'language': 'klingon',
            'display_name': 'test kernel',
            'interrupt_mode': 'signal',
            'env': {'var-a': 'val-a', 'var-b': 'val-b'},
            'metadata': {'meta-a': 'meta-val-a', 'meta-b': 'meta-val-b'}
        }

        data_from_kernelspec = json.loads(str(Kernelspec(**data_given)))

        assert data_given == data_from_kernelspec

    @pytest.mark.parametrize('interrupt_mode_enum', InterruptMode)
    def test_InterruptMode_enum_is_casted(self, interrupt_mode_enum):
        mandatory_args = {
            'argv': [], 'language': '', 'display_name': '',
        }

        kernelspec = Kernelspec(interrupt_mode=interrupt_mode_enum,
                                **mandatory_args)
        received_value = json.loads(str(kernelspec))['interrupt_mode']

        assert interrupt_mode_enum.value == received_value

    def test_optional_args(self):
        only_mandatory_args = {
            'argv': [], 'language': '', 'display_name': '',
        }
        Kernelspec(**only_mandatory_args)
