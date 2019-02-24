yamkix
======

Why?
----

- Because I like my yaml file to be nicely formatted
- Because
  https://marketplace.visualstudio.com/items?itemName=adamvoss.yaml
  creates (valid) yaml not compatible for kubernetes (and I mainly edit
  yaml files for kubernetes)
- Because
  https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml
  does not add explicit start of documents and I don't like it this way
- Because I'm not a js/typescript dev so I don't want to go into a
  VSCode extension with client and server language

What?
-----

.. code:: shell

    > ./yamkix -h
    usage: yamkix [-h] -i INPUT [-t TYP] [-o OUTPUT] [-n] [-e] [-q] [-f] [-d]

    Format yaml input file. By default, explicit_start is `On`, explicit_end is
    `Off` and array elements are pushed inwards the start of the matching
    sequence. Comments are preserved thanks to default parsing mode `rt`.

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            the file to parse
      -t TYP, --typ TYP     the yaml parser mode. Can be `safe` or `rt`
      -o OUTPUT, --output OUTPUT
                            the name of the file to generate (same as input file
                            if not specied)
      -n, --no-explicit-start
                            by default, explicit start of the yaml doc is `On`,
                            you can disable it with this option
      -e, --explicit-end    by default, explicit end of the yaml doc is `Off`, you
                            can enable it with this option
      -q, --no-quotes-preserved
                            by default, quotes are preserverd you can disable this
                            with this option
      -f, --default-flow-style
                            enable the default flow style `Off` by default. In
                            default flow style (with typ=`rt`), maps and lists are
                            written like json
      -d, --no-dash-inwards
                            by default, dash are pushed inwards use `--no-dash-inwards` to have the dash start at the sequence level

Config
------

- Explicit start of yaml docs by defaut
  (you can disable it with ``--no-explicit-start``)
- Quotes preserved by default
  (you can disable it with ``--no-quotes-preserved``)
- Arrays elements pushed inwards by default
  (you can disable it with ``--no-dash-inwards``)
- Output file is input file by default
- Comments preserved by default thanks to
  `ruamel.yaml <https://pypi.python.org/pypi/ruamel.yaml>`__ ``round_trip``
  mode (you can disable it with ``--typ safe``)

Where does the name 'yamkix' come from?
----------------------------------------

-  Thanks to
   http://online-generator.com/name-generator/product-name-generator.php
   that suggested me ``zamkix``. Just switched the starting ``z`` for
   the ``y`` of ``yaml``

Usage
-----

- Install the package with ``pip install --user yamkix``
- Sample **vscode** task :

.. code:: json

        {
          "taskName": "format yaml with yamkix",
          "type": "shell",
          "command": "yamkix --input ${file}",
          "group": "build",
          "presentation": {
            "reveal": "always",
            "panel": "shared"
          },
          "problemMatcher": []
        }
