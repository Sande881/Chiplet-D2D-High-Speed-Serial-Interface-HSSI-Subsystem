import matplotlib.pyplot as plt
import pandas as pd

def parse_cumulative_stats(filepath):
    data = {'time_ns': [], 'alu_cumulative': [], 'mispred_cumulative': []}
    time_step = 50 # 50ns dump window
    current_time = 0
    
    # Track the latest values found in the current dump block
    alu_val = 0
    mispred_val = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            if "Begin Simulation Statistics" in line:
                if current_time > 0:
                    data['time_ns'].append(current_time)
                    data['alu_cumulative'].append(alu_val)
                    data['mispred_cumulative'].append(mispred_val)
                current_time += time_step
                
            # Modern gem5 v25+ O3 statistics
            elif "system.cpu.executeStats0.numInsts" in line:
                alu_val = int(line.split()[1])
            elif "system.cpu.commitStats0.branchMispredicts" in line:
                mispred_val = int(line.split()[1])
                
    # Append the final block
    if current_time > 0:
        data['time_ns'].append(current_time)
        data['alu_cumulative'].append(alu_val)
        data['mispred_cumulative'].append(mispred_val)
        
    df = pd.DataFrame(data)
    
    # Calculate the delta per 50ns window to get instantaneous activity
    df['alu_activity'] = df['alu_cumulative'].diff().fillna(df['alu_cumulative'])
    df['mispredictions'] = df['mispred_cumulative'].diff().fillna(df['mispred_cumulative'])
    
    # Filter out periods with zero activity
    return df[df['alu_activity'] > 0]

# 1. Parse the data
df = parse_cumulative_stats('m5out_transient/stats.txt')

# 2. Plot the di/dt transient event
fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:blue'
ax1.set_xlabel('Time (ns)')
ax1.set_ylabel('ALU Accesses (Proxy for Idyn)', color=color)
ax1.plot(df['time_ns'], df['alu_activity'], color=color, linewidth=2, marker='o', markersize=4)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.6)

# Overlay branch misprediction events
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Branch Mispredictions', color=color)
ax2.bar(df['time_ns'], df['mispredictions'], width=25, color=color, alpha=0.4)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Pipeline Flush Transient: di/dt Event Profiling')
fig.tight_layout()
plt.savefig('didt_transient_profile.png', dpi=300)
print("Plot saved as didt_transient_profile.png")

# 3. Generate the PWL for Ngspice
# Define a scaling factor (e.g., 5 uA per access) and leakage (e.g., 1 mA)
I_PER_TOGGLE = 5.0e-6 
I_LEAKAGE = 1.0e-3 

df['current_A'] = (df['alu_activity'] * I_PER_TOGGLE) + I_LEAKAGE

pwl_filepath = 'cpu_transient.pwl'
with open(pwl_filepath, 'w') as f:
    for index, row in df.iterrows():
        time_sec = row['time_ns'] * 1e-9 
        f.write(f"{time_sec:.9e} {row['current_A']:.6e}\n")

print(f"Ngspice PWL waveform saved as {pwl_filepath}")
