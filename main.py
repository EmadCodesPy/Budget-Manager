from nicegui import ui
from pages.login_page import login_page
from pages.dashboard import dashboard
from pages.budget_page import budget_page
from pages.account_page import account_page

@ui.page('/')
def show_login():
    login_page()

@ui.page('/dashboard')
def show_dashboard():
    dashboard()

@ui.page('/budget')
def show_budget_page():
    budget_page()

@ui.page('/account')
def show_account_page():
    account_page()

ui.run(storage_secret='EmadsBudgetManager')