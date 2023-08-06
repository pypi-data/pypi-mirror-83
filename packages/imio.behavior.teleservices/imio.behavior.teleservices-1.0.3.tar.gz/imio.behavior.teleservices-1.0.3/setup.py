# -*- coding: utf-8 -*-
"""Installer for the imio.behavior.teleservices package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='imio.behavior.teleservices',
    version='1.0.3',
    description="Plone behavior to get (and set) global E-Guichet/Teleservices configuration into a Plone Application. Expose E-Guichet procedures in a select field.",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Christophe Boulanger',
    author_email='christophe.boulanger@imio.be',
    url='https://github.com/collective/imio.behavior.teleservices',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/imio.behavior.teleservices',
        'Source': 'https://github.com/collective/imio.behavior.teleservices',
        'Tracker': 'https://github.com/collective/imio.behavior.teleservices/issues',
        # 'Documentation': 'https://imio.behavior.teleservices.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['imio', 'imio.behavior'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'collective.z3cform.select2',
        'z3c.jbot',
        'Products.GenericSetup>=1.8.2',
        'plone.api>=1.8.4',
        'plone.restapi',
        'plone.app.contenttypes',
        'plone.app.dexterity',
        'plone.app.referenceablebehavior',
        'plone.app.relationfield',
        'plone.app.lockingbehavior',
        'plone.schema',
        'requests',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = imio.behavior.teleservices.locales.update:update_locale
    """,
)
