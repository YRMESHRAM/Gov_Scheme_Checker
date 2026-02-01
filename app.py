import os
import re
from flask import Flask, render_template, request
from rdflib import Graph, Namespace, URIRef

app = Flask(__name__)

# ==========================================
# 1. LOAD & CACHE DATA (ONCE AT STARTUP)
# ==========================================
ONTOLOGY_FILE = "schemes_knowledge_base.ttl"
g = Graph()
GOV = Namespace("http://example.org/gov-schemes#")

# Global list to store all schemes in memory (RAM)
ALL_SCHEMES = []

def load_data():
    """Loads RDF data into a simple Python list for instant searching."""
    global ALL_SCHEMES
    
    if not os.path.exists(ONTOLOGY_FILE):
        print("❌ Error: schemes_knowledge_base.ttl missing.")
        return

    print("⏳ Loading Knowledge Base... Please wait.")
    g.parse(ONTOLOGY_FILE, format="turtle")
    
    # Pre-fetch all schemes using one SPARQL query at startup
    query = """
    PREFIX gov: <http://example.org/gov-schemes#>
    SELECT ?name ?slug ?benefit ?url ?state ?keywords WHERE {
        ?scheme a gov:Scheme ;
                gov:hasName ?name ;
                gov:hasSlug ?slug ;
                gov:hasKeywords ?keywords .
        OPTIONAL { ?scheme gov:providesBenefit ?benefit } .
        OPTIONAL { ?scheme gov:hasLink ?url } .
        OPTIONAL { ?scheme gov:belongsToState ?state } .
    }
    """
    results = g.query(query)
    
    # Convert to Python Dictionaries
    ALL_SCHEMES = []
    for row in results:
        ALL_SCHEMES.append({
            "name": str(row.name),
            "slug": str(row.slug),
            "benefit": str(row.benefit)[:140] + "..." if row.benefit else "View details...",
            "full_benefit": str(row.benefit), # Keep full text for details
            "url": str(row.url) if row.url else None,
            "state": str(row.state) if row.state else "Central",
            "keywords": str(row.keywords).lower() # Lowercase for fast search
        })
    
    print(f"✅ Cached {len(ALL_SCHEMES)} schemes in memory. Ready!")

# Load data immediately
load_data()

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def format_to_points(text):
    if not text or str(text) in ["None", "nan", ""]: return []
    text = str(text).replace('﻿', '').strip()
    points = re.split(r'\n|(?<=\d)\. |\.\s(?=[A-Z])|(?=Step \d:)|(?=•)|(?=\*)', text)
    return [p.strip() for p in points if len(p.strip()) > 3]

def get_value(subject_uri, predicate):
    val = g.value(subject_uri, predicate)
    return str(val) if val else None

# ==========================================
# 3. FAST ROUTES
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # ⚡ INSTANT PYTHON SEARCH (No SPARQL)
    user_state = request.form.get('state')
    user_occ = request.form.get('occupation')
    user_cat = request.form.get('category')
    
    # Filter the list using Python (Extremely fast)
    results = []
    
    for s in ALL_SCHEMES:
        # 1. Check State
        if user_state and user_state != "All":
            # Show if scheme matches State OR is Central
            if user_state.lower() not in s['state'].lower() and "central" not in s['state'].lower():
                continue # Skip this scheme

        # 2. Check Keywords (Occupation / Category)
        # If user selected an occupation, it MUST exist in keywords
        if user_occ and user_occ.lower() not in s['keywords']:
            continue
            
        # If user selected a category, it MUST exist in keywords
        if user_cat and user_cat.lower() not in s['keywords']:
            continue
        
        results.append(s)

    return render_template('results.html', schemes=results, count=len(results))

@app.route('/scheme/<path:slug>')
def scheme_detail(slug):
    # ⚡ DIRECT LOOKUP (O(1) Speed)
    scheme_uri = URIRef(f"http://example.org/gov-schemes#{slug}")
    
    # We fetch fresh details from the Graph (not the cache) to ensure we get everything
    name = get_value(scheme_uri, GOV.hasName)
    
    if not name:
        return f"<h3>Scheme Not Found</h3><p>ID: {slug}</p><a href='/'>Home</a>", 404

    scheme_info = {
        "name": name,
        "url": get_value(scheme_uri, GOV.hasLink),
        "state": get_value(scheme_uri, GOV.belongsToState) or "Central",
        "benefit": format_to_points(get_value(scheme_uri, GOV.providesBenefit)),
        "eligibility": format_to_points(get_value(scheme_uri, GOV.hasEligibility)),
        "application": format_to_points(get_value(scheme_uri, GOV.hasApplication)),
        "documents": format_to_points(get_value(scheme_uri, GOV.requiresDocument))
    }
    
    return render_template('detail.html', s=scheme_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)