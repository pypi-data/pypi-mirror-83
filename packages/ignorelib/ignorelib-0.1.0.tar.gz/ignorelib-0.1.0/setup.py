# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ignorelib']
setup_kwargs = {
    'name': 'ignorelib',
    'version': '0.1.0',
    'description': 'Use the syntax and semantics of gitignore with custom ignore file names and locations',
    'long_description': "# ignorelib\n## Use the syntax and semantics of gitignore with custom ignore file names and locations\n\ngit has a comprehensive mechanism for selecting files to ignore inside repositories.\n`ignorelib` lets you use the same system, customized to your own needs.\n\nYou can read about the semantics of gitignore here: https://git-scm.com/docs/gitignore\n\nThis library is a lightly-modified version of the [gitignore implementation](https://github.com/dulwich/dulwich/blob/master/dulwich/ignore.py) in [dulwich](https://www.dulwich.io/), a pure Python implementation of git.\n\n# Installation\n```\npython -m pip install ignorelib\n```\n\n# Usage\nThe primary entrypoint is the class factory method `IgnoreFilterManager.build()`, with the following inputs:\n* `path`: the root path (required). All path checks you make are relative to this path.\n* `global_patterns`: an optional list of global ignore patterns. These are the things that should always be ignored (for git, this would be `.git` to exclude the repo directory)\n* `global_ignore_file_paths`: an optional list of file paths to attempt to load global ignore patterns from.\n  * Relative paths are relative to the root path (for git, this would be `.git/info/exclude`)\n  * User expansion is performed, so paths like (for git) `~/.config/git/ignore` work.\n  * Files that cannot be loaded are silently ignored, so you don't need to check if they exist or not.\n  * Patterns in these files take precendence over the patterns in `global_patterns`.\n* `ignore_file_name`: an optional file name for the per-directory ignore file (for git, this would be `.gitignore`).\n* `ignore_case`: an optional boolean for specifying whether to ignore case, defaulting to false.\n\nWith an `IgnoreFilterManager` object, you check if a given path is ignored with `is_ignored()`, which takes a (relative) path and returns `True` if it matches an ignore pattern.\nIt returns `False` if it is explicitly not ignored (using a pattern starting with `!`), or `None` if the file does not match any patterns.\nNote that this allows you to distinguish between the default state (not ignoring) and actually matching a pattern that prevents it from being ignored.\n\nTo iterate over not-ignored files, `IgnoreFilterManager.walk()` has the same interface as `os.walk()` but without taking a root path, as this comes from the the `IgnoreFilterManager`.\n\nAfter using an `IgnoreFilterManager` instance to get a number of paths, you can extract the state (i.e., all loaded patterns with their sources) in a JSON-serializable format with the `IgnoreFilterManager.to_dict()` method.\n",
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/ignorelib',
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
