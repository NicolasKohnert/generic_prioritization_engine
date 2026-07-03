Asset Priorization Engine 

This pipeline was developed to automate the priorization of infrastructure asstes and make them spatially visualizable. It serves as a bridge between raw CSV data and an intelligent decision-making foundation for BIM and GIS workflows


Objective

The project aimes to establish a transparent, automated " end-to-end" process:

-Data Processing: Validationand scoring of assets
-Historization: Traceable storage of asset state data in a SQLite database
-Connectivity: Gneration of geospatial data (GeoJSON) that can be integrated directly into ArcGIS Pro or Web-GIS applications


Insatallation

To set up the environment locally, ensure Python is installed and run the following command in your terminal
pip install -r requirements.txt


Usage

The entire project is automated for ease of use.To start the pipeline and initialize the data visualization:
1. Execute start_gis.bat with a double klick
2.The pipeline processes the data, updates the database, and automatically starts a web server
3 Open your browser at http://localhost:8000 to view the atest priorization map
