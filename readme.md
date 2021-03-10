[![build](https://github.com/a-nau/logging-extended/workflows/build/badge.svg)](https://github.com/a-nau/logging-extended/actions)
[![test](https://github.com/a-nau/logging-extended/workflows/test/badge.svg)](https://github.com/a-nau/logging-extended/actions)

# Logging Extended

This is a small project that came to life during my master's thesis. It is a small extension for the
common [logging](https://docs.python.org/3/library/logging.html) package of python to facilitate logging further.

Extension include:

- Adding helpful information (e.g. current git commit, changed files, main file path) (see [example](#additional-information))
- Option to automatically commit all new changes on start up (e.g. to track experiments closely) (see [example](#automatically-commit-changes))
- Additional log levels (see [example](#additional-log-levels-with-standard-formatting))
- Standard formatting (see [example](#additional-log-levels-with-standard-formatting))
- Pre-configured decorators for headlines and loops (see [example](#pre-configured-decorators))

## Installation

You can install the package using `pip`

```shell
pip install git+https://github.com/a-nau/logging-extended.git@latest
```

You can also download the [latest version](https://github.com/a-nau/logging-extended/archive/latest.tar.gz) as `.tar.gz`
from Github and install it with
`pip install PATH/TO/latest.tar.gz`

Note that you can also add this to your project's `requirements.txt`

```shell
git+https://github.com/a-nau/logging-extended.git@latest
```

## Usage

The usage is easy, and very similar to the standard `logging` module:

```python
import logging_extended as logging

logger = logging.getLogger(__name__)  # using __name__ enables module-wide settings
logger.info("Test")
```

You have the same possibilities for configuration, i.e. you can

- change the configuration with an `.ini` file (see [here](logging_extended/logging_config.ini))
- or directly in Python (see [here](logging_extended/example.py))

To disable logging, you can use

```python
logging.disable(logging.CONFIG)  # below this level everything will be ignored
```

## Examples of the extensions

### Additional information

The logger always prints some overview information on start up:

```shell script
##########################################################################################
Started run at 2021-02-14 18:53:10.335948
Started running: example.py (PATH\TO\logging_extended\example.py)
Current Git Commit: 8706c5488bbda7ff00ef1d3f8d4d21ee55f79600
Current Changed Files: []
Current Untracked Files: []
Git Config: {'auto_commit': False, 'commit_message': '...'}
##########################################################################################
```

### Automatically commit changes

You can set the git config, to automatically commit all changes on start of your project/file

```python
import logging_extended as logging

logging.setGitConfig({"auto_commit": True, "commit_message": "Experiment 3a"})
logger = logging.getLogger(__name__)

...
```

The changes will first be committed and the new commit hash will be saved in the log, so you can always refer back to
the exact implementation when you check the log file.

### Additional log levels with standard formatting

The log levels `verbose`, `track` and `config` have been added and can be use as usual. The log with standard formatting
looks like this then:

```shell script
[2021-02-14 18:56:53] [ VERBOSE] - test VERBOSE (<example.py:68>)
[2021-02-14 18:56:53] [   DEBUG] - test DEBUG (<example.py:68>)
[2021-02-14 18:56:53] [    INFO] - test INFO (<example.py:68>)
[2021-02-14 18:56:53] [   TRACK] - test TRACK (<example.py:68>)
[2021-02-14 18:56:53] [ WARNING] - test WARNING (<example.py:68>)
[2021-02-14 18:56:53] [   ERROR] - test ERROR (<example.py:68>)
[2021-02-14 18:56:53] [CRITICAL] - test CRITICAL (<example.py:68>)
[2021-02-14 18:56:53] [  CONFIG] - test CONFIG (<example.py:68>)
```

### Pre-configured decorators

The logger includes decorators for single lines that can be activated with (see [example](logging_extended/example.py))

```python
import logging_extended as logging

logger = logging.getLogger(__name__)

logger.info("test INFO", decorated=True, decorator="#")
```

which will print

```shell
[2021-02-14 18:59:43] [    INFO] - #####################################   test INFO   ##################################### (<example.py:92>)
```

For loops, there is an extra functionality to track the loop counter

```python
import logging_extended as logging

logger = logging.getLogger(__name__)

for i in range(3):
    logger.loop_counter("test", i, logging.INFO)
```

which results in

```shell script
[2021-02-14 18:56:53] [    INFO] - ###################################   test loop #000   ################################### (<example.py:80>)
[2021-02-14 18:56:53] [    INFO] - ###################################   test loop #001   ################################### (<example.py:80>)
[2021-02-14 18:56:53] [    INFO] - ###################################   test loop #002   ################################### (<example.py:80>)
```

## License

This code is distributed under the 3-Clause BSD License, see [LICENSE](LICENSE).


