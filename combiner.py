import json
import csv


geojson_file = "counties.geojson"  
lila_csv_file = "LILAavgFinal.csv"  
combined_csv_file = "combineddatafinal.csv"  
output_file = "us_counties_slim.geojson"  


columns_to_grab = [9,21,25,24,28]
data_dict = {}
with open(lila_csv_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fips_code = row["FIPS"].zfill(5)  
        data_dict[fips_code] = {"Avg_LILATracts": float(row["Avg_LILATracts"])}  


with open(combined_csv_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fips_code = row["FIPS"].zfill(5)  
        if fips_code not in data_dict:
            data_dict[fips_code] = {}  
        
        
        for idx in columns_to_grab:
            key = list(row.keys())[idx]  
            try:
                data_dict[fips_code][key] = float(row[key])  
            except ValueError:
                data_dict[fips_code][key] = row[key]  


with open(geojson_file, "r", encoding="utf-8") as file:
    geojson_data = json.load(file)


for feature in geojson_data["features"]:
    geoid = feature["properties"]["GEOID"]  
    if geoid in data_dict:
        
        feature["properties"].update(data_dict[geoid])

        
        keys_to_remove = ["STATEFP", "COUNTYFP", "COUNTYNS", "AFFGEOID","GEOID","LSAD","ALAND","AWATER"]
        for key in keys_to_remove:
            if key in feature["properties"]:
                del feature["properties"][key]


with open(output_file, "w", encoding="utf-8") as file:
    json.dump(geojson_data, file, indent=4)

print("Merging complete. Saved as:", output_file)
