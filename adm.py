# main.py (ou adm.py)

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy_garden.mapview import MapView, MapMarker
from kivymd.uix.screen import MDScreen
import json
import os
import hashlib
import re

# Importa a tela do mapa
from map import MapScreen

KV = '''
ScreenManager:
    LoginScreen:
        name: 'login_screen'
    SignupScreen:
        name: 'signup_screen'
    HomeScreen:
        name: 'home_screen'
    AdminScreen:
        name: 'admin_screen'
    MapScreen:
        name: 'map_screen'

<LoginScreen>:
    MDFloatLayout:
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Login"
            font_style: "H3"
            bold: True
            pos_hint: {"center_x": 0.5, "center_y": 0.8}
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDTextField:
            id: username
            hint_text: "Usuário"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            size_hint_x: 0.8
            mode: "rectangle"
            icon_right: "account"
            icon_right_color: 1, 1, 1, 0.7
            line_color_focus: 1, 1, 1, 1
            text_color: 1, 1, 1, 1
            hint_text_color: 1, 1, 1, 0.7
            background_color: 0, 0, 0, 0

        MDTextField:
            id: password
            hint_text: "Senha"
            password: True
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint_x: 0.8
            mode: "rectangle"
            icon_right_color: 1, 1, 1, 0.7
            line_color_focus: 1, 1, 1, 1
            text_color: 1, 1, 1, 1
            hint_text_color: 1, 1, 1, 0.7
            background_color: 0, 0, 0, 0

        MDIconButton:
            id: eye_button
            icon: root.password_icon
            pos_hint: {"center_x": 0.85, "center_y": 0.5}
            user_font_size: "24sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.7
            on_release: root.toggle_password_visibility()

        MDRaisedButton:
            text: "Entrar"
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            size_hint_x: 0.8
            md_bg_color: 1, 0, 0, 1
            on_release: root.login()

        MDTextButton:
            text: "Criar conta"
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            text_color: 1, 1, 1, 0.9
            on_release:
                root.manager.current = 'signup_screen'

<SignupScreen>:
    MDFloatLayout:
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Cadastro"
            font_style: "H3"
            bold: True
            pos_hint: {"center_x": 0.5, "center_y": 0.9}
            theme_text_color: "Custom"
            halign: "center"
            text_color: 1, 1, 1, 1

        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: 0.8
            size_hint_y: 0.65
            pos_hint: {"center_x": 0.5, "top": 0.85}
            spacing: dp(25)

            MDTextField:
                id: new_username
                hint_text: "Usuário"
                mode: "rectangle"
                icon_right: "account"
                icon_right_color: 1, 1, 1, 0.7
                line_color_focus: 1, 1, 1, 1
                text_color: 1, 1, 1, 1
                hint_text_color: 1, 1, 1, 0.7
                background_color: 0, 0, 0, 0

            MDTextField:
                id: email
                hint_text: "E-mail"
                mode: "rectangle"
                icon_right: "email"
                icon_right_color: 1, 1, 1, 0.7
                line_color_focus: 1, 1, 1, 1
                text_color: 1, 1, 1, 1
                hint_text_color: 1, 1, 1, 0.7
                background_color: 0, 0, 0, 0

            MDTextField:
                id: phone_number
                hint_text: "Número de telefone"
                mode: "rectangle"
                icon_right: "phone"
                icon_right_color: 1, 1, 1, 0.7
                line_color_focus: 1, 1, 1, 1
                text_color: 1, 1, 1, 1
                hint_text_color: 1, 1, 1, 0.7
                background_color: 0, 0, 0, 0
                text: "+55 "
                on_text:
                    root.fix_phone_prefix()
                on_focus:
                    if self.focus: root.fix_phone_prefix()

            BoxLayout:
                size_hint_y: None
                height: dp(48)

                MDTextField:
                    id: new_password
                    hint_text: "Senha"
                    password: root.password_hidden
                    mode: "rectangle"
                    icon_right_color: 1, 1, 1, 0.7
                    line_color_focus: 1, 1, 1, 1
                    text_color: 1, 1, 1, 1
                    hint_text_color: 1, 1, 1, 0.7
                    background_color: 0, 0, 0, 0

                MDIconButton:
                    icon: "eye-off" if root.password_hidden else "eye"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.7
                    on_release: root.toggle_password_visibility()

            BoxLayout:
                size_hint_y: None
                height: dp(48)

                MDTextField:
                    id: confirm_password
                    hint_text: "Confirmar senha"
                    password: root.confirm_password_hidden
                    mode: "rectangle"
                    icon_right_color: 1, 1, 1, 0.7
                    line_color_focus: 1, 1, 1, 1
                    text_color: 1, 1, 1, 1
                    hint_text_color: 1, 1, 1, 0.7
                    background_color: 0, 0, 0, 0

                MDIconButton:
                    icon: "eye-off" if root.confirm_password_hidden else "eye"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.7
                    on_release: root.toggle_confirm_password_visibility()

        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: 0.8
            size_hint_y: None
            height: dp(120)
            pos_hint: {"center_x": 0.5, "y": 0.05}
            spacing: dp(15)

            MDRaisedButton:
                text: "Cadastrar"
                size_hint_y: None
                height: dp(48)
                md_bg_color: 1, 0, 0, 1
                on_release: root.signup()

            MDTextButton:
                text: "Voltar para login"
                text_color: 1, 1, 1, 0.9
                size_hint_y: None
                height: dp(48)
                on_release: root.manager.current = 'login_screen'

<HomeScreen>:
    MDFloatLayout:
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            id: welcome_label
            text: "Bem-vindo!"
            font_style: "H4"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            text: "Sair"
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            size_hint_x: 0.5
            md_bg_color: 1, 0, 0, 1
            on_release:
                root.manager.current = 'login_screen'

<AdminScreen>:
    MDFloatLayout:
        md_bg_color: 0, 0, 0, 1

        MDTopAppBar:
            title: "Painel Administrativo"
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: root.back_to_home()]]

        ScrollView:
            pos_hint: {"top": 0.9, "left": 1}
            size_hint: 1, 0.8

            MDList:
                id: users_list
                spacing: "10dp"
                padding: "20dp"

        MDFloatingActionButton:
            icon: "refresh"
            pos_hint: {"x": 0.05, "y": 0.05}
            on_release: root.load_users()

<MapScreen>:
    MDFloatLayout:
        md_bg_color: 0, 0, 0, 1

        MDBoxLayout:
            id: map_box
            orientation: "vertical"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            size_hint: 0.9, 0.7

        MDLabel:
            text: "Tela do Mapa"
            halign: "center"
            pos_hint: {"center_x": 0.5, "center_y": 0.95}
            size_hint_y: None
            height: "40dp"

        MDRaisedButton:
            text: "Sair do mapa"
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
            on_release:
                root.manager.current = 'home_screen'
'''

