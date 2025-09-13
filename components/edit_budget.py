from nicegui import ui, app
from models import Transaction
from static.css.css_styling import Styling

def splitting_transaction():
    with ui.column().classes('w-full h-full items-center justify-center max-w-sm'):
        tx = Transaction(app.storage.user.get('username'))
        deductable_months = tx.get_deductable_months()
        with ui.card().classes('w-full h-full items-center'):
            ui.label('Split transactions over months').classes('font-semibold text-xl')
            ui.markdown('*This will **NOT** delete all previous transactions information').classes('text-xs text-grey -mt-3')
            name_input = ui.input('Name', placeholder='...').classes('w-full').props('outlined')
            amount_input = ui.number('Amount you want to deduct', min=1, placeholder='...').classes('w-full').props('outlined')
            months_input = ui.number('Number months you would like to deduct from', min=1, placeholder='...').classes('w-full').props('outlined')
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

            ui.button('Confirm', on_click=handle_edit_budget).classes('w-full')

def recurring_transaction():
    with ui.column().classes('w-full h-full items-center justify-center max-w-sm'):
        tx = Transaction(app.storage.user.get('username'))
        deductable_months = tx.get_deductable_months()
        with ui.card().classes('w-full h-full items-center'):
            ui.label('Set up recurring transaction').classes('font-semibold text-xl')
            ui.markdown('*This will **NOT** delete all previous transactions information').classes('text-xs text-grey -mt-3')
            name_input = ui.input('Name', placeholder='...').classes('w-full').props('outlined')
            amount_input = ui.number('Amount', min=1, placeholder='...').classes('w-full').props('outlined')
            months_input = ui.number('Number of months', min=1, placeholder='...').classes('w-full').props('outlined')
            ui.markdown(f'You can deduct from **{deductable_months}** months').classes('text-sm text-grey self-start -mt-4')
            #Type of transaction toggle
            with ui.row().classes('w-full text-xs justify-center -mt-4'):
                type_tx = ui.toggle(['Spending', 'Earning', 'Savings']).props('push').classes('self-center')
            
            def handle_recurring_payment():
                name = name_input.value
                amount = amount_input.value
                months = int(months_input.value)
                _type = type_tx.value
                #Validation
                if amount == None or months == None or _type == None:
                    ui.notify('Please fill in all fields', type='warning')
                    return
                #Validation
                if months > deductable_months:
                    ui.notify('There aren\'t that many months', type='warning')
                    return
                
                tx.reccuring_tx(amount=amount, months=months, name=name, _type=_type)
                ui.notify('Amount deducted', type='positive')

            ui.button('Confirm', on_click=handle_recurring_payment).classes('w-full')

def edit_budget():
    #Budget exist check
    tx = Transaction(app.storage.user.get('username')) 
    if not tx.get_total_budget():
        ui.navigate.to('/budget')
        return

    #Tabs
    with ui.row().classes('w-full items-center justify-center'):
        with ui.column().classes('w-full h-full items-center'):
            with ui.tabs().classes('rounded-lg z-10') as tabs:
                recurring = ui.tab('Reccuring Transaction')
                splitting = ui.tab('Split Transaction')
        with ui.column().classes('w-full h-full items-center'):
                Styling.logo().classes(Styling.hover()).classes('mt-3')\
                .tooltip('Back to dashboard').on(type='click', handler=lambda: ui.navigate.to('/dashboard'))      
                ui.label('Click above to go back').classes('text-sm text-grey')   

    with ui.row().classes('w-full h-full items-center justify-center'):
        #Tab content
        with ui.tab_panels(tabs, value=recurring):
            with ui.tab_panel(recurring):
                recurring_transaction()
            with ui.tab_panel(splitting):
                splitting_transaction()
