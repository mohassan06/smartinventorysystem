from product import Product
import csv

CATE_MIN = 1
CATE_MAX = len(Product.CATEGORIES)
CSV_HEAD = ["ID", "Name", "CategoryIndex", "Quantity", "Price", "ReorderLevel"]

def product_index(prod_list, pid):
    for i in range(len(prod_list)):
        if prod_list[i].get_product_id() == pid:
            return i
    return -1

def print_products(prod_list):
    if not prod_list:
        print("(no products)")
        return
    print(f"{'ID':<10}{'Name':<20}{'Category':<15}{'Qty':>6}{'Price':>10}{'Reorder':>9}")
    for p in prod_list:
        print(
            f"{p.get_product_id():<10}"
            f"{p.get_name():<20}"
            f"{p.get_category_name():<15}"
            f"{p.get_quantity():>6}"
            f"{p.get_price():>10.2f}"
            f"{p.get_reorder_level():>9}"
        )

def load_products(file):
    data = []
    with open(file, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            data.append(Product(
                row["ID"],
                row["Name"],
                int(row["CategoryIndex"]),
                int(row["Quantity"]),
                float(row["Price"]),
                int(row["ReorderLevel"])
            ))
    return data

def save_products(file, prod_list):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEAD)
        w.writeheader()
        for p in prod_list:
            w.writerow({
                "ID": p.get_product_id(),
                "Name": p.get_name(),
                "CategoryIndex": p.get_category(),
                "Quantity": p.get_quantity(),
                "Price": p.get_price(),
                "ReorderLevel": p.get_reorder_level()
            })

def add_product(prod_list):
    pid = input("Enter product ID: ").strip()
    if product_index(prod_list, pid) != -1:
        print("Product ID already exists.")
        return
    name = input("Enter product name: ").strip()
    while True:
        try:
            cat = int(input(f"Enter category index ({CATE_MIN}-{CATE_MAX}): "))
            if cat < CATE_MIN or cat > CATE_MAX:
                print("Invalid category.")
                continue
            break
        except ValueError:
            print("Please enter a number.")
    while True:
        try:
            qty = int(input("Enter quantity: "))
            if qty < 0:
                print("Must be >= 0.")
                continue
            break
        except ValueError:
            print("Please enter an integer.")
    while True:
        try:
            price = float(input("Enter price: "))
            break
        except ValueError:
            print("Please enter a valid number.")
    while True:
        try:
            rl = int(input("Enter reorder level: "))
            if rl < 0:
                print("Must be >= 0.")
                continue
            break
        except ValueError:
            print("Please enter an integer.")
    prod_list.append(Product(pid, name, cat, qty, price, rl))
    print("Product added.")

def remove_product(prod_list):
    pid = input("Enter product ID to remove: ").strip()
    idx = product_index(prod_list, pid)
    if idx == -1:
        print("Product not found")
        return
    prod_list.pop(idx)
    print("Product removed.")

def edit_product(prod_list):
    pid = input("Enter product ID to edit: ").strip()
    idx = product_index(prod_list, pid)
    if idx == -1:
        print("Product not found")
        return
    p = prod_list[idx]
    name = input(f"Name [{p.get_name()}]: ").strip()
    if name:
        p.set_name(name)
    cat_in = input(f"Category index ({CATE_MIN}-{CATE_MAX}) [{p.get_category()}]: ").strip()
    if cat_in:
        try:
            cat_val = int(cat_in)
            if CATE_MIN <= cat_val <= CATE_MAX:
                p.set_category(cat_val)
            else:
                print("Invalid category - keeping old.")
        except ValueError:
            print("Invalid input - keeping old.")
    price_in = input(f"Price [{p.get_price()}]: ").strip()
    if price_in:
        try:
            p.set_price(float(price_in))
        except ValueError:
            print("Invalid - keeping old.")
    rl_in = input(f"Reorder level [{p.get_reorder_level()}]: ").strip()
    if rl_in:
        try:
            rl_val = int(rl_in)
            if rl_val >= 0:
                p.set_reorder_level(rl_val)
            else:
                print("Invalid - keeping old.")
        except ValueError:
            print("Invalid - keeping old.")
    print("Product updated.")

def search_product(prod_list, term):
    t = term.lower()
    return [p for p in prod_list if t in p.get_name().lower() or t in p.get_category_name().lower()]

def list_products_by_category(prod_list):
    try:
        cat = int(input(f"Select category ({CATE_MIN}-{CATE_MAX}): "))
    except ValueError:
        print("Invalid category.")
        return
    filtered = [p for p in prod_list if p.get_category() == cat]
    if filtered:
        print_products(filtered)
    else:
        print("(no products in this category)")

def sell_product(prod_list):
    pid = input("Enter product ID to sell: ").strip()
    idx = product_index(prod_list, pid)
    if idx == -1:
        print("Product not found")
        return
    try:
        amt = int(input("Enter quantity to sell: "))
        if amt <= 0:
            print("Invalid quantity.")
            return
    except ValueError:
        print("Invalid quantity.")
        return
    if not prod_list[idx].sell(amt):
        print("Not enough stock to complete the sale.")
    else:
        print("Sale completed.")

def restock_product(prod_list):
    pid = input("Enter product ID to restock: ").strip()
    idx = product_index(prod_list, pid)
    if idx == -1:
        print("Product not found")
        return
    try:
        amt = int(input("Enter restock amount: "))
        if amt <= 0:
            print("Invalid amount.")
            return
    except ValueError:
        print("Invalid amount.")
        return
    prod_list[idx].restock(amt)
    print("Product restocked.")

def low_stock_report(prod_list):
    low_items = [p for p in prod_list if p.needs_restock()]
    if not low_items:
        print("No products below reorder level.")
    else:
        print("Low Stock Items:")
        print_products(low_items)

def inventory_summary(prod_list):
    total_qty = sum(p.get_quantity() for p in prod_list)
    print(f"Total products: {len(prod_list)}")
    print(f"Total quantity: {total_qty}")
