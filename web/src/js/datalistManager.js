/**
 * This programs is responsible for managing datalist-like html elements.
 * 
 * It now supports genres, and later will support searching for authors as well.
 * 
 * TODO:
 * - Add support for authors
 * - Directly integer the html template as a js function that will enable implementing
 *   it as just calling a function and giving it a div id to choose location
 * - Make it easily choosable wether to search for authors or genres or other things to come.
 * - Make it easy to implement new features (variables to choose from other than authors/genres)
 */


async function getData(fetch_url) {
    /**
     * This function returns the list of genres using the API
     */

    try {
        // Requête à l'API
        const response = await fetch(fetch_url);
        if (!response.ok) {
            throw new Error(`Erreur lors de la récupération des données : ${response.status}`);
        }
        const data = eval(await response.json());
        
        // Formater genre
        // e.g. "[[1, \"40k\"], [2, \"a%C5%9Fk\"], [3, \"academic\"]]" --> ["40k","a%C5%9Fk","academic"]
        
        const dataArray = data.map(genre => genre[1]);

        return dataArray;
        

    } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
    }
}


// get genres
const genres = getData("http://127.0.0.1:8000/get_genres/"); 
// get input element
const inputGenres = document.getElementById("genre-input");
// get datalist options element
const genresContainer = document.getElementById("genres-options");

// get genres
const authors = getData("http://127.0.0.1:8000/get_authors/"); 
// get input element
const inputAuthors = document.getElementById("author-input");
// get datalist options element
const authorsContainer = document.getElementById("authors-options");

// Add Event Listener to input for search
inputGenres.addEventListener("inputGenres", openSugestion(inputGenres, genresContainer))
inputAuthors.addEventListener("inputAuthors", openSugestion(inputAuthors, authorsContainer))
    
async function openSugestion(input, optionsContainer) {
    // Make the search not case sensitive
    const value = input.value.toLowerCase();

    // Clear previous options
    optionsContainer.innerHTML = "";

    if (value) {
        const allOptions = await options;

        // Filter and prioritize:
        // 1. Exact match
        // 2. Starts with the search term
        // 3. Contains the search term elsewhere
        const filteredOptions = allOptions
            .filter(option => option && option.toLowerCase().includes(value)) // Exclude non-matching genres
            .map(option => ({
                text: option,
                priority: option.toLowerCase() === value ? 0 :
                          option.toLowerCase().startsWith(value) ? 1 : 2
            }))
            .sort((a, b) => a.priority - b.priority) // Sort based on priority
            .map(option => option.text);

        // Display options in dropdown menu
        if (filteredOptions.length) {
            optionsContainer.style.display = "block";

            filteredOptions.forEach(option => {
                const div = document.createElement("div");
                div.textContent = option;

                // Add event listener to select an option
                div.addEventListener("click", () => {
                    input.value = option;
                    optionsContainer.style.display = "none";
                });

                optionsContainer.appendChild(div);
            });
        } else {
            optionsContainer.style.display = "none";
        }
    } else {
        optionsContainer.style.display = "none";
    }
};


// Hide the options container when the user clicks on the options button
document.addEventListener("click", (e) => {
    if (!inputAuthors.contains(e.target) && !authorsContainer.contains(e.target)) {
        optionsContainer.style.display = "none";
    }
    if (!inputGenres.contains(e.target) && !genresContainer.contains(e.target)) {
        genresContainer.style.display = "none";
    }
});