# 🏛️ Gov Scheme Finder

### 🎓 Academic Project: Semantic Web & Social Networks
**Course:** Semantic Web & Social Networks (SWSN)  
**License:** MIT License  

---

## 📖 Project Overview
**Gov Scheme Finder** is a Semantic Web application developed to demonstrate the power of **Ontologies** and **Linked Data** in e-governance. Unlike traditional keyword-based search engines, this project uses **RDF (Resource Description Framework)** and **SPARQL** to understand the *context* of a user's query (e.g., distinguishing between "State" and "Central" schemes or filtering by specific beneficiary categories).

This project was built to solve the difficulty citizens face in finding relevant government schemes due to scattered information.

## 🚀 Key Features
* **🧠 Semantic Search Engine:** Utilizes a custom-built Knowledge Base (`.ttl`) to map relationships between schemes, beneficiaries, and states.
* **⚡ Instant Lookup:** Implements in-memory graph caching for millisecond-latency search results.
* **🔗 Direct Application Links:** Automatically fetches and validates official application URLs.
* **📝 Smart Data Formatting:** dynamically converts unstructured text blocks into structured, readable bullet points.
* **📍 State vs. Central Filtering:** Intelligent inference logic to determine if a scheme belongs to a specific state or the central government.

## 🛠️ Technologies Used
* **Backend:** Python (Flask)
* **Semantic Web Stack:** `rdflib`, SPARQL, Turtle (`.ttl`) format
* **Data Processing:** Pandas (CSV to RDF conversion)
* **Frontend:** HTML5, Bootstrap 5, Jinja2 Templating

## ⚙️ How to Run
1.  **Install Dependencies:**
    ```bash
    pip install flask rdflib pandas
    ```
2.  **Build the Ontology:**
    ```bash
    python build_ontology.py
    ```
3.  **Start the Server:**
    ```bash
    python app.py
    ```

## 📜 License
This project is licensed under the **MIT License**.
EOF
