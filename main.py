import pandas as pd
import csv
from dateutil.parser import parse
import seaborn as sns

import matplotlib.pyplot as plt

input_filename = "expenses.csv"

committees = set()

with open(input_filename, mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        committees.add(row['Commitee'])

for committee in sorted(committees):
    print(committee)

input_filename = input("Enter the name of the file you would like to analyze: ")

df = pd.read_csv(input_filename)

fall_budget = 0
spring_budget = 0

in_fall_events = False
in_spring_events = False

for index, row in df.iterrows():
    event_source = row['Event/Source']
    estimated_expenses = row['Estimated Expenses']

    if pd.notna(event_source):
        if 'Fall Events' in event_source:
            in_fall_events = True
            in_spring_events = False
        elif 'Spring Events' in event_source:
            in_fall_events = False
            in_spring_events = True

    if in_fall_events and pd.notna(estimated_expenses):
        try:
            fall_budget += float(estimated_expenses.replace('$', '').replace(',', ''))
        except ValueError:
            continue

    if in_spring_events and pd.notna(estimated_expenses):
        try:
            spring_budget += float(estimated_expenses.replace('$', '').replace(',', ''))
        except ValueError:
            continue

print(f"Fall Budget: {fall_budget}")
print(f"Spring Budget: {spring_budget}")

expenses_filename = "expenses.csv"
input_filename = input("Enter the name of the file you would like to analyze: ")

expenses_df = pd.read_csv(expenses_filename)
budgets_df = pd.read_csv(input_filename)

def parse_date(date_str):
    try:
        return parse(str(date_str)).date()
    except (ValueError, TypeError):
        return None

expenses_df['Date Input'] = expenses_df['Date Input'].apply(parse_date)
expenses_df = expenses_df.dropna(subset=['Date Input'])

expenses_df['Total Cost'] = pd.to_numeric(expenses_df['Total Cost'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce').fillna(0)

expenses_df_sorted = expenses_df.sort_values(by='Date Input')

committee_totals = expenses_df_sorted.groupby('Commitee')['Total Cost'].sum().reset_index()
committee_totals.columns = ['Committee', 'Total Cost']

print("Sorted Expenses DataFrame:")
print(expenses_df_sorted)

print("\nTotal Cost for each committee:")
print(committee_totals)

committee_totals.to_csv('committee_totals.csv', index=False)

expenses_df_sorted['Commitee'] = expenses_df_sorted['Commitee'].str.strip().str.lower()

committee = input("Please enter the committee name: ").strip().lower()
committee_expenses = expenses_df_sorted[expenses_df_sorted['Commitee'] == committee]

print(f"\nFiltered expenses for committee '{committee}':")
print(committee_expenses)

fall_expenses = committee_expenses[(committee_expenses['Date Input'].apply(lambda x: x.month in range(8, 12)))]
spring_expenses = committee_expenses[(committee_expenses['Date Input'].apply(lambda x: x.month in range(1, 8)))]

print(f"\nFall expenses for committee '{committee}':")
print(fall_expenses)
print(f"\nSpring expenses for committee '{committee}':")
print(spring_expenses)

total_fall_expenses = fall_expenses['Total Cost'].sum()
total_spring_expenses = spring_expenses['Total Cost'].sum()

fall_difference = fall_budget - total_fall_expenses
spring_difference = spring_budget - total_spring_expenses

fall_status = "Underspent" if fall_difference >= 0 else "Overspent"
spring_status = "Underspent" if spring_difference >= 0 else "Overspent"

fall_large_purchases = fall_expenses[fall_expenses['Total Cost'] > 500]
spring_large_purchases = spring_expenses[spring_expenses['Total Cost'] > 500]

print(f"Committee: {committee}")

print("\nFall Semester:")
print(f"Total Expenses: {total_fall_expenses:.2f}")
print(f"Budget: {fall_budget:.2f}")
print(f"Difference: {fall_difference:.2f} ({fall_status})")
print("Large Purchases:")
for purchase in fall_large_purchases.itertuples():
    print(f"- Description: {purchase.Description}, Total Cost: {purchase._3:.2f}, Comments: {purchase.Comments}")

print("\nSpring Semester:")
print(f"Total Expenses: {total_spring_expenses:.2f}")
print(f"Budget: {spring_budget:.2f}")
print(f"Difference: {spring_difference:.2f} ({spring_status})")
print("Large Purchases:")
for purchase in spring_large_purchases.itertuples():
    print(f"- Description: {purchase.Description}, Total Cost: {purchase._3:.2f}, Comments: {purchase.Comments}")

sns.set(style="whitegrid")

committee_totals = committee_totals.sort_values(by='Total Cost', ascending=False)

plt.figure(figsize=(10, 8))
plt.pie(committee_totals['Total Cost'], colors=sns.color_palette("pastel", len(committee_totals)), startangle=140)
plt.title('Spending Distribution Among Committees')
plt.axis('equal')

labels = [f'{c} ({p:.1f}%)' for c, p in zip(committee_totals['Committee'], (committee_totals['Total Cost'] / committee_totals['Total Cost'].sum()) * 100)]
plt.legend(labels, loc='upper left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig('committee_spending_distribution.png')
plt.show()

committee = input("Please enter the committee name: ").strip().lower()
committee_expenses = expenses_df_sorted[expenses_df_sorted['Commitee'] == committee]

fall_expenses = committee_expenses[(committee_expenses['Date Input'].apply(lambda x: x.month in range(8, 12)))]
spring_expenses = committee_expenses[(committee_expenses['Date Input'].apply(lambda x: x.month in range(1, 8)))]

total_fall_expenses = fall_expenses['Total Cost'].sum()
total_spring_expenses = spring_expenses['Total Cost'].sum()

fall_difference = fall_budget - total_fall_expenses
spring_difference = spring_budget - total_spring_expenses

fall_status = "Underspent" if fall_difference >= 0 else "Overspent"
spring_status = "Underspent" if spring_difference >= 0 else "Overspent"

fall_large_purchases = fall_expenses[fall_expenses['Total Cost'] > 500]
spring_large_purchases = spring_expenses[spring_expenses['Total Cost'] > 500]

fall_utilized = (total_fall_expenses / fall_budget) * 100 if fall_budget != 0 else 0
spring_utilized = (total_spring_expenses / spring_budget) * 100 if spring_budget != 0 else 0

plt.figure(figsize=(10, 8))
budgets = {'Fall Budget': fall_budget, 'Spring Budget': spring_budget}
actual_spending = {'Fall Expenses': total_fall_expenses, 'Spring Expenses': total_spring_expenses}
percent_utilized = {'Fall Utilized (%)': fall_utilized, 'Spring Utilized (%)': spring_utilized}

labels = list(budgets.keys())
budget_values = list(budgets.values())
spending_values = list(actual_spending.values())
utilized_values = list(percent_utilized.values())

x = range(len(labels))

plt.bar(x, budget_values, width=0.4, label='Budget', color='#FF6D00', align='center')
plt.bar(x, spending_values, width=0.4, label='Actual Spending', color='#0033A0', align='edge')
for i, v in enumerate(utilized_values):
    plt.text(i - 0.15, budget_values[i] + 50, f'{v:.1f}%', color='black', fontweight='bold')
plt.xlabel('Semester')
plt.ylabel('Amount ($)')
plt.title(f'Actual Spending vs. Budget for {committee.capitalize()} Committee')
plt.xticks(x, labels)
plt.legend()
plt.tight_layout()
plt.savefig('actual_spending_vs_budget.png')
plt.show()

print(f"Committee: {committee}")

print("\nFall Semester:")
print(f"Total Expenses: {total_fall_expenses:.2f}")
print(f"Budget: {fall_budget:.2f}")
print(f"Difference: {fall_difference:.2f} ({fall_status})")
print("Large Purchases:")
for purchase in fall_large_purchases.itertuples():
    print(f"- Description: {purchase.Description}, Total Cost: {purchase._3:.2f}, Comments: {purchase.Comments}")

print("\nSpring Semester:")
print(f"Total Expenses: {total_spring_expenses:.2f}")
print(f"Budget: {spring_budget:.2f}")
print(f"Difference: {spring_difference:.2f} ({spring_status})")
print("Large Purchases:")
for purchase in spring_large_purchases.itertuples():
    print(f"- Description: {purchase.Description}, Total Cost: {purchase._3:.2f}, Comments: {purchase.Comments}")

def plot_cumulative_expenses_over_time(expenses_df_sorted, exclude_national=False, threshold_quantile=0.75):
    if exclude_national:
        filtered_expenses = expenses_df_sorted[expenses_df_sorted['Commitee'].str.lower() != 'nationals']
    else:
        filtered_expenses = expenses_df_sorted

    filtered_expenses = filtered_expenses.sort_values(by='Date Input')

    filtered_expenses['Cumulative Total'] = filtered_expenses['Total Cost'].cumsum()

    plt.figure(figsize=(14, 8))
    plt.plot(filtered_expenses['Date Input'], filtered_expenses['Cumulative Total'], marker='o', color='b', label='Cumulative Total')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Total Cost ($)')
    if exclude_national:
        plt.title('Cumulative Expenses Over Time for All Committees (Excluding National)')
    else:
        plt.title('Cumulative Expenses Over Time for All Committees (With National)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_cumulative_expenses_over_time(expenses_df_sorted, exclude_national=False, threshold_quantile=0.95)
plot_cumulative_expenses_over_time(expenses_df_sorted, exclude_national=True, threshold_quantile=0.95)

def create_spending_heat_map(expenses_df_sorted, exclude_national=False):
    if exclude_national:
        filtered_expenses = expenses_df_sorted[expenses_df_sorted['Commitee'].str.lower() != 'nationals']
    else:
        filtered_expenses = expenses_df_sorted

    filtered_expenses['Date Input'] = pd.to_datetime(filtered_expenses['Date Input'])

    filtered_expenses['Year'] = filtered_expenses['Date Input'].dt.year
    filtered_expenses['Month'] = filtered_expenses['Date Input'].dt.month

    aggregated_expenses = filtered_expenses.groupby(['Year', 'Month']).agg({'Total Cost': 'sum'}).reset_index()

    pivot_table = aggregated_expenses.pivot_table(index='Month', columns='Year', values='Total Cost', fill_value=0)

    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".2f", linewidths=.5)
    plt.xlabel('Year')
    plt.ylabel('Month')
    if exclude_national:
        plt.title('Heat Map of Spending Over Time (Excluding National)')
    else:
        plt.title('Heat Map of Spending Over Time (With National)')
    plt.tight_layout()
    plt.show()

create_spending_heat_map(expenses_df_sorted, exclude_national=False)
create_spending_heat_map(expenses_df_sorted, exclude_national=True)
