#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create plots directory if it doesn't exist
if not os.path.exists('plots'):
    os.makedirs('plots')

# Load the data
print("Loading sales data...")
df = pd.read_csv('Sales_Data.csv')

# Data cleaning and preparation
print("Cleaning and preparing data...")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['Month_Name'] = df['Date'].dt.strftime('%b')
df['Revenue'] = df['Sales'] * df['Quantity']

# Create summary statistics
print("\n--- SUMMARY STATISTICS ---")
print(f"Total Revenue: ${df['Revenue'].sum():,.2f}")
print(f"Total Transactions: {df.shape[0]}")
print(f"Total Products Sold: {df['Quantity'].sum()}")
print(f"Average Order Value: ${df.groupby('Customer_ID')['Revenue'].mean().mean():,.2f}")

# Show data overview
print("\n--- DATA OVERVIEW ---")
print(df.head())

# 1. Monthly Sales Trend
print("\nGenerating monthly sales trend...")
monthly_sales = df.groupby(['Year', 'Month', 'Month_Name'])['Revenue'].sum().reset_index()
pivot_table = monthly_sales.pivot_table(index='Month', columns='Year', values='Revenue')

plt.figure(figsize=(12, 6))
for column in pivot_table.columns:
    plt.plot(pivot_table.index, pivot_table[column], marker='o', label=str(column))
plt.title('Monthly Sales Trend by Year', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Revenue', fontsize=12)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True, alpha=0.3)
plt.legend(title='Year')
plt.tight_layout()
plt.savefig('plots/monthly_sales_trend.png')
plt.close()

# 2. Product Category Analysis
print("Analyzing product categories...")
category_sales = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(10, 6))
plt.bar(category_sales['Category'], category_sales['Revenue'])
plt.title('Revenue by Product Category', fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Revenue', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plots/category_sales.png')
plt.close()

# 3. Top 5 Products by Revenue
print("Identifying top products...")
product_sales = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).reset_index()
top_5_products = product_sales.head(5)

plt.figure(figsize=(10, 6))
plt.barh(top_5_products['Product'], top_5_products['Revenue'])
plt.title('Top 5 Products by Revenue', fontsize=16)
plt.xlabel('Total Revenue', fontsize=12)
plt.ylabel('Product', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plots/top_5_products.png')
plt.close()

# 4. Regional Sales Distribution
print("Analyzing regional sales...")
region_sales = df.groupby('Region')['Revenue'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(region_sales['Region'], region_sales['Revenue'])
plt.title('Revenue by Region', fontsize=16)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Total Revenue', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plots/region_sales.png')
plt.close()

# 5. Sales Quantity Distribution
plt.figure(figsize=(10, 6))
plt.hist(df['Quantity'], bins=20, alpha=0.7, edgecolor='black')
plt.title('Distribution of Sales Quantity', fontsize=16)
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plots/quantity_distribution.png')
plt.close()

# 6. Sales vs Quantity Scatter Plot
plt.figure(figsize=(10, 6))
categories = df['Category'].unique()
colors = ['blue', 'orange']
for i, category in enumerate(categories):
    subset = df[df['Category'] == category]
    plt.scatter(subset['Sales'], subset['Quantity'], alpha=0.5, label=category, color=colors[i % len(colors)])
plt.title('Relationship between Sales Price and Quantity', fontsize=16)
plt.xlabel('Sales Price', fontsize=12)
plt.ylabel('Quantity', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('plots/sales_quantity_scatter.png')
plt.close()

# Generate key insights
print("\n--- KEY INSIGHTS ---")

# Monthly revenue trend
monthly_revenue = df.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
max_revenue_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmax()]
print(f"Peak sales month: Year {max_revenue_month['Year']}, Month {max_revenue_month['Month']}")

# Best selling products
best_selling_product = product_sales.iloc[0]
print(f"Best-selling product: {best_selling_product['Product']} (Revenue: ${best_selling_product['Revenue']:,.2f})")

# Most profitable category
best_category = category_sales.iloc[0]
print(f"Most profitable category: {best_category['Category']} (Revenue: ${best_category['Revenue']:,.2f})")

# Best performing region
best_region = region_sales.loc[region_sales['Revenue'].idxmax()]
print(f"Best performing region: {best_region['Region']} (Revenue: ${best_region['Revenue']:,.2f})")

print("\nAnalysis complete. Plots saved to 'plots/' directory.")
print("To view the plots, open the files in the 'plots' folder.")
print("\nPlease press Ctrl+C to exit...") 