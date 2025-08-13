from nicegui import ui, app
from models import User
from static.css.css_styling import Styling

def login():
    
    with ui.column().classes('w-full h-full justify-center items-center z-20'):
        with ui.card().classes('w-full max-w-sm shadow-2xl mt-32 mb-40 pointer-events-auto'):
            ui.label('Login').classes('text-2xl font-bold mb-2 text-center')

            username_input = ui.input('Username').classes('w-full caret-blue-500')
            password_input = ui.input('Password', password=True).classes('w-full caret-blue-500')
            
            #Function to validate login and save details to storage
            def handle_login():
                if username_input.value == '' or password_input.value == '':
                    ui.notify('Please enter Username and Password', type='info')
                    return
                user = User.login(username_input.value, password_input.value)
                if not user:
                    ui.notify('Invalid Username or Password', type='negative')
                    return           
                ui.notify('Welcome', type='positive')

                app.storage.user['logged_in'] = True
                app.storage.user['username'] = user.username
                app.storage.user['name'] = user.name
                
                ui.navigate.to('/dashboard')
            
            ui.button('Log In', on_click=handle_login).classes('mt-4 w-full bg-blue-500 text-white hover:bg-blue-600')\
                .classes(Styling.hover())