# Funções auxiliares
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Classes de tela
class LoginScreen(Screen):
    password_icon = "eye-off"

    def login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if not username or not password:
            self.show_dialog("Erro", "Preencha todos os campos.")
            return

        users = load_users()
        hashed = hash_password(password)

        if username in users and users[username]["password"] == hashed:
            if users[username].get('blocked', False):
                self.show_dialog("Bloqueado", "Seu usuário está bloqueado. Contate o administrador.")
                return
            if not users[username].get('approved', False):
                self.show_dialog("Aguardando aprovação", "Seu cadastro ainda não foi aprovado pelo administrador.")
                return

            if users[username].get('is_admin', False):
                self.manager.current = 'admin_screen'
            else:
                self.manager.current = 'map_screen'  # usuário comum vai para mapa

            self.clear_fields()
        else:
            self.show_dialog("Erro", "Usuário ou senha inválidos.")

    def clear_fields(self):
        self.ids.username.text = ""
        self.ids.password.text = ""

    def show_dialog(self, title, text):
        if hasattr(self, '_dialog') and self._dialog:
            self._dialog.dismiss()
        self._dialog = MDDialog(title=title, text=text, size_hint=(0.8, None), auto_dismiss=True)
        self._dialog.open()

    def toggle_password_visibility(self):
        password_field = self.ids.password
        if password_field.password:
            password_field.password = False
            self.password_icon = "eye"
        else:
            password_field.password = True
            self.password_icon = "eye-off"
        self.ids.eye_button.icon = self.password_icon

