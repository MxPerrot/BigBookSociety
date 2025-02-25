$(document).ready(function() {
    $("#sendsearch").click(search($("#searchbar").text))
})

function search(criter) {
    $("#result").text = criter
}