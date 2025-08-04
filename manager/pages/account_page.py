from nicegui import ui, app
from models import User, Transaction
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

def account_page():
    card_bg ='bg-gradient-to-r from-cyan-400 to-blue-700 opactiy-50 shadow-2xl p-6 w-full flex-1 text-white transition ease-in-out hover:-translate-y-1 hover:scale-105'
    hover_class = 'transition ease-in-out hover:-translate-y-1 hover:scale-105'
    bg_class = 'bg-gradient-to-r from-cyan-400 to-blue-700 opactiy-50'

    def header():
        with ui.row().classes('w-full justify-center gap-10'):
            #Back to dashboard logo
            ui.label('MoneyManager').classes(bg_class).classes(f'bg-clip-text text-transparent text-4xl {hover_class}').tooltip('Dashboard')\
            .on('click', handler=lambda: ui.navigate.to('/dashboard'))
            #Toggle dark mode
            ui.switch('Dark Mode', on_change=ui.dark_mode().toggle).classes('absolute bottom-0 left-0').bind_value(app.storage.user, 'dark')
            
    
    def account_info():
        tx = Transaction(app.storage.user.get('username'))
        with ui.column().classes('w-full items-center'):
            #Account details row
            with ui.row().classes('w-full justify-between max-w-5xl'):
                #Account detials whole card
                with ui.card().classes('items-center w-full py-8').classes(card_bg):
                    with ui.row().classes('justify-between w-full'):
                        with ui.column():
                            ui.label(f"Username: {app.storage.user.get('username')}").classes('text-3xl font-semibold')
                            ui.label(f"Name: {app.storage.user.get('name')}").classes('text-lg text-white')
                        with ui.column():
                            #Delete confirmation Dialog
                            with ui.dialog() as dialog, ui.card().classes('items-center'):
                                ui.label('Are you sure you want to delete your account?').classes('font-semibold text-xl')
                                ui.label('*This can\'t be reversed').classes('text-sm text-grey')
                                with ui.row().classes('justify-between'):
                                    ui.button('Yes', on_click=lambda: dialog.submit('Yes')).classes('bg-red text-white')
                                    ui.button('No', on_click=lambda: dialog.submit('No'))
                            
                            async def delete_dialog():
                                result = await dialog
                                if result == 'Yes':
                                    user = User(app.storage.user.get('username'), app.storage.user.get('name'))
                                    user.delete_account()
                                    ui.navigate.to('/')
                                    return
                                else:
                                    return 
                            ui.button('Delete Account', on_click=delete_dialog).classes('bg-red text-white').props('rounded outline')\
                            .classes('transition ease-in-out hover:-translate-y-1 hover:scale-105')

                            def edit_account():
                                pass
                            ui.button('Edit', on_click=lambda: ui.notify('Working on this')).props('rounded').classes('w-full')\
                            .classes('transition ease-in-out hover:-translate-y-1 hover:scale-105')
                
            #Stat card row
            with ui.row().classes('w-full max-w-5xl justify-around items-center'):
                #Account total budget
                with ui.card().classes(card_bg):
                    with ui.column().classes('w-full items-center'):
                        ui.icon('edit', size='1.2rem').classes('self-start absolute top-3 left-3 p-2').on('click', handler=lambda: ui.navigate.to('/budget'))\
                        .classes('hover:bg-white/20 rounded-full cursor-pointer').tooltip('Edit')
                        ui.icon('account_balance_wallet', size='2rem')
                        total_budget = tx.get_total_budget()
                        ui.label(f'€{total_budget}').classes('text-xl')
                        ui.label('Total Budget').classes('text-2xl')
                #Account months budget
                with ui.card().classes(card_bg):
                    with ui.column().classes('w-full items-center'):
                        ui.icon('money', size='2rem')
                        monetly_budget = tx.get_fixed_monthly_budget()
                        ui.label(f'€{monetly_budget}').classes('text-xl')
                        ui.label('This months budget').classes('text-2xl')
                #Account months Spending
                with ui.card().classes(card_bg):
                    with ui.column().classes('w-full items-center'):
                        ui.icon('trending_down', size='2rem')
                        month = datetime.now().strftime('%Y-%B')
                        savings = tx.get_monthly_cash_flow(type='Spending', month=month)
                        ui.label(f'€{savings}').classes('text-xl')
                        ui.label('This months spending').classes('text-2xl')

            #Bottom stat row
            with ui.row().classes('w-full max-w-5xl justify-between'):
                #Includes: Month overview + Overview Statistics + budget progress
                with ui.column().classes('w-full flex-1'):
                    #Month overview
                    with ui.card().classes(card_bg):
                        with ui.column().classes('w-full'):
                            ui.label('Month Overview').classes('text-2xl underline underline-offset-8')
                            months_unsorted = tx.get_months()
                            months = sorted(months_unsorted, key=lambda m: datetime.strptime(m, '%Y-%B'))
                            selected_month = months[0]
                            
                            #Changes the values shown for the month overview
                            def update_overview():
                                selected_month = month_dropdown.value
                                monthly_budget = tx.get_fixed_monthly_budget()
                                amount_spent = tx.get_monthly_cash_flow(type='Spending', month=selected_month)
                                amount_earned = tx.get_monthly_cash_flow(type='Earning', month=selected_month)
                                amount_remaining = tx.get_monthly_budget(selected_month)
                                

                                monthly_budget_label.text = f'Monthly Budget: €{monthly_budget}'
                                amount_spent_label.text = f'Amount Spent: €{amount_spent:.1f}'
                                amount_earned_label.text = f'Amount Earned: €{amount_earned:.1f}'
                                if amount_remaining < 0:
                                    amount_remaining_label.text = f'Amount Remaining: €{amount_remaining:.1f}'
                                    amount_remaining_label.classes('text-red')
                                else:
                                    amount_remaining_label.text = f'Amount Remaining: €{amount_remaining:.1f}'
                                    amount_remaining_label.classes(remove='text-red')

                                update_chart = getattr(app.state, 'piechart', None)
                                if update_chart:
                                    update_chart(selected_month)
                                    
                                
                                
                                

                            #Makes the dropdown text white
                            ui.add_head_html('''
                                            <style>
                                            /* Make selected text white */
                                            .q-field__native span {
                                                color: white !important;
                                            }
                                            </style>
                                            ''')
                            month_dropdown = ui.select(months, value=selected_month, on_change=update_overview).classes('text-l')
                            
                            #Overview statisitcs
                            monthly_budget_label = ui.label().classes('text-xl')
                            amount_spent_label = ui.label().classes('text-xl')
                            amount_earned_label = ui.label().classes('text-xl')
                            #Savings icon + Remaining amount
                            with ui.row().classes('items-center'):
                                amount_remaining_label = ui.label().classes('text-xl')
                                ui.icon('savings', size='1.5rem').tooltip('Add to savings').classes('hover:bg-white/20 rounded-full p-0.5 -ml-4')\
                                .on('click', handler=lambda: ui.notify('Working on this'))
                            
                            update_overview()
                    
                    # Includes: Recent transactions + Budget progess 
                    with ui.card().classes(card_bg):
                        with ui.row().classes('w-full pb-1'):
                            #Recent transactions
                            with ui.column().classes('w-full flex-1'):
                                recent_transactions = tx.recent_tx(3)
                                ui.label('Recent Transactions')
                                ui.separator().classes('bg-white')
                                for name, amount, type_ in recent_transactions:
                                    with ui.column().classes('flex-1 w-full max-w-32'):
                                        with ui.row().classes('w-full items-center gap-2'):
                                            bg_color = 'bg-red-700 rounded-md px-2' if type_ == 'Spending' else 'bg-green-700 rounded-md px-2'
                                            ui.icon('fiber_manual_record', size='0.6rem').classes('text-gray')
                                            ui.label(name)
                                            with ui.column().classes('w-full flex-1 items-end'):
                                                with ui.element('div').classes(bg_color):
                                                    ui.label(f'€{amount}')
                            #Budget progress
                            with ui.column().classes('w-full flex-1'):
                                ui.label('Budget Progress')
                                ui.separator().classes('w-full bg-white')
                                with ui.row().classes('w-full justify-between items-center'):
                                    with ui.column().classes('w-full h-full flex-1 justify-center'):
                                        budget_progress, amount_spent_progress, total_budget_progress= tx.budget_progress(include_numbers=True)
                                        ratio_percentage = round(budget_progress, 3)
                                        ratio = round(budget_progress, 1) 
                                        progress_bar = '█'*int(ratio*10) + '▒'*(10-int(ratio*10))
                                        ui.markdown(progress_bar).classes('font-bold')
                                    with ui.column().classes('flex-1'):
                                        ui.label(f'{ratio_percentage*100:.1f}%')
                                with ui.row().classes('justify-center w-full pt-3'):
                                    ui.label(f'€{amount_spent_progress} / €{total_budget_progress}')

                # Month statistics
                with ui.column().classes('w-full flex-1 h-full max-h-'):
                    with ui.card().classes(card_bg):
                        ui.label('Month statistics').classes('text-2xl underline underline-offset-8')
                        piechart_container = ui.column().classes('w-full max-w-lg')
                        #Render piechart
                        def draw_piechart(month):
                            app.state.piechart = draw_piechart
                            try:
                                piechart_container.clear()
                            except:
                                return
                            
                            with piechart_container:
                                tx_names, tx_amount = tx.tx_piechart(month)
                                if tx_names == []:
                                    ui.label('No Transactions yet').classes('text-red')
                                    return
                                piechart_object = go.Figure(
                                                            data=[
                                                                go.Pie(
                                                                    labels=tx_names,
                                                                    values=tx_amount,
                                                                    textinfo='label+percent',
                                                                    insidetextorientation='radial',
                                                                    hole=0.3,
                                                                    hovertemplate='%{label}: €%{value} <extra></extra>',
                                                                    marker=dict(colors=px.colors.sequential.Blues[::-1]),
                                                                    showlegend=False
                                                                    )
                                                                ]
                                                            )                               
                                ui.plotly(piechart_object).classes('max-w-md')

                        draw_piechart(selected_month)

                                
    header()
    account_info()
