from nicegui import ui, app
from models import User, Transaction
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from exceptions import UsernameInUseError
from static.css.css_styling import Styling

def account_cards():
    #card_bg ='bg-gradient-to-r from-cyan-400 to-blue-700 opactiy-50 shadow-2xl p-6 w-full flex-1 text-white transition ease-in-out hover:-translate-y-1 hover:scale-105'    
    tx = Transaction(app.storage.user.get('username'))
    
    with ui.column().classes('w-full items-center'):
        #Account details row
        with ui.row().classes('w-full justify-between max-w-5xl'):
            #Account detials whole card
            with ui.card().classes('items-center w-full py-8').classes(Styling.card()):
                with ui.row().classes('justify-between w-full'):
                    user = User(app.storage.user.get('username'), app.storage.user.get('name'))
                    #Username + name + username_edit + name_edit
                    with ui.column():
                        #Username
                        with ui.row().classes('gap-2 items-center'):
                            ui.label(f"Username: {app.storage.user.get('username')}").classes('text-3xl font-semibold')
                            
                            with ui.dialog() as edit_username_dialog, ui.card().classes('items-center gap-0'):
                                ui.label('Edit username below').classes('font-semibold text-xl')
                                new_username_input = ui.input('New Username').classes('w-full')
                                ui.markdown(f'**Current username:** {user.username}').classes('text-grey text-sm self-start')
                                with ui.row().classes('w-full items-center justify-center'):
                                    ui.button('Submit', on_click=lambda: edit_username_dialog.submit(new_username_input.value))
                                    ui.button('Cancel', on_click=lambda: edit_username_dialog.submit(''))
                            
                            async def edit_username():
                                new_username = await edit_username_dialog
                                if new_username == '' or new_username == None or new_username == app.storage.user.get('username'):
                                    return
                                try:
                                    user.update_username_or_name(new_username, 'username')
                                    app.storage.user['username'] = new_username
                                    ui.navigate.to('/account')
                                    return
                                except UsernameInUseError:
                                    ui.notify('Username already in use :(', type='negative')
                                    return

                            ui.icon('edit', size='1.2rem').classes('opacity-70 p-1 hover:bg-white/20 rounded-full').on('click', handler=edit_username)

                        #Name
                        with ui.row().classes('gap-2 items-center'):
                            ui.label(f"Name: {app.storage.user.get('name')}").classes('text-lg')
                            
                            with ui.dialog() as edit_name_dialog, ui.card().classes('items-center gap-0'):
                                ui.label('Edit name below').classes('font-semibold text-xl')
                                new_name_input = ui.input('New Name').classes('w-full')
                                ui.markdown(f'**Current name:** {user.name}').classes('text-grey text-sm self-start')
                                with ui.row().classes('w-full items-center justify-center'):
                                    ui.button('Submit', on_click=lambda: edit_name_dialog.submit(new_name_input.value))
                                    ui.button('Cancel', on_click=lambda: edit_name_dialog.submit(''))
                            
                            async def edit_name():
                                new_name = await edit_name_dialog
                                if new_name == '' or new_name == None or new_name == app.storage.user.get('name'):
                                    return
                                user.update_username_or_name(new_name, 'name')
                                app.storage.user['name'] = new_name
                                ui.navigate.to('/account')
                                return

                            ui.icon('edit', size='1rem').classes('opacity-70 p-1 hover:bg-white/20 rounded-full').on('click', handler=edit_name)
                    
                    with ui.column():
                        #Delete confirmation Dialog
                        with ui.dialog() as delete_dialog, ui.card().classes('items-center'):
                            ui.label('Are you sure you want to delete your account?').classes('font-semibold text-xl')
                            ui.label('*This can\'t be reversed').classes('text-sm text-grey')
                            with ui.row().classes('justify-between'):
                                ui.button('Yes', on_click=lambda: delete_dialog.submit('Yes')).classes('bg-red text-white')
                                ui.button('No', on_click=lambda: delete_dialog.submit('No'))
                        
                        async def delete_user():
                            result = await delete_dialog
                            if result == 'Yes':
                                user = User(app.storage.user.get('username'), app.storage.user.get('name'))
                                user.delete_account()
                                ui.navigate.to('/')
                                return
                            else:
                                return 
                        
                        ui.button('Delete Account', on_click=delete_user).classes('bg-red text-white').props('rounded outline')\
                        .classes('transition ease-in-out hover:-translate-y-1 hover:scale-105')
            
        #Stat card row
        with ui.row().classes('w-full max-w-5xl justify-around items-center'):
            #Account total budget
            with ui.card().classes(Styling.card()):
                with ui.column().classes('w-full items-center'):
                    ui.icon('edit', size='1.2rem').classes('self-start absolute top-3 left-3 p-2 opacity-70').on('click', handler=lambda: ui.navigate.to('/budget'))\
                    .classes('hover:bg-white/20 rounded-full cursor-pointer').tooltip('Edit')
                    ui.icon('account_balance_wallet', size='2rem')
                    total_budget = tx.get_total_budget()
                    ui.label(f'€{total_budget:.1f}').classes('text-xl')
                    ui.label('Total Budget').classes('text-2xl')
            #Account months budget
            with ui.card().classes(Styling.card()):
                with ui.column().classes('w-full items-center'):
                    ui.icon('money', size='2rem')
                    monetly_budget = tx.get_fixed_monthly_budget()
                    ui.label(f'€{monetly_budget:.1f}').classes('text-xl')
                    ui.label('This months budget').classes('text-2xl')
            #Account months Spending
            with ui.card().classes(Styling.card()):
                with ui.column().classes('w-full items-center'):
                    ui.icon('savings', size='2rem')
                    month = datetime.now().strftime('%Y-%B')
                    spending = tx.get_total_savings()
                    ui.label(f'€{spending:.1f}').classes('text-xl')
                    ui.label('Savings').classes('text-2xl')

        #Bottom stat rows
        with ui.row().classes('w-full max-w-5xl justify-between'):
            #Includes: Month overview + Overview Statistics + budget progress
            with ui.column().classes('w-full flex-1'):
                #Month overview
                with ui.card().classes(Styling.card()):
                    with ui.column().classes('w-full'):
                        ui.label('Month Overview').classes('self-center text-2xl underline underline-offset-8')
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
                            # ui.icon('savings', size='1.5rem').tooltip('Add to savings').classes('hover:bg-white/20 rounded-full p-0.5 -ml-4')\
                            # .on('click', handler=lambda: ui.notify('Working on this'))
                        
                        update_overview()
                
                # Includes: Recent transactions + Budget progess 
                with ui.card().classes(Styling.card()):
                    with ui.row().classes('w-full pb-1'):
                        #Recent transactions
                        with ui.column().classes('w-full flex-1'):
                            recent_transactions = tx.recent_tx(3)
                            ui.label('Recent Transactions')
                            ui.separator().classes('bg-white')
                            for name, amount, type_ in recent_transactions:
                                with ui.column().classes('flex-1 w-full'):
                                    with ui.row().classes('w-full items-center gap-2'):
                                        bg_color = 'bg-red-700 rounded-md px-2' if type_ == 'Spending' else 'bg-green-700 rounded-md px-2'
                                        ui.icon('fiber_manual_record', size='0.6rem').classes('text-gray')
                                        ui.label(name)
                                        with ui.column().classes('w-full flex-1 items-end'):
                                            with ui.element('div').classes(bg_color):
                                                ui.label(f'€{amount:.2f}')
                        #Budget progress
                        with ui.column().classes('w-full flex-1'):
                            ui.label('Budget Progress')
                            ui.separator().classes('w-full bg-white')
                            with ui.row().classes('w-full items-center '):
                                with ui.column().classes('w-full h-full flex-1 justify-center items-center '):
                                    budget_progress, amount_spent_progress, total_budget_progress= tx.budget_progress(include_numbers=True)
                                    ratio_percentage = round(budget_progress, 3)
                                    ratio = round(budget_progress, 1)
                                    progress_bar = '█'*int(ratio*10) + '▒'*(10-int(ratio*10)) if ratio < 1 else '█'*10
                                    ui.markdown(progress_bar).classes('font-bold')
                                with ui.column().classes('flex-none pr-8 truncate ...'):
                                    ui.label(f'{ratio_percentage*100:.1f}%')
                            with ui.row().classes('justify-center w-full pt-3'):
                                ui.label(f'€{amount_spent_progress} / €{total_budget_progress}')

            # Month statistics
            with ui.column().classes('w-full flex-1 h-full max-h-'):
                with ui.card().classes(Styling.card()):
                    ui.label('Month statistics').classes('self-center text-2xl underline underline-offset-8')
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
                                                                showlegend=False,
                                                                title='Spending'
                                                                )
                                                            ]
                                                        )                               
                            ui.plotly(piechart_object).classes('max-w-md')

                    draw_piechart(selected_month)

