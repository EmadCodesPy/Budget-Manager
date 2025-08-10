from nicegui import ui, app
from components.budget import budget

def budget_page():
    
    #Dark mode check
    if app.storage.user.get('dark'):
        ui.dark_mode().enable()

    #Logged in check, its within a column to make sure the page and storage render first before the check
    with ui.column():
        if not app.storage.user.get('logged_in') or not app.storage.user.get('username'):
            ui.notify('Please log in first')
            ui.navigate.to('/')
            return
    
    #Budget from components folder
    budget()



