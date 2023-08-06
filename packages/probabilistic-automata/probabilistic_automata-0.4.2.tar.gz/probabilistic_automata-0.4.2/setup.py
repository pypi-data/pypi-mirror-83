# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['probabilistic_automata']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.0.0,<21.0.0',
 'dfa>=2.1.0,<3.0.0',
 'funcy>=1.14,<2.0',
 'lenses>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'probabilistic-automata',
    'version': '0.4.2',
    'description': 'Python library for manipulating probabilistic automata.',
    'long_description': '# Probabilistic Automata\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/probabilistic_automata/status.svg)](https://cloud.drone.io/mvcisback/probabilistic_automata)\n[![Docs](https://img.shields.io/badge/API-link-color)](https://mvcisback.github.io/probabilistic_automata)\n[![codecov](https://codecov.io/gh/mvcisback/probabilistic_automata/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/probabilistic_automata)\n[![PyPI version](https://badge.fury.io/py/probabilistic-automata.svg)](https://badge.fury.io/py/probabilistic-automata)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nPython library for manipulating Probabilistic Automata. This library\nbuilds upon the [`dfa`](https://github.com/mvcisback/dfa) package.\n\n<!-- markdown-toc start - Don\'t edit this section. Run M-x markdown-toc-generate-toc again -->\n**Table of Contents**\n\n- [Probabilistic Automata](#probabilistic-automata)\n- [Installation](#installation)\n- [Usage](#usage)\n    - [Dict <-> PDFA](#dict---pdfa)\n    - [DFA to PDFA](#dfa-to-pdfa)\n    - [Composition](#composition)\n\n<!-- markdown-toc end -->\n\n\n\n# Installation\n\nIf you just need to use `probabilistic_automata`, you can just run:\n\n`$ pip install probabilistic_automata`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\nThe `probabilistic_automata` library centers around the `PDFA` object\nwhich models a finite probabilistic transition system, e.g., a Markov\nDecision Process, as a `DFA` or Moore Machine over a product alphabet\nover the system\'s actions and the environment\'s stochastic action.\n\n```python\nimport probabilistic_automata as PA\n\ndef transition(state, composite_action):\n    sys_action, env_action = composite_action\n    return (state + sys_action + env_action) % 2\n\ndef env_dist(state, sys_action):\n    """Based on state and the system action, what are the probabilities \n    of the environment\'s action."""\n\n    return {0: 1/2, 1: 1/2}  # Always a coin flip.\n\nnoisy_parity = PA.pdfa(\n    start=0,\n    label=bool,\n    inputs={0, 1},\n    env_inputs={0, 1},\n    outputs={0, 1},\n    transition=transition,\n    env_dist=env_dist,   # Equivalently, PA.uniform({0, 1}).\n)\n```\n\nThe support and transition probabilities can easily calculated:\n\n```python\nassert noisy_parity.support(0, 0) == {0, 1}\nassert noisy_parity.transition_probs(0, 0) == {0: 1/2, 1: 1/2}\nassert noisy_parity.prob(start=0, action=0, end=0) == 1/2\n```\n\n## Dict <-> PDFA\n\nNote that `pdfa` provides helper functions for going from a dictionary\nbased representation of a probabilistic transition system to a `PDFA`\nobject and back.\n\n```python\nimport probabilistic_automata as PA\n\nmapping = {\n    "s1": (True, {\n        \'a\': {\'s1\': 0.5, \'s2\': 0.5},\n    }),\n    "s2": (False, {\n        \'a\': {\'s1\': 1},\n    }),\n}\n\nstart = "s1"\npdfa = PA.dict2pdfa(mapping=mapping, start=start)\nassert pdfa.inputs == {\'a\'}\n\nmapping2, start2 = PA.pdfa2dict(pdfa)\nassert start == start2\nassert mapping2 == mapping\n```\n\n\n## DFA to PDFA\n\nThe `probabilistic_automata` library has two convenience methods for\ntransforming a Deterministic Finite Automaton (`dfa.DFA`) into a\n`PDFA`.\n\n- The `lift` function simply creates a `PDFA` whose transitions are\n  deterministic and match the original `dfa.DFA`.\n\n```python\nimport probabilistic_automata as PA\nfrom dfa import DFA\n\nparity = DFA(\n    start=0,\n    inputs={0, 1},\n    label=bool,\n    transition=lambda s, c: (s + c) & 1,\n)\n\nparity_pdfa = lift(parity)\n\nassert pdfa.inputs == parity.inputs\nassert pdfa.env_inputs == {None}\n```\n\n- The `randomize` function takes a `DFA` and returns a `PDFA` modeling\n  the actions of the `DFA` being selected uniformly at random.\n\n```\nnoisy_parity = PA.randomize(parity)\n\nassert noisy_parity.inputs == {None}\nassert noisy_parity.env_inputs == noisy_parity.inputs\n```\n\n## Composition\n\nLike their deterministic variants `PDFA` objects can be combined in\ntwo ways:\n\n1. (Synchronous) Cascading Composition: Feed outputs of one `PDFA` into another.\n\n```python\nmachine = noisy_parity >> noisy_parity\n\nassert machine.inputs == noisy_parity.inputs\nassert machine.outputs == noisy_parity.outputs\nassert machine.start == (0, 0)\n\nassert machine.support((0, 0), 0) == {(0, 0), (0, 1), (1, 0), (1, 1)}\n```\n\n2. (Synchronous) Parallel Composition: Run two `PDFA`s in parallel.\n\n```python\nmachine = noisy_parity | noisy_parity\n\nassert machine.inputs.left == noisy_parity.inputs\nassert machine.inputs.right == noisy_parity.inputs\n\nassert machine.outputs.left == noisy_parity.outputs\nassert machine.outputs.right == noisy_parity.outputs\n\nassert machine.env_inputs.left == noisy_parity.env_inputs\nassert machine.env_inputs.right == noisy_parity.env_inputs\n\nassert machine.start == (0, 0)\nassert machine.support((0, 0), (0, 0)) == {(0, 0), (0, 1), (1, 0), (1, 1)}\n```\n\n**Note** Parallel composition results in a `PDFA` with\n`dfa.ProductAlphabet` input and output alphabets.\n',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/probabilistic_automata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
