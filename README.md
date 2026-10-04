# vidtoolz-jitter

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-jitter.svg)](https://pypi.org/project/vidtoolz-jitter/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-jitter?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-jitter/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-jitter/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-jitter/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-jitter/blob/main/LICENSE)

Add jitter effect to a video using moviepy

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-jitter
```
## Usage

type ``vid jitter --help`` to get help



## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-jitter
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
