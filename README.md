Asset Prioritization Engine 
<!-- Badges -->
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)


This pipeline was developed to automate the priorization of infrastructure assets and make them spatially visualizable. It serves as a bridge between raw CSV data and an intelligent decision-making foundation for BIM and GIS workflows


Objective

The project aims to establish a transparent, automated " end-to-end" process:

-Data Processing: Validation and scoring of assets
-Historization: Traceable storage of asset state data in a SQLite database
-Connectivity: Generation of geospatial data (GeoJSON) that can be integrated directly into ArcGIS Pro or Web-GIS applications


Installation

To set up the environment locally, ensure Python is installed and run the following command in your terminal
pip install -r requirements.txt


Usage

The entire project is automated for ease of use.To start the pipeline and initialize the data visualization:
1. Execute start_gis.bat with a double klick
2.The pipeline processes the data, updates the database, and automatically starts a web server
3 Open your browser at http://localhost:8000 to view the atest priorization map


Project Structure

/config   #config data
/data     #(locally loaded)
/engine   #corelogic
main.py   #start


Tech Stack

Languages: Python
GIS/BIM: GeoJSON, ArcGIS Integration
Data: SQLite, CSV
Tools: Git, VS Code


Contributing

Contributions are welcome"Feel free to open an issue or submit a pull request.
