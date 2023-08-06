#!/usr/bin/env python


from setuptools import setup

meta = {}
exec(open('./dotenv_cli/version.py').read(), meta)
meta['long_description'] = open('./README.md').read()

setup(
    name='dotenv-cli',
    version=meta['__VERSION__'],
    description='Simple dotenv CLI.',
    long_description=meta['long_description'],
    long_description_content_type='text/markdown',
    keywords='dotenv cli .env',
    author='Bastian Venthur',
    author_email='mail@venthur.de',
    url='https://github.com/venthur/dotenv-cli',
    python_requires='>=3',
    extras_require={
      'dev': [
          'pytest',
          'pytest-cov',
          'flake8',
      ]
    },
    packages=['dotenv_cli'],
    entry_points={
        'console_scripts': [
            'dotenv = dotenv_cli.__main__:main'
        ]
    },
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
