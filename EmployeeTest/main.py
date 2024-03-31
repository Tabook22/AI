import pandas as pd
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

def analyze_excel_sheet(file_path, agent_output):
    try:
        df = pd.read_excel(file_path, header=1)  # Assumes the header is on the second row
        print("DataFrame shape:", df.shape)
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None

    achieved_percentage_columns = {
        'Baqati': 2,  # Excel column 'D' is index 2 in pandas
        'Baqati Upgrade': 6,  # Excel column 'H' is index 6 in pandas
        'Hayyak Plus': 10,  # Excel column 'L' is index 10 in pandas
        'HBB': 14,  # Excel column 'P' is index 14 in pandas
        'HBB Upgrade': 18,  # Excel column 'T' is index 18 in pandas
    }
    employee_performance = {}

    for column, col_index in achieved_percentage_columns.items():
        print(f"Accessing index {col_index} for category '{column}'")
        if col_index >= len(df.columns):
            print(f"Column index {col_index} is out of bounds for the DataFrame.")
            continue

        df[f'{column} Achieved %'] = pd.to_numeric(df.iloc[:, col_index], errors='coerce')
        for _, row in df.iterrows():
            employee_name = row['Outlet/CSR']
            achieved_percent = row[f'{column} Achieved %']
            if employee_name not in employee_performance or achieved_percent > employee_performance[employee_name]['Achieved %']:
                employee_performance[employee_name] = {
                    'Achieved %': achieved_percent,
                    'Category': column
                }

    formatted_results = format_results(employee_performance)
    return formatted_results

def format_results(employee_performance):
    if not employee_performance:
        return "No data available to format."

    formatted_results = "List of all employees with their highest 'Achieved %' and corresponding category:\n"
    for employee_name, info in employee_performance.items():
        employee_info = f"{employee_name}: {info['Achieved %']}% in {info['Category']}"
        formatted_results += f"{employee_info}\n"

    return formatted_results

load_dotenv()
researcher = Agent(
    role="Senior Research Analyst",
    goal="Select the best employees based on their yearly performance",
    backstory="You are working at a Telecommunication Company named OmanTel, as a performance analyst and your main job is to select the best performance employees based on the Excel sheet which will be provided to you.",
    verbose=True,
    allow_delegation=False,
)

task1 = Task(
    description="""
import pandas as pd

def analyze_task(file_path):
    try:
        df = pd.read_excel(file_path, header=1)
    except Exception as e:
        return f"Error: {e}"

    achieved_percentage_columns = {
        'Baqati': 2,
        'Baqati Upgrade': 6,
        'Hayyak Plus': 10,
        'HBB': 14,
        'HBB Upgrade': 18
    }
    employee_performance = {}

    for column, col_index in achieved_percentage_columns.items():
        df[f'{column} Achieved %'] = pd.to_numeric(df.iloc[:, col_index], errors='coerce')
        for _, row in df.iterrows():
            employee_name = row['Outlet/CSR']
            achieved_percent = row[f'{column} Achieved %']
            if employee_name not in employee_performance or achieved_percent > employee_performance[employee_name]['Achieved %']:
                employee_performance[employee_name] = {
                    'Achieved %': achieved_percent,
                    'Category': column
                }

    formatted_results = "List of all employees with their highest 'Achieved %' and corresponding category:\\n"
    for employee_name, info in employee_performance.items():
        employee_info = f"{employee_name}: {info['Achieved %']}% in {info['Category']}"
        formatted_results += f"{employee_info}\\n"

    return formatted_results

file_path = r'C:\\Users\\Naser\\Dropbox\\myProjects\\myAIProjects\\EmployeeTest\\emp.xlsx'
result = analyze_task(file_path)
print(result)
""",
    agent=researcher,
    expected_output="A list of all employees with their names from the 'Outlet/CSR' column, their highest achieved percentage, and the corresponding category."
)

crew = Crew(agents=[researcher], tasks=[task1], verbose=2)
excel_file_path = r'C:\Users\Naser\Dropbox\myProjects\myAIProjects\EmployeeTest\emp.xlsx'

result = crew.kickoff()