from kivy.uix.modalview import ModalView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.clock import Clock


class TroublePop(ModalView):
    def __init__(self, question, func_if_yes, **kwargs):
        self.size_hint=(.7, .3)
        super(TroublePop, self).__init__(**kwargs)
        self.func_if_yes = func_if_yes
        self.build_layout(question)
    
    def build_layout(self, question):
        
        self.layout = RelativeLayout()
        self.label = Label(
            text=question,
            font_size='20dp',
            pos_hint={'center_x': .5, 'center_y': .8}
        )
        self.layout.add_widget(self.label)

        self.yes_btn = Button(
            text='Retry',
            font_size='30dp',
            pos_hint={'center_x': .5, 'center_y': .2},
            size_hint=(.5, .23)
        )
        self.yes_btn.bind(on_release=self.func_yes)
        self.layout.add_widget(self.yes_btn)
        self.add_widget(self.layout)
    
    def func_yes(self, event):
        self.dismiss()
        self.yes_btn.unbind(on_release=self.func_yes)

        # Run on a python thread to make the window close immediately
        self.func_if_yes()


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.relativelayout import RelativeLayout
    from kivy.uix.button import Button
    class testApp(App):
        def build(self):
            self.layout = RelativeLayout()
            self.btn = Button()
            self.btn.bind(on_press=self.open_popup)
            self.layout.add_widget(self.btn)
            return self.layout

        def open_popup(self, event):
            func = self.yes_was_clicked
            TroublePop("Trouble connecting", func).open()

        def yes_was_clicked(self):
            print("Yes was clicked")
    testApp().run()