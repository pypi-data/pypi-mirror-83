# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['breakword']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'breakword',
    'version': '0.3.0',
    'description': 'Mixing breakpoints with print debugging.',
    'long_description': '\n# breakword\n\n`breakword` is a small debugging utility that combines print debugging with breakpoint debugging. It aims to facilitate debugging the kind of problem where you might use print statements to quickly spot where something seems to be off, and then switch to a step by step debugger.\n\n`breakword` normally requires running your program twice and will only work properly if it is deterministic.\n\n\n## How to use\n\n1. Set the `PYTHONBREAKPOINT` environment variable to `breakword.breakpoint`.\n\n2. Use `breakpoint` like a `print` statement:\n\n```python\nfor i in range(10):\n    breakpoint(i)\n```\n\nThis will print out something like this:\n\n```\n$ python example.py\n⏎ standard 0\n⏎ sound 1\n⏎ character 2\n⏎ thank 3\n⏎ play 4\n⏎ however 5\n⏎ fish 6\n⏎ cultural 7\n⏎ either 8\n⏎ and 9\n```\n\n3. Use the `BREAKWORD` environment variable to set a breakpoint to what you want to investigate further. For instance, if you want to stop when `i == 6` in the above program, you can run the following command:\n\n\n```\n$ env BREAKWORD=fish python example.py\n⏎ standard 0\n⏎ sound 1\n⏎ character 2\n⏎ thank 3\n⏎ play 4\n⏎ however 5\n⏎ fish 6\n> example.py(2)<module>()\n-> for i in range(10):\n(Pdb) i\n6\n```\n\nYou can also give a comma-separated list of words, e.g. `BREAKWORD=sound,fish`.\n\n**Note:** `breakpoint()` with no arguments retains the normal behavior.\n\n![demo](https://raw.githubusercontent.com/breuleux/breakword/master/media/demo.png)\n\n\n## More functions\n\n* `breakword.log(*things, **config)`: Print a word and optionally other things after it.\n\n* `breakword.brk(watch=None, **config)`: Sets a breakpoint to trigger after `log` printed out the given word. If `watch` is `None` or not given, the `BREAKWORD` environment variable is consulted. If the variable is not set, nothing will happen.\n  * This is equivalent to `breakword.after(word).breakpoint()`.\n\n* `breakword.after(watch=None, **config)`: Returns an object that evaluates to `True` right after `log` printed out the given watch word. As with `brk`, if `watch` is `None` or not given, the `BREAKWORD` environment variable is consulted.\n\n* `breakword.word(**config)`: Returns the next word as a string. You can print it yourself, in which case it\'s basically like `log`, or you can store it in an object.\n\n* `breakword.logbrk(**config)`: Calls `log` and then `brk`.\n\n* `breakword.wordbrk(**config)`: Calls `word` and then `brk`. The word is returned.\n\n* `breakword.set_default_logger(logger)`: Set the logging function to use (defaults to `print`)\n\n\n## Tracking objects\n\n* `breakword.track(obj, all=False)` will set the `breakword` attribute in the object to the next word in the list. By setting the `BREAKWORD` environment variable, you will set a breakpoint to the corresponding call to `track`. Set the `all` argument to `True` and the attribute will contain a list. Note: this will not work if `obj` is an integer or string, in those cases track will print a warning.\n\n* `breakword.track_creation(*classes)` will set the `breakword` attribute on all instances of the given classes, when they are created. That way, you can set a breakpoint back to the creation of some object of interest.\n\n\n## Groups\n\nUse `breakword.groups.<name>` to get a "word group" with the given name. Each group generates words independently and will therefore not interfere with each other. They have `log`, `brk`, `after`, `word`, etc. as methods. The default group is `groups[""]`.\n\n\n```python\nfrom breakword import groups\n\nassert groups.aardvark == groups["aardvark"]\n\n# Log "a" in the aardvark group\ngroups.aardvark.log("a")\n\n# Log "b" in the pelican group\ngroups.pelican.log("b")\n\n# Get the next word in the pelican group\nword = groups.pelican.word()\n\n# Conditional behavior to perform only after the word "cherry"\nif groups.pelican.after("cherry"):\n    print("blah")\n```\n',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/breuleux/breakword',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
