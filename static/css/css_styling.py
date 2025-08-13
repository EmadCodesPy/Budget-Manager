from nicegui import ui

class Styling():
    #Card css
    @staticmethod
    def card():
        return 'bg-gradient-to-r from-cyan-400 to-blue-700 opactiy-50 shadow-2xl p-6 w-full flex-1 text-white transition ease-in-out hover:-translate-y-1 hover:scale-105'    

    #Login page background text
    @staticmethod
    def moneymanager_text(text_classes: str = '', column_classes: str = ''):
        with ui.column().classes('w-full justify-center items-center absolute top-0 z-0').classes(column_classes):
            opacity = [100,90,60,50,30,20,10]
            for x in opacity:                
                ui.label('Welcome to MoneyManager').classes('bg-gradient-to-r from-cyan-400 to-blue-700')\
                    .classes(f'bg-clip-text text-transparent text-6xl/[4.5rem] opacity-{x} whitespace-nowrap select-none')\
                    .classes('transition ease-in-out hover:-translation-y-1 hover:scale-110')\
                    .classes(text_classes)

    #Hover css
    @staticmethod
    def hover():
        return 'transition ease-in-out hover:-translate-y-1 hover:scale-105'
    
    #Background css
    @staticmethod
    def background():
        return 'bg-gradient-to-r from-cyan-400 to-blue-700 opactiy-50'
    
    #MoneyManager logo
    @staticmethod
    def logo():
        return ui.label('MoneyManager').classes('bg-gradient-to-r from-cyan-400 to-blue-700').classes(f'bg-clip-text text-transparent text-4xl')


    