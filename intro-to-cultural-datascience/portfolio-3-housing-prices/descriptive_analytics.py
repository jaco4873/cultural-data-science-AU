import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the housing data
df = pd.read_csv("data/lejemaal.csv")

# Create folders for our outputs
os.makedirs("output/statistics", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# These are the main numerical features we'll analyze
numerical_columns = [
    "rooms",
    "area",
    "deposit",
    "net_rent",
    "gross_rent",
    "net_price_per_sqm",
    "gross_price_per_sqm",
]

# Export basic stats for our numerical columns
numerical_stats = df[numerical_columns].describe()
numerical_stats.to_csv("output/statistics/numerical_statistics.csv")

# Plot rent distribution and room analysis
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Left plot: How net rent is distributed (excluding outliers above 12000 DKK)
rent_data = df[df["net_rent"] <= 12000]["net_rent"]
axes[0].hist(rent_data, bins=30, edgecolor="black")
axes[0].set_title("Distribution of Net Rent")
axes[0].set_xlabel("Net Rent (DKK)")
axes[0].set_ylabel("Frequency")

# Right plot: How rent varies by number of rooms
room_numbers = sorted(df["rooms"].unique())
room_rents = [df[df["rooms"] == room]["net_rent"] for room in room_numbers]
axes[1].boxplot(room_rents, labels=room_numbers)
axes[1].set_title("Net Rent by Number of Rooms")
axes[1].set_xlabel("Number of Rooms")
axes[1].set_ylabel("Net Rent (DKK)")

plt.tight_layout()
plt.savefig("output/plots/net_rent_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

# Analyze relationship between area and rent
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Left plot: Area vs Gross Rent (filtered for better visualization)
filtered_df = df[(df["area"] <= 200) & (df["gross_rent"] <= 15000)]
scatter = axes[0].scatter(
    filtered_df["area"],
    filtered_df["gross_rent"],
    c=filtered_df["rooms"],
    cmap="viridis",
    alpha=0.6,
)
axes[0].set_title("Area vs Gross Rent")
axes[0].set_xlabel("Area (m²)")
axes[0].set_ylabel("Gross Rent (DKK)")
axes[0].set_xlim(0, 200)
axes[0].set_ylim(0, 15000)
plt.colorbar(scatter, ax=axes[0], label="Number of Rooms")

# Right plot: Area vs Net Rent
filtered_df = df[(df["area"] <= 200) & (df["net_rent"] <= 15000)]
scatter = axes[1].scatter(
    filtered_df["area"],
    filtered_df["net_rent"],
    c=filtered_df["rooms"],
    cmap="viridis",
    alpha=0.6,
)
axes[1].set_title("Area vs Net Rent")
axes[1].set_xlabel("Area (m²)")
axes[1].set_ylabel("Net Rent (DKK)")
axes[1].set_xlim(0, 200)
axes[1].set_ylim(0, 15000)
plt.colorbar(scatter, ax=axes[1], label="Number of Rooms")

plt.tight_layout()
plt.savefig("output/plots/area_vs_rent.png", dpi=300, bbox_inches="tight")
plt.close()

# Create correlation matrix for numerical features
correlation_matrix = df[numerical_columns].corr()

fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(correlation_matrix, cmap="coolwarm", aspect="auto")
plt.colorbar(im)

# Add correlation values to the heatmap
for i in range(len(numerical_columns)):
    for j in range(len(numerical_columns)):
        text = ax.text(
            j, i, f"{correlation_matrix.iloc[i, j]:.2f}", ha="center", va="center"
        )

ax.set_xticks(range(len(numerical_columns)))
ax.set_yticks(range(len(numerical_columns)))
ax.set_xticklabels(numerical_columns, rotation=45)
ax.set_yticklabels(numerical_columns)
plt.title("Correlation Matrix of Numerical Variables")
plt.tight_layout()
plt.savefig("output/plots/correlation_matrix.png", dpi=300, bbox_inches="tight")
plt.close()

# Plot geographical distribution of properties
plt.figure(figsize=(12, 6))
city_counts = df["city"].value_counts()
plt.bar(city_counts.index, city_counts.values)
plt.title("Distribution of Properties by City")
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Number of Properties")
plt.tight_layout()
plt.savefig("output/plots/city_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

# Analyze price variations by postal code
plt.figure(figsize=(12, 6))
postal_codes = sorted(df["postal_code"].unique())
postal_prices = [
    df[df["postal_code"] == code]["net_price_per_sqm"] for code in postal_codes
]
plt.boxplot(postal_prices, labels=postal_codes)
plt.title("Price per m² by Postal Code")
plt.xticks(rotation=45)
plt.xlabel("Postal Code")
plt.ylabel("Net Price per m²")
plt.tight_layout()
plt.savefig("output/plots/price_by_postal_code.png", dpi=300, bbox_inches="tight")
plt.close()

# Plot property type distributions
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Left: Types of apartments
apartment_counts = df["apartment_type"].value_counts()
axes[0].bar(apartment_counts.index, apartment_counts.values)
axes[0].set_title("Distribution of Apartment Types")
axes[0].set_xlabel("Apartment Type")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis="x", rotation=45)

# Right: Room count distribution
room_counts = df["rooms"].value_counts().sort_index()
axes[1].bar(room_counts.index, room_counts.values)
axes[1].set_title("Distribution of Number of Rooms")
axes[1].set_xlabel("Number of Rooms")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.savefig("output/plots/descriptive_statistics.png", dpi=300, bbox_inches="tight")
plt.close()

# Analyze rent statistics by city
plt.figure(figsize=(12, 6))
city_stats = df.groupby("city")["gross_rent"].agg(["mean", "median", "std"]).round(2)
x = range(len(city_stats.index))
width = 0.25

plt.bar(
    [i - width for i in x], city_stats["mean"], width, label="Mean Rent", color="blue"
)
plt.bar(x, city_stats["median"], width, label="Median Rent", color="green")
plt.bar([i + width for i in x], city_stats["std"], width, label="Std Dev", color="red")
plt.title("Rent Statistics by City")
plt.xticks(x, city_stats.index, rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("output/plots/city_rent_statistics.png", dpi=300, bbox_inches="tight")
plt.close()

# Compare net and gross rent across postal codes
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Left: Average net rent by postal code
postal_net = df.groupby("postal_code")["net_rent"].mean().sort_index()
axes[0].bar(postal_net.index, postal_net.values)
axes[0].set_title("Mean Net Rent by Postal Code")
axes[0].set_xlabel("Postal Code")
axes[0].set_ylabel("Mean Net Rent (DKK)")
axes[0].tick_params(axis="x", rotation=45)

# Right: Average gross rent by postal code
postal_gross = df.groupby("postal_code")["gross_rent"].mean().sort_index()
axes[1].bar(postal_gross.index, postal_gross.values)
axes[1].set_title("Mean Gross Rent by Postal Code")
axes[1].set_xlabel("Postal Code")
axes[1].set_ylabel("Mean Gross Rent (DKK)")
axes[1].tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig("output/plots/mean_rents_by_postal_code.png", dpi=300, bbox_inches="tight")
plt.close()