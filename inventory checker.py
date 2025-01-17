import tkinter as tk
from tkinter import ttk

def add_inventory():
    brand_name = brand_name_entry.get()
    product_name = product_name_entry.get()
    item_qty = int(item_qty_entry.get())
    with open('inventory.txt', 'a') as file:
        file.write(f'{brand_name},{product_name},{item_qty}\n')
    brand_name_entry.delete(0, tk.END)
    product_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    generate_inventory()  


def update_inventory():
    brand_name = brand_name_entry.get()
    product_name = product_name_entry.get()
    item_qty = int(item_qty_entry.get())
    updated = False
    inventory_data = []
    
   
    with open('inventory.txt', 'r') as file:
        inventory_data = file.readlines()
        
    with open('inventory.txt', 'w') as file:
        for line in inventory_data:
            name, product, qty = line.strip().split(',')
            if name == brand_name and product == product_name:
                file.write(f'{brand_name},{product_name},{item_qty}\n')  
                updated = True
            else:
                file.write(line) 
                
    if not updated:
        show_search_popup(f'{brand_name} {product_name} not found in inventory.')
    brand_name_entry.delete(0, tk.END)
    product_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    generate_inventory()  # Update the list after updating an item


def search_inventory():
    brand_name = brand_name_entry.get()
    product_name = product_name_entry.get()
    found = False
    search_result = ""

    
    with open('inventory.txt', 'r') as file:
        for line in file:
            name, product, qty = line.strip().split(',')
            if name == brand_name and product == product_name:
                search_result = f'{name} - {product} - {qty}'
                found = True
                break

    if found:
        show_search_popup(search_result)  
    else:
        show_search_popup(f'{brand_name} {product_name} not found in inventory.') 

    brand_name_entry.delete(0, tk.END)
    product_name_entry.delete(0, tk.END)


def remove_inventory():
    selected_item = inventory_treeview.selection()
    if selected_item:
        brand_name = inventory_treeview.item(selected_item, 'values')[0]
        product_name = inventory_treeview.item(selected_item, 'values')[1]
        item_qty = inventory_treeview.item(selected_item, 'values')[2]

        with open('inventory.txt', 'r') as file:
            inventory_data = file.readlines()

        
        with open('inventory.txt', 'w') as file:
            for line in inventory_data:
                name, product, qty = line.strip().split(',')
                if name != brand_name or product != product_name or qty != item_qty:
                    file.write(line + '\n')

        generate_inventory()  


def generate_inventory():
    for row in inventory_treeview.get_children():
        inventory_treeview.delete(row) 

    with open('inventory.txt', 'r') as file:
        for line in file:
            name, product, qty = line.strip().split(',')


def show_search_popup(message):
    
    popup = tk.Toplevel(root)
    popup.title("Search Result")
    

    result_label = tk.Label(popup, text=message, font=("Arial", 12))
    result_label.pack(padx=10, pady=10)
    

    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=5)


def press(num):
    current = calc_entry.get()
    calc_entry.delete(0, tk.END)
    calc_entry.insert(tk.END, current + str(num))


def clear():
    calc_entry.delete(0, tk.END)


def calculate():
    try:
        result = eval(calc_entry.get())
        calc_entry.delete(0, tk.END)
        calc_entry.insert(tk.END, result)
    except:
        calc_entry.delete(0, tk.END)
        calc_entry.insert(tk.END, "Error")


def sort_inventory():

    popup = tk.Toplevel(root)
    popup.title("Sort Inventory")
    
    
    sort_label = tk.Label(popup, text="Sort By:", font=("Arial", 12))
    sort_label.pack(padx=10, pady=10)
    
    
    sort_quantity_asc_button = tk.Button(popup, text="Quantity (Low to High)", command=lambda: sort_by('quantity', 'asc'))
    sort_quantity_asc_button.pack(padx=5, pady=5)
    
    sort_quantity_desc_button = tk.Button(popup, text="Quantity (High to Low)", command=lambda: sort_by('quantity', 'desc'))
    sort_quantity_desc_button.pack(padx=5, pady=5)
    
    sort_brand_asc_button = tk.Button(popup, text="Brand (A to Z)", command=lambda: sort_by('brand', 'asc'))
    sort_brand_asc_button.pack(padx=5, pady=5)
    
    sort_brand_desc_button = tk.Button(popup, text="Brand (Z to A)", command=lambda: sort_by('brand', 'desc'))
    sort_brand_desc_button.pack(padx=5, pady=5)
    
    sort_product_asc_button = tk.Button(popup, text="Product (A to Z)", command=lambda: sort_by('product', 'asc'))
    sort_product_asc_button.pack(padx=5, pady=5)
    
    sort_product_desc_button = tk.Button(popup, text="Product (Z to A)", command=lambda: sort_by('product', 'desc'))
    sort_product_desc_button.pack(padx=5, pady=5)


