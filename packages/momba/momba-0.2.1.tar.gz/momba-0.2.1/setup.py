# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['momba',
 'momba.analysis',
 'momba.explore',
 'momba.jani',
 'momba.kit',
 'momba.model',
 'momba.moml',
 'momba.tools',
 'momba.utils']

package_data = \
{'': ['*']}

install_requires = \
['mxu>=0.0.6,<0.0.7']

extras_require = \
{'all': ['click>=7.0,<8.0'], 'cli': ['click>=7.0,<8.0']}

entry_points = \
{'console_scripts': ['momba-moml = momba.moml.__main__:main']}

setup_kwargs = {
    'name': 'momba',
    'version': '0.2.1',
    'description': 'A Python library for quantitative models.',
    'long_description': "# Momba\n\n[![PyPi Package](https://img.shields.io/pypi/v/momba.svg?label=latest%20version)](https://pypi.python.org/pypi/momba)\n[![Basic Checks](https://img.shields.io/github/workflow/status/koehlma/momba/Basic%20Checks?label=basic%20checks)](https://github.com/koehlma/momba/actions)\n[![Tests](https://img.shields.io/github/workflow/status/koehlma/momba/Run%20Tests?label=tests)](https://github.com/koehlma/momba/actions)\n[![Docs](https://img.shields.io/static/v1?label=docs&message=master&color=blue)](https://koehlma.github.io/momba/)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n*Momba* is a Python framework for dealing with quantitative models centered around the [JANI-model](http://www.jani-spec.org/) interchange format.\nMomba strives to deliver an integrated and intuitive experience to aid the process of model construction, validation, and analysis.\nIt provides convenience functions for the modular constructions of models effectively turning Python into a syntax-aware macro language for quantitative models.\nMomba's built-in simulator allows gaining confidence in a model, for instance, by rapidly prototyping a tool for interactive model exploration and visualization, or by connecting it to a testing framework.\nFinally, thanks to the JANI-model interchange format, several state-of-the-art model checkers and other tools are readily available for analysis.\n\n\n## Features\n\n* first-class **import and export** of **JANI models**\n* **syntax-aware macros** for the modular constructions of models with Python code\n* **built-in simulator** for PTAs, MDPs and other model types\n* interfaces to state-of-the-art model checkers, e.g., [The Modest Toolset](http://www.modestchecker.net/) and [Storm](https://www.stormchecker.org/)\n* pythonic and statically typed APIs to thinker with formal models\n\n\n## Getting Started\n\nMomba is available from the [Python Package Index](https://pypi.org/):\n```sh\npip install momba\n```\nCheck out the [examples](./examples) or read the [documentation](https://koehlma.github.io/momba/) to learn how to use Momba.\n\n\n## Why?\n\nThe idea to harvest a general purpose programming environment for formal modelling is not new at all.\nFor instance, the [SVL language](https://link.springer.com/chapter/10.1007/0-306-47003-9_24) combines the power of process algebraic modelling with the power of the bourne shell.\nMany formal modelling tools also already provide Python bindings, e.g., [Storm](https://moves-rwth.github.io/stormpy/) and [Spot](https://spot.lrde.epita.fr/).\nMomba tries not to be yet another incarnation of these ideas.\nWhile the construction of formal models clearly is an integral part of Momba, Momba is more than just a framework for constructing models with the help of Python.\nMost importantly, it also provides features to work with these models such as a simulator or an interface to different model checking tools.\nAt the same time, it is not just a binding to an API developed for another language, like C++.\nMomba is tool-agnostic and aims to provide a pythonic interface for dealing with formal models while leveraging existing tools.\nMomba covers the whole process from model creation through validation to analysis.\nTo this end, it is centered around the well-entrenched JANI-model interchange format.\n",
    'author': 'Maximilian Köhl',
    'author_email': 'koehl@cs.uni-saarland.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://depend.cs.uni-saarland.de/~koehl/momba/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
