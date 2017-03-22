#if [[ -f ~/.pythonrc && "$PYTHONSTARTUP" == "" ]]; then
#    export PYTHONSTARTUP="$HOME/.pythonrc"
#fi


try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    import os, atexit
    readline.parse_and_bind("tab: complete")
    history_file = os.path.expanduser('~/.python_history')
    if not os.path.exists(history_file):
        open(history_file, 'a').close()
    readline.read_history_file(history_file)
    atexit.register(readline.write_history_file, history_file)
    del readline, os, rlcompleter, atexit, history_file
