"""Populate the website's People page from the USMCC membership database.

Fetches the public member export of the collaboration database
(https://db.muoncollider.us) and writes one Hugo content folder per member
under content/all_people/ plus the content/people/index.md overview. The
database serves only members who are active AND consented to being listed
publicly (and only their public photo), so nobody who opted out can appear
here — don't work around it by hand-editing the generated files.

Photos come from the database too. A member without a database photo falls
back to a file in saved_photos/ named after them (FirstLast.jpg/png/...),
then to the default featured.png.

Run `python getPeople.py` from within the scripts directory.
"""

import glob
import os
import re
import shutil
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from pillow_heif import register_heif_opener

import resizePhotos

register_heif_opener()  # Add HEIC/HEIF support to PIL (saved_photos fallbacks)

# Path options
API_URL = os.environ.get("USMCCDB_API", "https://db.muoncollider.us/api/v1")
data_dir = "../content/all_people/"
target_dir = "../content/people/"

# Run options
hard_reset = True

# Database career-stage enum -> label shown on the card.
CAREER_LABELS = {
    "faculty": "Faculty",
    "staff": "Lab Scientist",
    "postdoc": "Postdoc",
    "grad": "Grad Student",
    "undergrad": "Undergrad",
    "engineer": "Engineer",
    "other": "Other",
}

# Database research areas -> short labels for the card and the area chart.
AREA_LABELS = {
    "Experimental Particle Physics": "Experiment",
    "Theoretical Particle Physics": "Theory",
    "Accelerator Physics": "Accelerator",
    "Other": "Other",
}


# Get ORCID website url (members without an ORCID iD get no external link)
def getOrcidURL(person):
    orcid = person.get("orcid")
    return f"https://orcid.org/{orcid}" if orcid else None


# Get area for web
def getArea(person):
    values = [a.strip() for a in (person.get("research_areas") or "").split(",") if a.strip()]
    labels = []
    for val in values:
        label = AREA_LABELS.get(val, val)
        if label not in labels:
            labels.append(label)
    return ", ".join(labels)


def getPosition(person):
    return CAREER_LABELS.get(person.get("career_stage"), "Other")


# Make alphanumeric tags to ID institutes
def getInstTag(inst):
    inst = inst.lower()
    result = re.sub(r'[\W_]+', '', inst)
    return result


# Directory-safe version of a member's name
def getFname(person):
    return re.sub(r'[^\w.-]', '', person["name"].replace(" ", ""))


def getPhoto(person, fname, person_path):
    """Put featured.<ext> in the person's folder: the database photo first,
    then a saved_photos/<fname>.* file, then the default image."""
    if glob.glob(f"{person_path}featured.*"):
        return

    # The database serves the photo only while the member is listed; it is
    # already normalized (WebP, capped size) — re-encode to JPEG for Hugo.
    if person.get("has_photo"):
        try:
            r = requests.get(f"{API_URL}/people/public/{person['id']}/photo", timeout=60)
            r.raise_for_status()
            img = Image.open(BytesIO(r.content)).convert("RGB")
            dest = f"{person_path}featured.jpg"
            img.save(dest, "JPEG", quality=90)
            resizePhotos.process_image(dest)
            return
        except Exception as e:
            print(f"Failed to retrieve database photo for {fname}: {e}")

    photos = [p for p in sorted(glob.glob(f"saved_photos/{fname}.*")) if not p.endswith(".tmp")]
    if photos:
        extension = photos[0].split(".")[-1]
        dest = f"{person_path}featured.{extension}"
        shutil.copy(photos[0], dest)
        if extension.lower() == "mpo":
            resizePhotos.convert_mpo_to_jpeg(Path(dest))
            dest = f"{person_path}featured.jpg"
        elif extension.lower() in ("heif", "heic"):
            resizePhotos.convert_heic_to_png(Path(dest))
            dest = f"{person_path}featured.png"
        resizePhotos.process_image(dest)
        return

    shutil.copy("featured.png", f"{person_path}featured.png")


# Get data and list of institutes and sort alphabetically
people = requests.get(f"{API_URL}/people/public", timeout=60).json()
stats = requests.get(f"{API_URL}/people/public/stats", timeout=60).json()
institutions = sorted({p["institution"] for p in people if p.get("institution")})

# Remove everything if hard_reset
if hard_reset:
    for f in glob.glob(f"{data_dir}*"):
        shutil.rmtree(f)

# The chart counts come from the anonymous stats endpoint, which covers ALL
# active members — including those who keep their names off this page — so
# the pies reflect the whole collaboration, not just the cards below them.
# (Separate buckets per chart: the old single dict silently merged its two
# "Other" keys, so both pies shared one combined Other count.)
by_area = stats["by_research_area"]
by_stage = stats["by_career_stage"]
area_counters = {
    "Accelerator": by_area.get("Accelerator Physics", 0),
    "Experiment": by_area.get("Experimental Particle Physics", 0),
    "Theory": by_area.get("Theoretical Particle Physics", 0),
    "Multiple": by_area.get("Multiple", 0),
}
# "Other" answers plus members with no recorded area.
area_counters["Other"] = stats["total"] - sum(area_counters.values())
career_counters = {
    "Faculty": by_stage.get("faculty", 0),
    "Lab Scientist": by_stage.get("staff", 0),
    "Grad Student": by_stage.get("grad", 0),
    "Undergrad": by_stage.get("undergrad", 0),
    "Postdoc": by_stage.get("postdoc", 0),
}
# Engineers and "other" career stages share the chart's Other slice.
career_counters["Other"] = stats["total"] - sum(career_counters.values())

