from nicegui import ui
from components.log_in import login
from components.sign_up import sign_up
from static.css.css_styling import Styling

def login_page():
    
    #CSS to make it not possible to scroll on the page
    ui.add_head_html('''
    <style>
        html, body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
    </style>
    ''')

    #Tabs
    with ui.row().classes('w-screen items-center justify-center'):
        with ui.tabs().classes('rounded-lg border') as tabs:
            log_in = ui.tab('Login')
            signup = ui.tab('Sign Up')

    #Tab content
    with ui.tab_panels(tabs, value=log_in):
        with ui.tab_panel(log_in):
            Styling.moneymanager_text()
            login()
            pass
        with ui.tab_panel(signup):
            Styling.moneymanager_text()
            sign_up()
            pass

