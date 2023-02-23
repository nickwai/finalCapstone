# ========The beginning of the class==========
# import Python tabulate module
from tabulate import tabulate


class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)
        self.for_sale = False

    '''
    Add the code to return the cost of the shoe in this method.
    '''
    def get_cost(self):
        return self.cost

    '''
    Add the code to return the quantity of the shoes.
    '''
    def get_quantity(self):
        return self.quantity

    '''
    Add a code to returns a string representation of a class.
    '''
    def __str__(self):
        return f'''===================================== 
Country:     {self.country} 
Code:        {self.code} 
Product:     {self.product}
Cost:        {self.cost}
Quantity:    {self.quantity}
====================================='''


# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []

# ==========Functions outside the class==============
'''
This function will open the file inventory.txt
and read the data from this file, then create a shoes object with this data
and append this object into the shoes list. One line in this file represents
data to create one object of shoes. You must use the try-except in this function
for error handling. Remember to skip the first line using your code.
'''


def read_shoes_data():
    try:
        # clear the list 'shoe_list' to avoid accumulate append a duplicate data into a list.
        shoe_list.clear()
        with open('inventory.txt', 'r') as file:
            for index, line in enumerate(file, 0):
                # set if condition to skip the file first line to avoid error.
                if index > 0:
                    line_list = line.strip('\n').split(',')
                    shoe_list.append(Shoe(line_list[0], line_list[1], line_list[2], line_list[3], line_list[4]))
    # except FileNotFoundError if 'inventory.txt' can't found and print valid error message
    except FileNotFoundError:
        print('Cannot found the file inventory.txt')


'''
This function will allow a user to capture data about a shoe and use this data to create a shoe object
and append this object inside the shoe list.
'''


def capture_shoes():
    shoe_country = input('Enter the country name of the new shoes: ')
    shoe_code = input('Enter the code of the new shoes: ')
    shoe_product = input('Enter the product name of the new shoes: ')
    try:
        shoe_cost = int(input('Enter the cost of the new shoes: '))
        shoe_quantity = int(input('Enter the quantity of the new shoes: '))
        # write and append the new shoes item into an "inventory.txt"
        with open('inventory.txt', 'a') as file:
            file.write(f'\n{shoe_country},{shoe_code},{shoe_product},{shoe_cost},{shoe_quantity}')
        # print new item added confirmation message
        print(f'\nNew shoes {shoe_product} added.')
    # except ValueError if user is not enter an integer number and print valid error message
    except ValueError:
        print('Invalid input! It must be an integer number.')


'''
This function will iterate over the shoes list and
print the details of the shoes returned from the __str__
function. Optional: you can organise your data in a table format
by using Python’s tabulate module.
'''


def view_all():
    read_shoes_data()
    data_list = []
    # "shoe_list" doesn't have the first role data, so add it manually
    top_row = ['Country', 'Code', 'Product', ' Cost', 'Quantity']
    for index1 in shoe_list:
        # convert the data to a string and store it to a list "data_list"
        data_list.append([index1.country, index1.code, index1.product, index1.cost, index1.quantity])
    # print a table format using Python tabulate module
    print(tabulate(data_list, headers=top_row, tablefmt='fancy_grid'))


'''
This function will find the lowest stock shoes items, store it to the list "stock_list" and return it.
'''


def get_lowest_stock():
    lowest_qty_item = []
    stock_list = []
    num = 0

    read_shoes_data()
    # get the first shoes item quantity from "shoe_list"
    for item in shoe_list:
        num = item.quantity
        break
    '''use first shoes item quantity as an initial number and compare to every shoes item quantity from "shoe_list" 
       and find the smallest quantity number'''
    for item1 in shoe_list:
        if item1.quantity < num:
            num = item1.quantity
            lowest_qty_item = item1
    '''use the smallest quantity number to compare to every shoes item quantity from "shoe_list" and find out which
       shoes has same quantity and store it into a list "stock_list"'''
    for stock in shoe_list:
        if stock.quantity == lowest_qty_item.quantity:
            stock_list.append(stock)
    return stock_list


'''
Display the lowest shoes quantity items
'''


def display_lowest_stock():
    for info in get_lowest_stock():
        print(info)


'''
This function will find the shoe object with the lowest quantity,
which is the shoes that need to be re-stocked. Ask the user if they
want to add this quantity of shoes and then update it.
This quantity should be updated on the file for this shoe.
'''


