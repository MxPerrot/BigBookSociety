// Pour damien <3

const url = "http://127.0.0.1:8000/users/me"
async function getMyData(url) {
    const result = await fetch(url);
    console.log(result.json())
}


getMyData(url)

// <script src="exempleAPI.js" defer></script>
// UTILISER JQUERY POUR ACCEDER AUX ELEMENTS HTML avec $("#id-de-l-element")...