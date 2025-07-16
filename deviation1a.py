#%%
# DONE WATTAGE


# CONSTANT
# --- Snip: imports & setup ---
import pandas as pd
import time
import os
from datetime import datetime

dataList = []

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# --- Load data ---
file_path = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledPiMachine\CompiledPIMachine.csv"
# file_path = r"\\192.168.2.19\ai_team\INDIVIDUAL FOLDER\Jed-san\JHUN DEVIATION\CompiledPIMachine.csv"
# uclLclFile = pd.read_excel('UCL_LCL.xlsx', sheet_name='Sheet1')

df = pd.read_csv(file_path, encoding='latin1')
df = df[(~df["MODEL CODE"].isin(['60CAT0203M']))]







# --- Blank frame ---
# 1ST DATAFRAME (compiledFrame)
emptyColumn = [
    "DATE", 
    "TIME", 
    "MODEL CODE", 
    "S/N", 
    "PASS/NG",
                                        #'2ND DATAFRAME (model_summary)'    
    "VOLTAGE MAX (V)", 
    "V_MAX PASS", 
    "AVE V_MAX PASS",                   #'V-MAX PASS AVG'
    "DEV V_MAX PASS",
    # "VOLTAGE MAX OOT",

    "WATTAGE MAX (W)",
    "WATTAGE MAX PASS",
    "AVE WATTAGE MAX (W)",                  #'WATTAGE MAX AVG'
    "DEV WATTAGE MAX (W)",
    # "WATTAGE MAX OOT",

    "CLOSED PRESSURE_MAX (kPa)",
    "CLOSED PRESSURE_MAX PASS",
    "AVE CLOSED PRESSURE_MAX (kPa)",        #'CLOSED PRESSURE_MAX AVG'
    "DEV CLOSED PRESSURE_MAX (kPa)", 
    # "CLOSED PRESSURE_MAX OOT",

    "VOLTAGE Middle (V)",
    "VOLTAGE Middle PASS",                  #"VOLTAGE Middle AVG"
    "AVE VOLTAGE Middle (V)",
    "DEV VOLTAGE Middle (V)",
    # "VOLTAGE Middle OOT",

    "WATTAGE Middle (W)",
    "WATTAGE Middle (W) PASS",              #"WATTAGE Middle AVG"
    "AVE WATTAGE Middle (W)",
    "DEV WATTAGE Middle (W)",
    # "WATTAGE Middle OOT",

    "AMPERAGE Middle (A)",
    "AMPERAGE Middle (A) PASS",             #"AMPERAGE Middle AVG"
    "AVE AMPERAGE Middle (A)",
    "DEV AMPERAGE Middle (A)",
    # "AMPERAGE Middle OOT",

    "CLOSED PRESSURE Middle (kPa)",
    "CLOSED PRESSURE Middle (kPa) PASS",    #"CLOSED PRESSURE Middle AVG"
    "AVE CLOSED PRESSURE Middle (kPa)",
    "DEV CLOSED PRESSURE Middle (kPa)",
    # "CLOSED PRESSURE Middle OOT",

    "VOLTAGE MIN (V)",
    "VOLTAGE MIN (V) PASS",                 #"VOLTAGE MIN (V) AVG"
    "AVE VOLTAGE MIN (V)",
    "DEV VOLTAGE MIN (V)",
    # "VOLTAGE MIN OOT",

    "WATTAGE MIN (W)",
    "WATTAGE MIN (W) PASS",                 #"WATTAGE MIN AVG"
    "AVE WATTAGE MIN (W)",
    "DEV WATTAGE MIN (W)",
    # "WATTAGE MIN OOT",

    "CLOSED PRESSURE MIN (kPa)",
    "CLOSED PRESSURE MIN (kPa) PASS",       #"CLOSED PRESSURE MIN AVG"
    "AVE CLOSED PRESSURE MIN (kPa)",
    "DEV CLOSED PRESSURE MIN (kPa)"
    # "CLOSED PRESSURE MIN OOT"

]
compiledFrame = pd.DataFrame(columns=emptyColumn)







