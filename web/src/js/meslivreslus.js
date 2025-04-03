import { API_PATH } from "./config.js";

document.addEventListener("DOMContentLoaded", function () {
    fetchBooksByUserId();
});

function fetchBooksByUserId() {
    const url = `${API_PATH}/get_books_by_user/`;
    document.getElementById("loading-spinner").style.display = "block";
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("Token")}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(books => {
        console.log('Réponse de l\'API :', books);

        const booksContainer = document.getElementById('books-container');
        booksContainer.innerHTML = '';

        if (books && books.length > 0) {
            books.forEach(book => {
                if (!book.id_livre) {
                    console.error("Erreur : L'ID du livre est indéfini ou null.");
                    return;
                }

                const bookCard = document.createElement('div');
                bookCard.className = 'card';
                bookCard.dataset.id = book.id_livre;

                const isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
                const coverUrl = (isbn !== "Aucun ISBN disponible") 
                ? `https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg?default=false` 
                : "../../public/img/couverture.jpg";      

                bookCard.innerHTML = `
                    <img class="card-img" src="${coverUrl}" alt="Couverture du livre ${book.titre}" onerror="this.onerror=null;this.src='../../public/img/couverture.jpg';" />
                
                    <div class="card-content">
                        <h2 class="card-title">${book.titre || "Titre non disponible"}</h2>
                        <h3 class="card-author">${book.nom_auteur || "Auteur inconnu"}</h3>
                    </div>
                `;

                booksContainer.appendChild(bookCard);
            });

            // Ajouter les événements aux boutons "Retirer"
            addRemoveEventListeners();
            addClickEventToBooks();
            document.getElementById("loading-spinner").style.display = "none";  
        } else {
            document.getElementById("loading-spinner").style.display = "none";  
            booksContainer.innerHTML = "<p>Aucun livre trouvé.</p>";
        }
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des livres :", error);
        document.getElementById('books-container').innerHTML = "<p>Erreur lors de la récupération des livres.</p>";
    });
}

function addRemoveEventListeners() {
    document.querySelectorAll(".bouton-retirer").forEach(button => {
        button.addEventListener("click", function (e) {
            e.stopPropagation(); // Empêche le clic de déclencher la redirection
            const bookId = this.dataset.id;
            removeBook(bookId);
        });
    });
}

function removeBook(bookId) {
    fetch(`${API_PATH}/delete_book/${bookId}`, { 
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("Token")}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log(`Livre ${bookId} supprimé avec succès.`);
            document.querySelector(`.card[data-id="${bookId}"]`).remove();
        } else {
            console.error('Erreur lors de la suppression du livre:', response.statusText);
        }
    })
    .catch(error => console.error('Erreur lors de la suppression du livre:', error));
}


function addClickEventToBooks() {
    document.querySelectorAll(".card").forEach(book => {
        book.addEventListener("click", function (e) {
            // Vérifier si l'élément cliqué est le bouton "Retirer"
            if (e.target.classList.contains("bouton-retirer")) return;

            const bookId = this.dataset.id;
            if (!bookId) { 
                console.error("Erreur : L'ID du livre est indéfini ou null.");
                alert("Impossible de trouver l'ID du livre. Veuillez réessayer.");
                return;
            }

            console.log(`Redirection vers le livre avec l'ID : ${bookId}`);
            window.location.href = `../html/livres.html?id=${bookId}`;
        });
    });
}
