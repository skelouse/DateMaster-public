from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

from kivy.app import App
import main
from main import ItemViewer, sm, DepSelect
from db.database import FireBase, DataBase
import importlib

refresh_token = ""


class TestApp(App):
    
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.id_token = ""
        self.local_id = ""
        self.make_dep(DepSelect)

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        Clock.schedule_interval(self.check_focus, .5)

    def check_focus(self, *dt):
        if Window.focus:
            pass
        else:
            try:
                self.refresh()
            except Exception as e:
                print(e)
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.refresh()
            # self.stop()
        return True 

    def make_dep(self, DepSelect):
        dep = self.selected_dep = 'Dairy'
        DepSelect.todo_deps[self.selected_dep] = {}
        DepSelect.todo_deps[dep]['todo'] = []
        DepSelect.todo_deps[dep]['hidden'] = []
        DepSelect.todo_deps[dep]['queue'] = []
        DepSelect.todo_deps[dep]['num'] = 0
        
        DepSelect.todo_deps[dep]['todo'].append(
            ('606105025', {'date': 0, 'desc': 'O Organics Milk Organic, 12.0 oz', 'ftype': 'oos', 'ghost': False, 'img': 'https://docs.google.com/uc?id=1QTeac1vMgBjALOGvXGs_nFzaEUyL5Zmo', 'price': '$0.00', 'upc': '7989340310'})
        )
        DepSelect.todo_deps[dep]['todo'].append(
            ('606105029', {'date': '11/30/2019', 'desc': 'REESE  SNACK  MIX', 'ftype': 'ood', 'ghost': False, 'img': 'none', 'price': '$0.00', 'upc': '3400021071'})
        )

    def build(self):
        self.refreshbtn = Button(
            text='ref',
            size_hint=(.1, .1)
        )
        self.refreshbtn.bind(on_press=self.refresh)
        sm.add_widget(ItemViewer(name='item_viewer'))
        sm.get_screen('item_viewer').add_widget(self.refreshbtn)
        return sm

    def refresh(self, *event):
        iv = sm.get_screen('item_viewer')
        iv.remove_widget(self.refreshbtn)
        importlib.reload(main)
        from main import ItemViewer, DepSelect
        sm.remove_widget(iv)
        self.make_dep(DepSelect)
        sm.add_widget(ItemViewer(name='item_viewer'))
        sm.get_screen('item_viewer').add_widget(self.refreshbtn)
        sm.get_screen('item_viewer').changeimg.open()

TestApp().run()
