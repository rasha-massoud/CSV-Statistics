import csv
import matplotlib.pyplot as plt
import numpy as np

# Initialize counters and age group bins
active_users = 0
female_users = 0
users_by_age_group = {
    "0-18": 0,
    "19-30": 0,
    "31-45": 0,
    "46-60": 0,
    "61+": 0,
}

# Specify the CSV file path
csv_file = "Data.csv"

try:
    # Read data from the CSV file
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        
        # Iterate through the rows in the CSV file
        for row in reader:
            status = row['Status']
            gender = row['Gender']
            age = int(row['Age'])
            
            # Count active users
            if status == 'Active':
                active_users += 1
    
            # Count female users
            if gender == 'Female':
                female_users += 1
            
            # Categorize users into age groups
            if age <= 18:
                users_by_age_group["0-18"] += 1
            elif age <= 30:
                users_by_age_group["19-30"] += 1
            elif age <= 45:
                users_by_age_group["31-45"] += 1
            elif age <= 60:
                users_by_age_group["46-60"] += 1
            else:
                users_by_age_group["61+"] += 1
    
    # Calculate percentage of females
    total_users = sum(users_by_age_group.values())
    percentage_females = (female_users / total_users) * 100
    
    # Display the statistics
    print(f"Number of Active Users: {active_users}")
    print(f"Percentage of Females: {percentage_females:.2f}%")
    print("Users Count per Age Group:")
    for age_group, count in users_by_age_group.items():
        print(f"{age_group}: {count}")
    
    # Create a bar chart of the distribution of users by age group
    age_groups = list(users_by_age_group.keys())
    user_counts = list(users_by_age_group.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(age_groups, user_counts)
    plt.xlabel("Age Group")
    plt.ylabel("User Count")
    plt.title("Distribution of Users by Age Group")
    plt.show()

except FileNotFoundError:
    print("Error: The specified CSV file was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
