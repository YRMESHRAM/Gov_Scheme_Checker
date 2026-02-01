import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import XSD
import urllib.parse
import os
import re

# ===============================
# 1. LOAD DATASET
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "updated_data.csv")

try:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    print(f"✅ Dataset loaded. Found {len(df)} schemes.")
except FileNotFoundError:
    print("❌ Error: 'updated_data.csv' not found.")
    exit()

# ===============================
# 2. SETUP GRAPH
# ===============================
GOV = Namespace("http://example.org/gov-schemes#")
g = Graph()
g.bind("gov", GOV)

indian_states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Puducherry", "Delhi", "Ladakh", "Jammu and Kashmir"
]

print("⚙️  Building Ontology...")

for index, row in df.iterrows():
    
    scheme_name = str(row['scheme_name']).strip()
    
    # --- FIX: ROBUST SLUG GENERATION ---
    # Keep only letters and numbers for the link ID
    clean_slug = re.sub(r'[^a-zA-Z0-9]', '-', scheme_name).lower()
    clean_slug = re.sub(r'-+', '-', clean_slug).strip('-') # Remove duplicate dashes
    
    scheme_uri = URIRef(f"http://example.org/gov-schemes#{clean_slug}")

    # Add Basic Info
    g.add((scheme_uri, RDF.type, GOV.Scheme))
    g.add((scheme_uri, GOV.hasName, Literal(scheme_name, datatype=XSD.string)))
    g.add((scheme_uri, GOV.hasSlug, Literal(clean_slug))) # Save the clean ID

    # Detect State
    details_text = str(row.get('details', ''))
    search_context = (scheme_name + " " + details_text).title()
    detected_state = "Central"
    for state in indian_states:
        if state in search_context:
            detected_state = state
            break
    g.add((scheme_uri, GOV.belongsToState, Literal(detected_state)))

    # Add Details (Benefits, Eligibility, etc.)
    for field, predicate in [
        ('benefits', GOV.providesBenefit),
        ('eligibility', GOV.hasEligibility),
        ('application_process', GOV.hasApplication),
        ('Required documents', GOV.requiresDocument),
        ('application_link', GOV.hasLink)
    ]:
        val = row.get(field, None)
        if pd.notna(val) and str(val).lower() != 'nan' and str(val).strip() != "":
            # Clean up the text slightly before saving
            clean_text = str(val).replace('﻿', '').strip()
            g.add((scheme_uri, predicate, Literal(clean_text)))

    # Keywords for Search
    tags = str(row.get('tags', ''))
    category = str(row.get('schemeCategory', ''))
    searchable_text = f"{scheme_name} {tags} {category} {detected_state}".lower()
    g.add((scheme_uri, GOV.hasKeywords, Literal(searchable_text)))

# ===============================
# 3. SAVE FILE
# ===============================
output_file = os.path.join(BASE_DIR, "schemes_knowledge_base.ttl")
g.serialize(destination=output_file, format="turtle")
print(f"🎉 Ontology Rebuilt! Saved to '{output_file}'.")
print("👉 NOW: Run 'python app.py' to see the changes.")