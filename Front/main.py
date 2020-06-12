import ssl
# THIS IS HACKY
ssl._create_default_https_context = ssl._create_unverified_context

from os.path import join
import time
import random
import requests
import copy
from sys import platform as sysplatform
from functools import partial
from threading import Thread
from traceback import format_exc
import importlib

from kivy.config import Config
Config.set('network', 'Mozilla/5.0 (X11; Linux x86_64)', 'curl')

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.storage.jsonstore import JsonStore

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage, Image
from kivy.uix.dropdown import DropDown

from db.database import FireBase, DataBase
from uix.keyboard import DateKeyboard
from uix.colorlabel import ColorLabel
from uix.trouble import TroublePop

if sysplatform == 'linux' or sysplatform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 0)
    Config.set('graphics', 'top', 0)
    Config.set('graphics', 'height', 800)
    Config.set('graphics', 'width', 496)
    # Config.set('graphics', 'height', 580)
    # Config.set('graphics', 'width', 496)
    Config.write()


#class AsyncImage(AsyncImage):


class ScreenMan(ScreenManager):
    background = 'images/background/default.jpg'
    def __init__(self, **kwargs):
        super(ScreenMan, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size,
                              pos=self.pos,
                              source=self.background)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
sm = ScreenMan(transition=NoTransition())


