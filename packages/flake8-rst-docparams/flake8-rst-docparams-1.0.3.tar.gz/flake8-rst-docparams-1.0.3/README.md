# README #

Flake8 check for missing parameter RST documentation in
Python based projects. 

### Install ###

#### From source ####

    git clone git@bitbucket.org:jakobsg/flake8-rst-docparams.git
    cd flake8-rst-docparams.git
    python3 setup.py install

#### From PyPi ####

    pip install flake8-rst-docparams

### Setup with Tox ###
    [testenv:flake8]
    basepython = python3
    skip_install = true
    deps =
        flake8
        flake8-rst-docparams
    commands =
        flake8
