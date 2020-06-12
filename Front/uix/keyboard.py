import time
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.modalview import ModalView
from kivy.uix.dropdown import DropDown

class DateKeyboard(ModalView):
    
    def __init__(self, **kwargs):
        super(DateKeyboard, self).__init__(**kwargs)
        self.layout = RelativeLayout()
        self.exit_btn = Button(
            color = (0.231, 0.647, 0.541, .8),
            background_color = (.17,.34,.52,1),
            text='Exit',
            font_size='35dp',
            pos_hint={'center_x': .2, 'center_y': .9},
            size_hint=(.4, .1)
        )
        self.exit_btn.bind(on_press=(self.dismiss))        

        self.keyboard = Keyboard()
        self.layout.add_widget(self.keyboard)
        self.layout.add_widget(self.exit_btn)

        year = time.localtime().tm_year
        self.dropdown = DropDown()
        for i in range(0, 6):
            btn = Button(
                color = (0.231, 0.647, 0.541, .8),
                background_color = (.17,.34,.52,1),
                text='%s' % str(year+i),
                size_hint_y=None,
                size_hint_x=None,
                width=Window.width/3,
                height=Window.height/10,
                font_size='35dp'
            )
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        
        self.mainbutton = Button(
            color = (0.231, 0.647, 0.541, .8),
            background_color = (.17,.34,.52,1),
            text='%s' % year,
            pos_hint={'center_x': .8, 'center_y': .9},
            font_size='50dp',
            size_hint=(.4, .1)
        )
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.layout.add_widget(self.mainbutton)

        self.add_widget(self.layout)


    def open(self, func_if_send):
        self.func_if_send = func_if_send
        super(DateKeyboard, self).open()

    def send_date(self, var_text, two_digits):
        if two_digits:
            date = (var_text[0:2] + '/' +
                var_text[2::] + '/' + self.mainbutton.text)
        else:
            date = (var_text[0:1] + '/' +
                var_text[1::] + '/' + self.mainbutton.text)
        Clock.schedule_once(partial(self.func_if_send, date), .1)
        self.dismiss()
        

class KBTN(Button):
    background_color = (.90,.63,.47,.8)
    color = (0.752, 0.607, 0.349, 1)

    def __init__(self, num, **kwargs):
        super(KBTN, self).__init__(**kwargs)
        self.num = num
        self.font_size = '40dp'
    
    def first_click(self, hit_num):
        if hit_num < int(time.strftime("%m")):
            setattr(self.parent.parent.parent.parent.mainbutton,
               'text', str(1+int(time.strftime("%Y"))))
        else:
            setattr(self.parent.parent.parent.parent.mainbutton,
               'text', str(time.strftime("%Y")))
        if hit_num == 0 and (11 >= int(str(time.strftime("%m")))):
            setattr(self.parent.parent.parent.parent.mainbutton,
               'text', str(time.strftime("%Y")))
        if self.num < 10:
            self.text = self.text[0:2]
            if hit_num == 2:
                if self.num > 2:
                    self.disabled = True
            else:
                if self.num > 3:
                    self.disabled = True
        elif self.num == 11:
            self.num = 0
            self.text = '0'
        else:
            self.text = ''
            self.disabled = True

    def second_click(self, text):
        if int(text) == 22:
            if self.isLeapYear():
                if self.num < 10:
                    self.disabled = False
            else:
                if self.num < 9:
                    self.disabled = False
        elif text[-1] == '3':
            self.disabled = True
            if int(text[0]) == 4:
                if self.num == 0:
                    self.disabled = False
            elif int(text[0]) == 6:
                if self.num == 0:
                    self.disabled = False
            elif int(text[0]) == 9:
                if self.num == 0:
                    self.disabled = False
            elif int(text[0:2]) == 11:
                if self.num == 0:
                    self.disabled = False
            else:
                if self.num < 2:
                    self.disabled = False
        else:
            if self.num < 10:
                if text[-1] == '0' and self.num == 0:
                    self.disabled = True
                else:
                    self.disabled = False
                
    def third_click(self):
        if self.num != 12:
            self.disabled = True
        else:
            self.text = 'Send'
            self.disabled = False
    
    def fourth_click(self, text):
        if self.num != 12 and self.num != 10:
            self.second_click(text)
        else:
            self.text = ''
            self.disabled = True

    def isLeapYear(self):
        ltime = time.localtime()
        if int(ltime.tm_mon) > 8:
            year = int(ltime.tm_year) + 1
        else:
            year = int(ltime.tm_year)
        if year%4 == 0:
            if year%100 == 0:
                if year%400 == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False


