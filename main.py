from read import read_products
from operation import display_products, process_sale, process_restock, add_product
from write import write_products


class StoreError(Exception):
    """Base exception class for store-related errors."""
    pass


class InventoryError(StoreError):
    """Exception raised for errors in inventory operations."""
    pass


class SalesError(StoreError):
    """Exception raised for errors in sales operations."""
    pass


def save_products(filename, products):
    """
    Save product data to a file with error handling.

    Args:
        filename (str): The name of the file to save to.
        products (list): List of product dictionaries to save.

    Raises:
        InventoryError: If there's an error saving the products.
    """
    try:
        write_products(filename, products)
    except Exception as e:
        raise InventoryError(f"Failed to save products: {e}")


def display_menu():
    """Display the main menu options for the store management system."""
    print("\n=== WeCare Beauty Store Management System ===")
    print("1. Display Products")
    print("2. Process Sale")
    print("3. Restock Products")
    print("4. Add Product")
    print("5. Exit")


def main():
    """
    Main program loop for the store management system.

    Handles menu navigation and calls appropriate functions based on user input.
    """
    try:
        products = read_products('products.txt')

        while True:
            display_menu()
            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == '1':
                display_products(products)
            elif choice == '2':
                process_sale(products)
            elif choice == '3':
                process_restock(products)
            elif choice == '4':
                products = add_product(products)
            elif choice == '5':
                save_products('products.txt', products)
                print("Thank you for using WeCare Store Management System!")
                break
            else:
                print("Invalid choice. Please try again.")

    except FileNotFoundError:
        print("Error: 'products.txt' file not found.")
    except InventoryError as e:
        print(f"Inventory error: {e}")
    except SalesError as e:
        print(f"Sales error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()