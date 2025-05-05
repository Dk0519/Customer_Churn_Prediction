import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta, date
import os

# Initialize Faker
fake = Faker()

# Create output directory
output_dir = "genrated_dataset"
os.makedirs(output_dir, exist_ok=True)

# 1. Generate customers.csv
num_customers = 1000
customers = []
for i in range(num_customers):
    customers.append({
        "customer_id": f"C{1000+i}",
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "signup_date": fake.date_between(start_date=date(2021, 1, 1), end_date=date(2023, 1, 1))
    })
customers_df = pd.DataFrame(customers)
customers_df.to_csv(f"{output_dir}/customers.csv", index=False)

# 2. Generate products.csv
categories = ["Electronics", "Fashion", "Books", "Grocery", "Beauty", "Fitness"]
num_products = 50
products = []
for i in range(num_products):
    category = random.choice(categories)
    products.append({
        "product_id": f"P{2000+i}",
        "product_name": f"{category}_{fake.word().capitalize()}",
        "category": category,
        "unit_price": round(random.uniform(100, 5000), 2)
    })
products_df = pd.DataFrame(products)
products_df.to_csv(f"{output_dir}/products.csv", index=False)

# 3. Generate sales_data.csv
num_sales = 10000
sales = []
for _ in range(num_sales):
    cust = random.choice(customers)
    prod = random.choice(products)
    order_date = fake.date_between(start_date=date(2022, 1, 1), end_date=date(2023, 12, 31))
    quantity = random.randint(1, 4)
    discount = round(random.uniform(0, 300), 2)
    sales.append({
        "customer_id": cust['customer_id'],
        "order_date": order_date,
        "product_id": prod['product_id'],
        "unit_price": prod['unit_price'],
        "quantity": quantity,
        "total_discount": discount
    })
sales_df = pd.DataFrame(sales)
sales_df.to_csv(f"{output_dir}/sales_data.csv", index=False)

print("✅ All 3 datasets successfully generated in folder:", output_dir)
