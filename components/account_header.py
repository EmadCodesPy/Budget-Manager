from nicegui import ui, app


def header():
    hover_class = 'transition ease-in-out hover:-translate-y-1 hover:scale-105'
    bg_class = 'bg-gradient-to-r from-cyan-400 to-blue-700 opactiy-50'

    with ui.row().classes('w-full justify-center gap-10'):
        #Back to dashboard logo
        ui.label('MoneyManager').classes(bg_class).classes(f'bg-clip-text text-transparent text-4xl {hover_class}').tooltip('Dashboard')\
        .on('click', handler=lambda: ui.navigate.to('/dashboard'))
        #Toggle dark mode
        ui.switch('Dark Mode', on_change=ui.dark_mode().toggle).classes('absolute bottom-0 left-0').bind_value(app.storage.user, 'dark')
        