class NumberPad(GridLayout):
    cols = 3
    def __init__(self, **kwargs):
        super(NumberPad, self).__init__(**kwargs)

        self.btn = KBTN(1, text='1\nJan')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(2, text='2\nFeb')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(3, text='3\nMar')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(4, text='4\nApr')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(5, text='5\nMay')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(6, text='6\nJun')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(7, text='7\nJul')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(8, text='8\nAug')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(9, text='9\nSep')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(10, text='10\nOct')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(11, text='11\nNov')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

        self.btn = KBTN(12, text='12\nDec')
        self.btn.bind(on_press=self.num_btn)
        self.add_widget(self.btn)

    def num_btn(self, event):
        data_sent = False
        if self.parent.digits_entered == 1:
            self.parent.label.text += str(event.num)
            for i in self.children:
                i.second_click(self.parent.label.text)

        elif self.parent.digits_entered == 2:
            self.parent.label.text += str(event.num)
            for i in self.children:
                i.third_click()
        
        elif self.parent.digits_entered == 3:
            # Where it sends the date
            self.modal = self.parent.parent.parent
            text = self.parent.label.text
            two_digits = self.parent.two_digits
            self.restart(self.parent)
            self.modal.send_date(text, two_digits)
            data_sent = True

        else:
            if event.num >= 10:
                self.parent.two_digits = True
            else:
                self.parent.two_digits = False
            for i in self.children:
                i.first_click(event.num)
                
            print('\n OUT \n')
            if event.num != 0:
                self.parent.label.text += str(event.num)
            else:
                self.parent.label.text += str(11)
        if not data_sent:
            self.parent.digits_entered += 1
            data_sent = False
    
    def restart(self, parent):
        parent.label.text = ''
        parent.digits_entered = 0
        for i in self.children:
            self.remove_widget(i)
        parent.remove_widget(self)
        parent.number_pad = NumberPad(
            size_hint=(None, None),
            size=(Window.width, Window.height/1.55))
        parent.add_widget(parent.number_pad)
            

class Keyboard(FloatLayout):
    background = 'images/background/default.jpg'
    digits_entered = 0
    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        with self.canvas.before:
            self.rect = Rectangle(size=self.size,
                              pos=self.pos,
                              source='images/background/default.jpg')
        self.bind(pos=self.update_rect, size=self.update_rect)


        self.label = Label(
            font_size='55dp',
            pos_hint={'center_x': .45, 'center_y': .71},
            size_hint=(None, None),
            size=(Window.width/5, Window.height/12),
        )
        self.add_widget(self.label)

        self.btn = Button(
            text='<<--',
            background_color = (.90,.63,.47,.8),
            color = (0.752, 0.607, 0.349, 1),
            font_size='60dp',
            pos_hint={'center_x': .84, 'center_y': .72},
            size_hint=(.32, .15),
            #size=(Window.width/4, Window.height/12)
        )
        self.btn.bind(on_press=self.backspace)
        self.add_widget(self.btn)
        self.number_pad = NumberPad(
            size_hint=(None, None),
            size=(Window.width, Window.height/1.55))
        self.add_widget(self.number_pad)

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


    def backspace(self, event):
        if self.digits_entered == 3:
            self.digits_entered = 2
            self.label.text = self.label.text[0:-1]
            for i in self.number_pad.children:
                i.fourth_click(self.label.text)
        
        elif self.digits_entered > 0:
            len_num = 1
            if self.two_digits:
                len_num = 2
            if len(self.label.text) == len_num:
                self.number_pad.restart(self)
            else:
                if self.digits_entered == 2:
                    self.label.text = self.label.text[0:-1]
                    for i in self.number_pad.children:
                        i.disabled = False
                        if self.label.text == '2':
                            if i.num > 2:
                                i.disabled = True
                        else:
                            if i.num > 3:
                                i.disabled = True
                    self.digits_entered = 1
                else:
                    self.label.text = self.label.text[0:-1]
        else:
            pass


if __name__ ==('__main__'):
    class KeyboardApp(App):
    
        def __init__(self, **kwargs):
            super(KeyboardApp, self).__init__(**kwargs)

        def build(self):
            self.date_keyboard = DateKeyboard()
            self.btn = Button(text='Open keyboard')
            self.btn.bind(on_press=self.callback)
            return self.btn

        def callback(self, *args):
            self.date_keyboard.open(self.func_if_send)

        def func_if_send(self, *args):
            print(args)


    KeyboardApp().run()



            