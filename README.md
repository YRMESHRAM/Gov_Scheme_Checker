# 🏛️ Gov Scheme Finder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com)
[![Semantic Web](https://img.shields.io/badge/RDF-SPARQL-orange.svg)](#)

> **🎓 Academic Project: Semantic Web & Social Networks (SWSN)**  
> Developed to demonstrate the practical application of Ontologies and Linked Data in e-governance.

---

## 📖 Project Overview

**Gov Scheme Finder** is a Semantic Web application designed to solve the difficulty citizens face in finding relevant government schemes across scattered platforms. 

Unlike traditional keyword-based search engines, this project uses **RDF (Resource Description Framework)** and **SPARQL** to understand the *context* of a user's query. This allows the system to intelligently distinguish between "State" and "Central" schemes, filter by specific beneficiary categories, and deliver highly relevant results.

## 🚀 Key Features

* **🧠 Semantic Search Engine:** Utilizes a custom-built Knowledge Base (`.ttl`) to map complex relationships between schemes, beneficiaries, and geographical regions.
* **⚡ Instant Lookup:** Implements in-memory graph caching to ensure millisecond-latency search results.
* **🔗 Direct Application Links:** Automatically fetches and validates official application URLs for easy access.
* **📝 Smart Data Formatting:** Dynamically converts unstructured text blocks into structured, readable bullet points.
* **📍 State vs. Central Filtering:** Employs intelligent inference logic to accurately determine a scheme's jurisdiction.

## 🛠️ Technologies Used

| Category | Technology |
| :--- | :--- |
| **Backend** | Python, Flask |
| **Semantic Web Stack** | `rdflib`, SPARQL, Turtle (`.ttl`) format |
| **Data Processing** | Pandas (CSV to RDF conversion) |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Jinja2 Templating |

---

## ⚙️ Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites
Ensure you have Python 3.8 or higher installed on your system.

### Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YRMESHRAM/Gov_Scheme_Checker.git](https://github.com/YRMESHRAM/Gov_Scheme_Checker.git)
   cd Gov_Scheme_Checker