# NO NEED TO EDIT (CONSTANT)
# --- CLEANING before loop ---
# df['S/N'] = df['S/N'].astype(str)
# df['MODEL CODE'] = df['MODEL CODE'].astype(str)
# df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
# df = df.dropna(subset=['DATE'])
# df = df[df['S/N'].str.len() >= 8]
# df = df[~df['MODEL CODE'].str.contains('M')]

# group_counts = df.groupby(['MODEL CODE', 'DATE']).size().reset_index(name='COUNT')
# valid_groups = group_counts[group_counts['COUNT'] >= 10][['MODEL CODE', 'DATE']]
# df = df.merge(valid_groups, on=['MODEL CODE', 'DATE'], how='inner')

# group_counts = df.groupby(['MODEL CODE', 'DATE']).size().reset_index(name='COUNT')
# df = df.merge(group_counts[['MODEL CODE', 'DATE']], on=['MODEL CODE', 'DATE'], how='inner')



df['S/N'] = df['S/N'].astype(str)
df['MODEL CODE'] = df['MODEL CODE'].astype(str)
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
df = df.dropna(subset=['DATE'])
df = df[df['S/N'].str.len() >= 8]
df = df[~df['MODEL CODE'].str.contains('M')]

# Get today's date without time for comparison
today = pd.Timestamp.now().normalize()

# Group and count entries
group_counts = df.groupby(['MODEL CODE', 'DATE']).size().reset_index(name='COUNT')

# Apply the COUNT >= 10 condition, but skip it for today
valid_groups = group_counts[(group_counts['COUNT'] >= 10) | (group_counts['DATE'] == today)][['MODEL CODE', 'DATE']]

