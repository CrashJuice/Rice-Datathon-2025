async function loadDataAndMerge() {
    // Load GeoJSON
    const geojson = await fetch('counties.geojson').then(res => res.json());
    
    // Load your CSV data (convert to JSON format beforehand if necessary)
    const data = await fetch('county-data.json').then(res => res.json());

    // Create a map of FIPS -> Data Value
    const dataMap = {};
    data.forEach(row => {
        dataMap[row.FIPS] = row.DataPoint;
    });

    // Merge data into GeoJSON
    geojson.features.forEach(feature => {
        const fips = feature.properties.FIPS;
        feature.properties.DataValue = dataMap[fips] || 0;  // Default to 0 if missing
    });

    return geojson;
}