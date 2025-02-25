# Genetic Data Lake Project

This project is an end-to-end synthetic genetic data lake designed to mimic real-world ancestry and genomic databases. It demonstrates a complete data pipeline—from data generation, ingestion, and storage to interactive visualization—using PostgreSQL, Docker, and Streamlit. The project integrates diverse datasets (individual demographics, family relationships, genetic variants, health metrics, and lifestyle information) to simulate how genetic data can be used in research and personalized medicine.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Data Generation](#data-generation)
- [Data Model](#data-model)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [ETL Process](#etl-process)
  - [Docker Compose Setup](#docker-compose-setup)
  - [Running the Streamlit Dashboard](#running-the-streamlit-dashboard)
- [Usage](#usage)
- [Project Explanation](#project-explanation)
- [License](#license)

---

## Overview

This project simulates a genetic data lake with multiple layers of information:

- **Individuals:** Detailed profiles with demographics and geographic data.
- **Relationships:** Parent-child connections to build family trees.
- **Marriages:** Marriage records with marriage and divorce dates.
- **SNP Definitions:** A catalog of single nucleotide polymorphisms (SNPs), which are tiny differences in the DNA code.
- **Indel Definitions & Genotypes:** Details about small insertions and deletions (indels) and the corresponding genotype data.
- **Structural Variants:** Records of large-scale genomic alterations.
- **Health Phenotypes:** Health and physical measurements (e.g., BMI, height, weight, blood type).
- **Lifestyle:** Information on lifestyle choices and occupations.

The accompanying Streamlit dashboard provides an interactive interface to explore the data, visualize trends, and gain insights into genetic patterns, health attributes, and lifestyle correlations.

---

## Project Structure

```
genetic_data_lake_project/
├── data_generation/         # Contains scripts for generating synthetic datasets
├── data_lake/               # Contains pre-generated CSV files (input data)
├── etl_load_csvs.py         # ETL script to load CSVs into PostgreSQL
├── docker-compose.yml       # Docker Compose configuration for PostgreSQL and Streamlit
└── streamlit_app/           # Contains the Streamlit dashboard code
    ├── Dockerfile           # Dockerfile for building the Streamlit container
    ├── requirements.txt     # Python dependencies for the Streamlit app
    └── app.py               # Main Streamlit dashboard application
```

---

## Data Generation

### How the Fake Data Was Created

The dataset was generated using a Python-based simulation engine designed to create realistic but completely synthetic genetic and demographic data. This process involved:

1. **Individuals Generation**
   - Used randomized distributions to create demographic details such as gender, birth year, and geographic location.
   - Each individual was assigned a unique ID.
   - Sample collection dates and sequencing coverage were simulated.

2. **Family Tree Simulation**
   - Parent-child relationships were generated using probability-based inheritance models.
   - Marriage and divorce records were assigned based on statistical trends.

3. **Genetic Variants**
   - **SNPs:** Created using a reference catalog of common genetic markers, assigning each individual a random but statistically realistic set of alleles.
   - **Indels & Structural Variants:** Simulated insertion/deletion events and large genomic changes.

4. **Health & Lifestyle**
   - Traits such as height, weight, blood type, and disease risk were assigned based on a mix of genetics and random environmental factors.
   - Lifestyle data (e.g., smoking, drinking, exercise habits) were simulated using probability models.

### Why This Matters
- The dataset is **realistic** but completely **synthetic**, meaning it does not contain any actual human data.
- It provides a **safe way** to work with genetic datasets without privacy concerns.
- The structure mirrors real-world genetic databases, making it useful for **data engineering and analytics**.

---

## Data Model

### 1. Individuals
- **Contains:**  
  Unique IDs, names, gender, birth date, location, sample collection date, sequencing coverage, and consent status.
- **Simple Explanation:**  
  A digital "profile" for each person, similar to an enriched contact list for genetic research.

### 2. Relationships
- **Contains:**  
  Parent-child links showing familial connections.
- **Simple Explanation:**  
  A family tree that helps study genetic inheritance.

### 3. Marriages
- **Contains:**  
  Marriage records including partner IDs, marriage dates, and divorce dates.
- **Simple Explanation:**  
  Information on family structures that can affect genetic inheritance.

### 4. SNP Definitions
- **Contains:**  
  A catalog of SNPs (single-letter differences in DNA) with allele variants, frequencies, and genomic locations.
- **Simple Explanation:**  
  A "dictionary" of tiny genetic variations that can influence traits and disease risks.

### 5. Indel Definitions & Genotypes
- **Contains:**  
  Details on small insertions and deletions in the DNA, along with genotype data showing which version each person carries.
- **Simple Explanation:**  
  Records of small DNA "edits" that can affect how genes function.

### 6. Structural Variants
- **Contains:**  
  Information on large-scale genomic changes like deletions, duplications, and rearrangements.
- **Simple Explanation:**  
  Big changes in the DNA that can have major impacts on an organism’s traits and health.

### 7. Health Phenotypes
- **Contains:**  
  Health metrics such as height, weight, BMI, eye color, blood type, and disease indicators.
- **Simple Explanation:**  
  A set of physical and health measurements similar to a medical record.

### 8. Lifestyle
- **Contains:**  
  Data on lifestyle factors including smoking, alcohol consumption, exercise, and occupation.
- **Simple Explanation:**  
  Information on daily habits that may interact with genetic predispositions.

---

## Setup and Installation

### Prerequisites

- **Docker Desktop:** Download from [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- **Python 3.9+** (if running locally)
- **PostgreSQL:** (If using Docker Compose, the PostgreSQL container is used.)

### ETL Process

1. **Place CSV Files:**
   - Copy all pre-generated CSV files into the `data_lake` folder.
2. **Run the ETL Script:**
   ```bash
   python etl_load_csvs.py
   ```
   - This script loads the CSV files into your PostgreSQL database in chunks.

### Docker Compose Setup

1. **Start Containers:**
   ```bash
   docker-compose up --build
   ```

### Running the Streamlit Dashboard

- **Using Docker:**  
  Access the app at [http://localhost:8501](http://localhost:8501).
- **Running Locally:**  
  ```bash
  streamlit run app.py
  ```

---

## Project Explanation

### Biological and Genetic Concepts Explained Simply

- **SNPs (Single Nucleotide Polymorphisms):**  
  Tiny variations in the DNA code—imagine a single letter typo in a long sentence. They are common and can affect traits and disease risks.

- **Indels (Insertions and Deletions):**  
  Small sections of DNA that are either inserted or removed, similar to adding or deleting words in a sentence, which can alter gene function.

- **Structural Variants:**  
  Large-scale changes in the genome such as deletions or duplications, which can have a significant impact on an organism’s traits.

- **Health Phenotypes & Lifestyle Data:**  
  Physical measurements (like height and weight) and lifestyle choices (such as smoking and occupation) help us study how genetics and environment together influence health.

- **Family Relationships & Marriages:**  
  These tables create a family tree, showing how genetic traits are inherited through generations.

---

## License

This project is provided "as is" for educational and portfolio purposes.

---

## Final Summary

This project showcases skills in **data engineering, containerization, and interactive analytics**. It integrates complex datasets into a PostgreSQL database and presents them through an interactive Streamlit dashboard. Complex genetic concepts are explained in simple terms, making the project accessible to both technical and non-technical audiences.
