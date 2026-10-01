'''
Author: Daniel Pena Arias 
Date: 10/01/2026
Original coursework: 12/09/2025
Program: pantry_classes
Description: This file contains the PantryItem and PantryManager classes.
It handles all data for pantry items, including adding, deleting, searching,
viewing inventory, and saving/loading inventory data.
'''
import csv
import math
from pathlib import Path
from datetime import datetime

class PantryItem:
    '''this class represents one pantry item. It stores the item's details and includes methods to set it's data
    and show it's information when needed'''
    def __init__(self, name, category, quantity, cost, notes, expiration_date):
        self.name = name 
        self.category = category
        self.quantity = quantity
        self.cost = cost
        self.expiration_date = expiration_date
        self.notes = notes
        self.entry_date = datetime.now().strftime('%m/%d/%Y')

    # this function displays the item's details in a readable format for viewing
    def display(self):
        print('Item:', self.name, '(Category:', self.category, ')')
        print('Quantity:', self.quantity, 'Price per item:$' + format(self.cost, '.2f'))
        print('Notes:', self.notes)
        print('Expires on:', self.expiration_date)
        print('Added on:', self.entry_date)
        print()
            
class PantryManager:
    '''Class for managing the pantry. Handles list of items, categories, and operations like add/delete/search/view/save/load'''   
    def __init__(self, data_path=None):
        self.data_path = Path(data_path) if data_path is not None else Path(__file__).with_name("pantry.csv")
        
        # this function initializes the manager with empty lists for items and default categories
        self.items = [] 
        self.categories = ['Sauces','Snacks','Cleaning Supplies', 'Baking Supplies','Spices']
        
    # this function adds a new item or updates quantity if exists, with input validation and auto-date, allows adding new categories.
    def add_item(self):
        
        # get basic info from user
        itemname = input('Enter item name: ')
        print('Available categories: ')
        print('', ', '.join(self.categories))
        cat = input('Enter category: ')
        notes = input('Enter notes: ')
        expiration_date = input('Enter expiration date (MM/DD/YYYY): ')

        # add new category if needed
        if cat not in self.categories:
            self.categories.append(cat)

        # get quantity with validation
        valid = False
        while valid == False:
            try:
                amount = int(input('Enter quantity: '))
                if amount <= 0:
                    raise ValueError
                valid = True
            except ValueError:
                print('Quantity must be a positive whole number. Please try again.')

        # get cost with validation
        valid = False
        while valid == False:
            try:
                price = float(input('Enter cost: '))
                if not math.isfinite(price) or price < 0:
                    raise ValueError
                valid = True
            except ValueError:
                print('Cost must be a finite, nonnegative number. Try again.')

        # check if item exsists
        found = False
        for item in self.items:
            if item.name == itemname:
                item.quantity += amount
                found = True
                break

        # if not found create new item and add to list
        if found == False:
            new_item = PantryItem(itemname, cat, amount, price, notes, expiration_date)
            self.items.append(new_item)

        print('Item added!')

    # this function deletes an item by name
    def delete_item(self):

        print()
        print('Current inventory:')
        for item in self.items:
            print(item.name, ' Quantity:', item.quantity)
        print()

        item_name = input('Enter name of item to delete: ')

        for item in self.items:
            if item.name == item_name:

                if item.quantity > 1:
                    try:
                        delete_amount = int(input('How many do you want to delete? '))

                        if delete_amount <= 0:
                            print('Invalid amount.')
                            return

                        if delete_amount < item.quantity:
                            item.quantity -= delete_amount
                            print(delete_amount, 'removed. Remaining quantity:', item.quantity)

                        elif delete_amount == item.quantity:
                            self.items.remove(item)
                            print('All items deleted.')

                        else:
                            print('You cannot delete more than the quantity you have.')

                    except ValueError:
                        print('Invalid input. Quantity must be in numbers.')
                    return

                else:
                    self.items.remove(item)
                    print('Item deleted.')
                    return
        print('Item not found.')
    
    def search_item(self):
        searchterm = input('Enter name or category to search: ')
        count = 0

        for item in self.items:
            if searchterm in item.name or searchterm in item.category:
                item.display()
                count += 1

        print(count, 'Items found')

    def view_all(self):
        print()
        print('All inventory items')
        print('-------------------')
        print()

        if self.items == []:
            print('Inventory is empty')
        else:
            for item in self.items:
                item.display()
    
    # this function views items by month with totals and text bar chart for categories, filters by entry date
    def view_by_month(self):

        valid = False
        while valid == False:
            try:
                monthnum = int(input('Enter month number (1-12): '))
                if 1 <= monthnum <= 12:
                    valid = True
                else:
                    print('Uh-oh! Try again, only use numbers from 1 to 12')
            except ValueError:
                print('Uh-oh! Try again, only use numbers from 1 to 12')

        totalprice = 0.0
        catcost = {}

        for item in self.items:
            item_month = int(item.entry_date.split('/')[0])

            if item_month == monthnum:
                itemtotal = item.cost * item.quantity
                totalprice += itemtotal

                if item.category in catcost:
                    catcost[item.category] += itemtotal
                else:
                    catcost[item.category] = itemtotal

        print()
        print('Month', monthnum, 'Report:')
        print('Current inventory value:$' + format(totalprice, ',.2f'))
        print('Each # represents about $10 of current inventory')
        print()

        if catcost == {}:
            print('No inventory for that month!')
            return

        for cat in catcost:
            price = catcost[cat]

            barlen = int(price / 10)
            bar = ''

            for i in range(barlen):
                bar += '#'

            print(cat + ':' + bar + '($' + format(price, ',.2f') + ')')

       # this function let's the user add a new category
    def add_category(self):
        print()
        print('Current categories:')
        print(','.join(self.categories))
        print()

        newcat = input('Enter new category name: ').strip()

        if newcat == '':
            print('Category name cannot be empty.')
            return

        if newcat in self.categories:
            print('Category already exists.')
        else:
            self.categories.append(newcat)
            print('Category added.')
    
    # Save quoted CSV fields so notes can contain commas and newlines.
    def save_data(self):
        with self.data_path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['NAME', 'CATEGORY', 'QUANTITY', 'COST', 'NOTES',
                             'ENTRY_DATE', 'EXPIRATION_DATE'])
            for item in self.items:
                writer.writerow([item.name, item.category, item.quantity, item.cost,
                                 item.notes, item.entry_date, item.expiration_date])
        print('Saved to file.')

    # Load inventory, including categories stored with existing items.
    def load_data(self):
        try:
            file = self.data_path.open('r', newline='', encoding='utf-8')
        except FileNotFoundError:
            print('No saved file found, starting a new one...')
            return

        loaded_items = []
        with file:
            for row in csv.DictReader(file):
                item = PantryItem(row['NAME'], row['CATEGORY'], int(row['QUANTITY']),
                                  float(row['COST']), row['NOTES'], row['EXPIRATION_DATE'])
                item.entry_date = row['ENTRY_DATE']
                loaded_items.append(item)
        self.items = loaded_items
        for item in self.items:
            if item.category not in self.categories:
                self.categories.append(item.category)
        print('Loaded inventory from file.')
