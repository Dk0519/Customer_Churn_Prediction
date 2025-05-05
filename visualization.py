import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Load sales data
sales = pd.read_csv('genrated_dataset/sales_data.csv', parse_dates=['order_date'])
sales['revenue'] = sales['unit_price'] * sales['quantity'] - sales['total_discount']

# Aggregate metrics
agg = sales.groupby('customer_id').agg({
    'order_date': ['min', 'max', 'nunique'],
    'revenue': 'sum'
}).reset_index()
agg.columns = ['customer_id', 'first_order', 'last_order', 'order_count', 'total_spent']

# Churn label
ref_date = sales['order_date'].max()
agg['days_since_last_order'] = (ref_date - agg['last_order']).dt.days
agg['churn'] = (agg['days_since_last_order'] > 30).astype(int)

# Set seaborn theme
sns.set_theme(style="whitegrid")

# 1. Pie Chart of Churn Distribution
churn_counts = agg['churn'].value_counts()
labels = ['Active (0)', 'Churned (1)']
colors = ['#2ecc71', '#e74c3c']
plt.figure(figsize=(6, 6))
plt.pie(churn_counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=[0, 0.1])
plt.title("Customer Churn Distribution")
plt.show()

# 2. Histogram of Days Since Last Order by Churn
plt.figure(figsize=(8, 5))
sns.histplot(data=agg, x='days_since_last_order', hue='churn', multiple='stack', palette='Set1', bins=20)
plt.title("Days Since Last Order (Stacked by Churn)")
plt.xlabel("Days Since Last Order")
plt.ylabel("Number of Customers")
plt.show()

# 3. Total Spend by Churn Status (Violin Plot)
plt.figure(figsize=(8, 5))
sns.violinplot(x='churn', y='total_spent', data=agg, palette='Set2')
plt.title("Distribution of Total Spend by Churn Status")
plt.xlabel("Churn Status")
plt.ylabel("Total Spend")
plt.show()

# 4. Swarm Plot: Order Count vs Total Spent by Churn
plt.figure(figsize=(9, 6))
sns.scatterplot(data=agg, x='order_count', y='total_spent', hue='churn', palette='coolwarm', alpha=0.7)
plt.title("Customer Order Count vs Total Spend")
plt.xlabel("Order Count")
plt.ylabel("Total Spend")
plt.legend(title="Churn")
plt.show()

# 5. Correlation Heatmap
plt.figure(figsize=(6, 4))
corr = agg[['order_count', 'total_spent', 'days_since_last_order', 'churn']].corr()
sns.heatmap(corr, annot=True, cmap='RdBu', fmt=".2f", linewidths=0.5, square=True)
plt.title("Feature Correlation with Churn")
plt.tight_layout()
plt.show()
