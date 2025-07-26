from nicegui import ui, app
from models import User, Transaction

def dashboard():

    def left_drawer():
        if not app.storage.user.get('logged_in') or not app.storage.user.get('username'):
            ui.notify('Please log in first')
            ui.navigate.to('/')
            return

        with ui.left_drawer(top_corner=True, bottom_corner=True).classes('border p-5'):
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
                    tx = Transaction(app.storage.user['username'])
                    tx.add_tx(name_input.value, type_input.value, amount_input.value, app.storage.user.get('month'))
                    ui.notify('Transaction added', type='positive')
                    
                

                ui.button('Submit', on_click=handle_transaction).classes('w-full')
    
    def header():
        with ui.header().classes('border p-5 bg-white text-black'):
            tx = Transaction(app.storage.user.get('username'))
            if not tx:
                ui.navigate.to('/')
                return
            months = tx.get_months()
            selected_month = months[0]
            
            with ui.row().classes('justify-between items-center w-full'):

                def update_budget(month=None):
                    selected_month = month_dropdown.value
                    app.storage.user['month'] = selected_month
                    budget = tx.get_monthly_budget(selected_month)
                    formatted_budget = f"€{budget:.2f}"
                   
                    budget_label.text = f"Total Budget: {formatted_budget}"
                    if budget < 0:
                        budget_label.classes('text-red')
                    else:
                        budget_label.classes(remove='text-red')

                month_dropdown = ui.select(months, value=selected_month, on_change=update_budget).classes('text-xl p-2 rounded-md border border-gray-300')   
                budget_label = ui.label().classes('text-3xl font-semibold')

                update_budget()
                
    def main():
        left_drawer()
        header()
    
    main()

