### Variables

| Variable           | Type     | Description                                      |
|--------------------|----------|--------------------------------------------------|
| `input_filename`   | String   | Name of the file to read expenses from.          |
| `committees`       | Set      | Stores unique committee names from the CSV file. |
| `fall_budget`      | Float    | Total budget for fall events.                    |
| `spring_budget`    | Float    | Total budget for spring events.                  |
| `in_fall_events`   | Boolean  | Flag to indicate if current events are fall events. |
| `in_spring_events` | Boolean  | Flag to indicate if current events are spring events. |

### Functions

| Function                          | Description                                                                                                 |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------|
| `parse_date(date_str)`            | Parses a date string into a date object, returning None if parsing fails.                                    |
| `plot_cumulative_expenses_over_time(expenses_df_sorted, exclude_national=False, threshold_quantile=0.75)` | Plots cumulative expenses over time, with an option to exclude national expenses.                           |
| `create_spending_heat_map(expenses_df_sorted, exclude_national=False)` | Creates a heat map of spending over time, with an option to exclude national expenses.                      |

### DataFrames

| DataFrame               | Description                                                |
|-------------------------|------------------------------------------------------------|
| `df`                    | DataFrame containing the CSV data.                         |
| `expenses_df`           | DataFrame containing expenses data after parsing dates.    |
| `expenses_df_sorted`    | DataFrame containing sorted expenses data.                 |
| `committee_totals`      | DataFrame containing total costs for each committee.       |
| `committee_expenses`    | DataFrame containing filtered expenses for a specific committee. |
| `fall_expenses`         | DataFrame containing fall expenses for a specific committee. |
| `spring_expenses`       | DataFrame containing spring expenses for a specific committee. |
| `fall_large_purchases`  | DataFrame containing large purchases in fall for a specific committee. |
| `spring_large_purchases`| DataFrame containing large purchases in spring for a specific committee. |
