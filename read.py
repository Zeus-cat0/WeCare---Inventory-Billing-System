def read_products(filename):
    """
    Read product data from a file and return as a list of dictionaries.

    Args:
        filename (str): The name of the file to read from.

    Returns:
        list: List of product dictionaries. Returns empty list if file not found.
    """
    products = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 5:
                        product = {
                            'product_name': parts[0],
                            'brand': parts[1],
                            'stock': int(parts[2]),
                            'cost_price': int(parts[3]),
                            'country': parts[4],
                            'selling_price': int(parts[3]) * 2
                        }
                        products.append(product)
    except FileNotFoundError:
        print(f"Warning: '{filename}' not found. Using empty list.")
    except ValueError as e:
        print(f"Data format error: {e}")
    return products