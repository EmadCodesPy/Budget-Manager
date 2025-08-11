from nicegui import ui, app
from models import Transaction
from static.css.css_styling import Styling

def new_budget():
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

def edit_budget():
    with ui.column().classes('w-full h-full items-center justify-center'):
        tx = Transaction(app.storage.user.get('username'))
        deductable_months = tx.get_deductable_months()
        with ui.card().classes('w-full h-full items-center'):
            ui.label('Deduct amount from multiple months').classes('font-semibold text-xl')
            ui.markdown('*This will **NOT** delete all previous transactions information').classes('text-xs text-grey -mt-3')
            name_input = ui.input('Name', placeholder='...').classes('w-full').props('outlined')
            amount_input = ui.number('Input amount you want to deduct', min=1, placeholder='...').classes('w-full').props('outlined')
            months_input = ui.number('Input number months you would like to deduct from', min=1, placeholder='...').classes('w-full').props('outlined')
            ui.markdown(f'You can deduct from **{deductable_months}** months').classes('text-sm text-grey self-start -mt-4')

            def handle_edit_budget():
                name = name_input.value
                amount = amount_input.value
                months = int(months_input.value)
                #Validation
                if amount == None or months == None:
                    ui.notify('Please fill in all fields', type='warning')
                    return
                #Validation
                if months > deductable_months:
                    ui.notify('There aren\'t that many months', type='warning')
                    return
                
                tx.deduct_from_months(total_amount=amount, months=months, name=name)
                ui.notify('Amount deducted', type='positive')

            ui.button('Deduct', on_click=handle_edit_budget).classes('w-full')

def budget():
    #Budget exist check
    tx = Transaction(app.storage.user.get('username')) 
    if not tx.get_total_budget():
        with ui.row().classes('w-full h-full items-center justify-center'):
            with ui.column().classes('w-full h-full justify-center max-w-sm items-center mt-40'):
                new_budget()
        return

    with ui.row().classes('w-full h-full items-center justify-center'):
        with ui.column().classes('w-full h-full items-center'):
            with ui.tabs().classes('rounded-lg justify-center') as tabs:
                    new = ui.tab('New Budget')
                    edit = ui.tab('Edit Budget')
            Styling.logo().classes(Styling.hover()).classes('mt-32')\
            .tooltip('Back to account').on(type='click', handler=lambda: ui.navigate.to('/account'))      
            
            ui.label('Click above to go back').classes('text-sm text-grey')        
    
    with ui.row().classes('w-full h-full items-center justify-center'):
        #Tab content
        with ui.tab_panels(tabs, value=new):
            with ui.tab_panel(new):
                new_budget()
            with ui.tab_panel(edit):
                edit_budget()