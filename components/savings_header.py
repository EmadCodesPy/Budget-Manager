from nicegui import ui, app 
from models import Transaction

def savings_header():
    tx = Transaction(app.storage.user.get('username'))
    if not tx:
        ui.navigate.to('/')
        return


    with ui.row().classes('justify-between items-center w-full'):
        
        def update_savings():
            total_savings =  0 if tx.get_total_savings() == None else tx.get_total_savings()
            amount_label.text = f'€{total_savings:.2f}'

            update_sv = getattr(app.state, 'show_savings', None)
            if update_sv:
                update_sv.refresh()

        app.state.savings = update_savings
        savings_label = ui.label('Total Savings:').classes('text-3xl font-semibold') 
        amount_label = ui.label().classes('text-3xl font-semibold ')
 
        app.state.update_savings = update_savings
        update_savings()

        ui.separator().classes('glossy')
