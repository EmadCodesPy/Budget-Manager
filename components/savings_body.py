from nicegui import ui, app
from models import Transaction

def savings_body():
    tx = Transaction(app.storage.user.get('username'))
            
    @ui.refreshable
    def show_savings():
        all_savings = tx.get_savings()
        if all_savings == 0:
            return
        #Transaction card below
        for transaction in all_savings:
            bar_color = 'bg-green-500'
            with ui.row().classes('justify-between items-center w-full border p-2 rounded-lg transition ease-in-out hover:-translate-y-1'):
                with ui.row().classes('items-center'):
                    ui.separator().classes(f'h-12 w-1 rounded-full justify-center {bar_color}')
                    with ui.column().classes('justify-center'):
                        ui.label(transaction['name']).classes('font-semibold')
                        ui.label(transaction['created_at']).classes('text-gray-500 text-sm')
                with ui.row().classes('items-center gap-4'):
                    ui.label(f"€{transaction['amount']:.2f}").classes('font-semibold text-xl')
                    #t is passed because if not, it will delete the last transaction in the loop, not the actual one
                    def delete_transaction(t=transaction):
                        tx.delete_tx(tx_id=t['id'])
                        app.state.show_savings.refresh()
                        app.state.update_savings()
                        ui.notify('Transaction Deleted', type='positive')
                    ui.button(icon='delete', on_click=delete_transaction).props('flat dense round')
    
    app.state.show_savings = show_savings
    show_savings()
