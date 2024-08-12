from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
import requests
from room import RoomScreen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[50, 100, 50, 100], spacing=20)

        # Set background color
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # white background
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Username input
        username_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        with username_layout.canvas.before:
            Color(1, 1, 1, 1)  # white background
            self.username_rect = Rectangle(size=username_layout.size, pos=username_layout.pos)
            username_layout.bind(size=self._update_username_rect, pos=self._update_username_rect)
        username_label = Label(text='Username:', size_hint=(None, None), size=(100, 40), color=(0, 0, 0, 1))
        self.username = TextInput(multiline=False)
        username_layout.add_widget(username_label)
        username_layout.add_widget(self.username)
        
        # Password input
        password_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        with password_layout.canvas.before:
            Color(1, 1, 1, 1)  # white background
            self.password_rect = Rectangle(size=password_layout.size, pos=password_layout.pos)
            password_layout.bind(size=self._update_password_rect, pos=self._update_password_rect)
        password_label = Label(text='Password:', size_hint=(None, None), size=(100, 40), color=(0, 0, 0, 1))
        password_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.password = TextInput(password=True, multiline=False)
        self.show_password_button = Button(text='Show', size_hint=(None, None), size=(60, 40), pos_hint={'center_y': 0.5},
                                           background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        self.show_password_button.bind(on_press=self.toggle_password_visibility)
        password_box.add_widget(self.password)
        password_box.add_widget(self.show_password_button)
        password_layout.add_widget(password_label)
        password_layout.add_widget(password_box)
        
        # Add layouts to main layout
        layout.add_widget(username_layout)
        layout.add_widget(password_layout)
        
        # Buttons
        self.buttons_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=100, spacing=10)
        self.login_button = Button(text='Login', size_hint=(None, None), size=(200, 40), pos_hint={'center_x': 0.5},
                                   background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        self.login_button.bind(on_press=self.validate_login)
        self.register_button = Button(text='Register', size_hint=(None, None), size=(200, 40), pos_hint={'center_x': 0.5},
                                      background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        self.register_button.bind(on_press=self.register_user)
        
        # Add black border to buttons
        self.login_button.bind(pos=self._update_button_border, size=self._update_button_border)
        self.register_button.bind(pos=self._update_button_border, size=self._update_button_border)

        self.buttons_layout.add_widget(self.login_button)
        self.buttons_layout.add_widget(self.register_button)
        
        layout.add_widget(self.buttons_layout)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_username_rect(self, instance, value):
        self.username_rect.pos = instance.pos
        self.username_rect.size = instance.size

    def _update_password_rect(self, instance, value):
        self.password_rect.pos = instance.pos
        self.password_rect.size = instance.size

    def _update_button_border(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0, 0, 1)
            Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=1.5)

    def toggle_password_visibility(self, instance):
        self.password.password = not self.password.password
        self.show_password_button.text = 'Hide' if not self.password.password else 'Show'

    def validate_login(self, instance):
        username = self.username.text
        password = self.password.text
        try:
            response = requests.post('http://10.77.138.10:5000/login', json={'username': username, 'password': password})
            response_data = response.json()
            if response_data.get('success'):
                print("Login successful!")
                self.manager.current = 'room'  # Switch to the room screen
            else:
                self.show_popup(response_data.get('message', "Invalid username or password."))
        except requests.exceptions.RequestException as e:
            self.show_popup(f"Connection error: {e}")

    def register_user(self, instance):
        username = self.username.text
        password = self.password.text
        try:
            response = requests.post('http://10.77.138.10:5000/register', json={'username': username, 'password': password})
            response_data = response.json()
            if response_data.get('success'):
                self.show_popup("User registered successfully.")
            else:
                self.show_popup(response_data.get('message', "Username already exists."))
        except requests.exceptions.RequestException as e:
            self.show_popup(f"Connection error: {e}")

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=message)
        button = Button(text='OK', size_hint=(None, None), size=(100, 40))
        content.add_widget(label)
        content.add_widget(button)
        popup = Popup(title='Notification', content=content, size_hint=(None, None), size=(300, 200))
        button.bind(on_press=popup.dismiss)
        popup.open()

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RoomScreen(name='room'))
        return sm

if __name__ == '__main__':
    LoginApp().run()
