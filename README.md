# Retail Sales Data Analysis

This project analyzes retail sales data to identify trends, best-selling products, and peak sales months using Python. The analysis includes data cleaning, visualization, and insights generation.

## Project Overview

The project analyzes sales data from a retail business, providing insights on:
- Monthly sales trends
- Product category performance
- Top-selling products
- Regional sales distribution
- Price-quantity relationships
- Customer purchase patterns
- Seasonal patterns

## Dataset

The dataset `Sales_Data.csv` contains 500 sales records with the following fields:
- Date: The date of the sale
- Product: The product sold (e.g., Smartphone, Laptop, Tablet)
- Category: Product category (Electronics or Accessories)
- Sales: The sale price
- Quantity: The quantity sold
- Customer_ID: Unique customer identifier
- Region: Geographic region (North, South, East, West)

## Key Insights

From the analysis, we discovered:

- **Peak Sales Month**: February 2021 had the highest sales
- **Best-Selling Product**: Laptops generated the highest revenue ($2,293,786)
- **Most Profitable Category**: Electronics ($6,666,675)
- **Best Performing Region**: West ($3,662,253)
- **Average Order Value**: $25,572
- **Top Customer**: Customer ID 1020 with $627,536 in purchases
- **Fastest Growing Product**: Smartphone with 36.96% growth rate

## Files in this Project

- `Sales_Data.csv`: Original sales dataset
- `simple_dashboard.py`: Basic sales analysis script that generates visualizations and key metrics
- `simple_advanced_analysis.py`: Advanced analysis script for customer insights, product performance trends, and price analysis
- `advanced_insights.txt`: Text file containing key findings from the advanced analysis
- `plots/`: Directory containing basic visualizations
- `advanced_plots/`: Directory containing advanced analysis visualizations
- `run_analysis.bat`: Windows batch script for easy execution
- `run_analysis.sh`: Shell script for Linux/Mac for easy execution

## Setup and Installation

### Prerequisites

- Python 3.6+
- Required packages: pandas, numpy, matplotlib

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/retail-sales-analysis.git
cd retail-sales-analysis

# Install required packages
pip install -r requirements.txt
```

## Usage

### Running the Analysis

You can run the analysis in two ways:

1. **Using the run scripts** (easiest method):
   
   For Windows:
   ```
   run_analysis.bat
   ```
   
   For Linux/Mac:
   ```
   ./run_analysis.sh
   ```
   
   These scripts provide a menu to run either the basic analysis, advanced analysis, or both.

2. **Running scripts individually**:

### Basic Analysis

Run the basic analysis script to generate key metrics and visualizations:

```bash
python simple_dashboard.py
```

This script will:
1. Clean the sales data
2. Calculate key metrics
3. Create visualizations in the `plots/` directory
4. Display key insights in the console

### Advanced Analysis

Run the advanced analysis script for deeper insights:

```bash
python simple_advanced_analysis.py
```

This script will:
1. Perform customer segmentation analysis
2. Analyze product performance over time
3. Identify regional preferences
4. Examine seasonal patterns
5. Analyze product pricing
6. Save insights to `advanced_insights.txt`
7. Generate visualizations in `advanced_plots/` directory

## Visualizations

The analysis generates several visualizations across two directories:

### Basic Visualizations (`plots/`)

1. **Monthly Sales Trend**: Line chart showing revenue by month
2. **Product Category Analysis**: Bar chart of revenue by category
3. **Top 5 Products by Revenue**: Horizontal bar chart of top performers
4. **Regional Sales Distribution**: Bar chart of revenue by region
5. **Sales Quantity Distribution**: Histogram of quantity distribution
6. **Sales vs Quantity**: Scatter plot showing relationship between price and quantity

### Advanced Visualizations (`advanced_plots/`)

1. **Top Customers**: Bar chart of highest-spending customers
2. **Purchase Count Distribution**: Histogram of customer purchase frequency
3. **Top Products Trend**: Line chart of monthly revenue for top products
4. **Product Growth Rates**: Bar chart of fastest growing products
5. **Regional Category Distribution**: Grouped bar chart of category performance by region
6. **Monthly Seasonality**: Bar chart of sales by month
7. **Category Seasonality**: Line chart of category sales by month
8. **Average Product Prices**: Bar chart of product pricing
9. **Price Distribution**: Histogram of price points for top products

## Analysis Workflow

1. **Data Cleaning**:
   - Convert date to datetime format
   - Create additional features (month, year)
   - Calculate revenue (sales × quantity)

2. **Basic Analysis**:
   - Analyze sales trends over time
   - Identify top-performing products and categories
   - Examine regional performance

3. **Advanced Analysis**:
   - Calculate customer metrics and identify top customers
   - Analyze product performance and growth rates
   - Identify regional preferences
   - Examine seasonal patterns
   - Analyze product pricing

4. **Insights Generation**:
   - Generate key metrics and findings
   - Create visualizations for data exploration
   - Save insights to text files

## Further Development

Potential enhancements:
- Predictive analysis for sales forecasting
- Customer segmentation analysis
- Inventory optimization recommendations
- Anomaly detection for unusual sales patterns
- Marketing campaign performance correlation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
