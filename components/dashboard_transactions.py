from nicegui import ui, app
from models import Transaction



def transactions():
    tx = Transaction(app.storage.user.get('username'))
            
    @ui.refreshable
    def show_transactions():
        transactions = tx.get_tx(app.storage.user.get('month'), incl_savings=False)
        #Transaction card below
        for transaction in reversed(transactions):
            bar_color = 'bg-green-500' if transaction['type'].lower() == 'earning' else 'bg-red-500'
            with ui.row().classes('justify-between items-center w-full border p-2 rounded-lg transition ease-in-out hover:-translate-y-1'):
                with ui.row().classes('items-center'):
                    ui.separator().classes(f'h-12 w-1 rounded-full justify-center {bar_color}')
                    with ui.column().classes('justify-center'):
                        ui.label(transaction['name']).classes('font-semibold')
                        ui.label(transaction['created_at']).classes('text-gray-500 text-sm')
                with ui.row().classes('items-center gap-4'):
                    ui.label(f"€{transaction['amount']:.2f}").classes('font-semibold text-xl')
                    def delete_transaction():
                        tx.delete_tx(tx_id=transaction['id'], month=app.storage.user.get('month'))
                        ui.notify('Transaction Deleted', type='positive')
                        app.state.show_transactions.refresh()
                        app.state.update_budget_func()
                    ui.button(icon='delete', on_click=delete_transaction).props('flat dense round')

    app.state.show_transactions = show_transactions
    
    show_transactions()
