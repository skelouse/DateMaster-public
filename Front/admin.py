from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.camera import Camera
from functools import partial

class ChangeImage(ModalView):
    # grid layout
        # Camera
        # Web
    def __init__(self, itemviewer, **kwargs):
        super(ChangeImage, self).__init__(**kwargs)
        self.itemviewer = itemviewer
        self.size_hint=(1, .4)
        self.build_layout()
    
    def build_layout(self):
        self.layout = GridLayout(cols=1)

        self.cambtn = Button(
            text='Camera',
            font_size='40dp'
        )
        self.cambtn.bind(on_press=self.usecamera)
        self.layout.add_widget(self.cambtn)

        self.webbtn = Button(
            text='Use Web',
            font_size='40dp'
        )
        self.webbtn.bind(on_press=self.useweb)
        self.layout.add_widget(self.webbtn)

        self.exitbtn = Button(
            text='Exit',
            font_size='40dp'
        )
        self.exitbtn.bind(on_press=self.dismiss)
        self.layout.add_widget(self.exitbtn)

        self.add_widget(self.layout)
        
    def usecamera(self, event):
        CameraTab(self.itemviewer).open()

    def useweb(self, event):
        pass

class WebTab(ModalView):
    def __init__(self, itemviewer, **kwargs):
        super(WebTab, self).__init__(**kwargs)
        self.itemviewer = itemviewer
        self.build_layout()

    def build_layout(self):
        pass


class CameraTab(ModalView):
    def __init__(self, itemviewer,**kwargs):
        super(CameraTab, self).__init__(**kwargs)
        self.itemviewer = itemviewer
        self.build_layout()

    def build_layout(self):

        self.grid=GridLayout(
            size_hint=(1, 1),
            cols=1,
            pos_hint={'center_y': .1, 'center_x': .5}
        )
        
        self.cam = Camera(
            play=False
        )
        self.grid.add_widget(self.cam)

        self.capturebtn = Button(
            text='Capture',
            font_size='40dp',
            size_hint_y=None,
            height='48dp',
        )
        self.capturebtn.bind(on_press=self.capture)
        self.grid.add_widget(self.capturebtn)

        self.exitbtn = Button(
            text='Exit',
            font_size='40dp',
            size_hint_y=None,
            height='48dp'
        )
        self.exitbtn.bind(on_press=self.exit)
        self.grid.add_widget(self.exitbtn)
        self.add_widget(self.grid)



    def capture(self, *args):
        print('camera args', args)
        self.pr = self.itemviewer.pr
        picstr = self.pr[1]['desc']

    def exit(self, event):
        self.dismiss()



        

class ChangeDesc(ModalView):
    # Relative layout
        # multiline equal font to desc block Textinput
        # save   //   exit
    def __init__(self, itemviewer, **kwargs):
        super(ChangeDesc, self).__init__(**kwargs)
        self.itemviewer = itemviewer
        self.size_hint=(1, .4)
        self.build_layout()

    def build_layout(self):
        self.layout = RelativeLayout()
        self.label = Label(
            text='Description = ',
            pos_hint={'center_y': .8},
            font_size='40dp'
        )
        self.layout.add_widget(self.label)

        self.desc = TextInput(
            hint_text='desc',
            pos_hint={'center_y': .5, 'center_x': .5},
            multiline=False,
            font_size='40dp',
            size_hint=(.9, .3)
        )
        self.layout.add_widget(self.desc)

        self.setbtn = Button(
            text='Set',
            font_size='25dp',
            pos_hint={'center_y': .2, 'center_x': .25},
            size_hint=(.4, .2)
        )
        self.layout.add_widget(self.setbtn)

        self.exitbtn = Button(
            text='Exit',
            font_size='25dp',
            pos_hint={'center_y': .2, 'center_x': .75},
            size_hint=(.4, .2)
        )
        self.exitbtn.bind(on_press=self.dismiss)
        self.layout.add_widget(self.exitbtn)

        self.add_widget(self.layout)


class ChangeGhost(ModalView):
    # Relative
        # label ghost? currently (y)
        # Yes // no
        # exit

    def __init__(self, itemviewer, **kwargs):
        super(ChangeGhost, self).__init__(**kwargs)
        self.itemviewer = itemviewer
        self.size_hint=(.6, .3)
        self.build_layout()

    def build_layout(self):
        self.layout = RelativeLayout()
        self.label = Label(
            text='Ghosted = ',
            pos_hint={'center_y': .8},
            font_size='40dp'
        )
        self.layout.add_widget(self.label)

        self.yesbtn = Button(
            text='set True',
            font_size='25dp',
            pos_hint={'center_y': .4, 'center_x': .25},
            size_hint=(.4, .2)
        )
        self.layout.add_widget(self.yesbtn)

        self.nobtn = Button(
            text='set False',
            font_size='25dp',
            pos_hint={'center_y': .4, 'center_x': .75},
            size_hint=(.4, .2)
        )
        self.layout.add_widget(self.nobtn)

        self.exitbtn = Button(
            text='Exit',
            font_size='40dp',
            pos_hint={'center_y': .15, 'center_x': .5},
            size_hint=(.6, .2)
        )
        self.layout.add_widget(self.exitbtn)

        self.add_widget(self.layout)

class UPCBase():

    def __init__(self, app):
        pass


def run(self):  # ItemViewer is self.
    self.upcdb = UPCBase
    self.changeghost = ChangeGhost(self)
    self.changedesc = ChangeDesc(self)
    self.changeimg = ChangeImage(self)
    fgc = (0.752, 0.607, 0.349, 1)  # orangish for text
    bgc = (.90,.63,.47,.95)  # orangish on grey button

    # Button to change image in upc_data
    self.imagebtn = Button(
        text='Change image',
        color=fgc,
        background_color=bgc,
        font_size='30dp',
        size_hint=(None, None),
        width=Window.width,
        height=Window.height/8
    )
    self.imagebtn.bind(on_press=self.changeimg.open)
    self.dropdown.add_widget(self.imagebtn)

    # Button to change desc in upc_data
    self.descbtn = Button(
        text='Change Description',
        color=fgc,
        background_color=bgc,
        font_size='30dp',
        size_hint=(None, None),
        width=Window.width,
        height=Window.height/8
    )
    self.descbtn.bind(on_press=self.changedesc.open)
    self.dropdown.add_widget(self.descbtn)

    # Button to change ghost in upc_data
    self.ghostbtn = Button(
        text='Change ghost',
        color=fgc,
        background_color=bgc,
        font_size='30dp',
        size_hint=(None, None),
        width=Window.width,
        height=Window.height/8
    )
    self.ghostbtn.bind(on_press=self.changeghost.open)
    self.dropdown.add_widget(self.ghostbtn)





