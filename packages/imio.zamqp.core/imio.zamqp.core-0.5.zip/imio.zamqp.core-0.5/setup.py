from setuptools import setup, find_packages

version = '0.5'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='imio.zamqp.core',
    version=version,
    description="Generic methods tu use amqp",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='Plone Python IMIO',
    author='IMIO',
    author_email='support@imio.be',
    url='https://github.com/imio/',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['imio', 'imio.zamqp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'collective.zamqp',
        'imio.dataexchange.core',
        'plone.dexterity',
        'requests',
    ],
    extras_require={'test': ['plone.app.testing']},
    entry_points="""
    # -*- Entry points: -*-
    """,
)
