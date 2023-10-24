import csv
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def generate_random_data(file_path, num_records):
    # Generate random data and store it in a CSV file
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ["ID", "Name", "Age", "Gender", "Status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, num_records + 1):
            name = f"User {i}"
            age = np.random.randint(15, 70)
            gender = "Male" if np.random.rand() < 0.5 else "Female"
            status = "Active" if np.random.rand() < 0.6 else "Inactive"
            writer.writerow({"ID": i, "Name": name, "Age": age, "Gender": gender, "Status": status})

def read_and_analyze_data(file_path):
    # Read data from the CSV file and generate statistics
    active_users = 0
    female_users = 0
    users_by_age_group = {
        "0-18": 0,
        "19-30": 0,
        "31-45": 0,
        "46-60": 0,
        "61+": 0,
    }

    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                status = row['Status']
                gender = row['Gender']
                age = int(row['Age'])

                if status == 'Active':
                    active_users += 1

                if gender == 'Female':
                    female_users += 1

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

    except FileNotFoundError:
        print("Error: The specified CSV file was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    return active_users, percentage_females, users_by_age_group

def create_gui(active_users, percentage_females, users_by_age_group):
    # Create a GUI application
    root = tk.Tk()
    root.title("User Statistics")

   # Set fixed dimensions for the main window
    root.minsize(600, 450)
    root.maxsize(600, 450)

    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('calibri', 12))
    style.configure('TFrame', background = 'white')

    tab_control = ttk.Notebook(root)

    # Tab 1 - General Statistics
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="General Statistics")

    tab1.grid_rowconfigure(0, weight=1)
    tab1.grid_columnconfigure(0, weight=1)

    statistics_frame = ttk.Frame(tab1, padding=(10, 10, 10, 10), relief=tk.RAISED)
    statistics_frame.grid(row=0, column=0, sticky='n', pady=30)

    lbl_title = ttk.Label(statistics_frame, text="User Statistics", font=("calibri", 16, "bold"), background='white')
    lbl_title.grid(row=0, column=0, padx=10)

    lbl_active_users = ttk.Label(statistics_frame, text=f"Active Users: {active_users}", background='white', font=("calibri", 12))
    lbl_active_users.grid(row=2, column=0, padx=10, pady=5)

    lbl_percentage_females = ttk.Label(statistics_frame, text=f"Percentage of Females: {percentage_females:.2f}%", background='white', font=("calibri", 12))
    lbl_percentage_females.grid(row=3, column=0, padx=10, pady=10)

    lbl_age_group_title = ttk.Label(statistics_frame, text="Number of Users in Each Age Group", font=("calibri", 12, "bold"), background='white')
    lbl_age_group_title.grid(row=4, column=0, padx=10, pady=5)

    for i, (age_group, count) in enumerate(users_by_age_group.items(), start=5):
        lbl_age_group = ttk.Label(statistics_frame, text=f"{age_group}: {count} users", background='white', font=("calibri", 12))
        lbl_age_group.grid(row=i, column=0, padx=10, pady=5)

    # Tab 2 - Users Count per Age Group
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Users Count per Age Group")

    age_groups = list(users_by_age_group.keys())
    user_counts = list(users_by_age_group.values())

    fig = Figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    ax.bar(age_groups, user_counts, color='skyblue')
    ax.set_xlabel("Age Group")
    ax.set_ylabel("User Count")
    ax.set_title("Distribution of Users by Age Group")

    canvas = FigureCanvasTkAgg(fig, master=tab2)
    canvas.get_tk_widget().pack()

    tab_control.pack(expand=1, fill="both")
    root.mainloop()

if __name__ == "__main__":
    # Define the CSV file path and the number of records to generate
    csv_file_path = "Advanced_Solution/AdvanceData.csv"
    num_records_to_generate = 30

    # Step 1: Generate random data and store it in a CSV file
    generate_random_data(csv_file_path, num_records_to_generate)

    # Step 2: Read and analyze the data
    data = read_and_analyze_data(csv_file_path)

    if data is not None:
        # Step 3: Create the GUI with statistics and charts
        active_users, female_users, users_by_age_group = data
        create_gui(active_users, female_users, users_by_age_group)
