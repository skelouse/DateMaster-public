import time
from datetime import date
import flask
import json

from .maketodo import Check
# {'local_id': '',
# 'dep': 'Dairy'
# 'ftype': 'mark',
# 'upc': '5300006898',
# 'sect': '050101047',
# 'phone_id: '4128457qb} 

def set_edited(data, db):
    ref = db.reference('%s' % data['local_id'])
    utc =  ref.child('timezone').get()
    today = time.gmtime(time.time()+(utc*60*60))
    stamp = ("%s/%s" % (today.tm_mon, today.tm_mday))
    
    send_data ={
        'product_list': {
            'user': data['phone_id'],
            'date': stamp
            },
        'todo_list': {
            'user': data['phone_id'],
            'date': stamp
            }
        }
    ref.child('edited_by').update(send_data)
    return flask.jsonify({'success': True})

def mark(data, db):
    dep = db.reference('%s/%s'
            % (data['local_id'], data['dep']))
    #print(dep.child('ItemData/%s' % data['upc']).get())

    # remove from todo
    dep.child('todo/%s' % data['sect']).delete()

    # in itemdata
    # + 1 mark_quantity
    quantity = dep.child('ItemData/%s/%s'
        % (data['upc'], 'mark_quantity')).get()
    send_data = {'mark_quantity': quantity+1}
    dep.child('ItemData/%s'
        % data['upc']).update(send_data)

    # in products
    # set marked to true
    send_data = {'marked': True}
    dep.child('Products/%s/%s' %
        (data['upc'], data['sect'])).update(send_data)

    # Change edited by todo
    set_edited(data, db)
    return flask.jsonify({'success': True, 'ftype': 'ok'})

def move(data, db):
    dep = db.reference('%s/%s'
            % (data['local_id'], data['dep']))
    #print(dep.child('ItemData/%s' % data['upc']).get())

    # remove from todo
    dep.child('todo/%s' % data['sect']).delete()

    # in itemdata
    # + 1 move_quantity
    quantity = dep.child('ItemData/%s/%s'
        % (data['upc'], 'move_quantity')).get()
    send_data = {'move_quantity': quantity+1}
    dep.child('ItemData/%s'
        % data['upc']).update(send_data)

    # in products
    # set moved to true
    send_data = {'moved': True}
    dep.child('Products/%s/%s' %
        (data['upc'], data['sect'])).update(send_data)
    
    # Change edited by todo
    set_edited(data, db)
    return flask.jsonify({'success': True, 'ftype': 'ok'})

def marknmove(data, db):
    dep = db.reference('%s/%s'
            % (data['local_id'], data['dep']))
    #print(dep.child('ItemData/%s' % data['upc']).get())

    # remove from todo
    dep.child('todo/%s' % data['sect']).delete()

    # in item data
    # + 1 marknmove_quantity
    quantity = dep.child('ItemData/%s/%s'
        % (data['upc'], 'marknmove_quantity')).get()
    send_data = {'marknmove_quantity': quantity+1}
    dep.child('ItemData/%s'
        % data['upc']).update(send_data)

    # in products
    # set marked and moved to true
    send_data = {'moved': True, 'marked': True}
    dep.child('Products/%s/%s' %
        (data['upc'], data['sect'])).update(send_data)
    
    # Change edited by todo
    set_edited(data, db)
    return flask.jsonify({'success': True, 'ftype': 'ok'})

def oos(data, db):
    dep = db.reference('%s/%s'
            % (data['local_id'], data['dep']))
    # update todolist ftype=oos date='0'
    send_data = {
        'date': '0',
        'ftype': 'oos',
        'desc': data['desc'],
        'img': data['img'],
        'price': data['price'],
        'upc': data['upc']
    }
    dep.child('todo/%s' % data['sect']).update(send_data)
    # update oos quantity in data
    quantity = dep.child('ItemData/%s/%s'
        % (data['upc'], 'oos_quantity')).get()
    send_data = {'oos_quantity': quantity+1}
    dep.child('ItemData/%s'
        % data['upc']).update(send_data)
    # set marked and moved to False date='0'
    send_data = {'moved': False, 'marked': False, 'date': '0'}
    dep.child('Products/%s/%s' %
        (data['upc'], data['sect'])).update(send_data)

    # Change edited by todo
    set_edited(data, db)
    return flask.jsonify({'success': True, 'ftype': 'oos'}) # ['ok', 'in_bri']

def new_date(data, db):
    # Receive new date from app
    utc = db.reference('%s/timezone' % data['local_id']).get()
    dep = db.reference('%s/%s'
            % (data['local_id'], data['dep']))
    mark_days = dep.child('mark_days').get()
    move_days = dep.child('move_days').get()
    check = Check(mark_days, move_days, utc)
    # Check if date is too far in the future

    # Check if needs to be marked or moved
    ftype, distance = check.real_check_all_num(data['date'], data['ghost'], False, False, 0)
    # Update date in products
    # Unmark
    # Unmove
    send_product = {
        'date': data['date'],
        'marked': False,
        'moved': False,
    }
    dep.child('Products/%s/%s'
        % (data['upc'], data['sect'])).update(send_product)

    # Update average date
    # Update date quantity
    if distance != 0:
        id_ref = dep.child('ItemData/%s' % data['upc'])
        id = id_ref.get()
        if id['date_quantity'] == 0:
            send_data ={
                'avg_date': distance,
                'date_quantity': 1
            }
            id_ref.update(send_data)
        else:
            avg = id['avg_date']
            quantity = id['date_quantity']
            num = avg*quantity
            avg_date = (num+distance) / (quantity+1)
            send_data ={
                'avg_date': avg_date,
                'date_quantity': (quantity+1)
            }
            id_ref.update(send_data)

    # change in todo
    todo_ref = dep.child('todo')
    if ftype == 'ok':
        todo_ref.child(data['sect']).delete()
    else:
        send_data = {
            'date': data['date'],
            'ftype': ftype,
            'desc': data['desc'],
            'img': data['img'],
            'price': data['price'],
            'upc': data['upc']
        }
        todo_ref.child(data['sect']).update(send_data)

    # change edited by
    set_edited(data, db)
    # return ok/mark/far
    return flask.jsonify({'success': True, 'ftype': ftype})

def hide(data, db):
    dep = db.reference('%s/%s'
            % (data['local_id'], data['dep']))
    send_product = {
        'date': "hidden"
    }
    # change in products
    dep.child('Products/%s/%s'
        % (data['upc'], data['sect'])).update(send_product)

    # change in todo
    send_product['ftype'] = 'oos'
    todo_ref = dep.child('todo')
    todo_ref.child(data['sect']).update(send_product)

    # change edited by
    set_edited(data, db)
    # return ok/mark/far
    return flask.jsonify({'success': True, 'ftype': 'ok'})