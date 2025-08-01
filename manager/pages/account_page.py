from nicegui import ui, App
from models import User, Transaction

def account_page():
    def left_drawer():
        with ui.left_drawer(top_corner=True, bottom_corner=True, elevated=True):
            ui.label('MoneyManager').classes('bg-gradient-to-r from-cyan-400 to-blue-700')\
                    .classes(f'bg-clip-text text-transparent text-4xl')
            ui.button('Dashboard', on_click=ui.navigate.back).props('rounded outline').classes('w-full')
    left_drawer()