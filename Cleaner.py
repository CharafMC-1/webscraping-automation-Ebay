import pandas as pd

df = pd.read_csv("ebay_tech_deals.csv", dtype=str)

for col in ["price", "Original_Price"]:
    df[col] = df[col].str.replace("US", "", regex=False)
    df[col] = df[col].str.replace("$", "", regex=False)
    df[col] = df[col].str.replace(",", "", regex=False)
    df[col] = df[col].str.strip()

df["Original_Price"] = df["Original_Price"].replace(
    ["NA", "N/A", "", None], pd.NA)
df["Original_Price"].fillna(df["price"], inplace=True)

df["Shipping_Info"] = df["Shipping_Info"].fillna("Shipping info unavailable")
df["Shipping_Info"] = df["Shipping_Info"].replace(
    ["N/A", "NA", "", " "], "Shipping info unavailable"
)
df["Shipping_Info"] = df["Shipping_Info"].str.strip()
df.loc[df["Shipping_Info"] == "", "Shipping_Info"] = "Shipping info unavailable"

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["Original_Price"] = pd.to_numeric(df["Original_Price"], errors="coerce")

df["discount_percentage"] = (
    (1 - (df["price"] / df["Original_Price"])) * 100).round(2)
df.loc[df["Original_Price"] == 0, "discount_percentage"] = 0

mask = (df["Title"].str.lower() == "unknown") & (
    df["price"].isin(df.loc[df["Title"].str.lower() != "unknown", "price"])
)
df = df[~mask]

df.to_csv("cleaned_ebay_deals.csv", index=False)

print("Cleaned data saved as cleaned_ebay_deals.csv")
