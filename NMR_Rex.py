import pandas as pd
import matplotlib.pyplot as plt
import glob
import re
import os


folder = "out_pint_Oxi_800_Bp"
df = pd.DataFrame(columns=["residue_number", "residue", "Rex"])
i = 0
os.chdir(folder)
file_list = glob.glob("*.cpmg")   # get a list of *.cpmg files
for file in file_list:
    name = file[0]
    # grab unumber from file name as residue no.
    residue_no = int(re.findall(r"\d+", file)[0])
    # columns separated by one or more spaces
    with open(file):
        data = pd.read_csv(file, header=0, sep=r"\s+")
        max_index = data["#nu_cpmg(Hz)"].idxmax()  # index of maximum frequency
        min_index = data["#nu_cpmg(Hz)"].idxmin()
        R2_max_f = data.loc[max_index]["R2(1/s)"]  # R2 of maximum frequency
        R2_min_f = data.loc[min_index]["R2(1/s)"]
        Rex = R2_min_f - R2_max_f

        df.loc[i] = [residue_no, name, Rex]
        i += 1


df = df.sort_values("residue_number")
filt = (df["residue_number"] < 1000)

fig, ax = plt.subplots()

df.loc[filt].plot(x="residue_number", y="Rex", legend=False, ax=ax)
ax.set_xlabel("residue number")
ax.set_ylabel("Rex")

fig.tight_layout()
plt.show()
fig.savefig("Rex.png")
