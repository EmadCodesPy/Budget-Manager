from nicegui import ui
from pages.login_page import login_page
from pages.dashboard import dashboard
from pages.new_budget_page import new_budget_page
from pages.account_page import account_page

@ui.page('/')
def show_login():
    login_page()

@ui.page('/dashboard')
def show_dashboard():
    dashboard()

@ui.page('/budget')
def show_budget_page():
    new_budget_page()

@ui.page('/account')
def show_account_page():
    account_page()
    
@ui.page('/edit_budget')
def show_edit_budget_page():
    pass

ui.run(storage_secret='EmadsBudgetManager')