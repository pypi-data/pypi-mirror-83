from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')
install_requires = (here / 'install_requires').read_text(encoding='utf-8').split('\n')


setup(
    name='apteryx',
    version='0.0.1',
    description='For math.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/apteryxlabs/apteryx_utils',
    author='Matthew Billman',
    author_email='matthew@apteryxlabs.com',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Office/Business',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='apteryxlabs, math, utils, apteryx',
    project_urls = {
        'Website' : 'https://apteryxlabs.com'
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires = install_requires,
    python_requires = '>=3',

)