let searchbar = $("#searchbar")
let button = $("#sendsearch")
let result = $("#result")
let authorBar = $("#authorIdBar")
let genreBar = $("#genreIdBar")

async function search() {
    let first = true
    let adress = "http://127.0.0.1:8000/search_books/"
    let title = searchbar.val()
    if (title != "") {
        adress += "?title="+title
        first = false
    }
    let author = authorBar.val()
    if (author != "") {
        if (first) {
            adress += "?authors="+author
            first = false
        } else {
            adress += "&authors="+author
        }
    }
    let genres = genreBar.val()
    if (genres != "") {
        if (first) {
            adress += "?genres="+genres
            first = false
        } else {
            adress += "&genres="+genres
        }
    }
    
    console.log(adress)
    try {
        const rawData = await fetch(adress)
        const data = await rawData.json()

        console.log(data)

        // Create an ordered list <ol> with the title of the book in the html document
        let list = document.createElement("ol")
        data.forEach(book => {
            let li = document.createElement("li")
            li.appendChild(document.createTextNode(book.titre))
            // add image with book.isbn as src
            // li.innerHTML += `<img src="https://covers.openlibrary.org/b/isbn/${book.isbn}-S.jpg" alt="Book Cover">`
            list.appendChild(li)
        })

        // Clear the previous result and add the new one
        result.html("");
        result.append(list); 


        
    } catch (error) {
        console.error("Erreur")
    }
}

$(document).ready(function() {
    button.click(search)
})
