#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create advanced plots directory if it doesn't exist
if not os.path.exists('advanced_plots'):
    os.makedirs('advanced_plots')

# Load the data
print("Loading sales data...")
df = pd.read_csv('Sales_Data.csv')

# Data preprocessing
print("Preprocessing data...")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['Month_Name'] = df['Date'].dt.strftime('%b')
df['Revenue'] = df['Sales'] * df['Quantity']

# ------------------------------------------
# 1. CUSTOMER PURCHASE ANALYSIS
# ------------------------------------------
print("\n--- CUSTOMER PURCHASE ANALYSIS ---")

# Calculate customer metrics
customer_analysis = df.groupby('Customer_ID').agg({
    'Revenue': ['sum', 'mean'],
    'Date': ['min', 'max', 'count']
}).reset_index()

# Flatten the multi-index columns
customer_analysis.columns = ['Customer_ID', 'Total_Revenue', 'Avg_Order_Value', 
                            'First_Purchase', 'Last_Purchase', 'Purchase_Count']

# Calculate days since first purchase and purchase frequency
latest_date = df['Date'].max()
customer_analysis['Days_as_Customer'] = (latest_date - customer_analysis['First_Purchase']).dt.days
customer_analysis['Purchase_Frequency'] = customer_analysis['Purchase_Count'] / customer_analysis['Days_as_Customer']
customer_analysis['Purchase_Frequency'] = customer_analysis['Purchase_Frequency'].replace([np.inf, -np.inf], 0)

# Get top customers
top_customers = customer_analysis.sort_values('Total_Revenue', ascending=False).head(10)

print(f"Total unique customers: {len(customer_analysis)}")
print(f"Average customer lifetime value: ${customer_analysis['Total_Revenue'].mean():,.2f}")
print(f"Average purchase frequency: {customer_analysis['Purchase_Frequency'].mean():.4f} purchases per day")

