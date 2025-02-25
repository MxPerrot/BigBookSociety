let searchbar = $("#searchbar")
let button = $("#sendsearch")
let result = $("#result")

async function search() {
    try {
        const result = await fetch("http://127.0.0.1:8000/search_author/"+searchbar.val())
        const data = await result.json()

        console.log(data)
    } catch (error) {
        console.error("Test")
    }
}

$(document).ready(function() {
    button.click(search)
})
