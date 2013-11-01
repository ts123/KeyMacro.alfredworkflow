#!/usr/bin/python
import sys

import alfred
import keymacro

def main(query):
    suggested_items = []
    uid = uid_generator()
    suggested_items.append(alfred.Item(
        attributes = { 'uid': uid.next(), 'arg': query },
        title = 'Execute following commands', subtitle = '', 
        icon = 'icon.png'))
    for command, script in keymacro.generate_applescripts(query):
        script = script.replace('''tell application "System Events" to ''', '')
        suggested_items.append(alfred.Item(
            attributes = { 'uid': uid.next(), 'arg': command },
            title = script, subtitle = '', 
            icon = 'icon.png'))
    alfred.write(alfred.xml(suggested_items))

def uid_generator():
    import time
    uid = time.time()
    while True:
        uid += 1
        yield uid

if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))

