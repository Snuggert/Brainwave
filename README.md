Brainwave
=========
Bar backend/frontend for the brainwave bar at sciencepark. Basically a POS
(Point Of Sale).

The project will be made using Python 2.7, Flask, HTML5 (JS/AJAX). All Python
MUST conform to PEP8 (http://www.python.org/dev/peps/pep-0008/).

Specifications
=========
* Pre-paid Selling
* Modulair screen (scalable)
* Administration
* Inventory
* Api
* Barteam login / assosiations login
* Two stocks on one tablet
* Utp cassier system
* Beer statistics
* pep8
* Mobile version(?)
* Customer frontend

#### Libraries
* Flask - http://flask.pocoo.org/ (Webframework)
* Flask-SQLAlchemy - http://pythonhosted.org/Flask-SQLAlchemy/ (SQLAlchemy
integration for Flask)
* Sass - http://sass-lang.com/ (Enhanced css, with things like nesting and
mixins)

#### Installation
To get everything working, a virtualenv (virtual environment) has to be set up.
Python has a tool for this: python-virtualenv. You can install this through
your package manager of choice. I do not know (and care) how to do this on
Windows or Mac.

To create the virtualenv, run the following command:
    `virtualenv --no-site-packages venv`

If your default python version is not 2.7, you can add the `-p` argument, to
point to the executable of the correct python version. For example:
    `virtualenv -p /usr/bin/python2 --no-site-packages venv`

The virtualenv is now installed in the `venv/` folder. To get into this
environment, run the following command (dependent on your shell).

Bash:
    `source venv/bin/activate`

Fish:
    `. venv/bin/activate.fish`

You now have access to the correct Python version, and to PIP, a Python
package manager. To install a package using PIP, the following command can be
used:
    `pip install <package>`

To ensure a package version, you can do this:
    `pip install <package>==<version>`

First install Yolk. This is a Python module that allows you to list all
installed packages:
    `pip install yolk`

You can now list your packages using the following command:
    `yolk -l`

Install the following packages:
* Flask==0.10.1
* Flask-Failsafe==0.2
* Flask-SQLAlchemy==1.0
* pyinotify==0.9.4
* watchdog==0.6.0

I will later take some time to explain the use of these packages.
