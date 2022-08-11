import sys

args_list = sys.argv[1:]
# Convert args to dict
args = {}
for arg in args_list:
    key = arg.split('=')[0]
    val = arg.split('=')[1]
    args[key] = val


def _migrate():
    pass


SIGNAL = args['s']
FORCE = args.get('force',False)
if SIGNAL == 'migrate':
    _migrate()
