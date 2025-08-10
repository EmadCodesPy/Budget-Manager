from nicegui import ui, app
from components.account_header import header
from components.account_cards import account_cards

def account_page():
    
    #Logged in check, its within a column to make sure the page and storage render first before the check
    with ui.column():
        if not app.storage.user.get('logged_in') or not app.storage.user.get('username'):
            ui.notify('Please log in first')
            ui.navigate.to('/')
            return                    
    
    header()
    account_cards()
