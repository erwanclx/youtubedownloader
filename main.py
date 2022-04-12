from kivy.clock import mainthread
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', False)

from pytube import YouTube
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import threading

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
                on_release: app.init_dl()
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def init_dl(self):
        self.dl_thread = threading.Thread(target=self.download)
        self.dl_thread.start()

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def close_dialog(self, inst):
        self.dialog.dismiss(force=True)
        self.dialog = ""

    def clear(self, inst):
        self.root.ids.urlfield.text = ""
        self.dialog.dismiss()

    def progress(self, stream=None, chunk=None, remaining=None):
        percent = (100 * (file_size - remaining)) / file_size
        self.root.ids.progress.value = percent

    def download(self):
        link = self.root.ids.urlfield.text
        domain1 = 'youtube.com/watch'
        domain2 = "youtu.be/"
        if domain1 in link or domain2 in link:
            global file_size
            yt = YouTube(self.root.ids.urlfield.text, on_progress_callback=self.progress)
            yt = yt.streams.filter(progressive=True).last()
            file_size = yt.filesize
            print('start')
            yt.download()
            print('end')
            threading.Thread(target=self.download_dialog(1)).start()
            self.download_dialog(1)
        else:
            threading.Thread(target=self.download_dialog(2)).start()
            self.download_dialog(2)

    @mainthread
    def download_dialog(self, value):
        dialog = None
        print(value)
        if value == 1:
            if not self.dialog:
                self.dialog = MDDialog(
                    text="Successful download!",
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

        elif value == 2:
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
