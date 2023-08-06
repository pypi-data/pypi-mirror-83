"""
Venture
 a CLI tool to initialize a new project


author: murmuur
"""
# Import Globals
from .libs import *


# Import local dependencies
from .libs import config_editor as config
from .libs import file_prep as prep

# Import dependencies
import os
import argparse
import sys
import json
import requests


def init():
    """
    Sets up the CLI
    """
    description = 'Initializes a project'
    parser = argparse.ArgumentParser(description=description,
                                     epilog='project type arguments are mutually exclusive')



    # Commands
    subparsers = parser.add_subparsers(title='Commands', help='command help')
    # ---> Init
    parser_init = subparsers.add_parser(
        'init', help=f'{bcolors.PURPLE}Initializes a new project{bcolors.ENDC}')
    parser_init.add_argument('destination', action='store', nargs=1, type=str,
                             help=f'{bcolors.RED}Location for new project{bcolors.ENDC}')
            # Venture Types
    type_group = parser_init.add_mutually_exclusive_group(required=False)
    type_group.add_argument('--blank', action='store_const', dest='type', const='b',
                            help=f'{bcolors.YELLOW}Creates a new blank project (default){bcolors.ENDC}')
    type_group.add_argument('-p', '--python', action='store_const', dest='type', const='p',
                            help=f'{bcolors.YELLOW}Creates a new python project{bcolors.ENDC}')
    type_group.add_argument('--shell', action='store_const', dest='type', const='s',
                            help=f'{bcolors.YELLOW}Creates a new shell project{bcolors.ENDC}')

    parser_init.add_argument('-r', '--remote', action='store_true', dest='remote',
                             help=f'{bcolors.DARKGREY}Creates remote github repository during project initialization{bcolors.ENDC}')
    parser_init.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                             help=f'{bcolors.DARKGREY}Changes output to be verbose{bcolors.ENDC}')

    # ---> config
    parser_config = subparsers.add_parser(
        'config', help=f'{bcolors.PURPLE}Opens config file for editing{bcolors.ENDC}')

            # Config Modes
    mode_group = parser_config.add_mutually_exclusive_group(required=False)
    mode_group.add_argument('--reset', action='store_const', dest='conf_mode', const='s',
                            help=f'{bcolors.YELLOW}Resets config.ini, use if missing/damaged{bcolors.ENDC}')
    mode_group.add_argument('--output', action='store_const', dest='conf_mode', const='o',
                            help=f'{bcolors.YELLOW}Outputs config file{bcolors.ENDC}')
    mode_group.add_argument('--templates', action='store_const', dest='conf_mode', const='t',
                            help=f'{bcolors.YELLOW}Outputs path to templates folder{bcolors.ENDC}')


    # Gets defaults from config
    remote = config.defaults(root_path).remote()
    verbose = config.defaults(root_path).verbose()
    type = config.defaults(root_path).type()

    # Sets defaults
    parser.set_defaults(init=False, config=False, verbose=verbose)
    parser_init.set_defaults(init=True, destination=None, type=type, remote=remote)
    parser_config.set_defaults(config=True, conf_mode=None)


    global ARGS
    ARGS = parser.parse_args()


def setup_config():
    """
    Resets config file
    """
    config.create_config(root_path)
    print(
        f'[{bcolors.GREEN}*{bcolors.ENDC}] Reset config file at {root_path}/config.ini')

def print_config():
    """
    Outputs contents of config file to console
    """
    config_path = root_path+'/config.ini'
    # print(f'[{bcolors.BLUE}#{bcolors.ENDC}] Displaying config file located at... ' +
    #       config_path, end='\n\n')
    config.display_config(config_path)

def make_remote_repo(username, access_token):
    """
    Makes remote repo and returns the clone url
    """
    # Contact API
    description = project_name + ' repository'
    payload = {'name': project_name, 'description': description}
    login = requests.post('https://api.github.com/' + 'user/repos',
                          auth=(username, access_token), data=json.dumps(payload))
    try:
        return json.loads(login.text)['clone_url']
    except KeyError:
        raise ConnectionAbortedError("Trouble making repository at... github.com/" + username + '/' + project_name)

