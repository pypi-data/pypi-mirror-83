

# ClickHouse query tools

Exposes ClickHouse internals to parse and manipulate ClickHouse queries.

## Install pre-built packages

You can install a pre-compiled package for your platform, for example, version 0.2-dev0 for python 3.7:

```
pip install dist/clickhouse_toolset-0.2.dev0-cp37-cp37m-linux_x86_64.whl
```

## Development

First, you need to clone the repo and its submodules.

```
git clone --recursive git@gitlab.com:tinybird/clickhouse-toolset.git
```

Then, you will compile the dependencies and the module itself. For this task you need to have gcc/g++ 8.

```
pip install --editable .
```

Another option is using some Makefile targets, e.g.

```
make build-3.7 test-3.7
```

### Generate pre-built packages

You have to install the `wheel` dependency: `pip install .[build]`, then, you can generate pre-compiled binaries for your platform using:

```
export $VERSION=<your_current_version>

python setup.py sdist bdist_wheel
python setup.py sdist
```

## Examples

Check tests directory

## Publish

1. Update VERSION in `setup.py`

2. Publish the test package for the version you want to use (use PYTHON_VERSION to use the version from you want to publish)

```
make publish-package PACKAGE=path/to/clickhouse-toolset.tar.gz REPOSITORY=test PYTHON_VERSION=3.8
```

3. Publish the production package

```
make publish-package PACKAGE=path/to/clickhouse-toolset.tar.gz REPOSITORY=production PYTHON_VERSION=3.8
```

## Docker

Build image:

```
docker build -t tinybird/chtoolset .
```

Compile the binaries from the container:

```
rm -rf ClickHouse/build && docker run --name chtoolset -v $PWD:/opt/chtoolset -it tinybird/chtoolset
```

Make tests inside the container (like running custom commands):

```
docker run --name chtoolset -v $PWD:/opt/chtoolset -it tinybird/chtoolset tail -f /dev/null
docker exec -it chtoolset /bin/bash
```
