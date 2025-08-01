from nicegui import ui, app
from models import User, Transaction

def account_page():
    def left_drawer():
        with ui.left_drawer(top_corner=True, bottom_corner=True, elevated=True):
            ui.label('MoneyManager').classes('bg-gradient-to-r from-cyan-400 to-blue-700')\
                    .classes(f'bg-clip-text text-transparent text-4xl')
            ui.button('Dashboard', on_click=ui.navigate.back).props('rounded outline').classes('w-full')

            with ui.dialog() as dialog, ui.card().classes('items-center'):
                ui.label('Are you sure you want to delete your account?').classes('font-semibold text-xl')
                ui.label('*This can\'t be reversed').classes('text-sm text-grey')
                with ui.row().classes('justify-between'):
                    ui.button('Yes', on_click=lambda: dialog.submit('Yes')).classes('bg-red text-white')
                    ui.button('No', on_click=lambda: dialog.submit('No'))
            
            async def show_dialog():
                result = await dialog
                if result == 'Yes':
                    user = User(app.storage.user.get('username'), app.storage.user.get('name'))
                    user.delete_account()
                    ui.navigate.to('/')
                    return
                else:
                    return
            ui.button('Delete Account', on_click=show_dialog).classes('bg-red w-full text-white').props('rounded outline')
    
    def account_info():
        with ui.card().classes('w-full h-full'):
            ui.markdown(f"**Username:** {app.storage.user.get('username')}").classes('text-6xl')
            ui.markdown(f"**Name:** {app.storage.user.get('name')}").classes('text-4xl')

    def graph_info():
        ui.label('Graph here')

    def main():
        with ui.row().classes('w-full h-full'):
            with ui.tabs().props('vertical') as tabs:
                account = ui.tab('Account Info')
                graph = ui.tab('Statistics')
            with ui.tab_panels(tabs, value=account).props('vertical'):
                with ui.tab_panel(account):
                    account_info()
                with ui.tab_panel(graph):
                    graph_info()

    main()
    left_drawer()


