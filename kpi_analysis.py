import pandas as pd
import os

# -------------------------------
# 1. LOAD DATA (WITH FIX)
# -------------------------------

file_path = "data.csv"

try:
    # Check if file exists and not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        df = pd.read_csv(file_path)
        print("✅ Loaded data from CSV file")
    else:
        raise ValueError("File is empty or missing")

except:
    print("⚠️ CSV file issue detected → using default dataset")

    # Default dataset (backup)
    data = {
        "customer_id": [1,1,2,2,3,3,4,5],
        "order_id": [101,102,103,104,105,106,107,108],
        "order_date": ["2024-01-01","2024-02-10","2024-01-05","2024-03-15",
                       "2024-02-20","2024-03-25","2024-03-01","2024-03-10"],
        "amount": [500,300,200,150,700,400,100,250],
        "status": ["completed","completed","completed","cancelled",
                   "completed","completed","completed","completed"]
    }

    df = pd.DataFrame(data)

# Convert date
df['order_date'] = pd.to_datetime(df['order_date'])

# Filter completed orders
df_completed = df[df['status'] == 'completed'].copy()

# -------------------------------
# 2. KPI CALCULATIONS
# -------------------------------

conversion_rate = len(df_completed) / len(df)
aov = df_completed['amount'].mean()

total_customers = df['customer_id'].nunique()
repeat_customers = df_completed['customer_id'].value_counts()
retained_customers = sum(repeat_customers > 1)
churn_rate = 1 - (retained_customers / total_customers)

# -------------------------------
# 3. PRINT KPI RESULTS
# -------------------------------
print("\n📊 KPI RESULTS")
print("---------------------------")
print(f"Conversion Rate: {conversion_rate:.2f}")
print(f"Average Order Value: ₹{aov:.2f}")
print(f"Churn Rate: {churn_rate:.2f}")

# -------------------------------
# 4. COHORT ANALYSIS
# -------------------------------

df_completed['month'] = df_completed['order_date'].dt.to_period('M')

df_completed['cohort'] = df_completed.groupby('customer_id')['order_date'] \
                                     .transform('min').dt.to_period('M')

cohort_data = df_completed.groupby(['cohort', 'month']) \
                          ['customer_id'].nunique().reset_index()

cohort_pivot = cohort_data.pivot(index='cohort',
                                columns='month',
                                values='customer_id')

# -------------------------------
# 5. PRINT COHORT
# -------------------------------
print("\n📈 COHORT ANALYSIS")
print("---------------------------")
print(cohort_pivot)

# -------------------------------
# 6. SAVE OUTPUT
# -------------------------------
cohort_pivot.to_csv("cohort_output.csv")

print("\n✅ Program executed successfully!")