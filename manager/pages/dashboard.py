from nicegui import ui, app
from models import Transaction
from datetime import datetime

def dashboard():
    if app.storage.user.get('dark'):
        ui.dark_mode().enable()

    def left_drawer():
        with ui.left_drawer(top_corner=True, bottom_corner=True, elevated=True, value=True):
            ui.label('MoneyManager').classes('bg-gradient-to-r from-cyan-400 to-blue-700')\
                    .classes(f'bg-clip-text text-transparent text-4xl')
            ui.markdown(f"**You are signed in as** {app.storage.user.get('username')}")
            def account():
                ui.navigate.to('/account')
                return
            ui.button('Account', on_click=account).classes('w-full').props('rounded outline')
            def logout():
                ui.navigate.to('/')
                app.storage.user['logged_in'] = False
                app.storage.user['username'] = None
                app.storage.user['name'] = None
                return
            ui.button('Logout', on_click=logout).classes('bg-red w-full text-white').props('rounded outline')

            with ui.card().classes('justify-center shadow-2xl w-full mt-6'):
                ui.markdown('### Add Transaction')
                name_input = ui.input('Name',placeholder='...').classes('w-full')
                type_input = ui.select(options=['Spending', 'Earning'], label='Type',value='Spending').classes('w-full')
                amount_input = ui.number("Amount", min=0, format='%.2f').classes('w-full')

                def handle_transaction():
                    if name_input.value == '' or type_input.value == '' or amount_input.value == '':
                        ui.notify('Please fill in all fields', type='warning')
                        return
                    tx = Transaction(app.storage.user.get('username'))
                    tx.add_tx(name_input.value, type_input.value, amount_input.value, app.storage.user.get('month'))
                    ui.notify('Transaction added', type='positive')
                    update_func = getattr(app.state, 'update_budget_func', None)
                    show_tx = getattr(app.state, 'show_transactions', None)
                    if update_func:
                        update_func()
                        show_tx()
                
                ui.button('Submit', on_click=handle_transaction).classes('w-full')\
                .classes('transition ease-in-out duration-150 hover:-translate-y-1 hover:scale-105')
            
            
            

    def header():
        tx = Transaction(app.storage.user.get('username'))
        if not tx:
            ui.navigate.to('/')
            return
        months_unsorted = tx.get_months()
        months = sorted(months_unsorted, key=lambda m: datetime.strptime(m, '%Y-%B'))
        if not months:
            ui.label('No budget yet').classes('text-red')
            return
        
        selected_month = months[0]
        
        with ui.row().classes('justify-between items-center w-full'):

            #Function to dynamically update the budget shown on month change in dropdown
            def update_budget():
                app.state.update_budget_func = update_budget
                selected_month = month_dropdown.value
                app.storage.user['month'] = selected_month
                budget = tx.get_monthly_budget(selected_month)
                formatted_budget = f"€{budget:.2f}"
                
                budget_label.text = f"Total Budget: {formatted_budget}"
                if budget < 0:
                    budget_label.classes('text-red')
                else:
                    budget_label.classes(remove='text-red')

                update_tx = getattr(app.state, 'show_transactions', None)
                if update_tx:
                    update_tx()
            
            month_dropdown = ui.select(months, value=selected_month, on_change=update_budget).classes('text-xl rounded-md')   
            budget_label = ui.label().classes('text-3xl font-semibold ')

            update_budget()
            ui.separator().classes('glossy')

    def main_body():
        tx = Transaction(app.storage.user.get('username'))
                
        transaction_container = ui.column().classes('w-full')
        
        def show_transactions():
            try:
                transaction_container.clear()
            except:
                #ui.navigate.to('/')
                return
            
            transactions = tx.get_tx(app.storage.user.get('month'))
            #Transaction card below
            for transaction in reversed(transactions):
                bar_color = 'bg-green-500' if transaction['type'].lower() == 'earning' else 'bg-red-500'
                with transaction_container:
                    with ui.row().classes('justify-between items-center w-full border p-2 rounded-lg'):
                        with ui.row().classes('items-center'):
                            ui.separator().classes(f'h-12 w-1 rounded-full justify-center {bar_color}')
                            with ui.column().classes('justify-center'):
                                ui.label(transaction['name']).classes('font-semibold')
                                ui.label(transaction['created_at']).classes('text-grey-500 text-sm')
                        with ui.row().classes('items-center gap-4'):
                            ui.label(f"€{transaction['amount']:.2f}").classes('font-semibold text-xl')
                            def delete_transaction():
                                tx.delete_tx(tx_id=transaction['id'], month=app.storage.user.get('month'))
                                ui.notify('Transaction Deleted', type='positive')
                                app.state.show_transactions()
                                app.state.update_budget_func()
                            ui.button(icon='delete', on_click=delete_transaction).props('flat dense round')
        app.state.show_transactions = show_transactions
        show_transactions()
       
    def dashboard_main():
        left_drawer()
        header()
        main_body()
    
    with ui.column():  
        if not app.storage.user.get('logged_in') or not app.storage.user.get('username'):
            ui.notify('Please log in first')
            ui.navigate.to('/')
            return
        
        tx = Transaction(app.storage.user.get('username'))
        
        if not tx.get_total_budget():
            ui.navigate.to('/budget')
            return

    dashboard_main()