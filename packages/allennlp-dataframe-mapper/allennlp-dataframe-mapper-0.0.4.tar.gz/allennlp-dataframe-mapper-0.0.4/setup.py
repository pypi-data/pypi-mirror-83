# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allennlp_dataframe_mapper',
 'allennlp_dataframe_mapper.common',
 'allennlp_dataframe_mapper.common.testing',
 'allennlp_dataframe_mapper.transforms']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=1.0.0,<2.0.0', 'sklearn-pandas>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'allennlp-dataframe-mapper',
    'version': '0.0.4',
    'description': '',
    'long_description': '# sklearn-pandas plugin for AllenNLP\n\n![Python 3.7](https://img.shields.io/badge/python-3.7%2B-brightgreen.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n[sklearn-pandas](https://github.com/scikit-learn-contrib/sklearn-pandas) plugin / wrapper for [AllenNLP](https://github.com/allenai/allennlp).\n\n## Install\n\n```sh\n$ pip install git+ssh://git@github.com/shunk031/allennlp-dataframe-mapper.git\n```\n\n## Usage\n\n### Config\n\n`mapper_iris.jsonnet`\n\n```json\n{\n    "type": "default",\n    "features": [\n        [["sepal length (cm)"], null],\n        [["sepal width (cm)"], null],\n        [["petal length (cm)"], null],\n        [["petal width (cm)"], null],\n        [["species"], [{"type": "flatten"}, {"type": "label-encoder"}]],\n    ],\n    "df_out": true,\n}\n```\n\n### Mapper\n\n```python\nfrom allennlp.common import Params\nfrom allennlp_dataframe_mapper import DataFrameMapper\n\nparams = Params.from_file("mapper_iris.jsonnet")\nmapper = DataFrameMapper.from_params(params=params)\n\nprint(mapper)\n# DataFrameMapper(df_out=True,\n#                 features=[([\'sepal length (cm)\'], None, {}),\n#                           ([\'sepal width (cm)\'], None, {}),\n#                           ([\'petal length (cm)\'], None, {}),\n#                           ([\'petal width (cm)\'], None, {}),\n#                           ([\'species\'], [FlattenTransform(), LabelEncoder()], {})])\n\nmapper.fit_transform(df)\n```\n\n## License\n\nMIT\n',
    'author': 'Shunsuke KITADA',
    'author_email': 'shunsuke.kitada.0831@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shunk031/allennlp-dataframe-mapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
