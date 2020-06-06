import random

class FireBase():
    def exchange_refresh_token(self, username, password):
        return (username+password)

class DataBase():
    db = {}
    def __init__(self, cred, list_of_section_ids, department):
        try:
            self.db[cred] = self.make_department(department, list_of_section_ids)
        except KeyError:
            self.db[cred] = {}
            self.db[cred] = self.make_department(department, list_of_section_ids)

    def make_department(self, department, list_of_section_ids):
        department = {
            'name': department[0],
            'mark_days': department[1],
            'move_days': department[2],
            'products_id': 12345,
            'edited_by': {
                'who': 'store',
                'date': '9/29/2019'
            }
        }
        new_list = {}
        for i in list_of_section_ids.items():
            sect = {}
            sect[i[1]] = {
                'desc': 'apple',
                'img': 'none',
                'marked': False,
                'moved': False,
                'date': '0'
            }
            new_list[i[0]] = sect
        department['products'] = new_list
        return department

    def make_todo(self, cred):
        todo = {}
        for i in self.db[cred]['products'].items():
            for k in i[1].items():
                ftype = self.check_ftype(k[1]['date'])
                
                item = {
                    'desc': 'apple',
                    'type': ftype,
                    'upc': i[0]
                }

                todo[k[0]] = item
        return todo
        # add to database after returning
        # change edited by, today, by todo

    def check_ftype(self, date):
        if date == '0':
            return 'oos'




class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        fb = FireBase()
        self.cred = fb.exchange_refresh_token(
            username, password
        )

    def save_initial_data(self):
        self.products = self.store.db[self.cred]
        self.products_id = self.store.db[self.cred]['products_id']
        # save all images on device

    def first_login(self, store):
        self.store = store
        self.save_initial_data()
        self.login(store)
    
    def login(self, store):
        self.todo = self.store.make_todo(self.cred)
        # update images on device
        # check products_id and edited_by to check for updates


if __name__ == '__main__':
    list_of_section_ids = {
        "upc1": "sect1",
        "upc2": "sect2",
        "upc3": "sect3"
    }  
    user = User('s3652c30', '123456')
    department = ('Dairy', 5, 3)
    store = DataBase(user.cred, list_of_section_ids, department)
    
    user.first_login(store)

    while True:
        user.login(store)
        exit()
