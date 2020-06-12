from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label

class ColorLabel(Label):
    def set_bgcolor(self,r,g,b,o):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(r,g,b,o)
            self.rect = Rectangle(pos=self.pos,size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size