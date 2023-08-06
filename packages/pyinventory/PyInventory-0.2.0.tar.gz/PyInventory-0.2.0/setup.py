# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inventory',
 'inventory.admin',
 'inventory.management',
 'inventory.management.commands',
 'inventory.migrations',
 'inventory.models',
 'inventory.tests',
 'inventory_project',
 'inventory_tests']

package_data = \
{'': ['*'],
 'inventory': ['static/*', 'templates/admin/inventory/item/*'],
 'inventory_project': ['templates/admin/*']}

install_requires = \
['bx_py_utils',
 'colorama',
 'colorlog',
 'django-admin-sortable2',
 'django-ckeditor',
 'django-dbbackup',
 'django-debug-toolbar',
 'django-import-export',
 'django-reversion-compare',
 'django-tagulous',
 'django-tools',
 'django>=2.2.0,<2.3.0',
 'gunicorn',
 'requests']

extras_require = \
{'docker': ['docker-compose'], 'postgres': ['psycopg2-binary']}

entry_points = \
{'console_scripts': ['manage = inventory_project.manage:main',
                     'publish = inventory_project.publish:publish',
                     'update_rst_readme = '
                     'inventory_project.publish:update_readme']}

setup_kwargs = {
    'name': 'pyinventory',
    'version': '0.2.0',
    'description': 'Web based management to catalog things including state and location etc. using Python/Django.',
    'long_description': '===========\nPyInventory\n===========\n\nWeb based management to catalog things including state and location etc. using Python/Django.\n\nCurrent status: Just start the project. Nothing is done, nothing is useable, yet ;)\n\nPull requests welcome!\n\n+-----------------------------------+-------------------------------------------------+\n| |Build Status on github|          | `github.com/jedie/PyInventory/actions`_         |\n+-----------------------------------+-------------------------------------------------+\n| |Build Status on travis-ci.org|   | `travis-ci.org/jedie/PyInventory`_              |\n+-----------------------------------+-------------------------------------------------+\n| |Coverage Status on codecov.io|   | `codecov.io/gh/jedie/PyInventory`_              |\n+-----------------------------------+-------------------------------------------------+\n| |Coverage Status on coveralls.io| | `coveralls.io/r/jedie/PyInventory`_             |\n+-----------------------------------+-------------------------------------------------+\n| |Status on landscape.io|          | `landscape.io/github/jedie/PyInventory/master`_ |\n+-----------------------------------+-------------------------------------------------+\n\n.. |Build Status on github| image:: https://github.com/jedie/PyInventory/workflows/test/badge.svg?branch=master\n.. _github.com/jedie/PyInventory/actions: https://github.com/jedie/PyInventory/actions\n.. |Build Status on travis-ci.org| image:: https://travis-ci.org/jedie/PyInventory.svg\n.. _travis-ci.org/jedie/PyInventory: https://travis-ci.org/jedie/PyInventory/\n.. |Coverage Status on codecov.io| image:: https://codecov.io/gh/jedie/PyInventory/branch/master/graph/badge.svg\n.. _codecov.io/gh/jedie/PyInventory: https://codecov.io/gh/jedie/PyInventory\n.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/jedie/PyInventory/badge.svg\n.. _coveralls.io/r/jedie/PyInventory: https://coveralls.io/r/jedie/PyInventory\n.. |Status on landscape.io| image:: https://landscape.io/github/jedie/PyInventory/master/landscape.svg\n.. _landscape.io/github/jedie/PyInventory/master: https://landscape.io/github/jedie/PyInventory/master\n\n-----\nabout\n-----\n\nThe focus of this project is on the management of retro computing hardware.\n\nPlan:\n\n* Web-based\n\n* Multiuser ready\n\n* Chaotic warehousing\n\n    * Grouped "Storage": Graphics card is in computer XY\n\n* Data structure kept as general as possible\n\n* You should be able to add the following to the items:\n\n    * Storage location\n\n    * State\n\n    * Pictures\n\n    * URLs\n\n    * receiving and delivering (when, from whom, at what price, etc.)\n\n    * Information: Publicly visible yes/no\n\n* A public list of existing items (think about it, you can set in your profile if you want to)\n\n* administration a wish & exchange list\n\nany many more... ;)\n\n-------\ninstall\n-------\n\nThere exists two kind of installation/usage:\n\n* local virtualenv (without docker)\n\n* docker-compose\n\nsee below\n\nprepare\n=======\n\n::\n\n    ~$ git clone https://github.com/jedie/PyInventory.git\n    ~$ cd PyInventory\n    ~/PyInventory$ make\n    help                 List all commands\n    install-poetry       install or update poetry\n    install              install PyInventory via poetry\n    manage-update        Collectstatic + makemigration + migrate\n    update               update the sources and installation\n    lint                 Run code formatters and linter\n    fix-code-style       Fix code formatting\n    tox-listenvs         List all tox test environments\n    tox                  Run pytest via tox with all environments\n    tox-py36             Run pytest via tox with *python v3.6*\n    tox-py37             Run pytest via tox with *python v3.7*\n    tox-py38             Run pytest via tox with *python v3.8*\n    pytest               Run pytest\n    update-rst-readme    update README.rst from README.creole\n    publish              Release new version to PyPi\n    run-dev-server       Run the django dev server in endless loop.\n    messages             Make and compile locales message files\n    run-server           Run the gunicorn server in endless loop.\n    backup               Backup everything\n    create-starter       Create starter file.\n    install-compose      Install "docker-compose", too\n    up                   Start containers via docker-compose\n    down                 Stop all containers\n    prune                Cleanup docker\n    build                Update docker container build\n    logs                 Display docker logs from all containers\n    dbbackup             Backup database\n    dbrestore            Restore a database backup\n    restart              Restart all containers\n\n.env\n====\n\nCreate a ``.env`` file, for some settings, e.g.:\n\n::\n\n    # enable Django-Debug-Toolbar:\n    ENABLE_DJDT=1\n\nlocal install without docker\n============================\n\n::\n\n    # install or update poetry:\n    ~/PyInventory$ make install-poetry\n    \n    # install PyInventory via poetry:\n    ~/PyInventory$ make install\n    ...\n    \n    # Collectstatic + makemigration + migrate:\n    ~/PyInventory$ make manage-update\n    \n    # Create a django super user:\n    ~/PyInventory$ ./manage.sh createsuperuser\n    \n    # start local dev. web server:\n    ~/PyInventory$ make run-dev-server\n\nThe web page is available via: ``http://127.0.0.1:8000/``\n\ndocker-compose usage\n====================\n\nInstall docker, e.g.: `https://docs.docker.com/engine/install/ubuntu/ <https://docs.docker.com/engine/install/ubuntu/>`_\n\n::\n\n    # Install "docker-compose" via poetry extras:\n    ~/PyInventory$ make install-compose\n    \n    # Start containers via docker-compose:\n    ~/PyInventory$ make up\n\nNotes:\n\n* at the first start it takes a little while until the database is created\n\n* The web page is available via: ``http://localhost:8000/``\n\n-----------\nScreenshots\n-----------\n\n|PyInventory v0.2.0 screenshot 1.png|\n\n.. |PyInventory v0.2.0 screenshot 1.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.2.0 screenshot 1.png\n\n----\n\n|PyInventory v0.1.0 screenshot 2.png|\n\n.. |PyInventory v0.1.0 screenshot 2.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 2.png\n\n----\n\n|PyInventory v0.1.0 screenshot 3.png|\n\n.. |PyInventory v0.1.0 screenshot 3.png| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory v0.1.0 screenshot 3.png\n\n----\n\n----------------\nMulti user usage\n----------------\n\nPyInventory supports multiple users. The idea:\n\n* Every normal user sees only his own created database entries\n\n* All users used the Django admin\n\nNote: All created Tags are shared for all existing users!\n\nSo setup a normal user:\n\n* Set "Staff status"\n\n* Unset "Superuser status"\n\n* Add user to "normal_user" group\n\n* Don\'t add any additional permissions\n\ne.g.:\n\n|normal user example|\n\n.. |normal user example| image:: https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory normal user example.png\n\n------------------------------\nBackwards-incompatible changes\n------------------------------\n\nNothing, yet ;)\n\n-------\nhistory\n-------\n\n* `compare v0.2.0...master <https://github.com/jedie/PyInventory/compare/v0.2.0...master>`_ **dev** \n\n    * tbc\n\n* `v0.2.0 - 24.10.2020 <https://github.com/jedie/PyInventory/compare/v0.1.0...v0.2.0>`_ \n\n    * Simplify item change list by nested item\n\n    * Activate Django-Import/Export\n\n    * Implement multi user usage\n\n    * Add Django-dbbackup\n\n    * Add docker-compose usage\n\n* `v0.1.0 - 17.10.2020 <https://github.com/jedie/PyInventory/compare/v0.0.1...v0.1.0>`_ \n\n    * Enhance models, admin and finish project setup\n\n* v0.0.1 - 14.10.2020\n\n    * Just create a pre-alpha release to save the PyPi package name ;)\n\n-----\nlinks\n-----\n\n+----------+------------------------------------------+\n| Homepage | `http://github.com/jedie/PyInventory`_   |\n+----------+------------------------------------------+\n| PyPi     | `https://pypi.org/project/PyInventory/`_ |\n+----------+------------------------------------------+\n\n.. _http://github.com/jedie/PyInventory: http://github.com/jedie/PyInventory\n.. _https://pypi.org/project/PyInventory/: https://pypi.org/project/PyInventory/\n\nDiscuss here:\n\n* `vogons.org Forum Thread (en) <https://www.vogons.org/viewtopic.php?f=5&t=77285>`_\n\n* `VzEkC e. V. Forum Thread (de) <https://forum.classic-computing.de/forum/index.php?thread/21738-opensource-projekt-pyinventory-web-basierte-verwaltung-um-seine-dinge-zu-katalog/>`_\n\n* `dosreloaded.de Forum Thread (de) <https://dosreloaded.de/forum/index.php?thread/3702-pyinventory-retro-sammlung-katalogisieren/>`_\n\n--------\ndonation\n--------\n\n* `paypal.me/JensDiemer <https://www.paypal.me/JensDiemer>`_\n\n* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2Fjedie%2FPyInventory%2F>`_\n\n* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_\n\n------------\n\n``Note: this file is generated from README.creole 2020-10-24 19:34:25 with "python-creole"``',
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
