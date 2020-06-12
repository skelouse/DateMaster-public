import json
import time
from os.path import join
from traceback import format_exc

import requests

class FireBase(): 
    wak = ""
    url = ""
    headers = {"Content-type": "application/json"}

    def __init__(self, app):
        self.app = app
        today = time.localtime()
        month = today.tm_mon
        day = today.tm_mday
        self.today = ("%s/%s" % (month, day))

    def get_data(self, *args):
        req = requests.get(self.url + self.app.local_id +
        '.json?auth=' + self.app.id_token)
        if req.ok:
            data = json.loads(req.content.decode())
            
            # print('date', data['edited_by']['todo_list']['date'])
            # if data['edited_by']['todo_list']['date'] != self.today:
            #     return ({'success': False, 'error': 'call_todo'})
            self.app.department_list = {}
            for i in data:
                if i != 'edited_by' and i != 'timezone':
                    todo_count = 0
                    todo = data[i]['todo']
                    for k in todo.items():
                        if k[1]['date'] != 'hidden':
                            todo_count += 1

                    self.app.department_list[i] = ({
                        'name': i,
                        'todo': todo,
                        'todo_count': todo_count
                    })
            return ({'success': True})
        else:
            return ({'success': False, 'error': 'request'})

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        req = requests.post(refresh_url, data=refresh_payload)
        if req.ok:
            local_id = req.json()['user_id']
            id_token = req.json()['id_token']
            return ({
                'success': True,
                'id_token': id_token,
                'local_id': local_id
            })
        else:
            return {'success': False}

    def sign_in(self, email, password, error_label):
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key="+self.wak
        #signin_url = 'http://localhost:5000/skelouse/test'
        signin_data = {"email": email, "password": password, "returnSecureToken": True}
        req = requests.post(signin_url, data=signin_data)

        if req.ok:
            localId = req.json()['localId']
            idToken = req.json()['idToken']
            refresh_token = req.json()['refreshToken']
            user_data_dir = self.app.user_data_dir
            filename = join(user_data_dir, "refresh_token.txt")
            with open(filename, "w") as f:
                f.write(refresh_token)
            self.app.local_id = localId
            self.app.id_token = idToken
            #self.app.data = self.get_data(localId, idToken, self.app.user_num)
            #self.app.on_start()
            return {'success': True}
        else:
            error_label.text = "Invalid Email or Password"
            return {'success': False}

    def on_fail(self, *args):
        print(args)

    def capture_bug(self, traceback, id_token):
        data_raw = traceback.split('\n')
        undef = False
        main_error = data_raw[-2]
        if len(main_error) >= 100:
            main_error = 'undef'
            undef = True
        req1 = requests.get(self.url + 'logs' +'/'+ ".json?auth=" + id_token)
        req_data = json.loads(req1.content.decode())

        in_data = False
        try:
            for i in req_data.items():
                if i[0] == main_error:
                    in_data = True
                    quantity = (i[1]['quantity'] + 1)
        except AttributeError:
            pass
        if in_data:
            if undef:
                data = json.dumps({main_error: {'traceback': traceback, 'quantity': quantity, 'date': self.today}})
                req = requests.post(self.url + 'logs' +'/'+ ".json?auth=" + id_token, data=data)
            else:
                data = json.dumps({main_error: {'traceback': traceback, 'quantity': quantity, 'date': self.today}})
        else:
            data = json.dumps({main_error: {'traceback': traceback, 'quantity': 1, 'date': self.today}})

        print('exception sending')
        req = requests.patch(self.url + 'logs' +'/'+ ".json?auth=" + id_token, data=data)
        print('exception sent = ', req.ok)





class DataBase():
    item_url = "/skelouse/item"
    todo_url = "/skelouse/todo"
    # todo_url = "http://localhost:5000/skelouse/todo"
    #item_url = 'http://localhost:5000/skelouse/item'
    headers = {"Content-type": "application/json"}


    def __init__(self, app):
        self.app = app

    def call_todo(self, id_token, local_id):
        print('Calling todo')
        data = {'id_token': id_token, 'local_id': local_id}
        send_data = json.dumps(data)
        req = requests.post(self.todo_url, data=send_data,
                            headers=self.headers)
        if req.ok:
            return {'success': True}
        else:
            self.app.fb.capture_bug(format_exc(), self.app.id_token)
            return {'success': False, 'error': req.error}

    def post_item(self, data):
        send_data = data[1]
        send_data['local_id'] = self.app.local_id
        send_data['sect'] = data[0]
        send_data['phone_id'] = self.app.user_num
        send_data['dep'] = self.app.selected_dep
        send_data = json.dumps(send_data)
        req = requests.post(self.item_url, data=send_data,
                         headers=self.headers)
        print('item posted')
        print(req.content.decode())
        return req

if __name__ == '__main__':
    global app
    app = 10
    fb = FireBase(app)
    a = 10
    fb.exchange_refresh_token('test@gmail.com')