# Loop over people
for person in people:

    if not person.get("institution"):
        print(f"Skipping {person['name']}: no current institution in the database")
        continue

    # Put data in paths based on the person's name
    fname = getFname(person)
    person_path = f"{data_dir}{fname}/"
    if not os.path.exists(person_path): os.mkdir(person_path)
    print("Adding", fname)

    getPhoto(person, fname, person_path)

    # Create index file with all the person's info
    position = getPosition(person)
    area = getArea(person)
    external_url = getOrcidURL(person)
    with open(f"{person_path}index.md", "w") as f:
        f.write("---\n")
        f.write(f"title: {person['name']}\n")
        if external_url:
            f.write(f"externalUrl: {external_url}\n")
        f.write(f"summary: {position}, {area}\n" if area else f"summary: {position}\n")
        f.write(f"type: {getInstTag(person['institution'])}\n")
        #f.write("showHero: true\n")
        f.write("---\n")

# Create main index file for ultimate site
output_file = f"{target_dir}/index.md"
with open(output_file, "w") as f:
    f.write("---\n")
    f.write("title: Meet the members of the US Muon Collider Collaboration\n")
    #f.write("layout: simple\n")
    f.write("---\n")

    f.write('<div style="display: flex; gap: 3rem; text-align: center;">\n')
    f.write('<div style="flex: 1;">\n')
    f.write('Area\n')
    f.write("{{< chart >}}\n")
    f.write("type: 'pie',\n")
    f.write("data: {\n")
    f.write("  labels: ['Accelerator', 'Experiment', 'Theory', 'Multiple', 'Other'],\n")
    f.write("  datasets: [{\n")
    f.write("	label: '# of members',\n")
    f.write(f"	data: [{area_counters['Accelerator']}, {area_counters['Experiment']}, {area_counters['Theory']}, {area_counters['Multiple']}, {area_counters['Other']}],\n")
    f.write("	backgroundColor: [\n")
    f.write("	  'rgba(255, 99, 132, 0.2)',\n")
    f.write("	  'rgba(255, 159, 64, 0.2)',\n")
    f.write("	  'rgba(255, 205, 86, 0.2)',\n")
    f.write("	  'rgba(75, 192, 192, 0.2)',\n")
    f.write("	  'rgba(54, 162, 235, 0.2)',\n")
    f.write("	  'rgba(153, 102, 255, 0.2)',\n")
    f.write("	  'rgba(201, 203, 207, 0.2)'\n")
    f.write("	],\n")
    f.write("	borderColor: [\n")
    f.write("	  'rgb(255, 99, 132)',\n")
    f.write("	  'rgb(255, 159, 64)',\n")
    f.write("	  'rgb(255, 205, 86)',\n")
    f.write("	  'rgb(75, 192, 192)',\n")
    f.write("	  'rgb(54, 162, 235)',\n")
    f.write("	  'rgb(153, 102, 255)',\n")
    f.write("	  'rgb(201, 203, 207)'\n")
    f.write("	],\n")
    f.write("  }]\n")
    f.write("}\n")
    f.write("{{< /chart >}}\n")
    f.write('</div>\n')

    f.write('<div style="flex: 1;">\n')
    f.write('Career Stage\n')
    f.write("{{< chart >}}\n")
    f.write("type: 'pie',\n")
    f.write("data: {\n")
    f.write('  labels: ["Faculty", "Lab Scientist", "Grad Student", "Undergrad", "Postdoc", "Other"],\n')
    f.write("  datasets: [{\n")
    f.write("	label: '# of members',\n")
    f.write(f"	data: [{career_counters['Faculty']}, {career_counters['Lab Scientist']}, {career_counters['Grad Student']}, {career_counters['Undergrad']}, {career_counters['Postdoc']}, {career_counters['Other']}],\n")
    f.write("	backgroundColor: [\n")
    f.write("	  'rgba(255, 99, 132, 0.2)',\n")
    f.write("	  'rgba(255, 159, 64, 0.2)',\n")
    f.write("	  'rgba(255, 205, 86, 0.2)',\n")
    f.write("	  'rgba(75, 192, 192, 0.2)',\n")
    f.write("	  'rgba(54, 162, 235, 0.2)',\n")
    f.write("	  'rgba(153, 102, 255, 0.2)',\n")
    f.write("	  'rgba(201, 203, 207, 0.2)'\n")
    f.write("	],\n")
    f.write("	borderColor: [\n")
    f.write("	  'rgb(255, 99, 132)',\n")
    f.write("	  'rgb(255, 159, 64)',\n")
    f.write("	  'rgb(255, 205, 86)',\n")
    f.write("	  'rgb(75, 192, 192)',\n")
    f.write("	  'rgb(54, 162, 235)',\n")
    f.write("	  'rgb(153, 102, 255)',\n")
    f.write("	  'rgb(201, 203, 207)'\n")
    f.write("	],\n")
    f.write("  }]\n")
    f.write("}\n")
    f.write("{{< /chart >}}\n")
    f.write('</div>\n')
    f.write('</div>\n')

    f.write("\n\nIf you'd like to join the collaboration, [reach out to us](mailto:usmcc-coord@fnal.gov).")
    for inst in institutions:
        f.write("\n\n")
        f.write(f"## {inst}\n")
        f.write(f'{{{{< people limit=2000 title=" " cardView=true where="Type" value="{getInstTag(inst)}" >}}}}\n')
    f.write("\n\nIf you'd like to join the collaboration, [reach out to us](mailto:usmcc-coord@fnal.gov).")
