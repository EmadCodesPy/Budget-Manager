from nicegui import ui, app
from models import Transaction
from static.css.css_styling import Styling
from components.savings_header import savings_header
from components.savings_body import savings_body

def left_drawer():
    with ui.left_drawer(top_corner=True, bottom_corner=True, elevated=True, value=True, fixed=True):
        Styling.logo()
        
        ui.markdown(f"**You are signed in as** {app.storage.user.get('username')}")
        def account():
            ui.navigate.to('/account')
            return
        ui.button('Account', on_click=account).classes('w-full').props('push rounded')
        def logout():
            ui.navigate.to('/')
            app.storage.user['logged_in'] = False
            app.storage.user['username'] = None
            app.storage.user['name'] = None
            return
        ui.button('Logout', on_click=logout).classes('bg-red w-full text-white').props('push rounded')

        with ui.dialog() as savings_dialog, ui.card().classes('w-full h-full'):
            ui.icon('close', size='1.5rem').on('click', handler=savings_dialog.close)\
            .classes('opacity-60 -m-3 hover:bg-gray-400/20 rounded-full cursor-pointer').tooltip('close')
            savings_header()
            savings_body()

        ui.button('Savings', on_click=savings_dialog.open).props('push rounded').classes('w-full bg-green')           

        with ui.card().classes('justify-center shadow-xl w-full mt-6'):
            ui.markdown('### Add Transaction')
            name_input = ui.input('Name',placeholder='...').classes('w-full')
            amount_input = ui.number("Amount", min=1, format='%.2f').classes('w-full pb-4')
            
            #CSS to adjust button group size
            ui.add_head_html("""
                            <style>
                                .q-btn-group {
                                max-width: 236px;
                                }
                                .q-btn-group .q-btn {
                                font-size: 0.75rem;
                                max-width: 78.6px;
                                /*max-width: px;*/
                                }
                                </style>
                            """)

            with ui.row().classes('w-full text-xs pb-1'):
                type_tx = ui.toggle(['Spending', 'Earning', 'Savings']).props('push')

            def handle_transaction():
                if name_input.value == '' or type_tx.value == None or amount_input.value == None:
                    ui.notify('Please fill in all fields', type='warning')
                    return
                tx = Transaction(app.storage.user.get('username'))
                tx.add_tx(name_input.value, type_tx.value, amount_input.value, app.storage.user.get('month'))
                ui.notify('Transaction added', type='positive')
                update_func = getattr(app.state, 'update_budget_func', None)
                show_tx = getattr(app.state, 'show_transactions', None)
                update_sv = getattr(app.state, 'update_savings', None)
                show_sv = getattr(app.state, 'show_savings', None)
                if update_func:
                    update_func()
                    show_tx.refresh()
                    update_sv()
                    show_sv.refresh()

            
            ui.button('Submit', on_click=handle_transaction).classes('w-full').props('push')

        