var bookID = null;

document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const bookId = params.get("id");

    console.log("ID du livre récupéré :", bookId); // DEBUG

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
            console.log("Données récupérées :", book); // DEBUG

            // Vérifie si la réponse est un tableau ou un objet
            if (!book || (Array.isArray(book) && book.length === 0)) {
                console.error("Erreur : Aucun livre trouvé ou réponse invalide.");
                document.querySelector(".card").innerHTML = "<p>Aucun livre trouvé.</p>";
                return;
            }

            const bookData = Array.isArray(book) ? book[0] : book;
            const bookContainer = document.querySelector(".card");
            const isbn = bookData.isbn13 || bookData.isbn || "Aucun ISBN disponible";
            const coverUrl = (isbn !== "Aucun ISBN disponible") 
                ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg?default=false` 
                : "../../public/img/couverture.jpg";      

            bookContainer.innerHTML = `
                <button onclick="history.back()">Go Back</button>
                <img class="card-img" src="${coverUrl}" alt="Couverture du livre ${bookData.titre}" onerror="this.onerror=null;this.src='../../public/img/couverture.jpg';" />
                <div class="card-content">
                    <h2 class="card-title">${bookData.titre || "Titre non disponible"}</h2>
                    <h3 class="card-author">${bookData.nom_auteur || "Auteur inconnu"}</h3>
                    <p class="card-description">${bookData.description || "Description non disponible"}</p>
                    <h4 class="card-editeur">Edition: ${bookData.nom_editeur || "Éditeur inconnu"}</h4>
                    <h4 class="card-pages">Pages: ${bookData.nombre_pages || "Nombre de pages inconnu"}</h4>
                    <h4 class="card-datesortie">Date de sortie: ${bookData.date_publication || "Non disponible"}</h4>
                    <button id="likeButton" class="like-button">
                        Like
                    </button>
                </div>
            `;

            const likeButton = document.getElementById("likeButton");
            likeButton.addEventListener("click", function () {
                likeButton.classList.toggle("liked");
                likeButton.textContent = likeButton.classList.contains("liked") ? "Liked" : "Like";
            });
        })
        .catch(error => {
            console.error("Erreur lors de la récupération du livre :", error);
        });
}
