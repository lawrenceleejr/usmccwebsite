import pandas as pd
import shutil
import os
import re
import wget
import math

def getInstTag(inst):
    inst = inst.lower()
    result = re.sub('[\W_]+', '', inst)
    return result

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRA9zzsaExWvt_QlFKUY8mWiSD9lMO_wPtNuybY2Qfc3YfX5gt4x-9dOcZwBJ3d9_pnWgEttGqiD8E3/pub?gid=0&single=true&output=csv"
df = pd.read_csv(url)

data_dir = "../content/all_people/"
target_dir = "../content/people/"

print(df)
institutions = sorted(df["institution"].unique())
print(institutions)

for i, entry in df.iterrows():
    fname = f"{entry['first']}{entry['last']}"
    person_path = f"{data_dir}{fname}/"

    if type(entry["photo"]) == type(""):
        extension = entry["photo"].split(".")[-1]
        if extension not in ["png", "jpg", "jpeg"]:
            shutil.copy("featured.png", f"{person_path}featured.png")
        else:
            wget.download(entry["photo"], out=f"{data_dir}{fname}/feature_{fname}.{extension}")
            if os.path.exists(f"{person_path}featured.png"):
                os.remove(f"{person_path}featured.png")
    else:
        shutil.copy("featured.png", f"{person_path}featured.png")

    if not os.path.exists(person_path): os.mkdir(person_path)
    with open(f"{person_path}index.md", "w") as f:
        f.write("---\n")
        f.write(f"title: {entry['first']} {entry['last']}\n")
        f.write(f"externalUrl: {entry['website']}\n")
        f.write(f"summary: {entry['position']}, {entry['area']}\n")
        f.write(f"type: {getInstTag(entry['institution'])}\n")
        f.write("showHero: true\n")
        f.write("---\n")

output_file = f"{target_dir}/index.md"
with open(output_file, "w") as f:
    f.write("---\n")
    f.write("title: Meet the people working on a Muon Collider\n")
    f.write("layout: simple\n")
    f.write("---\n")

    for inst in institutions:
        f.write("\n\n")
        f.write(f'{{{{< people limit=20 title="{inst}" cardView=true where="Type" value="{getInstTag(inst)}" >}}}}\n')

