import os
import py_compile
import shutil
import subprocess
import tempfile

import click

from py_deploy import __version__


def get_file_name(file_path):
    return file_path.rsplit('/', 1)[-1]


def get_pyc_name(file_path):
    return f"{get_file_name(file_path).rsplit('.', 1)[0]}.pyc"


@click.command()
@click.option('-i', '--identity-file', 'identity_file', help='SSH identity file')
@click.option('-P', '--port', 'port', help='SSH target port')
@click.option('-s', '--source', 'source', help='Source', default='.')
@click.option('-t', '--target', 'target', help='Target', required=True)
@click.option(
    '-e',
    '--exclude',
    'exclude_dirs',
    help='Dirs names to exclude',
    multiple=True,
    default=['tests', '.git', '__pycache__'],
)
@click.option('-v', '--verbose', 'verbose', is_flag=True)
@click.version_option(version=__version__)
def cli(identity_file, port, source, target, exclude_dirs, verbose):
    with tempfile.TemporaryDirectory() as dest_dir:
        if verbose:
            print(f'Compiling into {dest_dir}')

        for root, dirs, files in os.walk(source):
            if any(exclude_dir in root for exclude_dir in exclude_dirs):
                continue

            out_dir = os.path.join(dest_dir, root.lstrip(f'.{os.sep}'))
            os.makedirs(out_dir, mode=os.stat(root).st_mode, exist_ok=True)
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.py'):
                    out_file = py_compile.compile(file_path, cfile=os.path.join(out_dir, get_pyc_name(file)))
                    if verbose:
                        print(f'Compiled: {file_path} -> {out_file}')
                else:
                    shutil.copyfile(file_path, os.path.join(out_dir, get_file_name(file)))
                    if verbose:
                        print(f'Copied: {file_path} -> {os.path.join(out_dir, get_file_name(file))}')

        with tempfile.NamedTemporaryFile() as file:
            if verbose:
                print(f'Creating archive: {file}.zip')
            archive_path = shutil.make_archive(file.name, 'zip', dest_dir)

            command = [
                'scp',
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'BatchMode=yes',
            ]
            if identity_file:
                command.extend(('-i', identity_file))
            if port:
                command.extend(('-P', port))
            command.extend((archive_path, target))
            subprocess.run(command)

            if verbose:
                print(f'Unpacking archive into "dest" folder')

            ssh_command = [
                'ssh',
                '-o', 'StrictHostKeyChecking=no',
                target.split(':', 1)[0],
            ]
            if identity_file:
                ssh_command.extend(('-i', identity_file))
            if port:
                ssh_command.extend(('-P', port))
            subprocess.run(ssh_command + ['unzip', target.rsplit(":", 1)[-1], '-d', 'dest'], stdout=subprocess.PIPE)
            subprocess.run(ssh_command + ['rm', '-f', target.rsplit(":", 1)[-1]])
