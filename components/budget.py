from nicegui import ui, app
from models import Transaction
from static.css.css_styling import Styling

def budget():
    with ui.column().classes('w-screen h-screen items-center justify-center'):
        Styling.logo().classes(Styling.hover())\
            .tooltip('Back to account').on(type='click', handler=lambda: ui.navigate.to('/account'))      
        ui.label('Click above to go back').classes('text-sm text-grey')
        
        with ui.card().classes('w-screen max-w-sm shadow-2xl'):
            tx = Transaction(app.storage.user.get('username'))
            ui.label('Please allocate your budget').classes('font-semibold text-2xl')
            ui.label('*This will delete all previous transactions information').classes('text-sm text-grey')
            budget_input = ui.number('Budget', min=1, placeholder='$$$', format='%.2f').classes('w-full')
            if tx.get_total_budget():
                ui.markdown(f'**Current budget:** €{tx.get_total_budget()}').classes('text-sm text-grey')
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

def budget_from_all():
    with ui.column().classes('w-screen h-screen items-center justify-center'):
        with ui.card().classes('w-screen max-w-sm shadow-2xl'):
            ui.label('Deduct amount from multiple months').classes('font-semibold text-2xl')
            ui.markdown('*This will **NOT** delete all previous transactions information').classes('text-sm text-grey')
            amount = ui.number('Input amount you want to deduct', min=1).classes('w-full')
            months = ui.number('Input months you would like to deduct from', min=1).classes('w-full')
            ui.button('Submit')

if __name__ == '__main__':
     budget_from_all()
     ui.run()