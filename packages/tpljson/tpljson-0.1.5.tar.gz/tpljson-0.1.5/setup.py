"""
To Build:
    python3 setup.py clean
    python3 setup.py build

To Install from PyPi:

    pip3 install tpljson

To Test:
    # from directory where pytest.ini is
    pytest
"""
from setuptools import setup

setup(
    name='tpljson',
    version='0.1.5',
    url='https://github.com/OpenBigDataPlatform/tpljson',
    description='json compatible library supporting templating',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='OpenBigDataPlatform',
    author_email='',
    license='MIT License',
    packages=['tpljson'],
    keywords="json template",
    classifiers=[
      "Programming Language :: Python",
      "Development Status :: 4 - Beta",
      "Operating System :: OS Independent",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Programming Language :: Python :: 3 :: Only",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
    ],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'objectpath==0.6.1',
        'colorama==0.4.4',
        'commentjson==0.9.0',
        'lark-parser==0.7.8',
    ],
    python_requires='>=3.6',
    test_suite="tests"
)