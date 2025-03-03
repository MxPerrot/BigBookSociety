/**
 * This programs is responsible for managing datalist-like html elements.
 * 
 * It now supports genres, and authors and any other data with an appropriate getData function
 * 
 */


async function getData(url) {
    /*
    Get the data from the get_genres & get_authors routes of the api
    */
    try {

        // Fetch data
        const response = await fetch(url);

        // Check if response is valid
        if (!response.ok) {
            throw new Error(`Erreur lors de la récupération des données : ${response.status}`);
        }

        // Parse as json (will return nested arrays normally)
        const data = JSON.parse(await response.json());
         
        // Format nested arrays as id/name table
        const dataArray = data.map(row => {
            if (!Array.isArray(row) || row.length < 2) {
                console.error("Invalid row format:", row);
                return null; // Skip invalid rows
            }
            return { id: row[0], name: row[1] }; 
        }).filter(item => item !== null); // Remove invalid rows

        return dataArray;

    } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
    }
}

function createDatalist(container_id, id, label, url) {
    // HTML

    // Create the datalist container
    const $container = $("<div>").addClass("datalist-container");

    // Create the input element with a unique ID
    const $input = $("<input>")
        .attr("type", "text")
        .attr("id", `${id}-input`)
        .addClass("datalist-input")
        .attr("placeholder", label);

    // Create the options container with a unique ID
    const $optionsContainer = $("<div>")
        .attr("id", `${id}-options`)
        .addClass("datalist-options");

    // Append elements to the container
    $container.append($input, $optionsContainer);

    // Append the container to the given container
    $(`#${container_id}`).append($container);

    // Get the options as an array of objects { id, name }
    var options = getData(url);

    // Add Event Listener to input for search
    $input.on("input", async function () {
        const value = $input.val().toLowerCase().trim(); // Get input value and normalize

        // Clear previous options
        $optionsContainer.empty();

        if (value) {
            const allOptions = await options; // Wait for options to resolve

            if (!Array.isArray(allOptions)) {
                console.error("Expected an array but got:", allOptions);
                return;
            }

            // Filter and prioritize results
            const filteredOptions = allOptions
                .filter(option => option.name && option.name.toLowerCase().includes(value))
                .map(option => ({
                    id: option.id, // Keep ID
                    text: option.name, // Display name
                    priority: option.name.toLowerCase() === value ? 0 :
                            option.name.toLowerCase().startsWith(value) ? 1 : 2
                }))
                .sort((a, b) => a.priority - b.priority);

            // Display options in dropdown menu
            if (filteredOptions.length) {
                $optionsContainer.show();

                filteredOptions.forEach(option => {
                    const $div = $("<div>").text(option.text).addClass("suggestion-item");

                    // Add click event listener to select an option
                    $div.on("click", function () {
                        $input.val(option.text); // Set input to the name
                        $input.attr("data-selected-id", option.id); // Store the ID
                        $optionsContainer.hide();
                    });

                    $optionsContainer.append($div);
                });
            } else {
                $optionsContainer.hide();
            }
        } else {
            $optionsContainer.hide();
        }
    });

    // Hide dropdown when clicking outside
    $(document).on("click", function (e) {
        if (!$input.is(e.target) && !$optionsContainer.is(e.target) && !$optionsContainer.has(e.target).length) {
            $optionsContainer.hide();
        }
    });
}

// Function to get selected ID
function getSelectedID(input_element) {
    // FIXME : returns id even after field is cleared
    return input_element.attr("data-selected-id") || null;
}

