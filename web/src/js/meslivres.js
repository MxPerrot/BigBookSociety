document.addEventListener("DOMContentLoaded", function () {
    fetchBooksByUserId();
});

function fetchBooksByUserId() {
    const url = `http://127.0.0.1:8000/get_books_by_user/`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("Token")}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(books => {
        console.log('Réponse de l\'API :', books); // Affiche la réponse complète pour vérifier la structure

        if (books && books.length > 0) {
            const booksContainer = document.getElementById('books-container');
            booksContainer.innerHTML = '';

            books.forEach(book => {
                // Afficher la structure de chaque livre pour vérifier la présence de l'ID
                console.log("Structure du livre:", book);
                
                // Vérifier si l'ID est présent dans le livre
                if (!book.id_livre) {
                    console.error("Erreur : L'ID du livre est indéfini ou null.");
                    return; // Arrêter si l'ID est invalide
                }

                const bookCard = document.createElement('div');
                bookCard.className = 'card';
                bookCard.dataset.id = book.id_livre; // Utilisez id_livre ici au lieu de id

                const isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
                const coverUrl = isbn ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg` : "placeholder.jpg";

                bookCard.innerHTML = `
                    <img src="${coverUrl}" alt="Couverture du livre ${book.titre}" class="card-img" />
                    <div class="card-content">
                        <h2 class="card-title">${book.titre || "Titre non disponible"}</h2>
                        <h3 class="card-author">De ${book.nom_auteur || "Auteur inconnu"}</h3>
                        <button class="bouton-retirer" onclick="removeBook(${book.id_livre})">Retirer livre</button>
                    </div>
                `;

                booksContainer.appendChild(bookCard);
            });

            // Add click event listeners to each book card
            addClickEventToBooks();
        } else {
            document.getElementById('books-container').innerHTML = "<p>Aucun livre trouvé.</p>";
        }
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des livres :", error);
        document.getElementById('books-container').innerHTML = "<p>Erreur lors de la récupération des livres.</p>";
    });
}

function removeBook(bookId) {
    fetch(`http://127.0.0.1:8000/remove_book/${bookId}`, { 
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("Token")}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            document.querySelector(`.card[data-id="${bookId}"]`).remove();
        } else {
            console.error('Erreur lors de la suppression du livre:', response.statusText);
        }
    })
    .catch(error => console.error('Erreur lors de la suppression du livre:', error));
}

// Lien entre meslivres et la page de détail du livre
function addClickEventToBooks() {
    const books = document.querySelectorAll(".card");

    books.forEach(book => {
        book.addEventListener("click", (e) => {
            const bookId = book.dataset.id; 

            if (!bookId) { 
                console.error("Erreur : L'ID du livre est indéfini ou null.");
                alert("Impossible de trouver l'ID du livre. Veuillez réessayer.");
                return; 
            }

            console.log(`Redirection vers le livre avec l'ID : ${bookId}`);
            
            // Assurez-vous que l'ID est valide avant de rediriger
            if (bookId !== null) {
                window.location.href = `/web/src/html/livres.html?id=${bookId}`;
            } else {
                console.error("Erreur : L'ID du livre est null.");
            }
        });
    });
}