class SignupScreen(Screen):
    password_hidden = True
    confirm_password_hidden = True
    phone_prefix = "+55 "

    def fix_phone_prefix(self):
        phone = self.ids.phone_number
        if not phone.text.startswith(self.phone_prefix):
            text_without_prefix = phone.text.replace(self.phone_prefix, "")
            phone.text = self.phone_prefix + text_without_prefix
        if phone.cursor_index() < len(self.phone_prefix):
            phone.cursor = (len(self.phone_prefix), 0)

    def toggle_password_visibility(self):
        self.password_hidden = not self.password_hidden
        self.ids.new_password.password = self.password_hidden

    def toggle_confirm_password_visibility(self):
        self.confirm_password_hidden = not self.confirm_password_hidden
        self.ids.confirm_password.password = self.confirm_password_hidden

    def signup(self):
        username = self.ids.new_username.text.strip()
        email = self.ids.email.text.strip()
        phone = self.ids.phone_number.text.strip()

        if phone.startswith(self.phone_prefix):
            phone = phone[len(self.phone_prefix):].strip()

        password = self.ids.new_password.text.strip()
        confirm_password = self.ids.confirm_password.text.strip()

        if not all([username, email, phone, password, confirm_password]):
            self.show_dialog("Erro", "Preencha todos os campos.")
            return

        if not validate_email(email):
            self.show_dialog("Erro", "Informe um e-mail válido.")
            return

        if not self.validate_phone(phone):
            self.show_dialog("Erro", "Informe um número de telefone válido (8 a 11 dígitos).")
            return

        if not self.validate_password(password):
            self.show_dialog(
                "Erro",
                "Senha deve ter no mínimo 8 caracteres, incluindo letras maiúsculas, "
                "minúsculas, números e caracteres especiais."
            )
            return

        if password != confirm_password:
            self.show_dialog("Erro", "As senhas não coincidem.")
            return

        users = load_users()
        if username in users:
            self.show_dialog("Erro", "Usuário já existe.")
            return

        users[username] = {
            "email": email,
            "phone": f"{self.phone_prefix}{phone}",
            "password": hash_password(password),
            "approved": False,
            "blocked": False,
            "is_admin": False
        }
        save_users(users)
        self.show_dialog("Sucesso", "Usuário cadastrado com sucesso! Aguarde aprovação.")
        self.manager.current = 'login_screen'
        self.clear_fields()

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[^\w\s]", password):
            return False
        return True

    def validate_phone(self, phone):
        return phone.isdigit() and 8 <= len(phone) <= 11

    def clear_fields(self):
        self.ids.new_username.text = ""
        self.ids.email.text = ""
        self.ids.phone_number.text = self.phone_prefix
        self.ids.new_password.text = ""
        self.ids.confirm_password.text = ""

    def show_dialog(self, title, text):
        if hasattr(self, '_dialog') and self._dialog:
            self._dialog.dismiss()
        self._dialog = MDDialog(title=title, text=text, size_hint=(0.8, None), auto_dismiss=True)
        self._dialog.open()

class HomeScreen(Screen):
    pass

class AdminScreen(Screen):
    def on_pre_enter(self):
        self.load_users()

    def load_users(self):
        users = load_users()
        self.ids.users_list.clear_widgets()

        for username, user in users.items():
            status = "[color=00FF00]Aprovado[/color]" if user.get("approved", False) else "[color=FF0000]Pendente[/color]"
            blocked = "[color=FF0000]Bloqueado[/color]" if user.get("blocked", False) else "[color=00FF00]Ativo[/color]"
            text = f"{username} - {status} - {blocked}"
            secondary_text = f"Email: {user.get('email', '')} | Telefone: {user.get('phone', '')}"
            item = TwoLineListItem(
                text=text,
                secondary_text=secondary_text,
                on_release=lambda x, u=username: self.show_user_actions(u)
            )
            self.ids.users_list.add_widget(item)

    def show_user_actions(self, username):
        users = load_users()
        user = users.get(username)
        if not user:
            self.show_dialog("Erro", "Usuário não encontrado.")
            return

        menu_items = [
            {
                "text": "Aprovar" if not user.get("approved", False) else "Reprovar",
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=username: self.toggle_approval(x),
            },
            {
                "text": "Bloquear" if not user.get("blocked", False) else "Desbloquear",
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=username: self.toggle_block(x),
            },
            {
                "text": "Excluir",
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=username: self.delete_user(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.users_list,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def toggle_approval(self, username):
        users = load_users()
        users[username]["approved"] = not users[username].get("approved", False)
        save_users(users)
        self.menu.dismiss()
        self.load_users()
        self.show_dialog("Sucesso", f"Status de aprovação de {username} alterado!")

    def toggle_block(self, username):
        users = load_users()
        users[username]["blocked"] = not users[username].get("blocked", False)
        save_users(users)
        self.menu.dismiss()
        self.load_users()
        self.show_dialog("Sucesso", f"Status de bloqueio de {username} alterado!")

    def delete_user(self, username):
        users = load_users()
        if username in users:
            del users[username]
            save_users(users)
            self.menu.dismiss()
            self.load_users()
            self.show_dialog("Sucesso", f"Usuário {username} excluído!")

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.8, None), auto_dismiss=True)
        dialog.open()

    def back_to_home(self):
        self.manager.current = 'home_screen'

class MyApp(MDApp):
    title = "iJob"
    password_icon = "eye-off"

    def on_enter(self):
        self.update_markers()

    def update_markers(self):
        # Garante que o id map_box existe
        if "map_box" not in self.ids:
            print("ERRO: id 'map_box' não encontrado na tela do mapa!")
            return

        self.ids.map_box.clear_widgets()
        mapview = MapView(zoom=4, lat=-15.78, lon=-47.93)  # Centro do Brasil
        users = load_users()
        for username, user in users.items():
            lat = user.get("lat")
            lon = user.get("lon")
            if lat is not None and lon is not None:
                marker = MapMarker(lat=lat, lon=lon)
                mapview.add_marker(marker)
        self.ids.map_box.add_widget(mapview)

# ----------- APP -----------
class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    MyApp().run()