# Plot top customers by revenue
plt.figure(figsize=(12, 6))
plt.bar(top_customers['Customer_ID'].astype(str), top_customers['Total_Revenue'])
plt.title('Top 10 Customers by Revenue', fontsize=16)
plt.xlabel('Customer ID', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('advanced_plots/top_customers.png')
plt.close()

# Plot purchase frequency distribution
plt.figure(figsize=(10, 6))
plt.hist(customer_analysis['Purchase_Count'], bins=20, alpha=0.7, edgecolor='black')
plt.title('Distribution of Customer Purchase Count', fontsize=16)
plt.xlabel('Number of Purchases', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('advanced_plots/purchase_count_distribution.png')
plt.close()

# ------------------------------------------
# 2. PRODUCT PERFORMANCE OVER TIME
# ------------------------------------------
print("\n--- PRODUCT PERFORMANCE OVER TIME ---")

# Analyze product performance by month
product_monthly = df.groupby(['Product', 'Year', 'Month'])['Revenue'].sum().reset_index()
product_monthly['YearMonth'] = product_monthly['Year'].astype(str) + '-' + product_monthly['Month'].astype(str).str.zfill(2)

# Get the top 3 products
top_products = df.groupby('Product')['Revenue'].sum().sort_values(ascending=False).head(3).index.tolist()

# Filter to only include the top products
top_product_monthly = product_monthly[product_monthly['Product'].isin(top_products)]

# Plot the revenue trend for top products
plt.figure(figsize=(14, 7))
for product in top_products:
    product_data = top_product_monthly[top_product_monthly['Product'] == product]
    product_data = product_data.sort_values('YearMonth')
    plt.plot(product_data['YearMonth'], product_data['Revenue'], marker='o', label=product)

plt.title('Monthly Revenue for Top 3 Products', fontsize=16)
plt.xlabel('Year-Month', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.xticks(rotation=90)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('advanced_plots/top_products_trend.png')
plt.close()

# Calculate product growth rate (comparing first and second half of the data)
median_date = df['Date'].median()
first_half = df[df['Date'] < median_date].groupby('Product')['Revenue'].sum().reset_index()
first_half = first_half.rename(columns={'Revenue': 'First_Half_Revenue'})

second_half = df[df['Date'] >= median_date].groupby('Product')['Revenue'].sum().reset_index()
second_half = second_half.rename(columns={'Revenue': 'Second_Half_Revenue'})

product_growth = pd.merge(first_half, second_half, on='Product')
product_growth['Growth_Rate'] = (product_growth['Second_Half_Revenue'] - product_growth['First_Half_Revenue']) / product_growth['First_Half_Revenue']
product_growth = product_growth.sort_values('Growth_Rate', ascending=False)

print("Top 5 products by growth rate:")
for i, (_, row) in enumerate(product_growth.head(5).iterrows(), 1):
    print(f"{i}. {row['Product']}: {row['Growth_Rate']:.2%}")

print("\nBottom 5 products by growth rate:")
for i, (_, row) in enumerate(product_growth.tail(5).iterrows(), 1):
    print(f"{i}. {row['Product']}: {row['Growth_Rate']:.2%}")

# Plot product growth rates
plt.figure(figsize=(12, 6))
plt.bar(product_growth.head(5)['Product'], product_growth.head(5)['Growth_Rate'])
plt.title('Top 5 Products by Growth Rate', fontsize=16)
plt.xlabel('Product', fontsize=12)
plt.ylabel('Growth Rate', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('advanced_plots/top_growth_products.png')
plt.close()

# ------------------------------------------
# 3. REGIONAL ANALYSIS
# ------------------------------------------
print("\n--- REGIONAL SALES ANALYSIS ---")

# Analyze sales by region and product
region_product = df.groupby(['Region', 'Product'])['Revenue'].sum().reset_index()
region_product_pivot = region_product.pivot_table(index='Region', columns='Product', values='Revenue')

# Calculate regional product preferences
regional_preferences = []
for region in df['Region'].unique():
    region_data = region_product[region_product['Region'] == region]
    top_product = region_data.loc[region_data['Revenue'].idxmax()]
    regional_preferences.append({
        'Region': region,
        'Top_Product': top_product['Product'],
        'Revenue': top_product['Revenue']
    })

regional_preferences_df = pd.DataFrame(regional_preferences)
print("Top product by region:")
for _, row in regional_preferences_df.iterrows():
    print(f"  {row['Region']}: {row['Top_Product']} (${row['Revenue']:,.2f})")

# Plot regional category distribution
region_category = df.groupby(['Region', 'Category'])['Revenue'].sum().reset_index()
regions = df['Region'].unique()
categories = df['Category'].unique()

plt.figure(figsize=(12, 8))

bar_width = 0.35
x = np.arange(len(regions))

for i, category in enumerate(categories):
    category_data = region_category[region_category['Category'] == category]
    category_values = [category_data[category_data['Region'] == region]['Revenue'].sum() for region in regions]
    plt.bar(x + i*bar_width, category_values, width=bar_width, label=category)

plt.title('Revenue by Region and Category', fontsize=16)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.xticks(x + bar_width/2, regions)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('advanced_plots/region_category_distribution.png')
plt.close()

# ------------------------------------------
# 4. SEASONAL PATTERNS
# ------------------------------------------
print("\n--- SEASONAL PATTERN ANALYSIS ---")

# Month-of-year analysis
monthly_pattern = df.groupby(['Month', 'Month_Name'])['Revenue'].sum().reset_index()
monthly_pattern = monthly_pattern.sort_values('Month')

plt.figure(figsize=(12, 6))
plt.bar(monthly_pattern['Month_Name'], monthly_pattern['Revenue'])
plt.title('Monthly Sales Seasonality', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('advanced_plots/monthly_seasonality.png')
plt.close()

# Category seasonality
category_month = df.groupby(['Category', 'Month', 'Month_Name'])['Revenue'].sum().reset_index()
categories = df['Category'].unique()

plt.figure(figsize=(14, 7))
for category in categories:
    category_data = category_month[category_month['Category'] == category]
    category_data = category_data.sort_values('Month')
    plt.plot(category_data['Month_Name'], category_data['Revenue'], marker='o', label=category)

plt.title('Category Sales by Month', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('advanced_plots/category_seasonality.png')
plt.close()

# Identify peak sales months by category
peak_months = []
for category in df['Category'].unique():
    category_data = category_month[category_month['Category'] == category]
    peak_month = category_data.loc[category_data['Revenue'].idxmax()]
    peak_months.append({
        'Category': category,
        'Peak_Month': peak_month['Month_Name'],
        'Peak_Revenue': peak_month['Revenue']
    })

peak_months_df = pd.DataFrame(peak_months)
print("Peak sales month by category:")
for _, row in peak_months_df.iterrows():
    print(f"  {row['Category']}: {row['Peak_Month']} (${row['Peak_Revenue']:,.2f})")

# ------------------------------------------
# 5. PRICE ANALYSIS
# ------------------------------------------
print("\n--- PRICE ANALYSIS ---")

# Calculate price points for each product
price_analysis = df.groupby(['Product', 'Sales'])['Quantity'].sum().reset_index()
price_analysis = price_analysis.sort_values(['Product', 'Sales'])

# Calculate price statistics by product
price_stats = df.groupby('Product')['Sales'].agg(['min', 'max', 'mean', 'std']).reset_index()
price_stats = price_stats.sort_values('mean', ascending=False)

print("Price ranges by product:")
for _, row in price_stats.head(5).iterrows():
    print(f"  {row['Product']}: ${row['min']:.2f} - ${row['max']:.2f} (avg: ${row['mean']:.2f})")

# Plot average prices by product
plt.figure(figsize=(12, 6))
plt.bar(price_stats['Product'], price_stats['mean'])
plt.title('Average Price by Product', fontsize=16)
plt.xlabel('Product', fontsize=12)
plt.ylabel('Average Price ($)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('advanced_plots/avg_product_prices.png')
plt.close()

# Plot price distribution for selected products (top 3)
selected_products = price_stats.head(3)['Product'].tolist()
selected_data = df[df['Product'].isin(selected_products)]

plt.figure(figsize=(14, 7))
for product in selected_products:
    product_data = selected_data[selected_data['Product'] == product]
    plt.hist(product_data['Sales'], bins=10, alpha=0.5, label=product)

plt.title('Price Distribution for Top 3 Products', fontsize=16)
plt.xlabel('Price ($)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('advanced_plots/price_distribution.png')
plt.close()

# Save key insights to file
with open('advanced_insights.txt', 'w') as f:
    f.write("ADVANCED SALES ANALYSIS INSIGHTS\n")
    f.write("================================\n\n")
    
    f.write("1. CUSTOMER INSIGHTS\n")
    f.write("-------------------\n")
    f.write(f"Total unique customers: {len(customer_analysis)}\n")
    f.write(f"Average customer lifetime value: ${customer_analysis['Total_Revenue'].mean():,.2f}\n")
    f.write(f"Average purchase frequency: {customer_analysis['Purchase_Frequency'].mean():.4f} purchases per day\n\n")
    
    f.write("Top 3 customers by revenue:\n")
    for i, (_, row) in enumerate(top_customers.head(3).iterrows(), 1):
        f.write(f"  {i}. Customer {row['Customer_ID']}: ${row['Total_Revenue']:,.2f}\n")
    f.write("\n")
    
    f.write("2. PRODUCT PERFORMANCE\n")
    f.write("---------------------\n")
    f.write("Top 5 products by growth rate:\n")
    for i, (_, row) in enumerate(product_growth.head(5).iterrows(), 1):
        f.write(f"  {i}. {row['Product']}: {row['Growth_Rate']:.2%}\n")
    f.write("\n")
    
    f.write("3. REGIONAL INSIGHTS\n")
    f.write("-------------------\n")
    f.write("Top product by region:\n")
    for _, row in regional_preferences_df.iterrows():
        f.write(f"  {row['Region']}: {row['Top_Product']} (${row['Revenue']:,.2f})\n")
    f.write("\n")
    
    f.write("4. SEASONAL PATTERNS\n")
    f.write("-------------------\n")
    f.write("Peak sales month by category:\n")
    for _, row in peak_months_df.iterrows():
        f.write(f"  {row['Category']}: {row['Peak_Month']} (${row['Peak_Revenue']:,.2f})\n")
    f.write("\n")
    
    f.write("5. PRICE ANALYSIS\n")
    f.write("----------------\n")
    f.write("Price ranges by product (top 5 by average price):\n")
    for _, row in price_stats.head(5).iterrows():
        f.write(f"  {row['Product']}: ${row['min']:.2f} - ${row['max']:.2f} (avg: ${row['mean']:.2f})\n")

print("\nAdvanced analysis complete. Results saved to 'advanced_insights.txt' and plots saved to 'advanced_plots/' directory.")
print("To view the plots, open the files in the 'advanced_plots' folder.") 