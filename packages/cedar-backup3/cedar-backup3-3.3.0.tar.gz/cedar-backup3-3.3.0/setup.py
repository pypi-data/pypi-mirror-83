# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['CedarBackup3',
 'CedarBackup3.actions',
 'CedarBackup3.extend',
 'CedarBackup3.tools',
 'CedarBackup3.writers']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['cback3 = CedarBackup3.scripts:cback3',
                     'cback3-amazons3-sync = CedarBackup3.scripts:amazons3',
                     'cback3-span = CedarBackup3.scripts:span']}

setup_kwargs = {
    'name': 'cedar-backup3',
    'version': '3.3.0',
    'description': 'Implements local and remote backups to CD/DVD and Amazon S3',
    'long_description': '# Cedar Backup v3\n\n![](https://img.shields.io/pypi/l/cedar-backup3.svg)\n![](https://img.shields.io/pypi/wheel/cedar-backup3.svg)\n![](https://img.shields.io/pypi/pyversions/cedar-backup3.svg)\n![](https://github.com/pronovic/cedar-backup3/workflows/Test%20Suite/badge.svg)\n![](https://readthedocs.org/projects/cedar-backup3/badge/?version=latest&style=flat)\n\nCedar Backup is a software package designed to manage system backups for a\npool of local and remote machines.  Cedar Backup understands how to back up\nfilesystem data as well as MySQL and PostgreSQL databases and Subversion\nrepositories.  It can also be easily extended to support other kinds of\ndata sources.\n\nCedar Backup is focused around weekly backups to a single CD or DVD disc,\nwith the expectation that the disc will be changed or overwritten at the\nbeginning of each week.  If your hardware is new enough, Cedar Backup can\nwrite multisession discs, allowing you to add incremental data to a disc on\na daily basis.  Alternately, Cedar Backup can write your backups to the Amazon\nS3 cloud rather than relying on physical media.\n\nBesides offering command-line utilities to manage the backup process, Cedar\nBackup provides a well-organized library of backup-related functionality,\nwritten in the Python 3 programming language.\n\nThere are many different backup software systems in the open source world.\nCedar Backup aims to fill a niche: it aims to be a good fit for people who need\nto back up a limited amount of important data on a regular basis. Cedar Backup\nisn’t for you if you want to back up your huge MP3 collection every night, or\nif you want to back up a few hundred machines.  However, if you administer a\nsmall set of machines and you want to run daily incremental backups for things\nlike system configuration, current email, small web sites, source code\nrepositories, or small databases, then Cedar Backup is probably worth your\ntime.\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pronovic/cedar-backup3',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<=3.9',
}


setup(**setup_kwargs)
