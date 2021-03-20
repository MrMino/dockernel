# Dockernel

Makes it possible to utilize arbitrary docker images as Jupyter kernels.

## Installation, prerequisites

You will need Docker (obviously). For detailed instructions on how to install
it, see [Get Docker](https://docs.docker.com/get-docker/) page.

To install Dockernel, use Pip.

```
pip install dockernel
```

Make sure that the `jupyter` installation you wish to use with dockerized
kernels is in the same environment as `dockernel`. Keep in mind, that kernels
installed with Dockernel in one version may not necessarily work with a
different one.

## Usage

First, create a docker image that will host your kernel. This will require a
proper dockerfile. An example can be seen
[here](https://github.com/MrMino/dockernel/blob/master/example_dockerfile).

To build your image, use `docker build`. E.g. to build the example mentioned
above:

```
sudo docker build --tag my_kernel - < example_dockerfile
```

After that, use Dockernel to install the docker image as a Jupyter kernel:

```
dockernel install my_kernel --name dockerized_kernel
```

... and you should be ready to go! Fire up `jupyter notebook` and you should
see `dockerized_kernel` under "New" menu, or in the "Notebook" section of the
Launcher tab in `jupyter lab`.

## Issues or questions?

Post a new issue in the [Dockernell Issue Tracker at
GitHub](https://github.com/MrMino/dockernel/issues).
