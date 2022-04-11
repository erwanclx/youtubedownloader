from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', False)

from pytube import YouTube
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

KV = '''
MDBoxLayout:
    orientation: "vertical"      
    MDToolbar:
        title: "Youtube Downloader"
        md_bg_color: app.theme_cls.primary_color 
    MDBoxLayout:
        size_hint: [.9, .9]
        pos_hint: { 'top' : .95, 'right': .95}
        orientation: "vertical"
        BoxLayout:
            padding: "10dp"
            MDProgressBar:
                id: progress
                value: 0
        MDLabel:
            text: "Fill the field and click the Launch! button"       
        MDTextField:
            id: urlfield
            hint_text: "Paste your YouTube link"
            helper_text: "This field is required."
            helper_text_mode: "on_error"
        MDBoxLayout:
            
            MDFillRoundFlatIconButton:
                text: "Launch!"
                icon: "arrow-right-circle" 
                on_release: app.test()
                pos_hint: {"center_x": .9, "center_y": .5}
                
            MDFloatLayout:
                MDFloatingActionButton:
                    icon: "autorenew"
                    md_bg_color: app.theme_cls.error_color
                    on_release: app.show_alert_dialog()
                    pos_hint: {"center_x": .9, "center_y": .5}
'''


class Downloader(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def close_dialog(self, inst):
        self.dialog.dismiss()

    def clear(self, inst):
        self.root.ids.urlfield.text = ""
        self.dialog.dismiss()

    def progress(self, stream=None, chunk=None, remaining=None):
        percent = (100 * (file_size - remaining)) / file_size
        self.root.ids.progress.value = percent

    def test(self):
        link = self.root.ids.urlfield.text
        domain1 = 'youtube.com/watch'
        domain2 = "youtu.be/"
        if domain1 in link or domain2 in link:
            global file_size
            yt = YouTube(self.root.ids.urlfield.text, on_progress_callback=self.progress)
            print("Downloading...")
            yt = yt.streams.filter(progressive=True).last()
            file_size = yt.filesize

            yt.download()
            print("Download completed!!")
        else:
            if not self.dialog:
                self.dialog = MDDialog(
                    text="Please enter a valid Youtube link",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_dialog
                        )
                    ],
                )
            self.dialog.open()

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Reset the configuration?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="RESET",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.error_color,
                        on_release=self.clear
                    ),
                ],
            )
        self.dialog.open()

Downloader().run()
