document.addEventListener("DOMContentLoaded", function () {
    // const userId = "131"; // ID utilisateur forcé
    fetchBooksByUserId();
    /* const userId = getUserIdFromSession();
    if (userId) {
        fetchBooksByUserId(userId);
    } else {
        console.error("Aucun ID d'utilisateur trouvé.");
        document.getElementById('books-container').innerHTML = "<p>Aucun utilisateur trouvé.</p>";
    } */
});

/* function getUserIdFromSession() {
    return sessionStorage.getItem('userId');
} */

function fetchBooksByUserId() {
    const url = `http://127.0.0.1:8000/get_books_by_user/`; 

    fetch(url, {
                 method: 'GET',
                 headers: {
                     'Authorization': `Bearer ${localStorage.getItem("Token")}`,  // Include the token in the request
                     'Content-Type': 'application/json'
                 }
             })
        .then(response => response.json())
        .then(books => {
            console.log(books);
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
                            <button class="bouton-retirer" onclick="removeBook(${book.id})">Retirer livre</button>
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
    fetch(`http://127.0.0.1:8000/delete_book/${bookId}`, { 
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

// Lien entre meslivres et la page de détail du livre
function addClickEventToBooks() {
    const books = document.querySelectorAll(".card");
    
    books.forEach(book => {
      book.addEventListener("click", (e) => {
        window.location.href = `src/html/livres.html?id=${book.id}`;
      });
    });
}