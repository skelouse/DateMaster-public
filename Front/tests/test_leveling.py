from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from os.path import join

class TestApp(App):
    def build(self):
        self.store_file = JsonStore(join(self.user_data_dir, 'user_data.txt'))
        if self.store_file.exists('data'):
            self.ud = self.store_file.get('data')['content']
        else:
            self.ud = {'level': 0, 'level_xp': 100, 'xp': 0}
        
        self.btn = Button(
            text=str(self.ud)
        )
        self.btn.bind(on_press=self.mark_item)
        return self.btn

    def mark_item(self, event):
        self.add_xp(10)

    def add_xp(self, xp):
        new_xp = (self.ud['xp'] + xp)
        if new_xp >= self.ud['level_xp']:
            # level up
            self.ud['level'] += 1
            # find remainder xp after level up
            self.ud['xp'] = new_xp - self.ud['level_xp']
            # set new level_xp
            self.ud['level_xp'] *= 1.5

        else:
            self.ud['xp'] = new_xp

        self.btn.text = str(self.ud)
        

    def on_stop(self):
        self.store_file.put('data', content=self.ud)

TestApp().run()