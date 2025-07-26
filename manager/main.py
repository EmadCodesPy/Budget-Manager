from nicegui import ui, app
from pages.login_page import login_page
from pages.dashboard import dashboard

@ui.page('/')
def show_login():
    if app.storage.user.get('logged_in') == True:
        ui.notify('Welcome', type='positive')
        ui.navigate.to('/dashboard')
        return
    else:
        login_page()

@ui.page('/dashboard')
def show_dashboard():
    dashboard()

ui.run(storage_secret='test')