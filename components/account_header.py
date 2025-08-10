from nicegui import ui, app
from static.css.css_styling import Styling

def header():
    
    with ui.row().classes('w-full justify-center gap-10'):
        #Back to dashboard logo
        Styling.logo().classes(Styling.hover()).tooltip('Dashboard').on('click', handler=lambda: ui.navigate.to('/dashboard'))
        #Toggle dark mode
        ui.switch('Dark Mode', on_change=ui.dark_mode().toggle).classes('absolute bottom-0 left-0').bind_value(app.storage.user, 'dark')
        