# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['veho',
 'veho.columns',
 'veho.columns.enumerate',
 'veho.columns.enumerate.mapper',
 'veho.columns.getter',
 'veho.columns.mapper',
 'veho.dict',
 'veho.dict.select',
 'veho.entries',
 'veho.entries.enumerate',
 'veho.entries.enumerate.mapper',
 'veho.entries.enumerate.margin',
 'veho.entries.enumerate.zipper',
 'veho.entries.init',
 'veho.entries.mapper',
 'veho.entries.margin',
 'veho.entries.unwind',
 'veho.entries.zipper',
 'veho.enum',
 'veho.enum.matrix_directions',
 'veho.json',
 'veho.json.init',
 'veho.matrix',
 'veho.matrix.enumerate',
 'veho.matrix.enumerate.mapper',
 'veho.matrix.enumerate.margin',
 'veho.matrix.enumerate.zipper',
 'veho.matrix.init',
 'veho.matrix.mapper',
 'veho.matrix.margin',
 'veho.matrix.select',
 'veho.matrix.utils',
 'veho.matrix.zipper',
 'veho.object',
 'veho.object.Object',
 'veho.object.select',
 'veho.vector',
 'veho.vector.enumerate',
 'veho.vector.enumerate.mapper',
 'veho.vector.enumerate.margin',
 'veho.vector.enumerate.zipper',
 'veho.vector.init',
 'veho.vector.length',
 'veho.vector.mapper',
 'veho.vector.margin',
 'veho.vector.sparse_list',
 'veho.vector.zipper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'veho',
    'version': '0.0.6',
    'description': 'easy enumerate',
    'long_description': '# veho\n#### easy enumerate\n\n### Usage\n```python\nfrom veho.vector import mapper\nvect = [1,2,3]\nprint(mapper(vect,lambda x:x+1))\n```',
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydget/veho',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
