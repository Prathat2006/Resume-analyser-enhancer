import pandas as pd
import random

# Generate sample patient DataFrame
patients_df = pd.DataFrame({
    "Patient_ID": [f"P{i+1}" for i in range(50)],
    "Doctor_Name": [f"Doctor_{random.randint(1, 10)}" for _ in range(50)]
})

# Add additional numeric patient features
patients_df["BP_Systolic"] = [random.randint(100, 160) for _ in range(50)]
patients_df["BP_Diastolic"] = [random.randint(60, 100) for _ in range(50)]
patients_df["Heart_Rate"] = [random.randint(60, 100) for _ in range(50)]

# Generate sample doctor DataFrame
unique_doctors = patients_df["Doctor_Name"].unique()
doctors_df = pd.DataFrame({
    "Doctor_Name": unique_doctors,
    "Patient_ID": [patients_df[patients_df["Doctor_Name"] == doc]["Patient_ID"].iloc[0] for doc in unique_doctors]
})

# Add numeric doctor feature: Years of Experience
doctor_experience_map = {f"Doctor_{i}": random.randint(5, 30) for i in range(1, 11)}
doctors_df["Years_Experience"] = doctors_df["Doctor_Name"].map(doctor_experience_map)

# Merge updated data into final dataset
full_df_final = pd.merge(doctors_df, patients_df, on="Patient_ID")

# Save final dataset to CSV
final_csv_numeric_path = "clinical_trial_dataset_50_numeric.csv"
full_df_final.to_csv(final_csv_numeric_path, index=False)

print(f"Final dataset saved to: {final_csv_numeric_path}")
