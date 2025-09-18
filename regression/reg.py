import pandas as pd

# Create a small dataset
data = {
    "Size": [8, 12, 16, 20, 8, 12, 16, 20],
    "Brand": ["A", "A", "A", "A", "B", "B", "B", "B"],
    "Category": ["Soda", "Soda", "Soda", "Soda", "Juice", "Juice", "Juice", "Juice"],
    "Price": [1.49, 1.99, 2.49, 2.89, 1.79, 2.19, 2.59, 2.99]
}

df = pd.DataFrame(data)
print(df)


df_encoded = pd.get_dummies(df, columns=["Brand", "Category"], drop_first=True)
print(df_encoded)
