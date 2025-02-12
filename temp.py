import pandas as pd

file = "data/2024c_year.txt"
# file = "data/2024dea_cit_txt_.txt"
# load in df

df = pd.read_csv(file)
print(df.head())

# keep only the columns we need Market_and_Exchange_Names
df = df[["Market_and_Exchange_Names"]]
# print unique values sorted
print(df["Market_and_Exchange_Names"].unique().sort())
# keep only the unique values and sort them
unique_values = df["Market_and_Exchange_Names"].unique()
unique_values.sort()

# save to a new file
output_file = "data/unique_market_and_exchange_names.txt"
with open(output_file, "w") as f:
    for value in unique_values:
        f.write(f"{value}\n")
