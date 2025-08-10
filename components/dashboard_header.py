from nicegui import ui, app
from models import Transaction
from datetime import datetime


def header():
    tx = Transaction(app.storage.user.get('username'))
    if not tx:
        ui.navigate.to('/')
        return
    months_unsorted = tx.get_months()
    months = sorted(months_unsorted, key=lambda m: datetime.strptime(m, '%Y-%B'))
    if not months:
        ui.label('No budget yet').classes('text-red')
        ui.navigate.to('/budget')
        return
    
    selected_month = months[0]

    with ui.row().classes('justify-between items-center w-full'):
        #Function to dynamically update the budget shown on month change in dropdown
        def update_budget():
            #app.state.update_budget_func = update_budget      
            selected_month = month_dropdown.value
            app.storage.user['month'] = selected_month
            budget = tx.get_monthly_budget(selected_month)
            formatted_budget = f"€{budget:.2f}"
            
            budget_label.text = f"Total Budget: {formatted_budget}"
            if budget < 0:
                budget_label.classes('text-red')
            else:
                budget_label.classes(remove='text-red')

            #app.state.update_budget_func.refresh()
            update_tx = getattr(app.state, 'show_transactions', None)
            
            if update_tx:
                update_tx.refresh()
        
        app.state.update_budget_func = update_budget
        month_dropdown = ui.select(months, value=selected_month, on_change=update_budget).classes('text-xl rounded-md')   
        budget_label = ui.label().classes('text-3xl font-semibold ')

        update_budget()
        ui.separator().classes('glossy')
