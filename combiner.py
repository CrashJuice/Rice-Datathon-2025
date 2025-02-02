import json
import csv

# File paths (update with actual paths)
geojson_file = "counties.geojson"  # Your GeoJSON file
lila_csv_file = "LILAavgFinal.csv"  # LILA data CSV
combined_csv_file = "combineddatafinal.csv"  # Additional data CSV
output_file = "us_counties_slim.geojson"  # Merged output file

# Step 1: Load LILA Data into a Dictionary (FIPS -> Avg_LILATracts)
data_dict = {}
with open(lila_csv_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fips_code = row["FIPS"].zfill(5)  # Ensure 5-digit FIPS
        data_dict[fips_code] = {"Avg_LILATracts": float(row["Avg_LILATracts"])}  # Convert to float



# Step 3: Load GeoJSON File
with open(geojson_file, "r", encoding="utf-8") as file:
    geojson_data = json.load(file)

# Step 4: Merge Data into GeoJSON
for feature in geojson_data["features"]:
    geoid = feature["properties"]["GEOID"]  # Get GEOID from GeoJSON
    if geoid in data_dict:
        feature["properties"].update(data_dict[geoid])  # Merge all data into properties

# Step 5: Save Updated GeoJSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(geojson_data, file, indent=4)

print("Merging complete. Saved as:", output_file)
