import pandas as pd
import numpy as np
import random
from faker import Faker

# Initialize Faker to generate random data
fake = Faker()

# Set the seed for reproducibility
random.seed(0)
np.random.seed(0)

# Define parameters
num_rows = 10000
products = [
    "Carbonated Water - Orange",
    "Artichoke - Fresh",
    "Soup - Campbells Chili Veg",
    "Pork Loin Bine - In Frenched",
    "Calvados - Boulard",
    "Cookies Almond Hazelnut",
    "Cheese - Pied De Vents",
    "Sea Bass - Fillets",
    "Soup - Knorr, Ministrone",
    "Venison - Denver Leg Boneless",
    "Pork Salted Bellies",
    "Roe - Flying Fish",
    "Onion Powder",
    "Sole - Fillet",
    "Ostrich - Prime Cut",
    "Pie Shell - 5",
    "Clams - Littleneck, Whole",
    "Cucumber - English",
    "Beef - Tongue, Cooked",
    "Lobster - Tail 6 Oz"
]

# Generate unique product IDs
product_ids = [fake.bothify(text='PROD-#####-??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(len(products))]

# Create a mapping from product_id to product_name
product_mapping = dict(zip(product_ids, products))

# Set up the list of product IDs for the data
all_product_ids = [random.choice(product_ids) for _ in range(num_rows)]

# Generate the data
data = {
    'order_id': [fake.bothify(text='order-#####-??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(num_rows)],
    'customer_id': [f'Customer_{random.randint(1, 100)}' for _ in range(num_rows)],
    'order_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_rows)],
    'product_id': all_product_ids,
    'product_name': [product_mapping[pid] for pid in all_product_ids],
    'product_price': [round(random.uniform(5.0, 100.0),2) for _ in range(num_rows)],  # Use a uniform price for simplicity
    'quantity': [random.randint(1, 5) for _ in range(num_rows)]
}

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('orders.csv', index=False)

print("Created and saved to 'orders.csv'.")
