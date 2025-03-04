document.addEventListener("DOMContentLoaded", function () {
    const userId = getUserIdFromSession();
    if (userId) {
        fetchBooksByUserId(userId);
    } else {
        console.error("Aucun ID d'utilisateur trouvé.");
        document.getElementById('books-container').innerHTML = "<p>Aucun utilisateur trouvé.</p>";
    }
});

function getUserIdFromSession() {
 
    return sessionStorage.getItem('userId');
}

function fetchBooksByUserId(userId) {
    const url = `http://127.0.0.1:8000/get_books_by_user/${userId}`; 

    fetch(url)
        .then(response => response.json())
        .then(books => {
            if (books && books.length > 0) {
                const booksContainer = document.getElementById('books-container');
                booksContainer.innerHTML = ''; 

                books.forEach(book => {
                    const bookCard = document.createElement('div');
                    bookCard.className = 'card';
                    bookCard.dataset.id = book.id;

                    const isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
                    const coverUrl = isbn ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg` : "placeholder.jpg";

                    bookCard.innerHTML = `
                        <img src="${coverUrl}" alt="Couverture du livre ${book.titre}" class="card-img" />
                        <div class="card-content">
                            <h2 class="card-title">${book.titre || "Titre non disponible"}</h2>
                            <h3 class="card-author">De ${book.nom_auteur || "Auteur inconnu"}</h3>
                            <p class="card-description">Description: ${book.description || "Description non disponible"}</p>
                            <h4 class="card-editeur">Edition: ${book.editeur || "Éditeur inconnu"}</h4>
                            <h4 class="card-pages">Pages: ${book.nombre_pages || "Nombre de pages inconnu"}</h4>
                            <h4 class="card-datesortie">Date de sortie: ${book.date_sortie || "Non disponible"}</h4>
                            <button class="bouton-retirer" onclick="removeBook(${book.id})">Retirer livre</button>
                        </div>
                    `;

                    booksContainer.appendChild(bookCard);
                });
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
        method: 'DELETE'
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