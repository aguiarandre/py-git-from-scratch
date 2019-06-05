import argparse
import os
import logging
import coloredlogs

from database import Database
from workspace import Workspace
from blob import Blob

logging.basicConfig(level=logging.DEBUG)
coloredlogs.install(level='DEBUG',fmt='[%(process)d] %(levelname)s %(message)s %(asctime)s,%(msecs)03d')

parser = argparse.ArgumentParser('Grit version control system')
subparser = parser.add_subparsers(
	dest='command',
	help='command for the Grit system to perform'
)
init = subparser.add_parser(
	'init', 
	help='initialize empty Grit repository')
init.add_argument(
	'path',
	type=str,
	nargs='?', # a way to make path optional instead of using --path 
			   # and requiring people to pass --path='/path/to/file'
	default='.', 
	help='path to initialize empty Grit repository' 
)
commit = subparser.add_parser(
	'commit', 
	help='submit changes for storage')

args = parser.parse_args()

if args.command == 'init': # initialize .git folder

	# convert to absolute path (also works if already absolute path)
	absolute_path = os.path.abspath(args.path)
	git_path = os.path.join(absolute_path, '.git')

	git_folders = ['objects', 'refs']
	for folder in git_folders:
		path = os.path.join(git_path, folder)
		try:
		    os.makedirs(path)	
		except OSError as err:
		    logging.error(f'Error: Creating .git folder: {folder}\n{err}')
		    exit(1)
	logging.info(f'Initialized empty repository in {git_path}')

elif args.command == 'commit':
	root_path = os.path.abspath('.') # absolute path to current directory
	git_path  = os.path.join(root_path, '.git')
	db_path   = os.path.join(git_path, 'objects')

	workspace = Workspace(root_path)
	database  = Database(db_path)

	for path in workspace.list_files():
		data = workspace.read_file(path)
		blob = Blob(data)

		database.store(blob)

	logging.debug(f'Files committed.')
	
	exit(0)
else:
	logging.warning(f'{args.command} is not a Grit command (yet).')
	exit(1)

exit(0)


#parser.add_argument(
#	'command', 
#	type=str,
#    help='command for the grit system'
#)
#parser.add_argument(
#	'path', 
#	type=str, 
#	nargs='?', # a way to make path optional instead of using --path
#	default='.',
#	help='path to create the .git folder'
#)
# alias inflate='python3 -c "import zlib,sys; print(zlib.decompress(sys.stdin.buffer.read()).decode(\"ISO-8859-1\"))"' #ASCII

# alias inflate='python3 -c "import zlib,sys; print(zlib.decompress(sys.stdin.buffer.read()).decode(\"latin-1\"))"'
