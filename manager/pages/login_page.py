from nicegui import ui, app
from models import User
from exceptions import UsernameInUseError

def login_page():

    def moneymanager_text():
        with ui.column().classes('w-screen justify-center items-center absolute top-0 z-0 '):
            opacity = [100,90,60,50,30,20,10]
            for x in opacity:                
                ui.label('Welcome to MoneyManager').classes('bg-gradient-to-r from-cyan-400 to-blue-700')\
                    .classes(f'bg-clip-text text-transparent text-6xl/[4.5rem] opacity-{x}')

    def login():

        with ui.column().classes('w-screen items-center items-center'):
            moneymanager_text()
            with ui.card().classes('w-full max-w-sm shadow-lg mt-32 mb-40'):
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
                    
                    ui.notify('Welcome', type='positive')
                    ui.navigate.to('/dashboard')
                
                ui.button('Log In', on_click=handle_login).classes('mt-4 w-full bg-blue-500 text-white hover:bg-blue-600')\
                    .classes('transition ease-in-out duration-150 hover:-translate-y-1 hover:scale-105')
                

    def signup():
        with ui.column().classes('h-screen w-screen items-center mt-32 z-10'):
            moneymanager_text()
            with ui.card().classes('w-full max-w-sm shadow-lg'):
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
                .classes('transition ease-in-out duration-150 hover:-translate-y-1 hover:scale-105')

    with ui.row().classes('w-screen items-center justify-center'):
        with ui.tabs().classes('rounded-lg border') as tabs:
            log_in = ui.tab('Login')
            sign_up = ui.tab('Sign Up')

    with ui.tab_panels(tabs, value=log_in):
        with ui.tab_panel(log_in):
            login()
        with ui.tab_panel(sign_up):
            signup()
