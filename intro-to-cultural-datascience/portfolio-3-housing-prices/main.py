import pandas as pd


# Directory containing the HTML files
directory_path = 'data'  
# Get a sorted list of HTML files
data = pd.read_xml('data/lejemaal.xml')

# Rename columns to english
data.rename(columns={
    'LejemaalId': 'id',
    'AfdId': 'department_id',
    'SelId': 'company_id',
    'Adresse': 'address',
    'PostBy': 'postal_code_and_city',
    'Lejemaalstype': 'property_type',
    'Lejlighedstype': 'apartment_type',
    'Rum': 'rooms',
    'Areal': 'area',
    'BBRAreal': 'bbr_area',
    'Indskud': 'deposit',
    'NettoHusleje': 'net_rent',
    'BruttoHusleje': 'gross_rent'
}, inplace=True)

# Check for NA values in the dataset
na_counts = data.isna().sum()

# Print columns with NA values (if any)
if na_counts.any():
    print("\nColumns containing NA values:")
    print(na_counts[na_counts > 0])
else:
    print("\nNo NA values found in the dataset")

# Clean up numeric columns
numeric_columns = ['area', 'bbr_area', 'deposit', 'net_rent', 'gross_rent']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce').round(2)

# Calculate price per square meter
data['net_price_per_sqm'] = (data['net_rent'] / data['area']).round(2)
data['gross_price_per_sqm'] = (data['gross_rent'] / data['area']).round(2)

# Split PostBy into postal_code and city
data['postal_code'] = data['postal_code_and_city'].str.extract(r'(\d{4})')
data['city'] = data['postal_code_and_city'].str.extract(r'\d{4}\s+(.*)')

# Drop the original combined column if you don't need it
data = data.drop('postal_code_and_city', axis=1)

# Save the XML data to CSV
data.to_csv('data/lejemaal.csv', index=False)

