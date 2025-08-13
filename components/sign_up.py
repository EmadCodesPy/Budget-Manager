from nicegui import ui, app
from models import User
from exceptions import UsernameInUseError
from static.css.css_styling import Styling

def sign_up():
                
    with ui.column().classes('w-full h-full justify-center items-center z-20'):
        with ui.card().classes('w-full max-w-sm shadow-2xl mt-32 mb-40 pointer-events-auto'):
            ui.label('Sign Up').classes('text-2xl font-bold mb-2 text-center')

            username_input = ui.input('Username').classes('w-full caret-blue-500')
            name_input = ui.input('Name').classes('w-full caret-blue-500')
            password_input = ui.input('Password').props('type=password').classes('w-full caret-blue-500')

            #Function to validate sign up of new user
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

            ui.button('Sign Up', on_click=handle_signup).classes('w-full bg-blue-500 text-white hover-bg-blue-600')\
            .classes(Styling.hover())