#%%
# DONE WATTAGE


# CONSTANT
# --- Snip: imports & setup ---
import pandas as pd
import time
import os
from datetime import datetime

dataList = []

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# --- Load data ---
file_path = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv"
# uclLclFile = pd.read_excel('UCL_LCL.xlsx', sheet_name='Sheet1')

df = pd.read_csv(file_path, encoding='latin1')
df = df[(~df["MODEL CODE"].isin(['60CAT0203M']))]







# --- Blank frame ---
emptyColumn = [
    "DATE", 
    "TIME", 
    "MODEL CODE", 
    "S/N", 
    "PASS/NG",
    "VOLTAGE MAX (V)", 
    "V_MAX PASS", 
    "AVE V_MAX PASS",
    "DEV V_MAX PASS",
    "WATTAGE MAX (W)",
    "CLOSED PRESSURE_MAX (kPa)"
    

]
compiledFrame = pd.DataFrame(columns=emptyColumn)







# CONSTANT
# --- CLEANING before loop ---
df['S/N'] = df['S/N'].astype(str)
df['MODEL CODE'] = df['MODEL CODE'].astype(str)
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
df = df.dropna(subset=['DATE'])
df = df[df['S/N'].str.len() >= 8]
df = df[~df['MODEL CODE'].str.contains('M')]

group_counts = df.groupby(['MODEL CODE', 'DATE']).size().reset_index(name='COUNT')
valid_groups = group_counts[group_counts['COUNT'] >= 10][['MODEL CODE', 'DATE']]
df = df.merge(valid_groups, on=['MODEL CODE', 'DATE'], how='inner')










# --- Custom loop FIRST (to populate compiledFrame) ---
for a in range(len(df)):
    print(f"ROW: {a}")
    tempdf = df.iloc[[a]]
    model_code = tempdf["MODEL CODE"].values[0]

    dataFrame = {
        "DATE": tempdf["DATE"].values[0],
        "TIME": tempdf["TIME"].values[0],
        "MODEL CODE": model_code,
        "S/N": tempdf["S/N"].values[0],
        "PASS/NG": tempdf["PASS/NG"].values[0],
        "VOLTAGE MAX (V)": tempdf["VOLTAGE MAX (V)"].values[0],
        "WATTAGE MAX (W)": tempdf["WATTAGE MAX (W)"].values[0],  #  This line is now active
        "CLOSED PRESSURE_MAX (kPa)": tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0]
    }

    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["V_MAX PASS"] = tempdf["VOLTAGE MAX (V)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["WATTAGE MAX PASS"] = tempdf["WATTAGE MAX (W)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["CLOSED PRESSURE MAX PASS"] = tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0]

    dataList.append(dataFrame)

dataFrame = pd.DataFrame(dataList)
compiledFrame = pd.concat([compiledFrame, dataFrame], ignore_index=True)









# --- COMPUTE model_summary AFTER compiledFrame exists ---
today = pd.to_datetime(datetime.now().date())
results = []

for model, group in compiledFrame.groupby('MODEL CODE'):
    past_data = group[group['DATE'].dt.date < today.date()]
    if past_data.empty:
        print(f" Skipping {model}: No past data")
        continue

    latest_date = past_data['DATE'].max()
    latest_rows = past_data[past_data['DATE'] == latest_date]
    pass_avg = latest_rows['V_MAX PASS'].mean()
    wattage_avg = latest_rows["WATTAGE MAX (W)"].mean()
    closedPressure_avg = latest_rows["CLOSED PRESSURE_MAX (kPa)"].mean()

    results.append({
        'MODEL CODE': model,
        'LATEST DATE': latest_date.date(),
        'V-MAX PASS AVG': pass_avg,
        'WATTAGE MAX AVG': wattage_avg,
        'CLOSED PRESSURE_MAX (kPa)': closedPressure_avg
    })

model_summary = pd.DataFrame(results)
pass_avg_map = model_summary.set_index("MODEL CODE")["V-MAX PASS AVG"].to_dict()
wattage_avg_map = model_summary.set_index("MODEL CODE")["WATTAGE MAX AVG"].to_dict()
closedPressure_avg_map = model_summary.set_index("MODEL CODE")["CLOSED PRESSURE_MAX (kPa)"].to_dict()

# --- Now inject AVE V_MAX PASS ---
compiledFrame["AVE V_MAX PASS"] = compiledFrame["MODEL CODE"].map(pass_avg_map)
compiledFrame["AVE WATTAGE MAX (W)"] = compiledFrame["MODEL CODE"].map(wattage_avg_map)
compiledFrame["AVE CLOSED PRESSURE (kPa)"] = compiledFrame["MODEL CODE"].map(closedPressure_avg_map)

# --- Compute DEV V_MAX PASS ---
compiledFrame["DEV V_MAX PASS"] = (
    (compiledFrame["AVE V_MAX PASS"] - compiledFrame["V_MAX PASS"]) / compiledFrame["AVE V_MAX PASS"]
)
compiledFrame["DEV WATTAGE MAX (W)"] = (
    (compiledFrame["AVE WATTAGE MAX (W)"] - compiledFrame["WATTAGE MAX (W)"]) / compiledFrame["AVE WATTAGE MAX (W)"]
)
compiledFrame["DEV CLOSED PRESSURE (W)"] = (
    (compiledFrame["AVE CLOSED PRESSURE (kPa)"] - compiledFrame["CLOSED PRESSURE_MAX (kPa)"]) / compiledFrame["AVE CLOSED PRESSURE (kPa)"]
)






# --- Display results ---
print(" Final cleaned compiledFrame with averages:\n")
print(compiledFrame)

print("\n Summary model_summary:\n")
print(model_summary)

# %%
