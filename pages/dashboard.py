from nicegui import ui, app
from models import Transaction
from components.dashboard_header import header
from components.dashboard_left_drawer import left_drawer
from components.dashboard_transactions import transactions

def dashboard():
    
    #Dark mode check
    if app.storage.user.get('dark'):
        ui.dark_mode().enable()
    
    #Logged in check + Budget check, its within a column to make sure the page and storage render first before the check
    with ui.column():  
        if not app.storage.user.get('logged_in') or not app.storage.user.get('username'):
            ui.notify('Please log in first')
            ui.navigate.to('/')
            return
        
        #Budget exist check
        tx = Transaction(app.storage.user.get('username')) 
        if not tx.get_total_budget():
            ui.navigate.to('/budget')
            return

    left_drawer()
    header()
    transactions()