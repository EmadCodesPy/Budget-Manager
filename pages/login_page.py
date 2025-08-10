from nicegui import ui
from components.log_in import login
from components.sign_up import sign_up


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

    #Login page text background
    def moneymanager_text():
        with ui.column().classes('w-full justify-center items-center absolute top-0 z-0'):
            opacity = [100,90,60,50,30,20,10]
            for x in opacity:                
                ui.label('Welcome to MoneyManager').classes('bg-gradient-to-r from-cyan-400 to-blue-700')\
                    .classes(f'bg-clip-text text-transparent text-6xl/[4.5rem] opacity-{x} whitespace-nowrap select-none')\
                    .classes('transition ease-in-out hover:-translation-y-1 hover:scale-110')                   

    #Tabs
    with ui.row().classes('w-screen items-center justify-center'):
        with ui.tabs().classes('rounded-lg border') as tabs:
            log_in = ui.tab('Login')
            signup = ui.tab('Sign Up')

    #Tab content
    with ui.tab_panels(tabs, value=log_in):
        with ui.tab_panel(log_in):
            moneymanager_text()
            login()
            pass
        with ui.tab_panel(signup):
            moneymanager_text()
            sign_up()
            pass

