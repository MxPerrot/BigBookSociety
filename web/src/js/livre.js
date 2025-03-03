document.addEventListener("DOMContentLoaded", function () {
    const bookId = 1;
    fetchBookById(bookId);
});

function fetchBookById(id) {
    const url = `http://127.0.0.1:8000/get_book_data_by_id/${id}`;
    fetch(url)
        .then(response => response.json())
        .then(book => {
            console.log("Données récupérées :", book);
            
            if (book) {
                const bookContainer = document.querySelector(".card");
                
                bookContainer.innerHTML = `
                    <img src="${book.cover_url || '../../public/img/image_home.jpeg'}" alt="Book Cover" class="card-img">
                    <div class="card-content">
                        <h2 class="card-title">${book.titre || "Titre non disponible"}</h2>
                        <h3 class="card-author">${book.nom_auteur || "Auteur inconnu"}</h3>
                        <p class="card-description">${book.description || "Description non disponible"}</p>
                        <h4 class="card-editeur">${book.editeur || "Éditeur inconnu"}</h4>
                        <h4 class="card-pages">${book.nombre_pages || "Nombre de pages inconnu"}</h4>
                        <h4 class="card-datesortie">Sortie ${book.date_sortie || "Non disponible"}</h4>
                        <button class="bouton-ajouter">Ajouter livre</button>
                    </div>
                `;
            } else {
                document.querySelector(".card").innerHTML = "<p>Aucun livre trouvé.</p>";
            }
        })
        .catch(error => {
            console.error("Erreur lors de la récupération du livre :", error);
        });
}