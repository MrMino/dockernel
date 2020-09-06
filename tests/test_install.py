import pytest
from unittest.mock import Mock, sentinel
from dockernel.cli.install import generate_kernelspec_argv, image_digest
from dockernel.cli import main_arguments


class TestKernelspecArgvGeneration:
    IMAGE_NAME = 'example/image-name'

    @pytest.fixture
    def argv(self):
        return generate_kernelspec_argv(self.IMAGE_NAME)

    def test_argv_starts_with_usr_bin_env_python_m(self, argv):
        assert argv[:3] == ['/usr/bin/env', 'python', '-m']

    def test_argv_is_compatible_with_cli(self, argv):
        main_arguments.parse_args(argv[4:])

    def test_argv_contains_image_name(self, argv):
        argv[argv.index(self.IMAGE_NAME)] = sentinel.image_name
        assert sentinel.image_name in argv

    def test_argv_contains_connection_spec_path_template(self, argv):
        assert '{connection_file}' in argv

    def test_connection_file_path_is_in_the_right_place(self, argv):
        parsed = main_arguments.parse_args(argv[4:])
        assert parsed.connection_file == '{connection_file}'

    def test_image_name_is_in_the_right_place(self, argv):
        parsed = main_arguments.parse_args(argv[4:])
        assert parsed.image_name == self.IMAGE_NAME


class TestImageDigest:
    @pytest.fixture
    def image_attrs(self):
        return {'ContainerConfig': {'Hostname': None}}

    @pytest.fixture
    def docker_mock(self, image_attrs):
        client = Mock()
        image = client.images.get.return_value
        image.attrs = image_attrs
        return client

    def test_asks_about_the_correct_image(self, docker_mock):
        image_digest(docker_mock, sentinel.image_name)
        assert docker_mock.images.get.call_args == ((sentinel.image_name,),)

    def test_returns_image_hostname_from_given_client(self, docker_mock,
                                                      image_attrs):
        image_attrs['ContainerConfig'] = {'Hostname': sentinel.image_hostname}
        digest = image_digest(docker_mock, 'image-name')
        assert digest == sentinel.image_hostname
