from nicegui import ui, app
from models import Transaction

def budget_page():
    with ui.column().classes('w-screen h-screen items-center justify-center'):
        with ui.card().classes('w-full max-w-sm shadow-2xl mb-40'):
            tx = Transaction(app.storage.user.get('username'))
            ui.label('Please allocate your budget').classes('font-semibold text-2xl')
            ui.label('*This will delete all previous transactions information').classes('text-sm text-grey')
            budget_input = ui.number('Budget', min=0, placeholder='$$$', format='%.2f').classes('w-full')
            if tx.get_total_budget():
                ui.markdown(f'**Current budget is:** €{tx.get_total_budget()}').classes('text-sm text-grey')
            month_input = ui.number('Months', min=1, placeholder='...').classes('w-full pb-4')
            
            def handle_budget():
                if budget_input.value == None or month_input.value == None:
                    ui.notify('Please fill in all fields', type='warning')
                    return
                budget = budget_input.value
                months = int(month_input.value)            
                tx.delete_tx(all=True)
                tx.delete_budget()
                tx.allocate_budget(budget=budget, months=months)
                ui.notify('Budget added', type='positive')
                ui.navigate.to('/dashboard')

            ui.button('Allocate Budget', on_click=handle_budget).classes('w-full').classes('transition ease-in-out hover:-translate-y-1 hover:scale-105')
    
    with ui.column():
        if not app.storage.user.get('logged_in') or not app.storage.user.get('username'):
            ui.notify('Please log in first')
            ui.navigate.to('/')
            return
    



