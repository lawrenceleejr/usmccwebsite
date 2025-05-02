import pandas as pd
import shutil
import os
import re
import wget
import math
import glob
import gdown
import requests
from PIL import Image
from io import BytesIO


# Path options
#url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRA9zzsaExWvt_QlFKUY8mWiSD9lMO_wPtNuybY2Qfc3YfX5gt4x-9dOcZwBJ3d9_pnWgEttGqiD8E3/pub?gid=0&single=true&output=csv"
#url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCglOgkctIpKG5I35Ti7EuYg_ENYStsNxqFeLIIUzEnF4zy84618qldL7OCDYApiAhe-nti4cUrveC/pub?output=csv"
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtBLKwDW2dptdumtvgvqG6yYuQzMOVA1H2gN_StaJ0gcI3XGhOYZHlQWu9UF9P1G1vaHz6rdEKko2X/pub?gid=835474486&single=true&output=csv"
data_dir = "../content/alt_all_people/"
target_dir = "../content/alt_people/"

# Run options
hard_reset = True

# Get ORCID website url
def getOrcidURL(entry):
    orcid = entry['ORCID ID (if available)']
    if not orcid:
        return "mailto:"+entry['Email']
    if not "orcid.org" in str(orcid):
        orcid = "https://orcid.org/"+str(orcid)
    return orcid

# Get area for web
def getArea(entry):
    form_area = entry['Area(s) of Expertise']
    output_area = ""
    for val in form_area.split(", "):
        if not output_area == "":
            output_area += ", "
        if val == "Experimental Particle Physics": output_area += "Experiment"
        elif val == "Theoretical Particle Physics": output_area += "Theory"
        elif val == "Accelerator Physics": output_area += "Accelerator"
        else: output_area += val
    return output_area

def getPosition(entry):
    form_position = entry['Position']
    if form_position == "Graduate Student": return "Grad Student"
    if form_position == "Undergraduate Student": return "Undergrad"
    return form_position

# Make alphanumeric tags to ID institutes
def getInstTag(inst):
    inst = inst.lower()
    result = re.sub('[\W_]+', '', inst)
    result = "alt"+result #FIXME
    return result

# Get data and list of institutes and sort by size
df = pd.read_csv(url)
institutions = df['Primary Affiliation'].value_counts().index.tolist()

# Remove everything if hard_reset
if hard_reset:
    for f in glob.glob(f"{data_dir}*"):
        shutil.rmtree(f)

# Loop over people
for i, entry in df.iterrows():

    if entry['Public'] == 'Opt out': continue

    # Put data in paths based on the person's name
    fname = f"{entry['First Name']}{entry['Last Name']}".replace(" ","")
    person_path = f"{data_dir}{fname}/"
    if not os.path.exists(person_path): os.mkdir(person_path)
    print("Adding", fname)

    # Try to access photo from spreadsheet if it's not already there
    if not os.path.exists(f"{person_path}/feature_{fname}.*"):
        got_photo = False

        # Start by just checking the saved photos directory
        photos = glob.glob(f"saved_photos/{fname}*")
        if len(photos)>0:
            shutil.copy(photos[0], f"{person_path}featured.png")
            got_photo = True

        # If there's nothing there, use the spreadsheet
        if not got_photo:
            photo_url = entry['Photo link']
            if not pd.isna(photo_url):
                file_id = photo_url.split("id=")[-1] # https://drive.google.com/open?id=1STvUG313HJuftNQdrq4gY0rWIEDHF_3g
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                try:
                    response = requests.get(download_url)
                    response.raise_for_status()
                    image_data = response.content

                    # Detect image format
                    image = Image.open(BytesIO(image_data))
                    extension = image.format.lower()  # e.g., "jpeg", "png"
                    if not extension:
                        print(f"Could not detect image type for", fname)
                    else:
                        # Save file with detected extension
                        filename = f"saved_photos/{fname}.{extension}"
                        with open(filename, 'wb') as f:
                            f.write(image_data)
                        shutil.copy(f"saved_photos/{fname}.{extension}", f"{data_dir}{fname}/feature_{fname}.{extension}")
                        got_photo = True
                except:
                    print("Failed to retrieve image for", fname)

        # If this fails, copy the default photo to their path
        if not got_photo:
            shutil.copy("featured.png", f"{person_path}featured.png")

    # Create index file with all the person's info
    with open(f"{person_path}index.md", "w") as f:
        f.write("---\n")
        f.write(f"title: {entry['First Name']} {entry['Last Name']}\n")
        f.write(f"externalUrl: {getOrcidURL(entry)}\n")
        f.write(f"summary: {getPosition(entry)}, {getArea(entry)}\n")
        f.write(f"type: {getInstTag(entry['Primary Affiliation'])}\n")
        #f.write("showHero: true\n")
        f.write("---\n")

# Create main index file for ultimate site
output_file = f"{target_dir}/index.md"
with open(output_file, "w") as f:
    f.write("---\n")
    f.write("title: Meet the members of the US Muon Collider Collaboration\n")
    #f.write("layout: simple\n")
    f.write("---\n")

    f.write("\n\nIf you'd like to join the collaboration, [reach out to us](mailto:usmcc_coord@fnal.gov).")
    for inst in institutions:
        f.write("\n\n")
        #print(inst, "...")
        f.write(f"## {inst}\n")
        f.write(f'{{{{< people limit=20 title=" " cardView=true where="Type" value="{getInstTag(inst)}" >}}}}\n')
    f.write("\n\nIf you'd like to join the collaboration, [reach out to us](mailto:usmcc_coord@fnal.gov).")


