import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Use a seaborn color palette to get distinct colors for departments, sexes, or cities
color_palette = sns.color_palette("husl", 10)

# Function to generate test data where salary depends on the level
def generate_test_data(num_records=1000):
    # Define possible values for each field
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hannah', 'Isaac', 'Jack', 'Karen', 'Liam', 'Mia', 'Noah', 'Olivia']
    departments = ['HR', 'Finance', 'IT', 'Sales', 'Marketing', 'Engineering']
    levels = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']
    sexes = ['M', 'F']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    
    # Salary ranges depending on levels
    salary_ranges = {
        'Level 1': (30000, 50000),
        'Level 2': (40000, 60000),
        'Level 3': (50000, 80000),
        'Level 4': (70000, 100000),
        'Level 5': (90000, 150000)
    }
    
    # Generate random data
    data = []
    for _ in range(num_records):
        level = np.random.choice(levels)
        min_salary, max_salary = salary_ranges[level]
        data.append({
            'Name': np.random.choice(names),
            'department': np.random.choice(departments),
            'Level': level,
            'sex': np.random.choice(sexes),
            'city': np.random.choice(cities),
            'Salary': np.random.randint(min_salary, max_salary)
        })
    
    return pd.DataFrame(data)

# Step 2: Aggregating data by Level and selected attributes (Department, Sex, or City)
def aggregate_data(test_data, attribute, value):
    return test_data[test_data[attribute] == value].groupby('Level').agg(
        min_salary=('Salary', 'min'),
        max_salary=('Salary', 'max'),
        mean_salary=('Salary', 'mean'),
        quantile_25=('Salary', lambda x: np.percentile(x, 25)),
        quantile_75=('Salary', lambda x: np.percentile(x, 75))
    ).reset_index()

# Step 3: Function to plot salary ranges for multiple attributes and their values
def plot_salary_ranges_by(test_data, j_config):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    levels_numeric = {
        'Level 1': 1, 
        'Level 2': 2, 
        'Level 3': 3, 
        'Level 4': 4, 
        'Level 5': 5
    }
    
    # Base vertical spacing between values within each level
    spacing = 0.2  # Increased spacing to avoid overlap
    all_data_offset = 0.5  # Increased offset for the "All" data to avoid overlap
    
    index = 0  # To keep track of the color palette
    
    # Aggregate data for all values as a reference
    combined_data = test_data.groupby('Level').agg(
        min_salary=('Salary', 'min'),
        max_salary=('Salary', 'max'),
        mean_salary=('Salary', 'mean'),
        quantile_25=('Salary', lambda x: np.percentile(x, 25)),
        quantile_75=('Salary', lambda x: np.percentile(x, 75))
    ).reset_index()
    
    # Plot the "All" reference range with larger spacing above the attributes
    for i, row in combined_data.iterrows():
        numeric_level = levels_numeric[row['Level']]
        # Plot "All" line at the top with extra spacing
        ax.plot([row['min_salary'], row['max_salary']], 
                [numeric_level + all_data_offset, numeric_level + all_data_offset], 
                color='black', marker='|', linewidth=2, label='All Data' if i == 0 else "")
        ax.plot([row['quantile_25'], row['quantile_75']], 
                [numeric_level + all_data_offset, numeric_level + all_data_offset], 
                color='black', linewidth=6)
        ax.scatter(row['mean_salary'], numeric_level + all_data_offset, 
                   color='black', zorder=5)

    # Now plot for each attribute in j_config
    for attribute, values in j_config.items():
        for value in values:
            data = aggregate_data(test_data, attribute, value)
            color = color_palette[index % len(color_palette)]
            index += 1  # Move to the next color
            
            for i, row in data.iterrows():
                numeric_level = levels_numeric[row['Level']]
                offset = numeric_level + index * spacing
                ax.plot([row['min_salary'], row['max_salary']], [offset, offset], color=color, marker='|', linewidth=2)
                ax.plot([row['quantile_25'], row['quantile_75']], [offset, offset], color=color, linewidth=6)
                ax.scatter(row['mean_salary'], offset, color=color, zorder=5)

            ax.plot([], [], color=color, label=f'{attribute}: {value}')
    
    ax.set_xlabel('Salary', fontsize=12)
    ax.set_ylabel('Levels', fontsize=12)
    
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5'])
    
    ax.set_title(f'Salary Ranges by Level for Selected Attributes', fontsize=14, pad=15)
    
    ax.legend(title='Attributes', loc='upper left', fontsize=10)
    
    plt.tight_layout()
    
    return plt