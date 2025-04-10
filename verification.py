# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 08:56:16 2025

@author: Ronyt
"""

import pandas as pd
import os
import fnmatch
from sklearn.metrics import mean_absolute_error, f1_score

# Define the main directory
main_dir = r"C:\Users\Ronyt\EX3"

# Load reference files
cars_file = os.path.join(main_dir, "cars_final.xlsx")
workers_file = os.path.join(main_dir, "workers_final.xlsx")

cars_df = pd.read_excel(cars_file)
workers_df = pd.read_excel(workers_file)

# Function to find column name variations
def find_column_name(df, possible_names):
    for col in df.columns:
        if any(fnmatch.fnmatch(col.lower(), name.lower()) for name in possible_names):
            return col  # Return the first matching column name
    return None

# Find reference column names
price_col = find_column_name(cars_df, ["price", "price_predicted"])
job_role_col = find_column_name(workers_df, ["job_role", "job role", "role"])

if not price_col or not job_role_col:
    raise ValueError("Could not find expected columns in the reference files.")

reference_prices = cars_df[price_col]
reference_job_roles = workers_df[job_role_col]

# Store results
results = []

# Loop through subdirectories
for student_folder in os.listdir(main_dir):
    student_path = os.path.join(main_dir, student_folder)
    
    if os.path.isdir(student_path):  # Ensure it's a directory
        student_result = {"Student": student_folder}

        # Find student files dynamically
        cars_file_path = None
        workers_file_path = None

        for file in os.listdir(student_path):
            file_lower = file.lower()
            if "cars" in file_lower and file.endswith((".xls", ".xlsx")):
                cars_file_path = os.path.join(student_path, file)
            elif "worker" in file_lower and file.endswith((".xls", ".xlsx")):
                workers_file_path = os.path.join(student_path, file)

        try:
            # Process cars file
            if cars_file_path:
                student_cars_df = pd.read_excel(cars_file_path)
                student_price_col = find_column_name(student_cars_df, ["price", "price_predicted"])

                if student_price_col:
                    student_prices = student_cars_df[student_price_col]
                    
                    if len(student_prices) == len(reference_prices):
                        student_result["MAE"] = mean_absolute_error(reference_prices, student_prices)
                    else:
                        student_result["MAE"] = "Error: Different lengths"
                else:
                    student_result["MAE"] = "Error: Column not found"
            else:
                student_result["MAE"] = "Error: File missing"

            # Process workers file
            if workers_file_path:
                student_workers_df = pd.read_excel(workers_file_path)
                student_job_role_col = find_column_name(student_workers_df, ["job_role", "job role", "role"])

                if student_job_role_col:
                    student_job_roles = student_workers_df[student_job_role_col]

                    if len(student_job_roles) == len(reference_job_roles):
                        student_result["F1"] = f1_score(reference_job_roles, student_job_roles, average="macro")
                    else:
                        student_result["F1"] = "Error: Different lengths"
                else:
                    student_result["F1"] = "Error: Column not found"
            else:
                student_result["F1"] = "Error: File missing"

        except Exception as e:
            student_result["Error"] = str(e)

        results.append(student_result)

# Save results
results_df = pd.DataFrame(results)
results_file_path = os.path.join(main_dir, "results2.xlsx")
results_df.to_excel(results_file_path, index=False)

print(f"Results saved to {results_file_path}")