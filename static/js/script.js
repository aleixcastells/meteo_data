function submitData() {
    // Pre-process inputs

    let location_enabled_select = document.getElementById('location_enabled_select').value
    let location_name_input = document.getElementById('location_name_input').value
    let location_groups_input = document.getElementById('location_groups_input').value
    let location_coordinates_input = document.getElementById('location_coordinates_input').value
    let currents_coordinates_input = document.getElementById('currents_coordinates_input').value
    let location_exposure_range_a_input = parseInt(document.getElementById('location_exposure_range_a_input').value)
    let location_exposure_range_b_input = parseInt(document.getElementById('location_exposure_range_b_input').value)
    let refresh_rate_input = parseInt(document.getElementById('refresh_rate_input').value)

    const data = {
        location_enabled: Boolean(location_enabled_select),
        location_name: location_name_input,
        location_groups: location_groups_input.split(','),
        location_longitude: parseFloat(location_coordinates_input.split(',')[1]),
        location_latitude: parseFloat(location_coordinates_input.split(',')[0]),
        currents_longitude: parseFloat(currents_coordinates_input.split(',')[1]),
        currents_latitude: parseFloat(currents_coordinates_input.split(',')[0]),
        location_exposure_range: [location_exposure_range_a_input, location_exposure_range_b_input],
        refresh_rate: refresh_rate_input
    };

    console.log(data)

    // Validate or manipulate data as needed
    // For example: simple validation
    if (
        !data.location_enabled ||
        data.location_name == "" ||
        data.location_groups == "" ||
        isNaN(data.location_longitude) ||
        isNaN(data.location_latitude) ||
        isNaN(data.currents_longitude) ||
        isNaN(data.currents_latitude) ||
        isNaN(data.location_exposure_range[0]) ||
        isNaN(data.location_exposure_range[1]) ||
        isNaN(data.refresh_rate)
    ) {
        alert("Please fill out all fields correctly.");
        return;
    }

    // Send data to Flask using fetch
    fetch('http://localhost:5001/process_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            console.log(result); // Handle the response from Flask
            alert("Data submitted successfully!");
        })
        .catch(error => console.error('Error:', error));
}

function checkCurrents(inputId) {
    navigator.clipboard.readText().then(
        clipText => {

            let reducedCoords = coordReduce(clipText, 5);
            document.getElementById(inputId).value = reducedCoords;


            // Ensure the coordinates are valid before proceeding
            let coordinatesInput = document.getElementById(inputId).value;

            if (!coordinatesInput.includes(",")) {
                alert("Please enter valid coordinates in the format 'latitude,longitude'.");
                return;
            }

            let longitude = coordinatesInput.split(',')[1].trim();
            let latitude = coordinatesInput.split(',')[0].trim();

            if (isNaN(longitude) || isNaN(latitude)) {
                alert("Invalid coordinates format. Please ensure they are numbers.");
                return;
            }

            // Send the data to Flask using fetch
            fetch('http://localhost:5001/check_currents', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    currents_longitude: parseFloat(longitude),
                    currents_latitude: parseFloat(latitude)
                })
            })
                .then(response => response.json())
                .then(result => {
                    // Show an alert with the result (True or False)
                    if (result.result) { document.getElementById("currents_ok_sign").innerText = "🟢"; }
                    else { document.getElementById("currents_ok_sign").innerText = "🔴"; }
                })
                .catch(error => console.error('Error:', error));
        }
    ).catch(err => {
        console.error('Failed to read clipboard contents: ', err);
    });
}


function pasteLocation(inputId) {
    // Access the clipboard and read the content
    navigator.clipboard.readText().then(
        clipText => {
            // Reduce the precision of the coordinates to 4 decimal places
            let reducedCoords = coordReduce(clipText, 5);

            // Set the reduced string into the specified input field
            document.getElementById(inputId).value = reducedCoords;
        }
    ).catch(err => {
        console.error('Failed to read clipboard contents: ', err);
    });
}

function coordReduce(coordinates, decimalPlaces) {
    // Split the coordinates string into latitude and longitude
    let coords = coordinates.split(',');

    // Ensure the input string has two parts: latitude and longitude
    if (coords.length !== 2) {
        alert("Please enter valid coordinates in the format 'latitude,longitude'.");
        return null;
    }

    // Convert and fix the latitude and longitude to the specified number of decimal places
    let latitude = parseFloat(coords[0].trim());
    let longitude = parseFloat(coords[1].trim());

    if (isNaN(latitude) || isNaN(longitude)) {
        alert("Invalid coordinates format. Please ensure they are numbers.");
        return null;
    }

    // Reduce the precision to the specified number of decimal places
    latitude = latitude.toFixed(decimalPlaces);
    longitude = longitude.toFixed(decimalPlaces);

    // Combine them back into a string
    return `${latitude}, ${longitude}`;
}
