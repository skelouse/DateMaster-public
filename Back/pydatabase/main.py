# File: main.py
import json
import firebase_admin
from firebase_admin import db, credentials

import funcs.maketodo as maketodo
import funcs.item as item            

def skelouse(request):
    # request.path, request.method
    id = request.path.lstrip('/')
    #print('request.data>', request.data)
    #print('request.path> ', request.path)
    #print('id> ', id)
    #print('request.method>', request.method)

    # Takes local id at url/skelouse/todo
    # creates a todo list, posts and returns it
    if id == 'admin':
        data = json.loads(request.data)
        print(data)
        command = data['command']
        key = ""
        if key == data['key']:
            print(command)
            if command == 'todo':
                return maketodo.making_todo(json.loads(request.data), db)
        
        else:
            return flask.jsonify({'success': False, 'error': 'Invalid Key'})

    # Takes local id, ftype('mark', 'move' 'oos', 'movenmark', new_date), upc, sect_id
    if id == 'item':
        data = json.loads(request.data)
        ftype = data['ftype']
        print('ftype >', ftype)
        if ftype == 'mark':
            return item.mark(data, db)
        elif ftype == 'move':
            return item.move(data, db)
        elif ftype == 'oos':
            return item.oos(data, db)
        elif ftype == 'movenmark':
            return item.marknmove(data, db)
        elif ftype == 'new_date':
            return item.new_date(data, db)
        elif ftype == 'hide':
            return item.hide(data, db)