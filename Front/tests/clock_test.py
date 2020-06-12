import time

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock

class TestApp(App):
    def build(self):
        self.button = Button(text='test')
        self.button.bind(on_press=self.callback)
        return self.button

    def callback(self, event):
        Clock.schedule_once(self.test_clock, .1)
        
    def test_clock(self, *args):
        time.sleep(3)

TestApp().run()

