# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['penelope',
 'penelope.common',
 'penelope.cooccurrence',
 'penelope.corpus',
 'penelope.corpus.readers',
 'penelope.corpus.sparv',
 'penelope.ner',
 'penelope.network',
 'penelope.network.graphtool',
 'penelope.network.graphviz',
 'penelope.network.networkx',
 'penelope.notebook',
 'penelope.plot',
 'penelope.resources',
 'penelope.scripts',
 'penelope.topic_modelling',
 'penelope.topic_modelling.engine_gensim',
 'penelope.topic_modelling.engine_gensim.wrappers',
 'penelope.topic_modelling.engine_textacy',
 'penelope.utility',
 'penelope.vendor',
 'penelope.vendor.gensim',
 'penelope.vendor.textacy']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.1,<2.0.0',
 'bokeh>=2.2.1,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'ftfy>=5.8,<6.0',
 'gensim>=3.8.3,<4.0.0',
 'glove-python-binary>=0.2.0,<0.3.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'lxml>=4.5.2,<5.0.0',
 'memoization>=0.3.1,<0.4.0',
 'more_itertools>=8.5.0,<9.0.0',
 'nltk>=3.5,<4.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.2,<2.0.0',
 'pydotplus>=2.0.2,<3.0.0',
 'python-louvain>=0.14,<0.15',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.5.2,<2.0.0',
 'sklearn>=0.0,<0.1',
 'smart_open>=2.2.1,<3.0.0',
 'spacy>=2.3.2,<3.0.0',
 'statsmodels>=0.12.0,<0.13.0',
 'textacy>=0.10.1,<0.11.0',
 'wordcloud>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['compute_topic_model = '
                     'penelope.scripts.compute_topic_model:main',
                     'concept_cooccurrence = '
                     'penelope.scripts.concept_cooccurrence:main',
                     'vectorize_corpus = '
                     'penelope.scripts.vectorize_corpus:main']}

setup_kwargs = {
    'name': 'humlab-penelope',
    'version': '0.2.17',
    'description': 'Some text analysis utilities',
    'long_description': None,
    'author': 'Roger Mähler',
    'author_email': 'roger.mahler@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
