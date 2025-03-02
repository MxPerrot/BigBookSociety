let searchbar = $("#searchbar")
let button = $("#sendsearch")
var result = $("#result")
let author_container_id = "authorIdBar"
let genre_container_id = "genreIdBar"
let author_input_id = author_container_id + "-input"
let genre_input_id = genre_container_id + "-input"

console.log("RESULT = ", result)

async function search_book(url, title_input, author_input, genre_input, result_container) {
    console.log("RESULT SB = ", result_container)
    let first = true

    // Titre
    let title = title_input.val()
    if (title) {
        url += "?title="+title
        first = false
    }

    // Auteur
    let author = getSelectedID(author_input);
    if (author) {
        if (first) {
            url += "?authors="+author
            first = false
        } else {
            url += "&authors="+author
        }
    }

    // Genres
    let genres = getSelectedID(genre_input);
    if (genres) {
        if (first) {
            url += "?genres="+genres
            first = false
        } else {
            url += "&genres="+genres
        }
    }
    
    console.log(url)
    try {
        const rawData = await fetch(url)
        const data = await rawData.json()

        console.log(data)

        afficherLivres(data, result_container);
        
    } catch (error) {
        console.error("Erreur")
    }
}

button.on("click", function() {
    search_book(
        "http://127.0.0.1:8000/search_books/",
        searchbar,
        $(`#${author_input_id}`),
        $(`#${genre_input_id}`),
        result
    );
});

createDatalist("datalist-1",author_container_id,"Auteur","http://127.0.0.1:8000/get_authors/")
createDatalist("datalist-2",genre_container_id,"Genres","http://127.0.0.1:8000/get_genres/")