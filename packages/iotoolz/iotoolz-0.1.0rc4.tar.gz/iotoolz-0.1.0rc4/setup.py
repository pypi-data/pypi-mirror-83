# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iotoolz', 'iotoolz.extensions']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.4,<4.0.0',
 'cytoolz>=0.11.0,<0.12.0',
 'pydantic>=0.30',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0',
 'typing-extensions']

extras_require = \
{':sys_platform == "darwin" or sys_platform == "windows"': ['python-magic-bin>=0.4.0,<0.5.0'],
 ':sys_platform == "linux"': ['python-magic>=0.4.0,<0.5.0'],
 'all': ['boto3>=1.16.5,<2.0.0', 'minio>=6.0.0,<7.0.0'],
 'boto3': ['boto3>=1.16.5,<2.0.0'],
 'minio': ['minio>=6.0.0,<7.0.0']}

setup_kwargs = {
    'name': 'iotoolz',
    'version': '0.1.0rc4',
    'description': 'Consistent io iterface to read and write from/to both local and different remote resources (e.g. http, s3)',
    'long_description': '# iotoolz\n\n[![PyPI version](https://badge.fury.io/py/iotoolz.svg)](https://badge.fury.io/py/iotoolz)\n[![Build Status](https://travis-ci.com/e2fyi/iotoolz.svg?branch=master)](https://travis-ci.com/github/e2fyi/iotoolz)\n[![Coverage Status](https://coveralls.io/repos/github/e2fyi/iotoolz/badge.svg?branch=master)](https://coveralls.io/github/e2fyi/iotoolz?branch=master)\n[![Documentation Status](https://readthedocs.org/projects/iotoolz/badge/?version=latest)](https://iotoolz.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Downloads](https://pepy.tech/badge/iotoolz/month)](https://pepy.tech/project/iotoolz/month)\n\n`iotoolz` is an improvement over `e2fyi-utils` and is inspired partly by `toolz`.\n`iotoolz` is a lib to help provide a consistent dev-x for interacting with any IO resources.\nIt provides an abstract class `iotoolz.AbcStream` which mimics python\'s native `open`\nvery closely (with some additional parameters and methods such as `save`).\n\nAPI documentation can be found at [https://iotoolz.readthedocs.io/en/latest/](https://iotoolz.readthedocs.io/en/latest/).\n\nChange logs are available in [CHANGELOG.md](https://github.com/e2fyi/iotoolz/blob/master/CHANGELOG.md).\n\n> - Python 3.6 and above\n> - Licensed under [Apache-2.0](./LICENSE).\n\n## Supported streams\n\nCurrent the following streams are supported:\n\n- `iotoolz.FileStream`: wrapper over built-in `open` function (`file://`)\n- `iotoolz.TempStream`: in-memory stream that will rollover to disk (`tmp://`, `temp://`)\n- `iotoolz.HttpStream`: http or https stream implemented with `requests` (`http://`, `https://`)\n- `iotoolz.extensions.S3Stream`: s3 stream implemented with `boto3` (`s3://`, `s3a://`, `s3n://`)\n\n## Installation\n\n```bash\n# install the default packages only (most lite-weight)\npip install iotoolz\n\n# install dependencies for specific extension\npip install iotoolz[boto3]\n\n# install all the extras\npip install iotoolz[all]\n```\n\nAvailable extras:\n\n- `all`: All the optional dependencies\n- `boto3`: `boto3` for `iotoolz.extensions.S3Stream`\n- `minio`: TODO\n\n## Quickstart\n\n### iotoolz.streams\n\nThe helper object `iotoolz.streams.stream_factory` is a default singleton of\n`iotoolz.streams.Streams` provided to support most of the common use cases.\n\n`iotoolz.streams.open_stream` is a util method provided by the singleton helper to create\na stream object. This method accepts the same arguments as python\'s `open` method with\nthe following additional parameters:\n\n- `data`: optional str or bytes that will be passed into the stream\n- `fileobj`: optional file-like object which will be copied into the stream\n- `content_type`: optional mime type information to describe the stream (e.g. application/json)\n- `inmem_size`: determines how much memory to allocate to the stream before rolling over to local file system. Defaults to no limits (may result in MemoryError).\n- `schema_kwargs`: optional mapping of schemas to their default kwargs.\n\n```py\nfrom iotoolz.streams import open_stream\n\ndefault_schema_kwargs = {\n    "https": {"verify": False}  # pass to requests - i.e. don\'t verify ssl\n}\n\n# this will return a stream that reads from the site\nhttp_google = open_stream(\n    "https://google.com",\n    mode="r",\n    schema_kwargs=default_schema_kwargs\n)\n\nhtml = http_google.read()\ncontent_type = http_google.content_type\nencoding = http_google.encoding\n\n# this will write to the https endpoint using the POST method (default is PUT)\nwith open_stream("https://foo/bar", mode="wb", use_post=True) as stream:\n    stream.write(b"hello world")\n\n\n# this will write to a local path\n# save will write the current content to the local file\nfoo_txt = open_stream(\n    "path/to/foo.txt",\n    mode="w",\n    content_type="text/plain",\n    encoding="utf-8",\n    data="foo bar",\n).save()\n\n# go to the end of the buffer\nfoo_txt.seek(0, whence=2)\n# append more data\nfoo_txt.write("\\nnext line")\n# save and close the data\nfoo_txt.close()\n\n\n# save a local file to S3\nwith open_stream("key.txt", "rb") as csv_source,\n     open_stream("s3://bucket/folder/key.txt", "wb") as s3_sink:\n    csv_source.pipe(s3_sink)\n```\n\n## Piping streams\n\n`pipe` is method to push data to a sink (similar to NodeJS stream except it has no\nwatermark or buffering).\n\n```py\nfrom  iotoolz.streams import open_stream\n\nlocal_file = open_stream(\n    "path/to/google.html", content_type="text/html", mode="w"\n)\ntemp_file = open_stream(\n    "tmp://google.html", content_type="text/html", mode="wb"\n)\n\n# when source is closed, all sinks will be closed also\nwith open_stream("https://google.com") as source:\n    # writes to a temp file then to a local file in sequence\n    source.pipe(temp_file).pipe(local_file)\n\n\nlocal_file2 = open_stream(\n    "path/to/google1.html", content_type="text/html", mode="w"\n)\nlocal_file3 = open_stream(\n    "path/to/google2.html", content_type="text/html", mode="w"\n)\n\n# when source is closed, all sinks will be closed also\nwith open_stream("tmp://foo_src", mode="w") as source:\n    # writes in a fan shape manner\n    source.pipe(local_file2)\n    source.pipe(local_file3)\n\n    source.write("hello world")\n```\n\n> TODO support transform streams so that pipe can be more useful\n',
    'author': 'eterna2',
    'author_email': 'eterna2@hotmail.com',
    'maintainer': 'eterna2',
    'maintainer_email': 'eterna2@hotmail.com',
    'url': 'https://github.com/e2fyi/iotoolz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
