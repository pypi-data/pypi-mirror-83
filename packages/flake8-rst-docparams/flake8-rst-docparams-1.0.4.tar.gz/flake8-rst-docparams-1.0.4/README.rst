README
======

Flake8 check for missing parameter RST documentation in
Python based projects. 

Install
=======

From source
-----------

Terminal::

	git clone git@bitbucket.org:jakobsg/flake8-rst-docparams.git
	cd flake8-rst-docparams.git
	python3 setup.py install

From PyPi
---------

Terminal::

	pip install flake8-rst-docparams

Setup with Tox
==============

tox.ini::

    [testenv:flake8]
    basepython = python3
    skip_install = true
    deps =
        flake8
        flake8-rst-docparams
    commands =
        flake8
