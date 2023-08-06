from setuptools import setup, find_packages

version = '0.6.0'

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='imio.dataexchange.core',
    version=version,
    description="",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='',
    author='IMIO',
    author_email='support@imio.be',
    url='https://github.com/imio/',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['imio', 'imio.dataexchange'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'script': [
            'imio.amqp',
            'imio.dataexchange.db',
        ],
    },
    entry_points="""
    [console_scripts]
    incomingmail_dispatcher = imio.dataexchange.core.scripts.incomingmaildispatcher:main
    outgoingmail_dispatcher = imio.dataexchange.core.scripts.outgoingmaildispatcher:main
    outgoinggeneratedmail_dispatcher = imio.dataexchange.core.scripts.outgoinggeneratedmaildispatcher:main
    deliberation_dispatcher = imio.dataexchange.core.scripts.deliberationdispatcher:main
    incoming_email_dispatcher = imio.dataexchange.core.scripts.incomingemaildispatcher:main
    """,
)
