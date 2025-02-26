let searchbar = $("#searchbar")
let button = $("#sendsearch")
let result = $("#result")
let authorBar = $("#authorIdBar")
let genreBar = $("#genreIdBar")

async function search() {
    let first = true
    let adress = "http://127.0.0.1:8000/search_books/?"
    let title = searchbar.val()
    if (title != "") {
        adress += "title="+title
        first = false
    }
    let author = authorBar.val()
    if (author != "") {
        if (first) {
            adress += "authors="+author
            first = false
        } else {
            adress += "&authors="+author
        }
    }
    let genres = genreBar.val()
    if (genres != "") {
        if (first) {
            adress += "genres="+genres
            first = false
        } else {
            adress += "&genres="+genres
        }
    }
    
    console.log(adress)
    try {
        const result = await fetch(adress)
        const data = await result.json()

        console.log(data)
    } catch (error) {
        console.error("Test")
    }
}

$(document).ready(function() {
    button.click(search)
})
