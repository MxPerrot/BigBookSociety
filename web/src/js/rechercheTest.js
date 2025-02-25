let searchbar = $("#searchbar")
let button = $("#sendsearch")
let result = $("#result")

async function search() {
    let title = searchbar.val()
    try {
        const result = await fetch("http://127.0.0.1:8000/search_books/?title="+title)
        const data = await result.json()

        console.log(data)
    } catch (error) {
        console.error("Test")
    }
}

$(document).ready(function() {
    button.click(search)
})
