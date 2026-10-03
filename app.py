import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random

print("=== EDA RETAIL SALES PROJECT - TASK 1 ===")

# 1. DATA CREATE
np.random.seed(42)
n = 1000
categories = ['Furniture', 'Office Supplies', 'Technology']
sub_cats = {
    'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
    'Office Supplies': ['Paper', 'Storage', 'Binders', 'Art', 'Appliances'],
    'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers']
}
regions = ['West', 'East', 'Central', 'South']

data = []
start_date = datetime(2022, 1, 1)
for i in range(n):
    cat = random.choice(categories)
    sales = round(np.random.uniform(20, 1500), 2)
    profit = round(sales * np.random.uniform(-0.1, 0.4), 2)
    data.append({
        'Order Date': start_date + timedelta(days=random.randint(0, 900)),
        'Category': cat,
        'Sub-Category': random.choice(sub_cats[cat]),
        'Region': random.choice(regions),
        'Sales': sales,
        'Profit': profit,
        'Quantity': random.randint(1, 10),
        'Discount': random.choice([0, 0.1, 0.2])
    })

df = pd.DataFrame(data)
print(f"Data Created: {df.shape}")
print(df.head())

# 2. CHART 1: MONTHLY SALES TREND
df['Month'] = pd.to_datetime(df['Order Date']).dt.to_period('M').astype(str)
monthly = df.groupby('Month')['Sales'].sum().reset_index()

plt.figure(figsize=(12,5))
plt.plot(monthly['Month'], monthly['Sales'], marker='o', color='b')
plt.title('Monthly Sales Trend - Retail', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. CHART 2: TOP 10 SUB-CATEGORY
top_sub = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(10,5))
sns.barplot(x='Sales', y='Sub-Category', data=top_sub, palette='viridis')
plt.title('Top 10 Sub-Categories by Sales', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# 4. CHART 3: CORRELATION HEATMAP
plt.figure(figsize=(6,5))
corr = df[['Sales','Profit','Quantity','Discount']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1)
plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# 5. INSIGHTS
print("\n--- KEY INSIGHTS ---")
print(f"Total Sales: ${df['Sales'].sum():.2f}")
print(f"Total Profit: ${df['Profit'].sum():.2f}")
print(f"Best Region: {df.groupby('Region')['Sales'].sum().idxmax()}")
print(f"Best Category: {df.groupby('Category')['Sales'].sum().idxmax()}")
print("\nTASK 1 COMPLETED!")