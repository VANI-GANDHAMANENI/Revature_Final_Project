import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r"F:\Revature_Project\data\final_financial_data.csv"  # Ensure correct path
df = pd.read_csv(file_path)

# Convert column names to lowercase and replace spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Drop rows where essential columns are missing
df.dropna(subset=['year', 'revenue', 'net_income_x', 'company'], inplace=True)

# Convert 'year' column to integer (if it's stored as a string)
df['year'] = df['year'].astype(int)

# Set seaborn style
sns.set_style("whitegrid")

# 1. Revenue vs. Net Income over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='year', y='revenue', hue='company', marker='o')
sns.lineplot(data=df, x='year', y='net_income_x', hue='company', marker='s', linestyle='--')
plt.title("Revenue vs. Net Income Over Time")
plt.xlabel("Year")
plt.ylabel("Amount (in millions)")
plt.legend(title="Company")
plt.savefig("revenue_vs_net_income.png")  # Save as image

# 2. Market Cap Comparison by Company
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='company', y='market_cap(in_b_usd)', palette='coolwarm')
plt.xticks(rotation=45)
plt.title("Market Capitalization by Company")
plt.xlabel("Company")
plt.ylabel("Market Cap (in billion USD)")
plt.savefig("market_cap_comparison.png")

# 3. EBITDA vs. Net Income (Profitability)
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x='ebitda_x', y='net_income_x', hue='company', size='revenue', palette='viridis', sizes=(20, 200))
plt.title("EBITDA vs. Net Income (Profitability)")
plt.xlabel("EBITDA")
plt.ylabel("Net Income")
plt.savefig("ebitda_vs_net_income.png")

# 4. Debt-to-Equity Ratio Analysis
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='company', y='debt/equity_ratio', palette='muted')
plt.xticks(rotation=45)
plt.title("Debt-to-Equity Ratio by Company")
plt.xlabel("Company")
plt.ylabel("Debt-to-Equity Ratio")
plt.savefig("debt_to_equity_ratio.png")

# 5. Free Cash Flow Trends
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='year', y='free_cash_flow', hue='company', marker='o')
plt.title("Free Cash Flow Over Time")
plt.xlabel("Year")
plt.ylabel("Free Cash Flow")
plt.savefig("free_cash_flow_trends.png")

print("✅ Plots saved successfully!")
