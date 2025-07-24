from nicegui import ui
from nicegui_login import login_page

@ui.page('/login')
def show_login():
    login_page()

ui.run()