# Merge back to original dataframe
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
        "CLOSED PRESSURE_MAX (kPa)": tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0],
        "VOLTAGE Middle (V)": tempdf["VOLTAGE Middle (V)"].values[0],
        "WATTAGE Middle (W)": tempdf["WATTAGE Middle (W)"].values[0],
        "AMPERAGE Middle (A)": tempdf["AMPERAGE Middle (A)"].values[0],
        "CLOSED PRESSURE Middle (kPa)": tempdf["CLOSED PRESSURE Middle (kPa)"].values[0],
        "VOLTAGE MIN (V)": tempdf["VOLTAGE MIN (V)"].values[0],
        "WATTAGE MIN (W)": tempdf["WATTAGE MIN (W)"].values[0],
        "CLOSED PRESSURE MIN (kPa)": tempdf["CLOSED PRESSURE MIN (kPa)"].values[0]
    }

    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["V_MAX PASS"] = tempdf["VOLTAGE MAX (V)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["WATTAGE MAX PASS"] = tempdf["WATTAGE MAX (W)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["CLOSED PRESSURE_MAX PASS"] = tempdf["CLOSED PRESSURE_MAX (kPa)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["VOLTAGE Middle PASS"] = tempdf["VOLTAGE Middle (V)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["WATTAGE Middle (W) PASS"] = tempdf["WATTAGE Middle (W)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["AMPERAGE Middle (A) PASS"] = tempdf["AMPERAGE Middle (A)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["CLOSED PRESSURE Middle (kPa) PASS"] = tempdf["CLOSED PRESSURE Middle (kPa)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["VOLTAGE MIN (V) PASS"] = tempdf["VOLTAGE MIN (V)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["WATTAGE MIN (W) PASS"] = tempdf["WATTAGE MIN (W)"].values[0]
    if tempdf["PASS/NG"].values[0] == 1:
        dataFrame["CLOSED PRESSURE MIN (kPa) PASS"] = tempdf["CLOSED PRESSURE MIN (kPa)"].values[0]

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

    # PASS DISPLAY (compiledFrame)
    latest_date = past_data['DATE'].max()
    latest_rows = past_data[past_data['DATE'] == latest_date]
    pass_avg = latest_rows['V_MAX PASS'].mean()
    wattage_avg = latest_rows["WATTAGE MAX PASS"].mean() 
    closedPressure_avg = latest_rows["CLOSED PRESSURE_MAX PASS"].mean() 
    voltageMiddle_avg = latest_rows["VOLTAGE Middle PASS"].mean()
    wattageMiddle_avg = latest_rows["WATTAGE Middle (W) PASS"].mean()
    amperageMiddle_avg = latest_rows["AMPERAGE Middle (A) PASS"].mean() 
    closePressureMiddle_avg = latest_rows["CLOSED PRESSURE Middle (kPa) PASS"].mean()
    voltageMin_avg = latest_rows["VOLTAGE MIN (V) PASS"].mean()
    wattageMin_avg = latest_rows["WATTAGE MIN (W) PASS"].mean()
    closePressureMin_avg = latest_rows["CLOSED PRESSURE MIN (kPa) PASS"].mean()

    # AVERAGE DISPLAY (model_summary) DF
    results.append({
        'MODEL CODE': model,
        'LATEST DATE': latest_date.date(),
        'V-MAX PASS AVG': pass_avg,
        'WATTAGE MAX AVG': wattage_avg,
        'CLOSED PRESSURE_MAX AVG': closedPressure_avg,
        'VOLTAGE Middle AVG': voltageMiddle_avg,
        'WATTAGE Middle AVG': wattageMiddle_avg,
        'AMPERAGE Middle AVG': amperageMiddle_avg,
        'CLOSED PRESSURE Middle AVG': closePressureMiddle_avg,
        'VOLTAGE MIN (V) AVG': voltageMin_avg,
        'WATTAGE MIN AVG': wattageMin_avg,
        'CLOSED PRESSURE MIN AVG': closePressureMin_avg
    })

# AVERAGE DISPLAY (model_summary) DF
model_summary = pd.DataFrame(results)
pass_avg_map = model_summary.set_index("MODEL CODE")["V-MAX PASS AVG"].to_dict()
wattage_avg_map = model_summary.set_index("MODEL CODE")["WATTAGE MAX AVG"].to_dict()
closedPressure_avg_map = model_summary.set_index("MODEL CODE")['CLOSED PRESSURE_MAX AVG'].to_dict()
voltageMiddle_avg_map = model_summary.set_index("MODEL CODE")["VOLTAGE Middle AVG"].to_dict()
wattageMiddle_avg = model_summary.set_index("MODEL CODE")["WATTAGE Middle AVG"].to_dict()
amperageMiddle_avg = model_summary.set_index("MODEL CODE")["AMPERAGE Middle AVG"].to_dict()
closePressureMiddle_avg = model_summary.set_index("MODEL CODE")["CLOSED PRESSURE Middle AVG"].to_dict()
voltageMin_avg = model_summary.set_index("MODEL CODE")["VOLTAGE MIN (V) AVG"].to_dict()
wattageMin_avg = model_summary.set_index("MODEL CODE")["WATTAGE MIN AVG"].to_dict()
closePressureMin_avg = model_summary.set_index("MODEL CODE")["CLOSED PRESSURE MIN AVG"].to_dict()


# --- Now inject  ---AVERAGE DISPLAY (compiledFrame)
# 1
compiledFrame["AVE V_MAX PASS"] = compiledFrame["MODEL CODE"].map(pass_avg_map)
# 2
compiledFrame["AVE WATTAGE MAX (W)"] = compiledFrame["MODEL CODE"].map(wattage_avg_map)
# 3
compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"] = compiledFrame["MODEL CODE"].map(closedPressure_avg_map)
# 4
compiledFrame["AVE VOLTAGE Middle (V)"] = compiledFrame["MODEL CODE"].map(voltageMiddle_avg_map)
# 5
compiledFrame["AVE WATTAGE Middle (W)"] = compiledFrame["MODEL CODE"].map(wattageMiddle_avg)
# 6
compiledFrame["AVE AMPERAGE Middle (A)"] = compiledFrame["MODEL CODE"].map(amperageMiddle_avg)
# 7
compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"] = compiledFrame["MODEL CODE"].map(closePressureMiddle_avg)
# 8
compiledFrame["AVE VOLTAGE MIN (V)"] = compiledFrame["MODEL CODE"].map(voltageMin_avg)
# 9
compiledFrame["AVE WATTAGE MIN (W)"] = compiledFrame["MODEL CODE"].map(wattageMin_avg)
# 10
compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"] = compiledFrame["MODEL CODE"].map(closePressureMin_avg)



# --- Compute DEV DISPLAY --- (compiledFrame)
# 1
compiledFrame["DEV V_MAX PASS"] = (
    (compiledFrame["AVE V_MAX PASS"] - compiledFrame["V_MAX PASS"]) / compiledFrame["AVE V_MAX PASS"]
)
# 2
compiledFrame["DEV WATTAGE MAX (W)"] = (
    (compiledFrame["AVE WATTAGE MAX (W)"] - compiledFrame["WATTAGE MAX PASS"]) / compiledFrame["AVE WATTAGE MAX (W)"]
)
# 3
compiledFrame["DEV CLOSED PRESSURE_MAX (kPa)"] = (
    (compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"] - compiledFrame["CLOSED PRESSURE_MAX PASS"]) / compiledFrame["AVE CLOSED PRESSURE_MAX (kPa)"].astype(float)
)
# 4
compiledFrame["DEV VOLTAGE Middle (V)"] = (
    (compiledFrame["AVE VOLTAGE Middle (V)"] - compiledFrame["VOLTAGE Middle PASS"]) / compiledFrame["AVE VOLTAGE Middle (V)"]
)
# 5
compiledFrame["DEV WATTAGE Middle (W)"] = (
    (compiledFrame["AVE WATTAGE Middle (W)"] - compiledFrame["WATTAGE Middle (W) PASS"]) / compiledFrame["AVE WATTAGE Middle (W)"]
)
# 6
compiledFrame["DEV AMPERAGE Middle (A)"] = (
    (compiledFrame["AVE AMPERAGE Middle (A)"] - compiledFrame["AMPERAGE Middle (A) PASS"]) / compiledFrame["AVE AMPERAGE Middle (A)"]
)
# 7
compiledFrame["DEV CLOSED PRESSURE Middle (kPa)"] = (
    (compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"] - compiledFrame["CLOSED PRESSURE Middle (kPa) PASS"]) / compiledFrame["AVE CLOSED PRESSURE Middle (kPa)"]
)
# 8
compiledFrame["DEV VOLTAGE MIN (V)"] = (
    (compiledFrame["AVE VOLTAGE MIN (V)"] - compiledFrame["VOLTAGE MIN (V) PASS"]) / compiledFrame["AVE VOLTAGE MIN (V)"]
)
# 9
compiledFrame["DEV WATTAGE MIN (W)"] = (
    (compiledFrame["AVE WATTAGE MIN (W)"] - compiledFrame["WATTAGE MIN (W) PASS"]) / compiledFrame["AVE WATTAGE MIN (W)"]
)
# 10
compiledFrame["DEV CLOSED PRESSURE MIN (kPa)"] = (
    (compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"] - compiledFrame["CLOSED PRESSURE MIN (kPa) PASS"]) / compiledFrame["AVE CLOSED PRESSURE MIN (kPa)"]
)




# use this to print "DEV CLOSED PRESSURE_MAX (kPa)"
# for a in compiledFrame["DEV CLOSED PRESSURE_MAX (kPa)"]:
#     print(a)














# --- Display results ---
print(" Final cleaned compiledFrame with averages:\n")
print(compiledFrame)

print("\n Summary model_summary:\n")
print(model_summary)

# %%