def sort_by(criteria, order):
    
    inventory_data = []
    with open('inventory.txt', 'r') as file:
        for line in file:
            name, product, qty = line.strip().split(',')
            inventory_data.append((name, product, int(qty)))
    
    
    if criteria == 'quantity':
        inventory_data.sort(key=lambda x: x[2], reverse=(order == 'desc'))
    elif criteria == 'brand':
        inventory_data.sort(key=lambda x: x[0], reverse=(order == 'desc'))
    elif criteria == 'product':
        inventory_data.sort(key=lambda x: x[1], reverse=(order == 'desc'))
    
    
    for row in inventory_treeview.get_children():
        inventory_treeview.delete(row)
    
    for item in inventory_data:
        inventory_treeview.insert('', 'end', values=item)  # Insert each item

    show_search_popup(f"Inventory sorted by {criteria.capitalize()} ({'Descending' if order == 'desc' else 'Ascending'})")


root = tk.Tk()
root.title("Inventory Management and Calculator")


brand_name_label = tk.Label(root, text="Brand Name:")
brand_name_label.grid(row=0, column=0, padx=5, pady=5)
brand_name_entry = tk.Entry(root)
brand_name_entry.grid(row=0, column=1, padx=5, pady=5)

product_name_label = tk.Label(root, text="Product Name:")
product_name_label.grid(row=1, column=0, padx=5, pady=5)
product_name_entry = tk.Entry(root)
product_name_entry.grid(row=1, column=1, padx=5, pady=5)

item_qty_label = tk.Label(root, text="Item Quantity:")
item_qty_label.grid(row=2, column=0, padx=5, pady=5)
item_qty_entry = tk.Entry(root)
item_qty_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Inventory", command=add_inventory)
add_button.grid(row=3, column=0, padx=5, pady=5)
update_button = tk.Button(root, text="Update Inventory", command=update_inventory)
update_button.grid(row=3, column=1, padx=5, pady=5)
search_button = tk.Button(root, text="Search Inventory", command=search_inventory)
search_button.grid(row=4, column=0, padx=5, pady=5)
remove_button = tk.Button(root, text="Remove Inventory", command=remove_inventory)
remove_button.grid(row=4, column=1, padx=5, pady=5)


inventory_label = tk.Label(root, text="Inventory List")
inventory_label.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

inventory_treeview = ttk.Treeview(root, columns=("Brand", "Product", "Stock"), show="headings", height=10)
inventory_treeview.grid(row=6, column=0, padx=5, pady=5, columnspan=2)


inventory_treeview.heading("Brand", text="Brand Name")
inventory_treeview.heading("Product", text="Product Name")
inventory_treeview.heading("Stock", text="Stock")


inventory_treeview.column("Brand", width=150)
inventory_treeview.column("Product", width=150)
inventory_treeview.column("Stock", width=100)

generate_button = tk.Button(root, text="Generate Inventory", command=generate_inventory)
generate_button.grid(row=7, column=0, padx=5, pady=5, columnspan=2)


sort_button = tk.Button(root, text="Sort Inventory", command=sort_inventory)
sort_button.grid(row=8, column=0, padx=5, pady=5, columnspan=2)


calc_label = tk.Label(root, text="Calculator")
calc_label.grid(row=9, column=0, padx=5, pady=5, columnspan=2)

calc_entry = tk.Entry(root, width=20)
calc_entry.grid(row=10, column=0, padx=5, pady=5, columnspan=2)

button_frame = tk.Frame(root)
button_frame.grid(row=11, column=0, padx=5, pady=5, columnspan=2)

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
]

for (text, row, col) in buttons:
    tk.Button(button_frame, text=text, width=5, command=lambda t=text: press(t) if t != '=' else calculate()).grid(row=row, column=col)

clear_button = tk.Button(root, text="Clear", command=clear)
clear_button.grid(row=12, column=0, padx=5, pady=5, columnspan=2)

root.mainloop()
