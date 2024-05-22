import pandas as pd
import shutil
import os
import re
import wget
import math
import glob

# Path options
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRA9zzsaExWvt_QlFKUY8mWiSD9lMO_wPtNuybY2Qfc3YfX5gt4x-9dOcZwBJ3d9_pnWgEttGqiD8E3/pub?gid=0&single=true&output=csv"
data_dir = "../content/all_people/"
target_dir = "../content/people/"

# Run options
hard_reset = True

# Make alphanumeric tags to ID institutes
def getInstTag(inst):
    inst = inst.lower()
    result = re.sub('[\W_]+', '', inst)
    return result

# Get data and list of institutes
df = pd.read_csv(url)
institutions = sorted(df["institution"].unique())

# Remove everything if hard_reset
if hard_reset:
    for f in glob.glob(f"{data_dir}*"):
        shutil.rmtree(f)

# Loop over people
for i, entry in df.iterrows():

    # Put data in paths based on the person's name
    fname = f"{entry['first']}{entry['last']}"
    person_path = f"{data_dir}{fname}/"
    if not os.path.exists(person_path): os.mkdir(person_path)

    # Try to access photo from spreadsheet if it's not already there
    if not os.path.exists(f"{person_path}/feature_{fname}.*"):
        got_photo = False
        if type(entry["photo"]) == type(""):
            extension = entry["photo"].split(".")[-1]
            if extension in ["png", "jpg", "jpeg"]:
                wget.download(entry["photo"], out=f"{data_dir}{fname}/feature_{fname}.{extension}")
                got_photo = True
                if os.path.exists(f"{person_path}featured.png"):
                    os.remove(f"{person_path}featured.png")
        # If this fails, copy the default photo to their path
        if not got_photo:
            shutil.copy("featured.png", f"{person_path}featured.png")

    # Create index file with all the person's info
    with open(f"{person_path}index.md", "w") as f:
        f.write("---\n")
        f.write(f"title: {entry['first']} {entry['last']}\n")
        f.write(f"externalUrl: {entry['website']}\n")
        f.write(f"summary: {entry['position']}, {entry['area']}\n")
        f.write(f"type: {getInstTag(entry['institution'])}\n")
        #f.write("showHero: true\n")
        f.write("---\n")

# Create main index file for ultimate site
output_file = f"{target_dir}/index.md"
with open(output_file, "w") as f:
    f.write("---\n")
    f.write("title: Meet the people working on a Muon Collider\n")
    f.write("layout: simple\n")
    f.write("---\n")

    for inst in institutions:
        f.write("\n\n")
        f.write(f'{{{{< people limit=20 title="{inst}" cardView=true where="Type" value="{getInstTag(inst)}" >}}}}\n')

