def write_products(filename, products):
    """
    Write product data to a file in CSV format.

    Args:
        filename (str): The name of the file to write to.
        products (list): List of product dictionaries to write.
    """
    try:
        with open(filename, 'w') as file:
            for p in products:
                line = f"{p['product_name']},{p['brand']},{p['stock']},{p['cost_price']},{p['country']}\n"
                file.write(line)
    except Exception as e:
        print(f"Failed to write to {filename}: {e}")