from os.path import join
import time
import random
import sys

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import Rectangle

from db.database import FireBase, DataBase

if sys.platform == 'linux' or sys.platform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'height', '750')
    Config.set('graphics', 'width', '370')
    pc = True
# from kivy.config import Config
# Config.set('graphics', 'position', 'custom')
# Config.set('graphics', 'left', 0)
# Config.set('graphics', 'top', 0)
# Config.set('graphics', 'height', 1366)
# Config.set('graphics', 'width', 768)
# if sys.platform == 'linux' or sys.platform == 'win32':
#     from kivy.config import Config
#     Config.set('graphics', 'position', 'custom')
#     Config.set('graphics', 'left', 0)
#     Config.set('graphics', 'top', 0)
#     Config.set('graphics', 'height', 800)
#     Config.set('graphics', 'width', 496)
if sys.platform == 'linux' or sys.platform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 0)
    Config.set('graphics', 'top', 0)
    Config.set('graphics', 'height', 600)
    Config.set('graphics', 'width', 300)


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


class Admin(Screen):
    # Basically my page for editing items, adding new, creating kehe, deleting items.
    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        

class ItemViewer(Screen):
    # Return to where you left off popup

    # Create a list with todo, last item is len-1
    # With a list it can be skipped through and returned into(object):
    def __init__(self, **kwargs):
        super(ItemViewer, self).__init__(**kwargs)

    # def send_date():
        # check if it needs to be marked or moved, if so,
        # append it to the end of the list


class Login(Screen):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.build_layout()

    def build_layout(self):
        self.welcome = Label(
            color=(.17,.34,.52,1),
            font_size='45dp',
            text='Hello,',
            pos_hint={'center_x': .5, 'center_y': .805}
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
            background_color=(.17,.34,.52,.5),
            foreground_color=(0.231, 0.647, 0.541, 1),
            font_size='30dp',
            hint_text='Password',
            password=True,
            size_hint=(.95, .1),
            pos_hint={'center_x': .5, 'center_y': .48}
        )
        self.add_widget(self.password)

        self.error_msg = Label(
            color=(0,1,0,1),
            font_size='17dp',
            size_hint=(.1, .1),
            pos_hint={'center_x': .5, 'center_y': .39}
        )
        self.add_widget(self.error_msg)

        self.login_btn = Button(
            color=(0.752, 0.607, 0.349, 1),
            background_color=(.90,.63,.47,1),
            text='Login',
            font_size='40dp',
            size_hint=(.8, .1),
            pos_hint={'center_x': .5, 'center_y': .27}
        )
        self.login_btn.bind(on_release=self.login)
        self.add_widget(self.login_btn)

        self.try_btn = Button(
            color=(0.752, 0.607, 0.349, 1),
            background_color=(.90,.63,.47,1),
            text='Try Again',
            font_size='40dp',
            size_hint=(.8, .1),
            pos_hint={'center_x': .5, 'center_y': .17}
        )
        self.try_btn.bind(on_press=self.retry_refresh_token)

    def login(self, event):
        self.error_msg.test=''
        req = fb.sign_in(self.email.text, self.password.text, self.error_msg)
        if req['success']:
            print('calling app.login')
            app.login()
        elif self.error_msg.text == '':
            self.error_msg.text = 'Problem connecting'

    def retry_refresh_token(self, event):
        filename = join(app.user_data_dir, "refresh_token.txt")
        with open(filename, 'r') as f:
            refresh_token = f.read()
        # if refresh_token and data
        req = fb.exchange_refresh_token(refresh_token)
        if req['success']:
            app.id_token = req['id_token']
            app.local_id = req['local_id']
            app.login()
        else:
            self.error_msg.text='Expired Token'


class DepSelect(Screen):
    def __init__(self, **kwargs):
        super(DepSelect, self).__init__(**kwargs)
        app = App.get_running_app()  # For testing
        self.dep_list = app.department_list
        self.build_layout()

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
            btn.bind(on_press=(self.select_dep))
            self.grid.add_widget(btn)
        self.add_widget(self.grid)
    
    def select_dep(self, event):
        print('selected - %s' % event.dep)



class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

    def sign_out(self):
        global sm
        # this needs to be done somehow to clear out screen widgets
        # ""no dupes""
        # just a test code, not actually tested
        sm = ScreenMan(transition=NoTransition())
        sm.add_widget(Login(name='login'))
        sm.current = 'login'


class MasterDateApp(App):
    def __init__(self, **kwargs):
        super(MasterDateApp, self).__init__(**kwargs)
        global fb
        global db
        fb = FireBase(self)
        db = DataBase(self)
        # user num for database entries
        self.user_num = self.get_user_num()

    def build(self):
        global app
        app = self
        print('user_num', self.user_num)
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
            req = fb.exchange_refresh_token(refresh_token)
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

    def login(self):
        # return main
        req = fb.get_data()
        print('app.login')
        if req['success']:
            self.fill_open_dep_select()
            return sm
        else:
            if req['error'] == 'call_todo':
                req = db.call_todo(self.id_token, self.local_id)
                if req['success']:
                    self.login()
                elif self.login_attempts <= 3:
                    print('trying login again')
                    self.login_attempts += 1
                    self.login()
                else:
                    raise Exception('connection')
            elif req['error'] == 'request' and self.login_attempts <= 3:
                print('trying login again')
                self.login_attempts += 1
                self.login()
            else:
                raise Exception('connection')

    def get_user_num(self):
        try:
            filename = join(self.user_data_dir, "user_num.txt")
            with open(filename, "r") as f:
                user_num = f.read()
            return user_num
        except FileNotFoundError:
            user_num = str(random.randint(1000000000, 9999999999))
            filename = join(self.user_data_dir, "user_num.txt")
            with open(filename, "w") as f:
                f.write(user_num)
            return user_num

    def fill_open_dep_select(self):
        sm.add_widget(DepSelect(name='dep_select'))
        sm.current = 'dep_select'

if __name__ == "__main__":
    MasterDateApp().run()
    # Capture bug
    #DateApp().run()
