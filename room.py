from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import socket
import json
import threading

class RoomScreen(Screen):
    def __init__(self, **kwargs):
        super(RoomScreen, self).__init__(**kwargs)
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.room_input = TextInput(hint_text='Enter Room Number', multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.room_input)
        
        self.status_label = Label(text="Not connected", size_hint=(1, 0.2))
        self.layout.add_widget(self.status_label)
        
        self.join_button = Button(text='Join Room', size_hint=(1, 0.2))
        self.join_button.bind(on_press=self.join_room)
        self.layout.add_widget(self.join_button)
        
        self.add_widget(self.layout)
        
        self.sock = None
        self.SERVER_ADDRESS = "127.0.0.1"
        self.SERVER_PORT = 5200

    def join_room(self, instance):
        room_number = self.room_input.text
        if not room_number:
            self.show_popup("Error", "Please enter a room number.")
            return
        
        self.status_label.text = "Connecting..."
        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.SERVER_ADDRESS, self.SERVER_PORT))
            self.status_label.text = "Connected to server"
           
            threading.Thread(target=self.handle_server_response, args=(room_number,)).start()
            
        except Exception as e:
            self.status_label.text = f"Connection failed: {e}"
            self.sock = None
    
    def handle_server_response(self, room_number):
        try:
            self.sock.sendall(json.dumps({
                'type': 'join',
                'game_id': room_number
            }).encode('utf-8'))
            
            response = self.sock.recv(1024).decode('utf-8')
            data = json.loads(response)
            if data['type'] == 'start':
                self.status_label.text = f"Game started as player {data['player']} with color {data['color']}"
            elif data['type'] == 'waiting':
                self.status_label.text = "Waiting for another player..."
            else:
                self.status_label.text = "Unexpected response from server"
                
        except Exception as e:
            self.status_label.text = f"Error: {e}"
    
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message)
        close_button = Button(text='Close', size_hint=(1, 0.2))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.5, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

# Example usage:
if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager
    
    class MyApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(RoomScreen(name='room'))
            return sm
    
    MyApp().run()
