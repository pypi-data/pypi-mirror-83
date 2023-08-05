# Python application deployer

This command line script exists for fast deployment to remote server.
Was mostly created for test purposes and might have some issues.

## Used languages/packages

Python3.6 and [click](https://click.palletsprojects.com/en/7.x/).
This script uses `ssh`, `scp`, `zip` and `unzip` commands inside.

## Installation and usage

To install simply run `pip install py_deploy`

You can also install it from git: `pip install git+https://github.com/velykanov/py_deploy.git`

To deploy your application to the server simply run `py-deploy -t username@host:/some/dir/`.
This command would deploy current directory to remote server.

Here's the full list of options:
```shell script
-i, --identity-file TEXT  SSH identity file
-P, --port TEXT           SSH target port
-s, --source TEXT         Source  (default: '.')
-t, --target TEXT         Target  [required]
-e, --exclude TEXT        Dirs names to exclude  (default: ['tests', '.git', '__pycache__'])
-v, --verbose
--version                 Show the version and exit.
--help                    Show this message and exit.
```

### Please note!

This tool won't work if your python versions are mismatched
(for instance your app is written using Python3.8 including
some specific features and you're running this tool using Python3.6).
