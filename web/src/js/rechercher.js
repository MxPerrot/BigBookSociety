let searchbar = $("#searchbar")
let button = $("#sendsearch")
var result = $("#result")
let author_container_id = "authorIdBar"
let genre_container_id = "genreIdBar"
let author_input_id = author_container_id + "-input"
let genre_input_id = genre_container_id + "-input"

function loadSearch() {
    let data = sessionStorage.getItem("searchData");
    console.log(JSON.parse(data))
    if (data) {
        afficherLivres(JSON.parse(data), result);
    }
}

async function search_book(url, title_input, author_input, genre_input, result_container) {
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
    const rawData = await fetch(url)
    const data = await rawData.json() // FIXME: sometimes need to be parsed (JSON.parse(...))

    afficherLivres(data, result_container);
    stringCache = JSON.stringify(data)
    sessionStorage.setItem("searchData", stringCache);
}

button.on("click", function() {
    document.getElementById("loading-spinner").style.display = "block";
    search_book(
        "http://127.0.0.1:8000/search_books/",
        searchbar,
        $(`#${author_input_id}`),
        $(`#${genre_input_id}`),
        result
    );
    document.getElementById("loading-spinner").style.display = "none";  
});

createDatalist("datalist-1",author_container_id,"Auteur","http://127.0.0.1:8000/get_authors/")
createDatalist("datalist-2",genre_container_id,"Genres","http://127.0.0.1:8000/get_genres/")

// Slider double node
$( function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 500,
      values: [ 75, 300 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
      " - $" + $( "#slider-range" ).slider( "values", 1 ) );
  } );