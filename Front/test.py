import os
import importlib
import sys
import ast

# if sys.platform == 'linux' or sys.platform == 'win32':
#     from kivy.config import Config
#     Config.set('graphics', 'height', '600')
#     Config.set('graphics', 'width', '370')
#     pc = True

# class Test() in each .py file
# Build directory in kivy pages, test any file

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
import main
from main import sm
import admin
import tutorial_screen


if sys.platform == 'linux' or sys.platform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 0)
    Config.set('graphics', 'top', 0)
    Config.set('graphics', 'height', 800)
    Config.set('graphics', 'width', 496)
    Config.write()

class genericButton(Button):
    def __init__(self, **kwargs):
        super(genericButton, self).__init__(**kwargs)
        self.font_size='60dp'


class TestLayout(Screen):
    def __init__(self, **kwargs):
        super(TestLayout, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.layout = RelativeLayout()
        self.grid = GridLayout(cols=1)

        self.tutbtn = genericButton(text='Tutorial')
        self.tutbtn.bind(on_press=self.test_tutorial)
        self.grid.add_widget(self.tutbtn)

        self.screensbtn = genericButton(text='Screens')
        self.screensbtn.bind(on_press=self.test_screens)
        self.grid.add_widget(self.screensbtn)

        self.dbbtn = genericButton(text='Database')
        self.dbbtn.bind(on_press=self.test_db)
        self.grid.add_widget(self.dbbtn)

        
        self.layout.add_widget(self.grid)
        self.add_widget(self.layout)

        self.refresh_button = Button(
            text='ref',
            size_hint=(.1, .1),
            pos_hint={'center_x': .99, 'center_y': .99}
        )

    def test_screens(self, event):
        self.layout.remove_widget(self.grid)

        self.screengrid = GridLayout(cols=1)

        self.loginbtn = genericButton(text='Login')
        self.loginbtn.bind(on_press=self.login_screen)
        self.screengrid.add_widget(self.loginbtn)

        self.depbtn = genericButton(text='Dep Select')
        self.depbtn.bind(on_press=self.depselect_screen)
        self.screengrid.add_widget(self.depbtn)

        self.viewbtn = genericButton(text='item viewer')
        self.viewbtn.bind(on_press=self.itemviewer_screen)
        self.screengrid.add_widget(self.viewbtn)

        self.homebtn = genericButton(text='Home')
        self.homebtn.bind(on_press=self.home)
        self.screengrid.add_widget(self.homebtn)

        self.layout.add_widget(self.screengrid)


    ###################
    # LOGIN SCREEN
    ###################
    def login_screen(self, event):
        print('testing login screen')
        self.log_num = 0
        self.login = main.Login(name='login')
        self.refresh_button.bind(on_press=self.refresh_login)
        self.login.add_widget(self.refresh_button)
        sm.add_widget(self.login)
        sm.current = 'login'

    def refresh_login(self, event):
        print('refreshing')
        self.login.remove_widget(self.refresh_button)
        self.log_num += 1
        try:
            importlib.reload(main)
            self.login = main.Login(name='login%s'%self.log_num)
            self.login.add_widget(self.refresh_button)
            sm.add_widget(self.login)
            sm.current = 'login%s'%self.log_num
        except Exception as e:
            self.login.remove_widget(self.refresh_button)
            self.login.add_widget(self.refresh_button)
            print('compile error\n- ', e)

    ###################
    # DEP_SELECT SCREEN
    ###################
    def depselect_screen(self, event):
        print('testing dep_select screen')
        self.get_department_list_from_file()
        self.log_num = 0
        self.depselect = main.DepSelect(name='dep_select')
        self.refresh_button.bind(on_press=self.refresh_depselect)
        self.depselect.add_widget(self.refresh_button)
        sm.add_widget(self.depselect)
        sm.current = 'dep_select'

    def refresh_depselect(self, event):
        print('refreshing')
        self.depselect.remove_widget(self.refresh_button)
        self.log_num += 1
        try:
            importlib.reload(main)
            self.depselect = main.DepSelect(name='dep_select%s'%self.log_num)
            self.depselect.add_widget(self.refresh_button)
            sm.add_widget(self.depselect)
            sm.current = 'dep_select%s'%self.log_num
        except Exception as e:
            self.depselect.remove_widget(self.refresh_button)
            self.depselect.add_widget(self.refresh_button)
            print('compile error\n- ', e)

    def get_department_list_from_file(self):
        with open('Front/DateMaster/tests/test_save.txt', encoding='ISO-8859-1') as f:
            app.department_list = {}
            read_data = (f.read())
            data = ast.literal_eval(read_data)
            for i in data:
                if i != 'edited_by' and i != 'timezone':
                    todo = data[i]['todo']
                    app.department_list[i] = ({
                        'name': i,
                        'todo': todo,
                        'todo_count': len(todo)
                    })

    ###################
    # ITEM_VIEWER SCREEN
    ###################
    def itemviewer_screen(self, event):
        print('testing item_viewer screen')
        self.get_department_list_from_file()
        self.depselect = main.DepSelect(name='dep_select')
        sm.add_widget(self.depselect)

        self.select_dep(main.ItemViewer)
        self.log_num = 0
        self.itemviewer = main.ItemViewer(name='item_viewer')
        
        self.refresh_button.bind(on_press=self.refresh_itemviewer)
        self.itemviewer.add_widget(self.refresh_button)
        sm.add_widget(self.itemviewer)
        sm.current = 'item_viewer'

    def refresh_itemviewer(self, event):
        print('refreshing')
        self.itemviewer.remove_widget(self.refresh_button)
        self.log_num += 1
        try:
            importlib.reload(main)
            self.select_dep(main.ItemViewer)
            self.itemviewer = main.ItemViewer(name='item_viewer%s'%self.log_num)
            self.itemviewer.add_widget(self.refresh_button)
            sm.add_widget(self.itemviewer)
            sm.current = 'item_viewer%s'%self.log_num
        except Exception as e:
            self.itemviewer.remove_widget(self.refresh_button)
            self.itemviewer.add_widget(self.refresh_button)
            print('compile error\n- ', e)

    def select_dep(self, ItemViewer):
        ItemViewer.todo = []
        ItemViewer.todo_num = 0
        app.selected_dep = 'Dairy'
        todo = app.department_list['Dairy']['todo']
        for i in todo.items():
            ItemViewer.todo.append(i)




    ###################
    # TEST_TUTORIAL
    ###################
    def test_tutorial(self, event):
        # self.get_department_list_from_file()
        # for i in app.department_list['Dairy']['todo'].items():
        #     print(i[1]['ftype'], i)

        app.department_list = {}
        
        self.tutorial = tutorial_screen.Tutorial(main.DepSelect, main.ItemViewer, sm, name=('tutorial'))
        
        self.log_num = 0
        
        self.refresh_button.bind(on_press=self.refresh_tutorial)
        
        sm.add_widget(self.tutorial)
        sm.get_screen('tutorial').refresh_button = self.refresh_button
        sm.current = 'tutorial'

    def refresh_tutorial(self, event):
        print('refreshing')
        if self.log_num == 0:
            sm.get_screen('tutorial').clear_widgets()
        else:
            sm.get_screen('tutorial%s'%self.log_num).clear_widgets()
        self.log_num += 1 
        #try:
        importlib.reload(tutorial_screen)
        self.tutorial = tutorial_screen.Tutorial(main.DepSelect, main.ItemViewer, sm, name=('tutorial%s'%self.log_num))
        
        sm.add_widget(self.tutorial)
        sm.get_screen('tutorial%s'%self.log_num).refresh_button = self.refresh_button
        sm.current = 'tutorial%s'%self.log_num
        #except Exception as e:
            # self.tutorial.remove_widget(self.refresh_button)
            # self.tutorial.add_widget(self.refresh_button)
            # print('compile error\n- ', e)

    ###################
    # TEST_TUTORIAL
    ###################

    def test_db(self, event):
        print('testing database')



    def home(self, event):
        for i in self.layout.children:
            self.layout.remove_widget(i)
        self.layout.add_widget(self.grid)


from main import MasterDateApp
class TestApp(MasterDateApp):
    orientation='portrait'
    def build(self):
        global app
        app = self
        sm.add_widget(TestLayout(name='testlayout'))
        return sm


if __name__ == '__main__':
    TestApp().run()