class ItemViewer(Screen):
    todo = []  # Items that need action taken, taken from DepSelect.todo_deps
    thread_running = False
    todo_num = 0
    queue = []
    blank = (
        '',{
            'date': '',
            'desc': '',
            'ftype': '',
            'ghost': '',
            'img': 'none',
            'price': '',
            'upc': ''
        }
    )

    # Created a list with todo, last item is len-1
    # With a list it can be skipped through and returned into(object):
    def __init__(self, **kwargs):
        super(ItemViewer, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.build_layout()
        self.re_product(self.blank)

    def on_enter(self):
        info = DepSelect.todo_deps[self.app.selected_dep]
        self.todo = info['todo']
        self.hidden = info['hidden']
        self.todo_num = info['num']
        self.queue = info['queue']
        self.re_product(self.get_product())
        try:
            import admin
            importlib.reload(admin)
            admin.run(self)
            print('admin_user')
        except ModuleNotFoundError:
            pass

    def build_layout(self):
        #app.selected_dep
        lblbgc = (0.231, 0.647, 0.541, .8)  # blueish for text
        fgc = (0.752, 0.607, 0.349, 1)  # orangish for text
        bgc = (.90,.63,.47,.95)  # orangish on grey button
        #bgc2 = (.90,.63,.47,.2)
        # (.40,.23,.07,.95) # blueish back for label bg

        #fgc = (0.231, 0.647, 0.541, 1)
        
        #fgc=(1,1,1,1)

        
        self.dropdown = DropDown()

        self.hidebtn = Button(
            text='Hide This Item',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(None, None),
            width=Window.width,
            height=Window.height/8
        )
        self.hidebtn.bind(on_press=self.hide_item)
        self.dropdown.add_widget(self.hidebtn)

        self.change_depbtn = Button(
            text='Change Department',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(None, None),
            width=Window.width,
            height=Window.height/8
        )
        self.change_depbtn.bind(on_press=self.change_dep)
        self.dropdown.add_widget(self.change_depbtn)

        self.sign_outbtn = Button(
            text='Sign Out',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(None, None),
            width=Window.width,
            height=Window.height/8
        )
        self.sign_outbtn.bind(on_press=self.sign_out)
        self.dropdown.add_widget(self.sign_outbtn)

        self.menubtn = Button(
            text='Menu',
            font_size='30dp',
            size_hint=(.9, .05),
            color=fgc,
            background_color=bgc,
            pos_hint={'center_x':.5, 'center_y':.075}
        )
        self.menubtn.bind(on_release=self.dropdown.open)
        self.add_widget(self.menubtn)

        self.info=ColorLabel(
            color=fgc,
            font_size='25dp',
            size_hint=(.94, .05),
            pos_hint={'center_x':.5, 'center_y': .782}
        )
        self.info.set_bgcolor(.40,.23,.07,.95)
        self.add_widget(self.info)

        self.rightbtn = Button(
            text='>>',
            color=lblbgc,
            background_color=(.17,.34,.52,.3),
            font_size='55dp',
            size_hint=(.2, .48),
            pos_hint={'center_x': .9, 'center_y': .48}
        )
        self.rightbtn.bind(on_press=self.go_right)
        self.add_widget(self.rightbtn)

        self.leftbtn = Button(
            text='<<',
            color=lblbgc,
            background_color=(.17,.34,.52,.3),
            font_size='55dp',
            size_hint=(.2, .48),
            pos_hint={'center_x': .1, 'center_y': .48}
        )
        self.leftbtn.bind(on_press=self.go_left)
        self.add_widget(self.leftbtn)

        self.section_id = ColorLabel(
            color=lblbgc,
            pos_hint={'center_y': .832, 'center_x': .5},
            size_hint=(.96, .05),
            font_size='30dp'
        )
        self.section_id.set_bgcolor(.17,.34,.52,.3)
        self.add_widget(self.section_id)


        self.product_desc = ColorLabel(
            pos_hint={'center_x': .5, 'center_y': .96},
            font_size='23dp',  # used to be 30
            color=lblbgc,
            size_hint=(None, None),
            size=(Window.width, Window.height/9.5),
            halign='center'
        )
        self.product_desc.set_bgcolor(.17,.34,.52,.5)

        self.product_desc.text_size = self.product_desc.size
        self.add_widget(self.product_desc)


        self.img = AsyncImage(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(.5, .5),
            allow_stretch=True
        )
        self.add_widget(self.img)
        self.product_upc = ColorLabel(
            size_hint=(.98, .05),
            color=lblbgc,
            pos_hint={'center_y': .882, 'center_x': .5},
            font_size='30dp',
            halign='left'
        )
        self.product_upc.set_bgcolor(.17,.34,.52,.4)
        self.add_widget(self.product_upc)
        self.mark_btn = Button(
            text='Marked',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(.35, .12),
            pos_hint={'center_x':.5, 'center_y':.17}
        )
        self.mark_btn.bind(on_press=self.marked)

        self.move_btn = Button(
            text='Moved',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(.35, .12),
            pos_hint={'center_x':.5, 'center_y':.17}
        )
        self.move_btn.bind(on_press=self.moved)

        self.marknmove_btn = Button(
            text='Marked &\nMoved',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(.35, .12),
            pos_hint={'center_x':.5, 'center_y':.17}
        )
        self.marknmove_btn.bind(on_press=self.marknmove)


        self.outstock_btn = Button(
            text='Out of\nStock',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(.33, .12),
            pos_hint={'center_x':.85, 'center_y':.17}
        )
        self.outstock_btn.bind(on_press=self.oos)
        self.add_widget(self.outstock_btn)

        self.date_btn = Button(
            text='New\nDate',
            color=fgc,
            background_color=bgc,
            font_size='30dp',
            size_hint=(.33, .12),
            pos_hint={'center_x':.15, 'center_y':.17}
        )
        self.date_btn.bind(on_press=self.open_keyboard)
        self.add_widget(self.date_btn)

    def pre_load_next_images(self, num):
        try:
            img = self.todo[num+1][1]['img']
            if img != 'none':
                AsyncImage(source=img)
        except IndexError:
            pass

    def re_product(self, product, *dt):
        self.pr = product
        self.pre_load_next_images(self.todo_num)
        self.product_desc.text=self.pr[1]['desc']  # desc
        ftype = self.pr[1]['ftype']  # ftype
        self.remove_widget(self.mark_btn)
        self.remove_widget(self.move_btn)
        self.remove_widget(self.marknmove_btn)
        if ftype == 'oos':
            fmsg = 'Enter a date for this item?'
        elif ftype == 'mark':
            self.add_widget(self.mark_btn)
            fmsg = 'Mark this item?'
        elif ftype == 'move':
            self.add_widget(self.move_btn)
            fmsg = 'Move this item?'
        elif ftype == 'ood':
            fmsg = 'Out of Date?'
        elif ftype == 'movenmark':
            self.add_widget(self.marknmove_btn)
            fmsg = 'Mark & Move?'
        else:
            fmsg = 'None'
          
        self.info.text=("Date: %s  %s"
            % (self.pr[1]['date'], fmsg))  # date / action
        
        word = self.pr[0] 
        new_word = (word[0:3]+' - '+word[3:6]+' - '+word[6::])
        self.section_id.text = new_word

        if self.pr[1]['img'] == 'none':
            self.img.color = [1, 1, 1, 0]
        else:
            self.img.color = [1, 1, 1, 1]
            self.img.source=self.pr[1]['img']  # img
        
        self.product_upc.text=self.pr[1]['upc']  # upc

    def change_dep(self, event):
        if self.thread_running:
            Clock.schedule_once(self.change_dep, .1)
        else:
            DepSelect.todo_deps[ self.app.selected_dep ]['queue'] = copy.deepcopy(self.queue)
            self.queue = []
            self.dropdown.dismiss()
            self.re_product(self.blank)
            DepSelect.todo_deps[ self.app.selected_dep ]['num'] = self.todo_num
            sm.current = 'dep_select'
    
    def sign_out(self, event):
        global sm
        self.dropdown.dismiss()
        for i in sm.screens:
            sm.remove_widget(i)
        sm.add_widget(Login(name='login'))
        sm.current = 'login'

    def marked(self, event):
        self.mfuncs()

    def moved(self, event):
        self.mfuncs()

    def marknmove(self, event):
        self.mfuncs()        

    def mfuncs(self):
        self.send_pr = self.pr
        t = Thread(target=self.post_item,
                         args=(self.send_pr, self.todo_num))
        t.daemon = True
        t.start()
        self.next_item()

    def oos(self, event):
        self.send_pr = self.pr
        if self.pr[1]['ftype'] == 'oos':
            self.next_item()
        else:
            self.send_pr[1]['ftype'] = 'oos'
            t = Thread(target=self.post_item,
                         args=(self.send_pr, self.todo_num))
            t.daemon = True
            t.start()
            self.next_item()

    def send_date(self, pr, date, *args):
        self.send_pr = pr
        self.send_pr[1]['date'] = date
        self.send_pr[1]['ftype'] = 'new_date'
        self.thread_running = True
        self.next_item()
        t = Thread(target=self.post_item,
                         args=(self.send_pr, self.todo_num))
        t.daemon = True
        t.start()

    def hide_item(self, event):
        self.send_pr = self.pr
        self.send_pr[1]['ftype'] = 'hide'
        t = Thread(target=self.post_item,
                        args=(self.send_pr, self.todo_num))
        t.daemon = True
        t.start()
        self.next_item()

    def post_item(self, *args):
        self.thread_running = True
        print("args", args)
        try:
            try:
                ftype = None
                pr = args[0]
                req = self.app.db.post_item(pr)
                if req.ok:
                    try:
                        ftype = req.json()['ftype']  # Possible breakpoint
                        pr[1]['ftype'] = ftype
                        if ftype == 'ok':
                            self.app.department_list[self.app.selected_dep]['todo_count'] -= 1
                        elif ftype == 'oos':
                            pr[1]['date'] = '0'
                        else:
                            self.queue.append(pr)
                    except KeyError as e:
                        print(e)
                        TroublePop("Trouble connecting", partial(self.post_item, args[0], args[1])).open()
                else:
                    TroublePop("Trouble connecting", partial(self.post_item, args[0], args[1])).open()
                
            except requests.exceptions.ConnectionError:
                TroublePop("Trouble connecting", partial(self.post_item, args[0], args[1])).open()
        except Exception:
            app = App.get_running_app()
            app.fb.capture_bug(format_exc(), app.id_token)
            print('ERROR IN THREAD\n\nERROR IN THREAD')
        self.thread_running = False

    def open_keyboard(self, event):
        self.app.date_keyboard.open(partial(self.send_date, self.pr))

    def go_left(self, *event):
        if self.todo_num >= 1:
            self.todo_num-=1
            self.re_product(self.get_product())
        else:
            return False

    def go_right(self, event):
        self.next_item()

    def next_item(self, *dt):
        print(self.app.local_id)
        # where to deal with queue
        print('length of todo', len(self.todo))
        if self.queue:
            print("There's a queue!")
            # Calling reproduct to build the screen
            self.re_product(self.todo[self.todo.index(self.queue.pop())])
        else:
            if (self.todo_num + 1) == len(self.todo):
                # Reached end
                # Wait for thread to finish
                if self.thread_running:
                    self.pr=('', {'desc': '', 'ftype': '', 'date': '', 'img': ''})
                    self.product_desc.text=''  # desc
                    self.info.text=''
                    self.section_id.text=''
                    self.product_upc.text=''
                    self.remove_widget(self.mark_btn)
                    self.remove_widget(self.move_btn)
                    self.remove_widget(self.marknmove_btn)
                    self.img.color = [1, 1, 1, 0]
                    Clock.schedule_once(self.next_item, 1)
                else:
                    self.todo_num = 0
                    Clock.schedule_once(partial(self.re_product, self.get_product()), .1)
                    
                    sm.current = 'dep_select'
            else:
                self.todo_num += 1
                self.re_product(self.get_product())

    def back_pressed(self):
        if self.go_left() == False:
            sm.current = 'dep_select'

    def get_product(self):
        try:
            return self.todo[self.todo_num]
        except IndexError:
            self.todo_num = 0
            return self.todo[0]


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.build_layout()

    def build_layout(self):
        self.welcome = Label(
            color=(.17,.34,.52,1),
            font_size='45dp',
            text='Hello,',
            pos_hint={'center_x': .42, 'center_y': .805}
        )
        self.add_widget(self.welcome)

        self.welcome2 = Label(
            color=(.17,.34,.52,.5),
            font_size='30dp',
            text='welcome to\nDate Master.',
            pos_hint={'center_x': .5, 'center_y': .73}
        )
        self.add_widget(self.welcome2)

        self.email = TextInput(
            padding=(50,75,0,0),
            multiline=False,
            background_color=(.17,.34,.52,.5),
            foreground_color=(0.231, 0.647, 0.541, 1),
            font_size='30dp',
            hint_text='Email',
            size_hint=(.95, .1),
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        self.add_widget(self.email)

        self.password = TextInput(
            padding=(50,75,0,0),
            multiline=False,
            background_color=(.17,.34,.52,.5),
            foreground_color=(0.231, 0.647, 0.541, 1),
            font_size='30dp',
            hint_text='Password',
            password=True,
            size_hint=(.95, .1),
            pos_hint={'center_x': .5, 'center_y': .48}
        )
        self.password.bind(on_text_validate=self.login)
        self.add_widget(self.password)

        self.error_msg = Label(
            color=(0,1,0,1),
            font_size='30dp',
            size_hint=(.1, .1),
            pos_hint={'center_x': .5, 'center_y': .9}
        )
        self.add_widget(self.error_msg)

        self.login_btn = Button(
            color=(0.752, 0.607, 0.349, 1),
            background_color=(.90,.63,.47,1),
            text='Login',
            font_size='40dp',
            size_hint=(.8, .1),
            pos_hint={'center_x': .5, 'center_y': .36}
        )
        self.login_btn.bind(on_release=self.login)
        self.add_widget(self.login_btn)

        self.try_btn = Button(
            color=(0.752, 0.607, 0.349, 1),
            background_color=(.90,.63,.47,1),
            text='Try Again',
            font_size='40dp',
            size_hint=(.8, .1),
            pos_hint={'center_x': .5, 'center_y': .27}
        )
        self.try_btn.bind(on_press=self.retry_refresh_token)

    def login(self, event):
        self.error_msg.test=''
        # For testing
        if self.email.text == 't':
            self.email.text = 'test@gmail.com'
            self.password.text = '123456'
        elif self.email.text == 's':
            self.email.text = 's3652c30@gmail.com'
            self.password.text = '123456'
        #
        req = self.app.fb.sign_in(self.email.text, self.password.text, self.error_msg)
        if req['success']:
            print('calling app.login')
            self.app.login(1)
        elif self.error_msg.text == '':
            self.error_msg.text = 'Problem connecting'

    def on_enter(self):
        self.email.text = ''
        self.password.text = ''

    def retry_refresh_token(self, event):
        filename = join(self.app.user_data_dir, "refresh_token.txt")
        with open(filename, 'r') as f:
            refresh_token = f.read()
        # if refresh_token and data
        req = self.app.fb.exchange_refresh_token(refresh_token)
        if req['success']:
            self.app.id_token = req['id_token']
            self.app.local_id = req['local_id']
            self.app.login()
        else:
            self.error_msg.text='Expired Token'

    def back_pressed(self):
        self.app.stop()


class DepSelect(Screen):
    # todo_deps holds all the information to load up itemviewer
    todo_deps = {}
    def __init__(self, **kwargs):
        super(DepSelect, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.dep_list = self.app.department_list
        for dep in self.dep_list:
            self.todo_deps[dep] = {}
            self.todo_deps[dep]['num'] = 0
        self.build_layout()
        
    def on_enter(self):
        for i in self.grid.children:
            i.text = '%s - (%s)' % (i.dep, self.dep_list[i.dep]['todo_count'])
        if self.app.user['skip_tutorial']:
            pass
        else:
            from tutorial_screen import Tutorial
            sm.add_widget(Tutorial(DepSelect, ItemViewer, sm, name='tutorial'))
            sm.current='tutorial'

    def build_layout(self):
        self.intro = Label(
            color = (.17,.34,.52,1),
            text='Select a department:',
            font_size='30dp',
            size_hint=(.8, .2),
            pos_hint={'center_x': .5, 'center_y': .96}
        )
        self.add_widget(self.intro)

        self.grid = GridLayout(
            cols=1,
            spacing='5dp',
            col_default_width=.8,
            size_hint=(.8, .8),
            pos_hint={'center_x': .5, 'center_y': .525}
        )
        for i in self.dep_list.items():
            btn = Button(
                font_size='35dp',
                color=(0.752, 0.607, 0.349, .55),
                background_color=(.17,.34,.52,.85),
                text='%s - (%s)' % (i[0], i[1]['todo_count']),
                size_hint_max_y='50dp'
            )
            btn.dep = i[0]
            btn.go_back = False
            btn.todo_num = 0
            btn.bind(on_press=(self.select_dep))
            self.grid.add_widget(btn)
        self.add_widget(self.grid)

    def select_dep(self, event):
        dep = event.dep
        self.app.selected_dep = dep
        try:
            if 'item_viewer' not in sm.screen_names:
                sm.add_widget(ItemViewer(name='item_viewer'))
            self.todo_deps[dep]['todo']
            sm.current = 'item_viewer'
        except KeyError:
            self.todo_deps[dep]['todo'] = []
            self.todo_deps[dep]['hidden'] = []
            self.todo_deps[dep]['queue'] = []
            self.todo_deps[dep]['num'] = 0

            for i in self.dep_list[dep]['todo'].items():
                if i[1]['date'] == 'hidden':
                    self.todo_deps[dep]['hidden'].append(i)
                else:
                    self.todo_deps[dep]['todo'].append(i)
                    # print(i)
            self.select_dep(event)

    def back_pressed(self):
        self.app.stop()


class MasterDateApp(App):
    todo_list = None
    def __init__(self, **kwargs):
        super(MasterDateApp, self).__init__(**kwargs)
        self.fb = FireBase(self)
        self.db = DataBase(self)
        self.date_keyboard = DateKeyboard()
        # user num for database entries
        self.store_file = JsonStore(join(self.user_data_dir, 'store_file.txt'))
        try:
            self.storage = self.store_file.get('data')['content']
            self.user = self.storage['user_data']
            self.user_num = self.user['num']
            
        except KeyError:
            self.storage = {}
            self.user = {
                'num': str(random.randint(1000000000, 9999999999)),
                'level': 1,
                'skip_tutorial': 0
                }
            self.storage['user_data'] = self.user
            self.user_num = self.user['num']
        self.save()

    def save(self):
        self.store_file.put('data', content=self.storage)

    def on_stop(self):
        self.save()

    def build(self):
        print('user_num', self.user_num)
        # Loader.loading_image = 'images/loading.gif'
        try:
            filename = join(self.user_data_dir, "refresh_token.txt")
            with open(filename, 'r') as f:
                refresh_token = f.read()
        except FileNotFoundError:
            # Open login page
            sm.add_widget(Login(name='login'))
            return sm
        else:
            # if refresh_token and data
            req = self.fb.exchange_refresh_token(refresh_token)
            if req['success']:
                self.id_token = req['id_token']
                self.local_id = req['local_id']
                self.login_attempts = 0
                return self.login()

            else:
                # return login
                login_screen = Login(name='login')
                login_screen.error_msg.text = 'Expired Token(Login or try again)'
                login_screen.add_widget(login_screen.try_btn)
                sm.add_widget(login_screen)
                return sm

    def login(self, *args):
        # return main
        req = self.fb.get_data()
        print('app.login')
        if args and req['success']:
            # if args, login was called from the login screen
            sm.add_widget(DepSelect(name='dep_select'))
            sm.current = 'dep_select'
        elif req['success']:
            sm.add_widget(DepSelect(name='dep_select'))
            return sm
        else:
            if req['error'] == 'call_todo':
                req = self.db.call_todo(self.id_token, self.local_id)
                if req['success']:
                    print('todo was success')
                    if args:
                        return self.login(1)
                    else:
                        return self.login()

                # remove this
                elif self.login_attempts <= 3:
                    print('trying login again')
                    self.login_attempts += 1
                    if args:
                        return self.login(1)
                    else:
                        return self.login()
                else:
                    # return a blank screen, open trouble popup, with try again
                    # as partial(self.login, 1)
                    raise Exception('connection')

            # remove this
            elif req['error'] == 'request' and self.login_attempts <= 3:
                print('trying login again')
                self.login_attempts += 1
                if args:
                    return self.login(1)
                else:
                    return self.login()
            else:
                # return a blank screen, open trouble popup, with try again
                # as partial(self.login, 1)
                raise Exception('connection')

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            sm.current_screen.back_pressed()
            # self.stop()
        return True 
        
    def on_pause(self):
        self.save()
        return True

    def on_resume(self):
        # Check connection to DB
        return True


if __name__ == "__main__":
    test = True

    if test:
        MasterDateApp().run()
    else:
        try:
            MasterDateApp().run()
        except Exception:
            print("EXCEPTION CAUGHT IN MAIN THREAD")
            app = App.get_running_app()
            app.fb.capture_bug(format_exc(), app.id_token)
        # Capture bug
        #DateApp().run()