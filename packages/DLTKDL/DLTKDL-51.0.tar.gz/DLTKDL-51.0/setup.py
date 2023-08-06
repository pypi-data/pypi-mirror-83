import sys

if sys.version_info.major != 3:
    raise Exception('DLTKDL requires Python 3.x')
tf_version_str = 'tensorflow==2.3.0'
if sys.version_info.minor == 8:
    tf_version_str = 'tensorflow>=2.2.0'

from distutils.core import setup
import setuptools

with open('README.md', encoding='utf-8') as readme_file:
    readme_file.readline()
    readme = readme_file.read()
exec(open('dltkdl/version.py').read())

setup(
    name='DLTKDL',
    packages=setuptools.find_packages(),
    package_data={'DLTKDL': ['text/shallownlp/ner_models/*']},
    version=51.0,
    license='GPL-3.0 License',
    description='DLTKDL is a wrapper for TensorFlow and Keras that makes deep learning and AI more accessible and '
                'easier to apply',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='DLTK',
    author_email="connect@qubitai.tech",
    url = 'https://github.com/dltk-ai/Deep-Learning',
    keywords=['tensorflow', 'keras', 'deep learning', 'machine learning'],
    install_requires=[
        tf_version_str,
        'scipy==1.5.2',
        # 'pillow'
        'scikit-learn>=0.21.3',
        'matplotlib >= 3.0.0',
        'pandas >= 1.0.1',
        'fastprogress >= 0.1.21',
        'keras_bert>=0.81.0',
        'requests',
        'joblib',
        'langdetect',
        'theano',
        'jieba',
        'cchardet',
        'networkx>=2.3',
        'bokeh',
        'seqeval',
        'packaging',
        'tensorflow_datasets',
        'transformers>=2.11.0',  # due to breaking change in v2.11.0
        'ipython',
        'syntok',
        'whoosh',
        # these libraries are manually installed on-the-fly when required by an invoked method
        # 'shap',  # used by TabularPredictor.explain
        # 'eli5 >= 0.10.0', # forked version used by TextPredictor.explain and ImagePredictor.explain
        # 'stellargraph>=0.8.2', # forked version used by graph module
        # 'allennlp', # required for Elmo embeddings since TF2 TF_HUB does not work
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
