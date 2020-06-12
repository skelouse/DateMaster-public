# ##Tutorial needs to be able to be opened at any time,  MODALVIEW?
# Need a skip tutorial button Always present


from kivy.app import App
from kivy.core.window import Window

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.graphics import Rectangle, Color, Rotate, PushMatrix, PopMatrix

from uix.colorlabel import ColorLabel


class Arrow(Image):
    source='images/arrow.png'

class ArrowDown(Image):
    source='images/arrow_down.png'


class Tutorial(Screen):
    todo_deps = {'Dairy': {}}
    done = False
    def __init__(self, DepSelect, ItemViewer, sm, **kwargs):
        super(Tutorial, self).__init__(**kwargs)
        import time
        self.app = App.get_running_app()
        self.thread_running = False
        self.ItemViewer = ItemViewer
        self.sm = sm
        self.next_func = None
        self.hidebtn = Button()

        today = time.localtime()
        month = today.tm_mon
        day = today.tm_mday
        year = today.tm_year
        mark_day = ("%s/%s/%s" % (month, day+5, year))
        move_day = ("%s/%s/%s" % (month, day+3, year))
        ood_day = ("%s/%s/%s" % (month, day, year))

        todo = {
            '050126008' : {'date': 0,
                'desc': 'MILOS TEA, SWEET',
                'ftype': 'oos',
                'img': 'https://docs.google.com/uc?id=',
                'price': '$0.00',
                'upc': '9147504189'},
            '606105020' : {'date': mark_day,
                'desc': 'Nestle Milk Low Fat, Chocolate',
                'ftype': 'mark',
                'img': 'https://docs.google.com/uc?id=',
                'price': '$0.00',
                'upc': '2800077212'},
            '050125029' : {'date': move_day,
                'desc': 'FLORIDAS NATURAL ORANGE JUICE',
                'ftype': 'move',
                'img': 'https://docs.google.com/uc?id=',
                'price': '$0.00',
                'upc': '1630016824'},
            '050119007' : {'date': ood_day,
                'desc': 'YOPLAIT GO GURT YOGURT, LOW FAT, RASPBERRY, STRAWBERRY BANANA',
                'ftype': 'ood',
                'img': 'https://docs.google.com/uc?id=',
                'price': '$0.00',
                'upc': '7047013773'}
        }
        self.dep_list = {}
        self.dep_list['Dairy'] = ({
            'name': 'Dairy',
            'todo': todo,
            'todo_count': len(todo)
        })
        self.DepSelect = DepSelect
        DepSelect.build_layout(self)

        #self.layout = RelativeLayout()
        self.block = Button(
            background_normal = '',
            background_color=(0,0,0,.1)

        )
        with self.block.canvas:
            Color(1,0,0,-.3)
            Rectangle(pos=(200, 700), size=(100,100))
        #self.add_widget(self.block)
        #self.layout = RelativeLayout()
        fgc = (0.752, 0.607, 0.349, 1)  # orangish for text
        bgc = (.90,.63,.47,.95)  # orangish on grey button
        self.skipbtn = Button(
            text='Skip Tutorial',
            color=fgc,
            background_color=bgc,
            font_size='20dp',
            pos_hint={'center_x': .115, 'center_y': .4},
            size_hint=(.23, .05)
            )
        self.skipbtn.bind(on_press=self.skip_tutorial)
        self.add_widget(self.skipbtn)

    def hide_item(self, event):
        pass


    def back_pressed(self):
        self.app.exit()


    def pre_load_next_image(self, num):
        pass

    def skip_tutorial(self, *event):
        self.app.user['skip_tutorial'] = True
        self.app.save()
        self.sm.current='dep_select'


    def on_enter(self):
        #try:
        #self.add_widget(self.refresh_button)  # for test
        # except AttributeError:
        #     print('Attribute Error')
        #     exit()
        self.select_dep_prompt()

    def select_dep_prompt(self):
        lblbgc = (0.231, 0.647, 0.541, .8)
        #self.add_widget(self.layout)
        self.label = ColorLabel(
            text="There are 4\nitems that need to\nbe checked in Dairy\n   <Tap the box>",
            pos_hint={'center_x':.58, 'center_y':.65},
            font_size='30dp',
            color=lblbgc,
            size_hint=(.65, .2),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.5)

        #self.label.text_size = self.label.size
        self.add_widget(self.label)
        self.arrow = Arrow(
            pos_hint={'center_x': .6, 'center_y': .8}
        )
        self.add_widget(self.arrow)
        # Orb around #4 "You can see there are four items that need to be checked in dairy"<tap anywhere>
        # Orb around whole button "Tap the department to begin"<tap button>
        # facade department list@ for tutorial containing 1 of each ex
        # sm.current='item_viewer'

    def oos_item_prompt(self):
        self.outstock_btn.unbind(on_press=self.next_item)
        lblbgc = (0.231, 0.647, 0.541, 1)
        self.label = ColorLabel(
            text='This item is Out of Stock\n<tap anywhere>',
            pos_hint={'center_x':.58, 'center_y':.6},
            font_size='30dp',
            color=lblbgc,
            size_hint=(.82, .14),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow.pos_hint={'center_x': .6, 'center_y': .7}
        self.add_widget(self.arrow)
        self.next_func = self.mark_item_prompt
        self.outstock_btn.bind(on_press=self.next_func)
        self.block.bind(on_press=self.oos_item_prompt2)
        self.add_widget(self.block)
        self.add_widget(self.skipbtn)

    def oos_item_prompt2(self, event):
        fgc = (0.752, 0.607, 0.349, 1)  # orangish for text
        lblbgc = (0.231, 0.647, 0.541, .8)
        self.remove_widget(self.arrow)
        self.remove_widget(self.label)
        self.remove_widget(self.block)
        self.label = ColorLabel(
            text='Add a new date',
            pos_hint={'center_x': .48, 'center_y': .31},
            color=lblbgc,
            font_size='30dp',
            size_hint=(.57, .06),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow = ArrowDown(
            pos_hint={'center_x': .25, 'center_y': .25}
        )
        self.add_widget(self.arrow)



        # first dep list item is oos
        # Orb around new_date "This item is Out of stock so it needs a new date"<tap new_date>
        #self.open_datekeyboard(1)

    def mark_item_prompt(self, *dt):
        lblbgc = (0.231, 0.647, 0.541, 1)
        self.remove_widget(self.arrow)
        self.remove_widget(self.label)
        self.remove_widget(self.block)
        self.add_widget(self.block)
        self.block.bind(on_press=self.mark_item_prompt2)
        self.label = ColorLabel(
            text='This item might need\nto be marked down\n<tap anywhere>',
            pos_hint={'center_x':.55, 'center_y':.57},
            font_size='30dp',
            color=lblbgc,
            size_hint=(.79, .17),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow = Arrow(
            pos_hint={'center_x': .6, 'center_y': .7}
        )
        self.add_widget(self.arrow)
        self.block.unbind(on_press=self.oos_item_prompt2)
        #self.add_widget(self.block)
        #self.add_widget(self.skipbtn)

    def mark_item_prompt2(self, event):
        lblbgc = (0.231, 0.647, 0.541, .8)
        self.remove_widget(self.arrow)
        self.remove_widget(self.label)
        self.remove_widget(self.block)
        self.label = ColorLabel(
            text='Mark applicable items\nthen press marked,\nor enter a new date',
            pos_hint={'center_x': .5, 'center_y': .37},
            color=lblbgc,
            font_size='30dp',
            size_hint=(.8, .22),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow = ArrowDown(
            pos_hint={'center_x': .5, 'center_y': .25}
        )
        self.add_widget(self.arrow)
        self.arrow2 = ArrowDown(
            pos_hint={'center_x': .25, 'center_y': .25}
        )
        self.add_widget(self.arrow2)

        self.next_func = self.move_item_prompt


        # Orb around Marked button "After marking it down, press here to go to the next item<tap marked button>

    def move_item_prompt(self, *dt):
        self.remove_widget(self.label)
        self.remove_widget(self.arrow)
        self.remove_widget(self.arrow2)
        self.remove_widget(self.block)
        lblbgc = (0.231, 0.647, 0.541, 1)
        self.add_widget(self.block)
        self.block.bind(on_press=self.move_item_prompt2)
        self.label = ColorLabel(
            text='This item might need to be\nmoved to the markdown area\n<tap anywhere>',
            pos_hint={'center_x':.55, 'center_y':.56},
            font_size='28dp',
            color=lblbgc,
            size_hint=(.90, .17),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow = Arrow(
            pos_hint={'center_x': .6, 'center_y': .7}
        )
        self.add_widget(self.arrow)
        self.block.unbind(on_press=self.mark_item_prompt2)

    def move_item_prompt2(self, event):
        lblbgc = (0.231, 0.647, 0.541, .8)
        self.remove_widget(self.arrow)
        self.remove_widget(self.arrow2)
        self.remove_widget(self.label)
        self.remove_widget(self.block)
        self.label = ColorLabel(
            text='Move marked products\nthen press Moved,\nor enter a new date',
            pos_hint={'center_x': .5, 'center_y': .37},
            color=lblbgc,
            font_size='28dp',
            size_hint=(.75, .22),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow = ArrowDown(
            pos_hint={'center_x': .5, 'center_y': .25}
        )
        self.add_widget(self.arrow)
        self.arrow2 = ArrowDown(
            pos_hint={'center_x': .25, 'center_y': .25}
        )
        self.add_widget(self.arrow2)
        self.next_func = self.ood_item_prompt
        # Third item needs to be moved
        # Orb around Move this item? "This item needs to be moved to a markdown area"<tap anywhere>
        # Orb around Moved button  "after moving it, press here to go to the next item<tap moved button>

    def ood_item_prompt(self, *dt):
        self.remove_widget(self.arrow)
        self.remove_widget(self.arrow2)
        self.remove_widget(self.label)
        self.remove_widget(self.block)
        lblbgc = (0.231, 0.647, 0.541, 1)
        self.add_widget(self.block)
        self.block.bind(on_press=self.ood_item_prompt2)
        self.label = ColorLabel(
            text='This item could be\nout of date\n<tap anywhere>',
            pos_hint={'center_x':.55, 'center_y':.56},
            font_size='30dp',
            color=lblbgc,
            size_hint=(.72, .13),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow = Arrow(
            pos_hint={'center_x': .6, 'center_y': .7}
        )
        self.add_widget(self.arrow)
        self.block.unbind(on_press=self.move_item_prompt2)
        # Fourth item needs to be ood
        # Orb around ood message  "This item needs to be pulled"<tap anywhere>
        # Orb around new date button "After pulling it, if all the items were ood\n
        #                             mark out of stock, otherwise, enter the new date
        #                             "<tap new date or oos>
        #self.open_datekeyboard(1)

    def ood_item_prompt2(self, event):
        lblbgc = (0.231, 0.647, 0.541, .8)
        self.remove_widget(self.arrow)
        self.remove_widget(self.label)
        self.remove_widget(self.block)
        self.label = ColorLabel(
            text='Add a new date, or mark oos',
            pos_hint={'center_x': .5, 'center_y': .35},
            color=lblbgc,
            font_size='30dp',
            size_hint=(1, .1),
            halign='center'
        )
        self.label.set_bgcolor(.17,.34,.52,.95)
        self.add_widget(self.label)
        self.arrow = ArrowDown(
            pos_hint={'center_x': .25, 'center_y': .25}
        )
        self.add_widget(self.arrow)

        self.arrow2 = ArrowDown(
            pos_hint={'center_x': .75, 'center_y': .25}
        )
        self.add_widget(self.arrow2)
        self.done = True


        # Last item is NONE
        # Orb around Menu  "Open the menu" <tap menu>
        # Orb around Change Department  "Change to a different department that needs to be checked" <tap change department>
        # sm.current='tut_dep select'
        # make sure Dairy - (0)

        # Orb around the 0  "'Dairy' department is done being checked, and we are done with the tutorial.  Good luck!<tap anywhere>
        # Reload to real dep_select

    def open_keyboard(self, event):
        self.remove_widget(self.arrow)
        self.remove_widget(self.label)
        self.app.date_keyboard.open(self.send_func)
        # Orb around month  "First enter the month of expiration"<tap febuary>
        # Orb around 0 "Then enter first number for day"<tap 0>
        # Orb around 5 "Then enter second number for day"<tap 5>
        # Orb around send "Lastly send the date"<tap send date>
        # self.app.tut_date_keyboard.dismiss()

    def send_func(self, *args):
        self.next_item()

    def select_dep(self, event):

        # Don't actually load item viwer screen, simply remove all current widgets
        # and build layout for self!!
        ItemViewer = self.ItemViewer
        dep = 'Dairy'
        sm = self.sm
        self.queue = False
        self.todo = []
        self.todo_num = 0
        self.app.selected_dep = dep
        self.todo_deps[dep]['todo'] = []
        self.todo_deps[dep]['hidden'] = []
        self.todo_deps[dep]['queue'] = []

        # Later this number can be pulled from storage if date is equal to today
        # along with return to where you left off popup
        self.todo_deps[dep]['num'] = 0

        for i in self.dep_list[dep]['todo'].items():
            if i[1]['date'] == 'hidden':
                self.todo_deps[dep]['hidden'].append(i)
            else:
                self.todo_deps[dep]['todo'].append(i)
        self.clear_widgets()
        ItemViewer.build_layout(self)
        #self.add_widget(self.refresh_button)  # For test
        info = self.todo_deps[dep]
        self.todo = info['todo']
        self.hidden = info['hidden']
        self.todo_num = info['num']
        self.queue = info['queue']
        ItemViewer.re_product(self, self.get_product())
        self.oos_item_prompt()

    def pre_load_next_images(self, *dt):
        pass

    def change_dep(self, event):
        pass

    def sign_out(self, event):
        pass

    def go_right(self, event):
        pass

    def go_left(self, event):
        pass

    def marked(self, event):
        self.next_item()

    def moved(self, event):
        self.next_item()

    def marknmove(self, event):
        pass

    def oos(self, event):
        self.next_item()

    def next_item(self):
        if self.done:
            self.skip_tutorial()
            return True
        else:
            self.ItemViewer.next_item(self)
        self.next_func()

    def re_product(self, product, *dt):
        self.ItemViewer.re_product(self, product)

    def get_product(self):
        try:
            return self.todo[self.todo_num]
        except IndexError:
            self.todo_num = 0
            return self.todo[0]





if __name__ == "__main__":
    from test import TestApp
    TestApp.local_id = '123456'
    TestApp().run()