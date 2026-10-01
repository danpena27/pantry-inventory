'''
Author: Daniel Pena Arias
Date: 10/01/2026
Original coursework: 12/09/2025
Program: pantry_main.py
Description: This file runs the pantry inventory program.
it displays the menu and calls the PantryManager class methods.
'''

from pantry_classes import PantryManager

def menu(manager):
    # shows menu and calls functions based on input
    while True:
        print('')
        print('Pantry Inventory menu')
        print('1. Add Pantry Item')
        print('2. Delete Item')
        print('3. Search Items')
        print('4. View All Items')
        print('5. Monthly Report')
        print('6. Add Category')
        print('7. Save/Exit')
        print('')

        select = input('Make a selection(1-7): ')

        if select == '1':
            manager.add_item()

        elif select == '2':
            manager.delete_item()

        elif select == '3':
            manager.search_item()

        elif select == '4':
            manager.view_all()

        elif select == '5':
            manager.view_by_month()

        elif select == '6':
            manager.add_category()

        elif select == '7':
            manager.save_data()
            print('Goodbye!')
            break

        else:
            print('Wrong selection, try again.')
def main():
    manager = PantryManager()
    manager.load_data()
    menu(manager)

if __name__ == '__main__':
    main()
