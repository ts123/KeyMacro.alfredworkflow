#!/usr/bin/python

def main(args, debug=False):
    for _, script in generate_applescripts(args):
        exec_shell_command(['osascript', '-e', script], debug)

def generate_applescripts(args):
    COMMAND_SEPARATOR = ','
    commands = args.split(COMMAND_SEPARATOR)
    for command in commands:
        yield command, create_applescript(command)
        
def create_applescript(command):
    OPTION_SEPARATOR = ':'
    DEFAULT_DELAY_TIME = '0.5'
    KEYCODE_MAP = {
            'esc':'53', 'delete':'51', 'tab':'48', 'space':'49', 'return':'36', 
            'f1':'122', 'f2':'120', 'f3':'99', 'f4':'118', 'f5':'96', 'f6':'97', 
            'f7':'98', 'f8':'100', 'f9':'101', 'f10':'109', 'f11':'103', 'f12':'111', 
            'f13':'105', 'f14':'107', 'f15':'113',
            'left':'123', 'right':'124', 'down':'125', 'up':'126',
            'min':'27', 'colon':'39', 'comma':'43', }

    command = command.split(OPTION_SEPARATOR)
    key = command[0]
    if 1 < len(command):
        option = command[1]
    else:
        option = ''

    if not key:
        if option:
            return 'delay %s' % option
        else:
            return 'delay %s' % DEFAULT_DELAY_TIME

    command_name = 'keystroke'
    if 'n' in option:
        command_name = 'key code'
        key = reduce(lambda x, y: x.replace(y, KEYCODE_MAP[y]), KEYCODE_MAP, key)
        key = eval(key)
    else:
        key = '"'+key+'"'

    modifiers = []
    if 'm' in option:
        modifiers.append('command down')
    if 's' in option:
        modifiers.append('shift down')
    if 'c' in option:
        modifiers.append('control down')
    if 'o' in option:
        modifiers.append('option down')

    applescript = 'tell application "System Events" to {command_name} {key}'
    if modifiers:
        applescript = applescript + ' using {{ {modifiers} }}'
    return applescript.format(command_name = command_name, key = key, modifiers = ','.join(modifiers))

def exec_shell_command(command, debug=False):
    if debug:
        print ' '.join(command)
        return
    import subprocess
    subprocess.call(command)

if __name__ == '__main__':
    import sys
    main(' '.join(sys.argv[1:]), debug=True)