def initialize_project():
    """
    Goes through process of initializing a project
    """
    path = ARGS.destination[0]
    type = ARGS.type
    verbose = ARGS.verbose
    remote = ARGS.remote

    # Checks if path is valid
    try:
        is_valid_path(path)
    except FileExistsError as err:
        print(f'{bcolors.RED}FileExistsError{bcolors.ENDC}:', err,
              f'\nUse {bcolors.YELLOW}[-h]{bcolors.ENDC} option for help')
        exit()

    # Makes github repo
    if remote:
        username, access_token = config.get_github_info(root_path)
        # Create Github remote repository
        if verbose:
            print(f'[{bcolors.BLUE}~{bcolors.ENDC}] Contacting github API')
        try:
            remote_url = make_remote_repo(username, access_token)
        except ConnectionAbortedError as err:
            print(f'{bcolors.RED}ConnectionAbortedError{bcolors.ENDC}:', err,
                  f'\nUse {bcolors.YELLOW}[-h]{bcolors.ENDC} option for help')
            exit()
        if verbose:
            print(
                f'[{bcolors.GREEN}*{bcolors.ENDC}] Created github remote repository')

    # Change into new project directory
    parent_dir = os.path.abspath(os.path.join(path, os.pardir))
    os.chdir(parent_dir)
    if verbose:
        print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Changed to new directory')

    # Setup type of project
    if type == 'p':
        if verbose:
            print(
                f'[{bcolors.BLUE}~{bcolors.ENDC}] Creating python project from templat')
        prep.new_pyfile(project_name, root_path)
        if verbose:
            print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Python project created')
    else:
        os.mkdir(path)
        if verbose:
            print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Created new directory')
    os.system(f'echo "# {project_name}" >> {project_name}/README.md')
    if verbose:
        print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Created README.md')

    # Change into new project
    os.chdir(path)
    if verbose:
        print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Changed to new directory')

    # Initialize new repository
    os.system('git init')
    if verbose:
        print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Created git repository')

    # Adds to origin
    if remote:
        # Add remote repo to origin
        remote_ssh = 'git@github.com:' + username + '/' + project_name + '.git'
        os.system('git remote add origin ' + remote_ssh)
        if verbose:
            print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Added url to origin')

    # Stage all files
    os.system('git add .')
    if verbose:
        print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Staged all files')

    # Initial commit
    os.system('git commit -m "initial commit"')
    if verbose:
        print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Committed initial commit')

    # Creates and checkouts to dev branch
    os.system('git checkout -b dev')
    if verbose:
        print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Created and checkout to dev branch')

    # Pushes to github repo
    if remote:
        # Push to github
        os.system('git push -u origin master')
        if verbose:
            print(f'[{bcolors.GREEN}*{bcolors.ENDC}] Pushed to github')

def main():
    # Set globals
    global project_name, root_path
    # Get root path
    root_path = os.path.abspath(os.path.join(__file__, os.pardir))
    init()

    # Check if init was run
    if ARGS.init == True:
        # Get config data
        project_name = ARGS.destination[0].split('/')[-1]
        initialize_project()
    # Check if config was run
    elif ARGS.config == True:
        # Check if mode is in setup
        mode = ARGS.conf_mode
        # Remake config
        if mode == 's':
            setup_config()
        # Print mode
        elif mode == 'o':
            print_config()
        elif mode == 't':
            print(root_path+'/templates/')
        # Open config file in vim
        else:
            config_path = root_path+'/config.ini'
            os.system(f'vim {config_path}')
    else:
        print(f'{bcolors.RED}Missing Command{bcolors.ENDC}: mising command for venture',
              f'\nUse {bcolors.YELLOW}[-h]{bcolors.ENDC} option for help')
        exit()

if __name__ == '__main__':
    main()
