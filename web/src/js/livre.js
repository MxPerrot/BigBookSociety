document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const bookId = params.get("id");

    if (bookId) {
        fetchBookById(bookId);
    } else {
        console.error("Aucun ID de livre trouvé dans l'URL.");
        document.querySelector(".card").innerHTML = "<p>Aucun livre trouvé.</p>";
    }
});
function fetchBookById(id) {
    const url = `http://127.0.0.1:8000/get_book_data_by_id/${id}`;
    
    fetch(url)
        .then(response => response.json())
        .then(book => {
            console.log("Données récupérées :", book[0].titre);
            
            if (book) {

                const bookContainer = document.querySelector(".card");
                const isbn = book[0].isbn13 || book[0].isbn || "Aucun ISBN disponible";
                const coverUrl = (isbn !== "Aucun ISBN disponible") 
                ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg?default=false` 
                : "../../public/img/couverture.jpg";      

                bookContainer.innerHTML = `
                    <img src="${coverUrl}" alt="Couverture du livre ${book[0].titre}" onerror="this.onerror=null;this.src='../../public/img/couverture.jpg';" />                </div>
                    <div class="card-content">
                        <h2 class="card-title"> ${book[0].titre || "Titre non disponible" }</h2>
                        <h3 class="card-author"> De ${book[0].nom_auteur || "Auteur inconnu"}</h3>
                        <p class="card-description"> Description: ${book[0].description || "Description non disponible"}</p>
                        <h4 class="card-editeur">Edition: ${book[0].editeur || "Éditeur inconnu"}</h4>
                        <h4 class="card-pages">Pages: ${book[0].nombre_pages || "Nombre de pages inconnu"}</h4>
                        <h4 class="card-datesortie">Date de sortie: ${book[0].date_sortie || "Non disponible"}</h4>
                    </div>
                `;//<button class="bouton-ajouter">Ajouter livre</button>
            } else {
                document.querySelector(".card").innerHTML = "<p>Aucun livre trouvé.</p>";
            }
        })
        .catch(error => {
            console.error("Erreur lors de la récupération du livre :", error);
        });
}