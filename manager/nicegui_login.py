from nicegui import ui
from models import User
from exceptions import UsernameInUseError


def login():

    with ui.column().classes('h-screen w-screen items-center mt-32'):
        with ui.card().classes('w-full max-w-sm shadow-lg'):
            ui.label('Login').classes('text-2xl font-bold mb-2 text-center')

            username_input = ui.input('Username').props('type=email').classes('w-full')
            password_input = ui.input('Password').props('type=password').classes('w-full')
            
            def handle_login():
                if username_input.value == '' or password_input.value == '':
                    ui.notify('Please enter Username and Password', type='info')
                    return
                user = User.login(username_input.value, password_input.value)
                if user:
                    ui.notify('Welcome', type='positive')
                    return
                elif not user:
                    ui.notify('Invalid Username or Password', type='negative')
                    return
                
            
            ui.button('Log In', on_click=handle_login).classes('mt-4 w-full bg-blue-500 text-white hover:bg-blue-600')


def signup():
    with ui.column().classes('h-screen w-screen items-center mt-32'):
        with ui.card().classes('w-full max-w-sm shadow-lg'):
            ui.label('Sign Up').classes('text-2xl font-bold mb-2 text-center')

            username_input = ui.input('Username').classes('w-full')
            name_input = ui.input('Name').classes('w-full')
            password_input = ui.input('Password').props('type=password').classes('w-full')

            def handle_signup():
                if username_input.value == '' or name_input.value == '' or password_input.value == '':
                    ui.notify('Please fill in all fields', type='info')
                    return
                try:
                    user = User.sign_up(username_input.value, name_input.value, password_input.value)
                except UsernameInUseError:
                    ui.notify('Username already in use :(', type='negative')
                    return
                if user:
                    ui.notify(f'Welcome {name_input.value}', type='positive')
                    return

            ui.button('Sign Up', on_click=handle_signup).classes('w-full bg-blue-500 text-white hover-bg-blue-600')


with ui.tabs().classes('w-screen') as tabs:
    log_in = ui.tab('Login')
    sign_up = ui.tab('Sign Up')

with ui.tab_panels(tabs, value=log_in).classes('w-full'):
    with ui.tab_panel(log_in):
        login()
    with ui.tab_panel(sign_up):
        signup()

ui.run(host='127.0.0.1', port=8001)