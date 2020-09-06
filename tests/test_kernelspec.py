import pytest
import json
from dockernel.kernelspec import (Kernelspec, InterruptMode,
                                  user_kernelspec_store, kernelspec_dir,
                                  ensure_kernelspec_store_exists,
                                  install_kernelspec)
from pathlib import Path


@pytest.fixture
def tmpdir(tmpdir):
    """Workaround for tmpdir being py.path.LocalPath instead of Path"""
    return Path(str(tmpdir))


@pytest.fixture
def kernelspec_dict():
    return {
        'argv': ['some', 'argument', 'vector'],
        'language': 'klingon',
        'display_name': 'test kernel',
        'interrupt_mode': 'signal',
        'env': {'var-a': 'val-a', 'var-b': 'val-b'},
        'metadata': {'meta-a': 'meta-val-a', 'meta-b': 'meta-val-b'}
    }


@pytest.fixture
def kernelspec(kernelspec_dict):
    return Kernelspec(**kernelspec_dict)


class TestInterruptMode:
    @pytest.mark.parametrize('enum', InterruptMode)
    def test_values_are_same_as_names(self, enum):
        assert enum.name == enum.value

    @pytest.mark.parametrize('enum', InterruptMode)
    def test_values_are_strings(self, enum):
        assert isinstance(enum.value, str)


class TestKernelspec:
    def test_kernelspec_renders_json_dict(self, kernelspec, kernelspec_dict):
        dict_from_kernelspec = json.loads(kernelspec.json())
        assert dict_from_kernelspec == kernelspec_dict

    @pytest.mark.parametrize('interrupt_mode', InterruptMode)
    def test_InterruptMode_enum_is_casted(self, interrupt_mode,
                                          kernelspec_dict):
        del kernelspec_dict['interrupt_mode']
        kernelspec = Kernelspec(interrupt_mode=interrupt_mode,
                                **kernelspec_dict)

        received_value = json.loads(kernelspec.json())['interrupt_mode']

        assert interrupt_mode.value == received_value

    def test_optional_args_are_optional(self):
        Kernelspec(argv=['cmd'], language='', display_name='')


class TestEnsureKernelspecStoreExists:
    @pytest.fixture
    def store(self, tmpdir):
        return tmpdir/'kernels'

    def test_store_dir_is_created_if_absent(self, store):
        assert not store.exists()
        ensure_kernelspec_store_exists(store)
        assert store.is_dir()

    def test_store_dir_is_not_created_if_present(self, store):
        store.mkdir()
        ensure_kernelspec_store_exists(store)

    def test_raises_ValueError_when_directory_name_is_not_store(self, tmpdir):
        with pytest.raises(ValueError):
            ensure_kernelspec_store_exists(tmpdir/'system32')


class TestKernelspecStoreDir:
    @pytest.mark.parametrize('system_type', ('Linux', 'Windows', 'Darwin'))
    def test_works_for_supported_platforms(self, system_type):
        user_kernelspec_store(system_type)

    def test_raises_TypeError_on_unknown_system(self):
        with pytest.raises(ValueError):
            user_kernelspec_store('unknown system type')


class TestKernelspecDir:
    def test_kernel_id_is_dir_name(self):
        store = Path('/path/to/kernels/')
        kernel_id = 'my-awesome-kernel'
        returned_path = kernelspec_dir(store, kernel_id)

        assert returned_path == store/kernel_id

    @pytest.mark.parametrize('bad_id', ('{bad}', '<very></bad>', '=+!~'))
    def test_raises_ValueError_when_given_bad_id(self, bad_id):
        with pytest.raises(ValueError):
            kernelspec_dir(Path(), bad_id)


class TestInstallKernelspec:
    @pytest.fixture
    def kernelspec_dir(self, tmpdir):
        return tmpdir/'my-kernel'

    @pytest.fixture
    def kernelspec_file(self, kernelspec_dir):
        return kernelspec_dir/'kernel.json'

    def test_raises_ValueError_if_kernelspec_exists(self, kernelspec_dir,
                                                    kernelspec):
        kernelspec_dir.mkdir()
        with pytest.raises(ValueError):
            install_kernelspec(kernelspec_dir, kernelspec)

    def test_creates_kernelspec_directory(self, kernelspec_dir, kernelspec):
        assert not kernelspec_dir.exists()
        install_kernelspec(kernelspec_dir, kernelspec)
        assert kernelspec_dir.is_dir()

    def test_creates_kernelspec_file(self, kernelspec_dir, kernelspec,
                                     kernelspec_file):
        assert not kernelspec_file.exists()
        install_kernelspec(kernelspec_dir, kernelspec)
        assert kernelspec_file.is_file()

    def test_populates_kernelspec_file_with_valid_json(self, kernelspec_dir,
                                                       kernelspec_file,
                                                       kernelspec):
        install_kernelspec(kernelspec_dir, kernelspec)
        json.loads(kernelspec_file.read_text())

    def test_populates_file_with_kernelspec_data(self, kernelspec_dir,
                                                 kernelspec_file, kernelspec):
        install_kernelspec(kernelspec_dir, kernelspec)
        text_contents = kernelspec_file.read_text()
        assert text_contents == kernelspec.json()
