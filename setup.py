from setuptools import setup

setup(
    name = 'defensio',
    version = '0.9',
    description = 'Small but full featured library for Defensio 2.0',
    author = 'Camilo Lopez',
    author_email = 'clopez@websense.com',
    packages = ['defensio'],
    long_description="""
            Easily access Defensio anti-spam web service version 2.0
      """,
      classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        ],
      keywords='defensio spam api',
      license='GPL'
    )
