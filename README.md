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

_Note for Linux users:

If you run into permission errors with `docker` or `dockernel` - either use
`sudo`, or follow the steps outlined in [Manage Docker as a non-root
user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
guide._

### Creating a Dockernel image

First, create a docker image that will host your kernel. This will require a
proper dockerfile. A full example for IPython kernel can be seen
[here](https://github.com/MrMino/dockernel/blob/master/example_dockerfile).

Most kernels take a path to a "connection file" (also called "control file" by
some kernels) as a CLI argument. This file contains all of the information
necessary to start up a kernel, including TCP ports to use, IP address, etc.

When running your container, Dockernel will supply this file and put it into a
predefined path in the container. This path will be given via an environment
variable visible in the container as `$DOCKERNEL_CONNECTION_FILE`.

Therefore, in order for the kernel to know the connection settings it should
use, you need to pass the contents of this variable in `CMD` of the container.
For example, for IPython kernel:

```
CMD python -m ipykernel_launcher -f $DOCKERNEL_CONNECTION_FILE
```

Or for the Rust kernel (Evcxr, see the
[example Rust
dockerfile](https://github.com/MrMino/dockernel/blob/master/example_dockerfile)):

```
CMD evcxr_jupyter --control_file $DOCKERNEL_CONNECTION_FILE
```

To build your image, use `docker build`. E.g. to build the example mentioned
above:

```
docker build --tag my_kernel - < example_dockerfile
```

### Installing your image as a Jupyter Kernel

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
