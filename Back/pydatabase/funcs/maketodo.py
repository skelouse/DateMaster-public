import time
from datetime import date
import flask
import json
class Check():
    # All stores update at 12am central time
    def __init__(self, mark_days, move_days, utc):
        self._today = time.gmtime(time.time()+(utc*60*60))
        self._month = self._today.tm_mon
        self._day = self._today.tm_mday
        self._year = self._today.tm_year
        self.d0 = date(self._year, int(self._month), int(self._day))
        self.mark_days = 5
        self.move_days = 3

    def real_check_all(self, date_of, ghost, marked, moved, count):
        
        # move, mark, ood, oos, marknmove
        # deal with count here
        # Checks sales
            # If an item sold case_count then recieved case,
            # put in avg date

        try:
            if date_of == 'hidden':
                return 'hidden'
            int(date_of)
            return 'oos'
        except ValueError:
            date_of = date_of.split('/')
            d1 = date(int(date_of[2]), int(date_of[0]), int(date_of[1]))
            if d1 <= self.d0:  # change this to '<=' to show todays date as ood
                return 'ood'
            elif ((d1-self.d0).days <= int(self.move_days) and
                (marked == False) and (moved == False) and (ghost == False)):
                return 'movenmark'
            elif ((d1-self.d0).days <= int(self.move_days) and
                (marked == True) and (moved == False) and (ghost == False)):
                return 'move'
            elif ((d1-self.d0).days <= int(self.mark_days) and
                (marked == False) and (ghost == False)):
                return 'mark'
            else:
                return 'ok'
    
    def real_check_all_num(self, date_of, ghost, marked, moved, count):
        
        # move, mark, ood, oos, marknmove
        # deal with count here
        # Checks sales
            # If an item sold case_count then recieved case,
            # put in avg date

        try:
            if date_of == 'hidden':
                return ('hidden', 0)
            int(date_of)
            return ('oos', 0)
        except ValueError:
            date_of = date_of.split('/')
            d1 = date(int(date_of[2]), int(date_of[0]), int(date_of[1]))
            if d1 <= self.d0:  # change this to '<=' to show todays date as ood
                return ('ood', (d1-self.d0).days)
            elif ((d1-self.d0).days <= int(self.move_days) and
                (marked == False) and (moved == False) and (ghost == False)):
                return ('movenmark', (d1-self.d0).days)
            elif ((d1-self.d0).days <= int(self.move_days) and
                (marked == True) and (moved == False) and (ghost == False)):
                return ('move', (d1-self.d0).days)
            elif ((d1-self.d0).days <= int(self.mark_days) and
                (marked == False) and (ghost == False)):
                return ('mark', (d1-self.d0).days)
            else:
                return ('ok', (d1-self.d0).days)
        
            

def making_todo(req, db):
    data = db.reference().get()
    data.pop("Upc_data")
    try:
        data.pop("logs")
    except KeyError:
        print("no logs, can't delete")
    for i in data:
        todo_store(data[i], db, i)

    return flask.jsonify({'success': True})

def todo_store(data, db, local_id):
    print('making todo for = ', local_id)
    data.pop('edited_by')
    utc = data.pop('timezone')
    for department in data.items():
        todo = {}
        check = Check(department[1]['mark_days'], department[1]['move_days'], utc)
        for upc in department[1]['Products'].items():
            for sect_id in upc[1].items():
                item = sect_id[1]

                # find type
                ftype = check.real_check_all(item['date'], item['ghost'],
                    item['marked'], item['moved'], item['count'])
                #print(ftype, item['date'])
                if ftype != 'ok':
                    todo[sect_id[0]] = {
                        'upc': upc[0],
                        'date': item['date'],
                        'ftype': ftype,
                        'desc': item['desc'],
                        'img': item['img'],
                        'price': item['price'],
                        'ghost': item['ghost']
                    }
                else:
                    todo[sect_id[0]] = None
        todo_ref = db.reference('%s/%s' % (local_id, department[0]))
        todo_ref.child('todo').update(todo)

        today = today = time.gmtime(time.time()+(utc*60*60))
        stamp = ("%s/%s" % (today.tm_mon, today.tm_mday))
    todo_list = {
            'user': 'admin',
            'date': stamp
        }

    edited_ref = db.reference('%s/%s' % (local_id, 'edited_by'))
    edited_ref.child('todo_list').update(todo_list)
    
                


if __name__ == "__main__":
    check = Check(5,3, -6)
    a = check.real_check_all('11/21/2019', False, False, False, 0)
    print(a)