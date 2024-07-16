import os
import glob
import requests
import zipfile
import pandas as pd
from icecream import ic
from pandas import IndexSlice as idx

# Data download is not done here since it seems it requires an explicit demand to download.

dataset_file = "data/ESCO dataset - v1.2.0 - classification - fr - csv.zip"
green_skills_file = "data/greenSkillsCollection_fr.csv"

if not os.path.isfile(green_skills_file):
    print(f"Extracting {zip_filename}...")
    with zipfile.ZipFile(zip_filename, "r") as z:
        z.extractall("data")

# TODO Here properly read the
green_skills = pd.read_csv(
    green_skills_file,
    usecols=[
        # "conceptType",
        # "conceptUri",
        "preferredLabel",
        # "status",
        "skillType",
        "reuseLevel",
        # "altLabels",
        "description",
        # "broaderConceptUri",
        "broaderConceptPT",
    ],
    index_col=[
        # "conceptType",
        # "conceptUri",
        "preferredLabel",
        # "status",
        "skillType",
        "reuseLevel",
        # "altLabels",
        "description",
        # "broaderConceptUri",
        # "broaderConceptPT",
    ],
)

os.makedirs("outputs", exist_ok=True)
green_skills.to_excel("outputs/filtered_data.xlsx")
