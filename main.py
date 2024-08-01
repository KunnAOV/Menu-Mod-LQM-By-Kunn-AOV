from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import filechooser
import zipfile
import os
import shutil
import subprocess

class SkinApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        select_btn = Button(text="Chọn file mod")
        select_btn.bind(on_press=self.select_file)
        layout.add_widget(select_btn)
        
        apply_btn = Button(text="Áp dụng")
        apply_btn.bind(on_press=self.apply_skin)
        layout.add_widget(apply_btn)
        
        remove_btn = Button(text="Gỡ bỏ")
        remove_btn.bind(on_press=self.remove_skin)
        layout.add_widget(remove_btn)
        
        back_btn = Button(text="Quay lại")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        return layout

    def select_file(self, instance):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            self.selected_file = selection[0]
            print(f"Selected file: {self.selected_file}")

    def apply_skin(self, instance):
        if hasattr(self, 'selected_file'):
            destination_dir = "/data/data/com.garena.game.kgvn/files/Resources/"

            try:
                with zipfile.ZipFile(self.selected_file, 'r') as zip_ref:
                    zip_ref.extractall("/data/local/tmp/temp_skin")
                
                subprocess.run(["su", "-c", f"cp -r /data/local/tmp/temp_skin/* {destination_dir}"], check=True)
                subprocess.run(["su", "-c", "rm -r /data/local/tmp/temp_skin"], check=True)
                print(f"Extracted {self.selected_file} to {destination_dir}")
            except Exception as e:
                print(f"Error: {e}")

    def remove_skin(self, instance):
        skin_dir = "/data/data/com.garena.game.kgvn/files/Resources/"
        try:
            subprocess.run(["su", "-c", f"rm -r {skin_dir}/*"], check=True)
            print("Removed all custom skins")

            default_skin_dir = "/data/data/com.garena.game.kgvn/files/DefaultResources/"
            subprocess.run(["su", "-c", f"cp -r {default_skin_dir}/* {skin_dir}"], check=True)
            print("Reverted to default skin")
        except Exception as e:
            print(f"Error: {e}")

    def go_back(self, instance):
        pass

if __name__ == '__main__':
    SkinApp().run()
              
