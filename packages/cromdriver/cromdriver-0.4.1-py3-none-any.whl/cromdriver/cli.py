import argparse
import os
import shutil

import cromdriver

parser = argparse.ArgumentParser()

parser.add_argument(
    'action', help='Action from cromdriver : `get`, `del`, `list`, `test`')
#parser.add_argument('del', help='Delete a specified version of chromedriver')
#parser.add_argument('list', help='List all the chromedrivers version in your machine')
#parser.add_argument('test', help='test if you have the last release')

parser.add_argument('-v', '--version', help='Version of chromedriver')
parser.add_argument('-p', '--platform',
                    help='Platform of chromedriver (linux, darwin or win)')

args = parser.parse_args()

# print(args)
if args.action == 'get':
    if args.version is None:
        latest_release_web = cromdriver.get_latest_release_web()
        cromdriver.download_chromedriver(latest_release_web, args.platform)
        cromdriver.set_latest_release_file(latest_release_web)
        print('Path : {}'.format(os.path.join(
            cromdriver.APP_DATA, 'RELEASE', latest_release_web)))
    else:
        cromdriver.download_chromedriver(args.version, args.platform)
        print('Path : {}'.format(os.path.join(
            cromdriver.APP_DATA, 'RELEASE', args.version)))

elif args.action == 'list':
    release_directory = os.path.join(cromdriver.APP_DATA, 'RELEASE')
    list_files = os.listdir(release_directory)

    if list_files:
        print('Chromedrivers downloaded :')
        for direc in list_files:
            if os.path.isdir(os.path.join(release_directory, direc)):
                print('   - {}'.format(direc))
    else:
        print('No Chromedrivers available')

elif args.action == 'test':
    print('Last release on your machine : {}'.format(
        cromdriver.get_latest_release_file()))
    print('Last release on http://chromedriver.storage.googleapis.com/index.html : {}'.format(
        cromdriver.get_latest_release_web()))

elif args.action == 'del':
    if args.version is not None:
        directory_to_delete = os.path.join(
            cromdriver.APP_DATA, 'RELEASE', args.version)
        shutil.rmtree(directory_to_delete)
        print('Version {} deleted'.format(args.version))
    else:
        print('Please provide a version to delete with -v/--version')

else:
    print('Action not possible. Please choose between : `get`, `del`, `list`, `test`')