def re_stock():
    restock_list = []
    # show user all the lowest stock shoes items
    print('\n=== The lowest stock shoes list ===')
    display_lowest_stock()

    # ask user do they want to restock the items. Print out the shoes item and ask user one by one
    for index1 in get_lowest_stock():
        user_input1 = input(f'\nDo you want restock the product: {index1.code}, {index1.product} (yes or no)? ')
        if user_input1.lower() == 'yes':
            # if user want to restore this time, ask them to enter the new stock quantity
            user_input2 = input('Enter the new quantity: ')
            if user_input2.isdigit():
                # store the product code and new quantity into a list "restock_list"
                restock_list.append([index1.code, int(user_input2)])
                # display a stock updated confirmation and show the new quantity
                print(f'\nThe product ({index1.code}, {index1.product}) stock has been updated. '
                      f'New stock quantity has {user_input2}')
            else:
                # set a condition and print valid error if user is not enter an integer number
                print('The shoes quantity must be an integer number.')
                break
        # print the product current quantity if user don't want to restore it
        elif user_input1.lower() == 'no':
            print(f'You do not want to restock the product {index1.code}, {index1.product}. '
                  f'It has stock quantity {index1.quantity}')
        else:
            # print a valid error message if user is not enter "yes" or "no"
            print('Input invalid! Only can choose "yes" or "no".')
            break
    # use for loop to update all the items quantity in "shoe_list" that user want to restock
    for value1 in shoe_list:
        for value2 in restock_list:
            if value1.code == value2[0]:
                value1.quantity = int(value2[1])

    with open('inventory.txt', 'w') as file:
        # "shoe_list" doesn't have the first role data, so add it manually
        file.write(f'Country,Code,Product,Cost,Quantity')
    with open('inventory.txt', 'a') as file1:
        # write the updated data into the "shoe_list"
        for new_line in shoe_list:
            file1.write(f'\n{new_line.country},{new_line.code},{new_line.product},{new_line.cost},{new_line.quantity}')


'''
 This function will search for a shoe from the list
 using the shoe code and return this object so that it will be printed.
'''


def search_shoe(shoe_code):
    read_shoes_data()
    for index3 in shoe_list:
        if shoe_code == index3.code:
            return index3


'''
This function will calculate the total value for each item.
Please keep the formula for value in mind: value = cost * quantity.
Print this information on the console for all the shoes.
'''


def value_per_item():
    read_shoes_data()
    for index4 in shoe_list:
        value = int(index4.cost) * int(index4.quantity)
        print(f'=====================================\n'
              f'Country:     {index4.country}\n'
              f'Code:        {index4.code}\n'
              f'Product:     {index4.product}\n'
              f'Cost:        {index4.cost}\n'
              f'Quantity:    {index4.quantity}\n'
              f'Total value: {value}\n'
              f'=====================================\n')


'''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''


def highest_qty():
    highest_qty_item = []
    stock_list1 = []
    num1 = 0
    read_shoes_data()

    # get the first shoes item quantity from "shoe_list"
    for item2 in shoe_list:
        num1 = item2.quantity
        break
    '''use first shoes item quantity as an initial number and compare to every shoes item quantity from "shoe_list" 
       and find the largest quantity number'''
    for item3 in shoe_list:
        if item3.quantity > num1:
            num1 = item3.quantity
            highest_qty_item = item3
    '''use the largest quantity number to compare to every shoes item quantity from "shoe_list" and find out which
       shoes has same quantity and store it into a list "stock_list"'''
    for stock1 in shoe_list:
        if stock1.quantity == highest_qty_item.quantity:
            stock1.for_sale = True
            stock_list1.append(stock1)

    # print all the highest stock and for sale items
    print('\n=== The highest stock shoes list ===')
    for hs in stock_list1:
        print(hs)

    # print all the for sale items
    print('\n======= Being for sale items =======')
    for vs in stock_list1:
        if vs.for_sale:
            print(vs)


# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''

while True:
    # presenting the menu to the user and
    # making sure that the user input is convert to lower case.
    menu = input('''\nSelect one of the following Options below:
r  - register a new shoes
i  - search a shoes by code and show the information 
va - view all shoes in stock
vl - view the lowest stock shoes
rs - restock the shoes
vh - view the highest stock and for sale items
vv - view total value of each shoe items
q  - quit
: ''').lower()

    if menu == 'r':
        capture_shoes()

    if menu == 'i':
        user_input = input('\nEnter the shoe code that you want to search: ')
        if search_shoe(user_input) is None:
            print('Cannot found the shoes.')
        else:
            print(search_shoe(user_input))

    if menu == 'va':
        view_all()

    if menu == 'vl':
        # print all the lowest stock items
        print('\n=== The lowest stock shoes list ===')
        display_lowest_stock()

    if menu == 'rs':
        re_stock()

    if menu == 'vh':
        highest_qty()

    if menu == 'vv':
        value_per_item()

    if menu == 'q':
        print('Good Bye')
        exit()

