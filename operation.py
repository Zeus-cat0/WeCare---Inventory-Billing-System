import datetime
from write import write_products


def display_products(products):
    """
    Display all products in a formatted table.

    Args:
        products (list): List of product dictionaries to display.
    """
    if not products:
        print("No products available.")
        return
    print("\nAvailable Products:")
    print("-" * 75)
    print("{:<4} {:<20} {:<15} {:<10} {:<15} {:<12}".format(
        "No.", "Product Name", "Brand", "Stock", "Origin", "Selling Price"))
    print("-" * 75)
    
    for idx, p in enumerate(products, start=1):
        print("{:<4} {:<20} {:<15} {:<10} {:<15} Rs.{:<12}".format(
            idx,
            p['product_name'],
            p['brand'],
            p['stock'],
            p['country'],
            p['selling_price']
        ))
    print("-" * 75)


def process_sale(products):
    """
    Process a sale transaction including promotions and invoice generation.

    Args:
        products (list): List of product dictionaries.

    Features:
        - Buy 3, get 1 free promotion
        - Stock validation
        - Invoice generation with VAT calculation
    """
    display_products(products)
    transaction = []
    while True:
        try:
            choice = input("\nEnter product number to buy (or 'done' to finish): ").strip()
            if choice.lower() == 'done':
                break

            product_index = int(choice) - 1
            if product_index < 0 or product_index >= len(products):
                print("Invalid product number. Please try again.")
                continue

            product = products[product_index]
            qty = int(input("Enter quantity to buy (paid): "))
            if qty <= 0:
                print("Quantity must be positive.")
                continue

            free = (qty // 3) * 1  
            total_required = qty + free

            if product['stock'] < total_required:
                max_possible_sets = product['stock'] // 4 
                remaining_items = product['stock'] % 4
                
                if max_possible_sets > 0:
                    max_paid = max_possible_sets * 3
                    max_free = max_possible_sets * 1
                    print(f"Not enough stock. You can buy up to {max_paid} (get {max_free} free) for a total of {max_paid + max_free} items.")
                else:
                    print(f"Not enough stock for promotion. You can buy up to {product['stock']} individual units at regular price.")
                continue

            transaction.append({
                'product': product,
                'quantity': qty,
                'free': free,
                'total_received': total_required
            })

            print("\nCurrent Purchase Summary:")
            print("-" * 50)
            for item in transaction:
                p = item['product']
                print(f"{p['product_name']} ({p['brand']})")
                print(f"Total: {item['total_received']} (Paid: {item['quantity']}, Free: {item['free']})")
                print(f"Price per unit: Rs.{p['selling_price']}")
                print(f"Amount: Rs.{item['quantity'] * p['selling_price']}")
                print("-" * 50)

        except ValueError:
            print("Invalid input. Please enter numbers only.")

    if not transaction:
        print("No items purchased. Transaction cancelled.")
        return

    customer_name = input("Enter customer name: ")
    subtotal = sum(item['quantity'] * item['product']['selling_price'] for item in transaction)
    vat = subtotal * 0.13  
    total_amount = subtotal + vat

    invoice_lines = [
        "=" * 50,
        "WeCare Beauty Store Invoice",
        "=" * 50,
        f"Customer: {customer_name}",
        f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-" * 50,
        "Items Purchased:",
        "-" * 50
    ]

    for item in transaction:
        p = item['product']
        invoice_lines.extend([
            f"Product: {p['product_name']} ({p['brand']})",
            f"Total received: {item['total_received']} (Paid: {item['quantity']}, Free: {item['free']})",
            f"Price per unit: Rs.{p['selling_price']}",
            f"Amount: Rs.{item['quantity'] * p['selling_price']}",
            "-" * 50
        ])
        p['stock'] -= item['total_received']

    invoice_lines.extend([
        f"Subtotal: Rs.{subtotal}",
        f"VAT (13%): Rs.{vat:.2f}",
        f"Total Amount: Rs.{total_amount:.2f}",
        "=" * 50,
        "Thank you for shopping with WeCare!"
    ])

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    invoice_filename = f"invoice_{customer_name}_{timestamp}.txt"
    with open(invoice_filename, 'w') as file:
        file.write('\n'.join(invoice_lines))

    write_products('products.txt', products)

    print("\nInvoice Summary:")
    for line in invoice_lines:
        print(line)
    print(f"Invoice saved as: {invoice_filename}")


def process_restock(products):
    """
    Process restocking of products by adding to existing stock.

    Args:
        products (list): List of product dictionaries to restock.
    """
    display_products(products)
    while True:
        try:
            choice = input("\nEnter product number to restock (or 'done' to finish): ").strip()
            if choice.lower() == 'done':
                break

            index = int(choice) - 1
            if index < 0 or index >= len(products):
                print("Invalid product number.")
                continue

            product = products[index]
            print(f"Selected: {product['product_name']} ({product['brand']})")
            print(f"Current stock: {product['stock']}")

            quantity = int(input("Enter quantity to add: "))
            if quantity <= 0:
                print("Quantity must be positive.")
                continue

            product['stock'] += quantity
            print("Stock updated successfully.")
            print(f"New stock: {product['stock']}")
            print("-" * 50)

            write_products('products.txt', products)

        except ValueError:
            print("Please enter a valid number.")

    print("Restocking complete.")
    display_products(products)


def add_product(products):
    """
    Add new products to the inventory.

    Args:
        products (list): List of existing product dictionaries.

    Returns:
        list: Updated list of products with new items added.
    """
    print("\n=== Add New Products ===")
    
    try:
        num_to_add = int(input("How many products do you want to add? "))
        if num_to_add <= 0:
            print("Number must be positive.")
            return products
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return products

    for i in range(num_to_add):
        print(f"\nAdding Product {i + 1} of {num_to_add}")
        try:
            name = input("Product name: ").strip()
            brand = input("Brand: ").strip()
            stock = int(input("Stock quantity: "))
            cost_price = int(input("Cost price: "))
            origin = input("Country of origin: ").strip()

            if stock <= 0 or cost_price <= 0:
                print("Values must be positive.")
                continue

            product = {
                'product_name': name,
                'brand': brand,
                'stock': stock,
                'cost_price': cost_price,
                'country': origin,
                'selling_price': cost_price * 2
            }

            products.append(product)
            print("Product added successfully!")
            print("-" * 50)

        except ValueError:
            print("Invalid entry. Numbers required for stock and price.")

    write_products('products.txt', products)
    return products