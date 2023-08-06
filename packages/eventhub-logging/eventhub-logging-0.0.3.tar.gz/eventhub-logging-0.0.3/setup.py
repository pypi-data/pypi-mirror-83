from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name="eventhub-logging",
    version="0.0.3",
    description="logging to azure eventhub module",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # packages=find_packages(),
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

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

    # project_urls={  # Optional
    #     'Source': 'https://github.com/pypa/sampleproject/',
    # },
)


