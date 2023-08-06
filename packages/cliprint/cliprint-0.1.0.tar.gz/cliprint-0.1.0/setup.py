import setuptools

long_description = """
|PyPI - Version| |Downloads| |Code style: black|

CliPrint
=========

   A lightweight library of python printing functions.

=====

`View on GitHub`_, `contact Finn`_ or `sponsor this project ❤️`_!

.. _View on GitHub: https://github.com/finnmglas/cliprint
.. _contact Finn: https://contact.finnmglas.com
.. _sponsor this project ❤️: https://sponsor.finnmglas.com

.. |PyPI - Version| image:: https://img.shields.io/pypi/v/cliprint?color=000
   :target: https://pypi.org/project/cliprint/
.. |Downloads| image:: https://img.shields.io/badge/dynamic/json?style=flat&color=000&maxAge=10800&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fcliprint
   :target: https://pepy.tech/project/cliprint
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
"""

setuptools.setup(
    name="cliprint",
    version="0.1.0",
    description="A lightweight library of python printing functions.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="",
    url="http://github.com/finnmglas/cliprint",
    author="Finn M Glas",
    author_email="finn@finnmglas.com",
    license="MIT",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [],
    },
    install_requires=[],
    test_suite="nose.collector",
    tests_require=["nose"],
    include_package_data=True,
    zip_safe=False,
)
