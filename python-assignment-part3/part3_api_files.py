import requests  # type: ignore
import json
from datetime import datetime
import os

# Custom Logger for Task 4
def log_error(context, error_msg):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR in {context}: {error_msg}\n")

# Task 1 — File Read & Write Basics
def task_1():
    print("=== Task 1: File Read & Write Basics ===\n")
    # Part A — Write
    notes = [
        "Topic 1: Variables store data. Python is dynamically typed.\n",
        "Topic 2: Lists are ordered and mutable.\n",
        "Topic 3: Dictionaries store key-value pairs.\n",
        "Topic 4: Loops automate repetitive tasks.\n",
        "Topic 5: Exception handling prevents crashes.\n"
    ]
    
    with open("python_notes.txt", "w", encoding="utf-8") as f:
        f.writelines(notes)
    print("File written successfully.")

    extra_notes = [
        "Topic 6: Functions make code reusable.\n",
        "Topic 7: File I/O allows persistent storage.\n"
    ]
    with open("python_notes.txt", "a", encoding="utf-8") as f:
        f.writelines(extra_notes)
    print("Lines appended.\n")

    # Part B — Read
    print("--- Reading File ---")
    try:
        with open("python_notes.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for idx, line in enumerate(lines, 1):
            print(f"{idx}. {line.rstrip('\n')}")
            
        print(f"\nTotal number of lines: {len(lines)}")
        
        keyword = input("\nEnter a keyword to search for: ")
        print(f"Searching for '{keyword}'...")
        found = False
        for line in lines:
            if keyword.lower() in line.lower():
                print(line.rstrip('\n'))
                found = True
        
        if not found:
            print(f"No match found for keyword '{keyword}'.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        log_error("task_1_read", str(e))
    print("\n" + "="*50 + "\n")

# Task 2 & Task 3C — API Integration + Robust API Calls
def make_robust_get(url):
    try:
        response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.ConnectionError as e:
        print("Connection failed. Please check your internet.")
        log_error(f"fetch_products ({url})", f"ConnectionError — {e}")
    except requests.exceptions.Timeout as e:
        print("Request timed out. Try again later.")
        log_error(f"fetch_products ({url})", f"Timeout — {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        log_error(f"fetch_products ({url})", f"Exception — {e}")
    return None

def make_robust_post(url, json_data):
    try:
        response = requests.post(url, json=json_data, timeout=5)
        return response
    except requests.exceptions.ConnectionError as e:
        print("Connection failed. Please check your internet.")
        log_error(f"post_product ({url})", f"ConnectionError — {e}")
    except requests.exceptions.Timeout as e:
        print("Request timed out. Try again later.")
        log_error(f"post_product ({url})", f"Timeout — {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        log_error(f"post_product ({url})", f"Exception — {e}")
    return None

def task_2():
    print("=== Task 2 (and 3C): API Integration ===\n")
    # Step 1 — Fetch and Display Products
    print("--- Step 1: Fetch 20 Products ---")
    response = make_robust_get("https://dummyjson.com/products?limit=20")
    
    products = []
    if response and response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        
        print(f"{'ID':<4} | {'Title':<30} | {'Category':<15} | {'Price':<8} | {'Rating'}")
        print("-" * 72)
        for p in products:
            title = p.get('title', '')[:30]
            print(f"{p.get('id', ''):<4} | {title:<30} | {p.get('category', ''):<15} | ${p.get('price', 0):<7.2f} | {p.get('rating', '')}")
    else:
        print("Failed to fetch products.")

    # Step 2 — Filter and Sort
    print("\n--- Step 2: Filter and Sort (Rating >= 4.5, Price Descending) ---")
    filtered_products = [p for p in products if p.get('rating', 0) >= 4.5]
    sorted_products = sorted(filtered_products, key=lambda x: x.get('price', 0), reverse=True)
    
    print(f"{'ID':<4} | {'Title':<30} | {'Price':<8} | {'Rating'}")
    print("-" * 55)
    for p in sorted_products:
        title = p.get('title', '')[:30]
        print(f"{p.get('id', ''):<4} | {title:<30} | ${p.get('price', 0):<7.2f} | {p.get('rating', '')}")

    # Step 3 — Search by Category
    print("\n--- Step 3: Fetch Laptops ---")
    laptops_response = make_robust_get("https://dummyjson.com/products/category/laptops")
    if laptops_response and laptops_response.status_code == 200:
        laptops_data = laptops_response.json().get("products", [])
        for laptop in laptops_data:
            print(f"- {laptop.get('title')} (${laptop.get('price')})")
    
    # Step 4 — POST Request
    print("\n--- Step 4: POST /add ---")
    new_product = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }
    post_response = make_robust_post("https://dummyjson.com/products/add", new_product)
    if post_response:
        print("Status Code:", post_response.status_code)
        try:
            print(json.dumps(post_response.json(), indent=2))
        except:
            print(post_response.text)
            
    print("\n" + "="*50 + "\n")

# Task 3 — Exception Handling
def safe_divide(a, b):
    # Returns the result of a / b. Catches ZeroDivisionError and TypeError.
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"
    except Exception as e:
        return f"Unexpected Error: {e}"

def read_file_safe(filename):
    # Tries to open and read the given file, catches exceptions and uses finally block.
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred reading the file: {e}")
        return None
    finally:
        print("File operation attempt complete.")

def task_3_A_B_D():
    print("=== Task 3: Exception Handling ===\n")
    print("--- Part A: Guarded Calculator ---")
    print("safe_divide(10, 2)   ->", safe_divide(10, 2))
    print("safe_divide(10, 0)   ->", safe_divide(10, 0))
    print("safe_divide('ten', 2)->", safe_divide("ten", 2))
    print()

    print("--- Part B: Guarded File Reader ---")
    content = read_file_safe("python_notes.txt")
    if content:
        print("Successfully read python_notes.txt (First 30 chars):", repr(content[:30]) + "...")  # type: ignore
        
    read_file_safe("ghost_file.txt")
    print()

    print("--- Part D: Input Validation Loop ---")
    while True:
        user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()
        if user_input.lower() == 'quit':
            break
        
        try:
            product_id = int(user_input)
            if not (1 <= product_id <= 100):
                print("Warning: Please enter an integer between 1 and 100.")
                continue
        except ValueError:
            print("Warning: That is not a valid integer. Try again.")
            continue
            
        print(f"Fetching product {product_id}...")
        response = make_robust_get(f"https://dummyjson.com/products/{product_id}")
        if response:
            if response.status_code == 404:
                print("Product not found.")
            elif response.status_code == 200:
                data = response.json()
                print(f"Found: {data.get('title')} - ${data.get('price')}")
            else:
                print(f"Unexpected status code: {response.status_code}")
                
    print("\n" + "="*50 + "\n")

# Task 4 — Logging to File
def task_4():
    print("=== Task 4: Error Logger Demonstration ===\n")
    print("--- Triggering intentional errors to log ---")
    
    # 1. Trigger ConnectionError
    print("Attempting to connect to non-existent host...")
    make_robust_get("https://this-host-does-not-exist-xyz.com/api")
    
    # 2. Trigger HTTP 404 (Not a python exception, requires manual logging)
    print("Attempting to fetch product ID 999...")
    res = make_robust_get("https://dummyjson.com/products/999")
    if res is not None and res.status_code != 200:
        err_msg = f"HTTPError — {res.status_code} Not Found for product ID 999"
        print(err_msg)
        log_error("lookup_product", err_msg)
        
    print("\n--- Contents of error_log.txt ---")
    log_content = read_file_safe("error_log.txt")
    if log_content:
        print(log_content)
        
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    task_1()
    task_2()
    task_3_A_B_D()
    task_4()
