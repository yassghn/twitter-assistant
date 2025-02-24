twitter_assistant
=================

*assist in the twittering...*

twitter blocking script written with python and selenium

setup
-----

clone

.. code-block:: gitignore

   git clone git@github.com:yassghn/twitter_assistant

setup virtualenv

.. code-block:: boo

    $ pythom -m venv ./twitter_assistant

activate virtualenv (select correct script for your os/shell)

.. code-block:: boo

    $ cd ./twitter_assistant

    $ ./Scripts/Activate.ps1


install requirements

.. code-block:: boo

    $ pip install -r ./requirements.txt

running
-------

cd src dir & let the assistant assist!

.. code-block:: boo

    $ cd ./src

    $ pythom -m twitter_assistant -s racism -v

usage
-----

    ``[-h] [-s [QUERY]] [-nb [QUERY]] [-v]``

    -h, --help              show this help message and exit
    -s, --search            add search query
    -nb, --nuke-button      use nuke button to block
    -v, --verbose           turn on verbose logging

notes
-----

| the ``-nb [QUERY], --nukebutton [QUERY]``
| script's argument is meant to work with the `nuke-button <https://github.com/yassghn/nuke-button>`_ project.
|
| to get that going, you should setup a custom firefox profile for selenium
| usage complete with a userscript manager and the `nuke-button <https://github.com/yassghn/nuke-button>`_ installed.
|
| then edit the config dictionary global constant near the top of `twitter_assistant.py </src/twitter_assistant/twitter_assistant.py>`_
| adding your browser profile's ``root-directory`` to the ``ffprofile_folder`` key/value pair.

license
-------

`OUI </license>`__