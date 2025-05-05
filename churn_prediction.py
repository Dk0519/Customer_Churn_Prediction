import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load datasets
sales = pd.read_csv('sales_data.csv', parse_dates=['order_date'])
products = pd.read_csv('products.csv')
customers = pd.read_csv('customers.csv', parse_dates=['signup_date'])

# Revenue calculation
sales['revenue'] = sales['unit_price'] * sales['quantity'] - sales['total_discount']

# Aggregate customer metrics
agg = sales.groupby('customer_id').agg({
    'order_date': ['min', 'max', 'nunique'],
    'revenue': 'sum'
}).reset_index()
agg.columns = ['customer_id', 'first_order', 'last_order', 'order_count', 'total_spent']

# Churn label: No orders in last 30 days
ref_date = sales['order_date'].max()
agg['days_since_last_order'] = (ref_date - agg['last_order']).dt.days
agg['churn'] = (agg['days_since_last_order'] > 30).astype(int)

# Features and labels
X = agg[['order_count', 'total_spent', 'days_since_last_order']]
y = agg['churn']

# Model training
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluation
report = classification_report(y_test, y_pred)
with open("churn_report.txt", "w") as f:
    f.write(report)
print(report)
