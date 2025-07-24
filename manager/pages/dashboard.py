from nicegui import ui, app
import sys
from models import User, Transaction

sys.path.append('/Users/Emad/Desktop/Github port/Budget-Manager/manager')

#user = User.login('dummy', 'dummy')
#app.storage.user['name'] = user.name
def dashboard():

    def left_drawer():
        if not app.storage.user['logged_in']:
            ui.notify('Please log in first')
            ui.navigate.to('/')
            return

        with ui.left_drawer().classes('border p-5'):
            ui.markdown(f"**You are signed in as** {app.storage.user['username']}")
            ui.button('Account').classes('w-full')
            def logout():
                    ui.navigate.to('/')
                    app.storage.user['logged_in'] = False
                    app.storage.user['username'] = None
                    app.storage.user['name'] = None
            ui.button('Logout', on_click=logout).classes('bg-red w-full')

            with ui.card().classes('justify-center shadow-lg w-full mt-6'):
                ui.markdown('### Add Transaction')
                name_input = ui.input('Name',placeholder='...').classes('w-full')
                type_input = ui.select(options=['Spending', 'Earning'], label='Type',value='Spending').classes('w-full')
                amount_input = ui.number("Amount", min=0, format='%.2f').classes('w-full')

                def handle_transaction():
                    if name_input.value == '' or type_input.value == '' or amount_input.value == '':
                        ui.notify('Please fill in all fields', type='warning')
                        return
                    

                ui.button('Submit', on_click=handle_transaction).classes('w-full')

    left_drawer()
