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

green_skills = pd.read_csv(
    green_skills_file,
    usecols=[
        # "conceptType",
        "conceptUri",
        "preferredLabel",
        # "status",
        "skillType",
        "reuseLevel",
        # "altLabels",
        "description",
        "broaderConceptUri",
        "broaderConceptPT",
    ],
    index_col=["conceptUri"],
)

occupations = pd.read_csv(
    "data/occupations_fr.csv",
    usecols=[
        # "conceptType",
        "conceptUri",
        # "iscoGroup",
        "preferredLabel",
        # "altLabels",
        # "hiddenLabels",
        # "status",
        # "modifiedDate",
        # "regulatedProfessionNote",
        # "scopeNote",
        # "definition",
        # "inScheme",
        # "description",
        "code",
    ],
    index_col=["conceptUri"],
).rename(
    columns={
        "preferredLabel": "occupationLabel",
        # "description": "occupationDescription",
        "code": "iscoCode",
    }
)

occupation_skill_relations = pd.read_csv(
    "data/occupationSkillRelations_fr.csv",
    usecols=[
        "occupationUri",
        "relationType",
        # "skillType",
        "skillUri",
    ],
    index_col=["skillUri"],
)

df = (
    green_skills.join(occupation_skill_relations)
    .reset_index()
    .set_index("occupationUri")
    .join(occupations, how="inner")
    .reset_index()
    .set_index(["preferredLabel"])
    .drop(columns=["occupationUri", "conceptUri", "broaderConceptUri"])
)


os.makedirs("outputs", exist_ok=True)
df.to_excel("outputs/filtered_data.xlsx")
