twitter_assistant
=================

*assist in the twittering...*

twitter blocking script written with python and selenium

setup
-----

* clone repo

    ``$ git clone git@github.com:yassghn/twitter_assistant``

* setup virtualenv

    ``$ pythom -m venv twitter_assistant/``

* cd dir

    ``$ cd twitter_assistant/``

* activate virtualenv (select correct script for your os)

    ``$ ./Scripts/Activate.ps1``

* install requirements

    ``$ pip install -r ./requirements.txt``

running
-------

* cd dir

    ``$ cd twitter_assistant/``

* activate virtualenv (select correct script for your os)

    ``$ ./Scripts/Activate.ps1``

* cd src dir

    ``$ cd src/``

* let the assistant assist!

    ``$ pythom -m twitter_assistant -s racism -v``

usage
-----

    ``[-h] [-s [QUERY]] [-nb [QUERY]] [-v]``

    -h, --help            show this help message and exit
    -s [QUERY], --search [QUERY]
                        add search query
    -nb [QUERY], --nuke-button [QUERY]
                        use nuke button to block
    -v, --verbose         turn on verbose logging

notes
-----

the ``-nb [QUERY], --nukebutton [QUERY]`` \
script's argument is meant to work with the [nuke-button](https://github.com/yassghn/nuke-button) project.

to get that going, you should setup a custom firefox profile for selenium \
usage complete with a userscript manager and the [nuke-button](https://github.com/yassghn/nuke-button) installed.

then edit the config dictionary global constant near the top of [twitter_assistant.py](/src/twitter_assistant/twitter_assistant.py) \
adding your browser profile's ``root-directory`` to the ``ffprofile_folder`` key/value pair.

license
-------

`OUI </license>`__