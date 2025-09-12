from nicegui import ui, app
from models import Transaction
from static.css.css_styling import Styling

def make_new_budget():
    with ui.column().classes('w-full h-full items-center justify-center'):
        with ui.card().classes('w-full h-full items-center'):
            tx = Transaction(app.storage.user.get('username'))
            ui.label('Allocate new budget').classes('font-semibold text-xl')
            ui.label('*This will delete all previous transactions information').classes('text-xs text-grey -mt-3')
            budget_input = ui.number('Budget', min=1, placeholder='$$$', format='%.2f').classes('w-full').props('outlined')
            if tx.get_total_budget():
                ui.markdown(f'**Current budget:** €{tx.get_total_budget()}').classes('text-sm text-grey self-start -mt-4')
            month_input = ui.number('Months', min=1, placeholder='...').classes('w-full').props('outlined')
            
            def handle_new_budget():
                budget = budget_input.value
                months = int(month_input.value)
                #Validation
                if budget == None or months == None:
                    ui.notify('Please fill in all fields', type='warning')
                    return
    
                tx.delete_tx(all=True)
                tx.delete_budget()
                tx.allocate_budget(budget=budget, months=months)
                ui.notify('Budget added', type='positive')
                ui.navigate.to('/dashboard')

            ui.button('Allocate Budget', on_click=handle_new_budget).classes('w-full').classes('transition ease-in-out hover:-translate-y-1 hover:scale-105')

def new_budget():
    #Budget exist check
    tx = Transaction(app.storage.user.get('username')) 
    if not tx.get_total_budget():
        with ui.row().classes('w-full h-full items-center justify-center'):
            with ui.column().classes('w-full h-full justify-center max-w-sm items-center mt-40'):
                make_new_budget()
        return

    with ui.row().classes('w-full h-full items-center justify-center'):
        with ui.column().classes('w-full h-full items-center'):
            Styling.logo().classes(Styling.hover()).classes('mt-32')\
            .tooltip('Back to account').on(type='click', handler=lambda: ui.navigate.to('/account'))      
            ui.label('Click above to go back').classes('text-sm text-grey')
            make_new_budget()
    
