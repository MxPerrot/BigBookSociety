document.addEventListener("DOMContentLoaded", fetchBooks);

function fetchBooks(url) {

  fetch(url)
    .then(response => response.text())
    .then(data => {
      console.log("Réponse brute de l'API : ", data);

      if (data.startsWith("'") && data.endsWith("'")) {
        data = data.slice(1, -1);
      }

      try {
        const books = JSON.parse(data);
        console.log("Réponse analysée (books) : ", books);
        
        const scroller = document.querySelector(".media-scroller");
        if (!scroller) {
          console.error("Erreur : Élément .media-scroller introuvable !");
          return;
        }

        scroller.innerHTML = ""; // On vide l'ancien contenu

        if (Array.isArray(books) && books.length > 0) {
          books.forEach(book => {
            const titre = book.titre || "Titre non disponible";
            const isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
            const auteur = book.nom_auteur && book.nom_auteur.length > 0 ? book.nom_auteur.join(", ") : "Auteur inconnu";
            const genre = book.libelle_genre && book.libelle_genre.length > 0 ? 
              book.libelle_genre[0].includes(',') ? book.libelle_genre[0].split(',')[0] : book.libelle_genre[0] : 
              "Genre inconnu";

            const coverUrl = (isbn !== "Aucun ISBN disponible") 
              ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg?default=false` 
              : "public/img/couverture.jpg";

            const bookHTML = `
              <div class="media-element">
                <div>
                  <div class="isbn">
                    <img src="${coverUrl}" alt="Couverture du livre ${titre}" />
                  </div>
                  <div class="Livres">
                    <h3>${titre}</h3>
                    <p>${auteur}</p>
                    <p>${genre}</p>
                  </div>
                </div>
              </div>
            `;

            scroller.innerHTML += bookHTML;
          });

          setupInfiniteScroll(scroller);
        } else {
          scroller.innerHTML = "<p>Aucun livre trouvé.</p>";
        }
      } catch (error) {
        console.error("Erreur lors de l'analyse des données : ", error);
      }
    })
    .catch(error => {
      console.error("Erreur lors de la récupération des données : ", error);
    });
}

function setupInfiniteScroll(scroller) {
  const prevButton = document.querySelector(".previous");
  const nextButton = document.querySelector(".next");

  if (!prevButton || !nextButton) {
    console.error("Boutons next/previous introuvables !");
    return;
  }

  prevButton.addEventListener("click", () => shiftCarousel(scroller, "prev"));
  nextButton.addEventListener("click", () => shiftCarousel(scroller, "next"));
}

function shiftCarousel(scroller, direction) {
  const firstElement = scroller.firstElementChild;
  const lastElement = scroller.lastElementChild;

  if (direction === "next") {
    scroller.appendChild(firstElement.cloneNode(true)); // Clone le premier élément et l'ajoute à la fin
    scroller.removeChild(firstElement); // Supprime l'original
  } else if (direction === "prev") {
    scroller.prepend(lastElement.cloneNode(true)); // Clone le dernier élément et l'ajoute au début
    scroller.removeChild(lastElement); // Supprime l'original
  }
}


fetchBooks("http://127.0.0.1:8000/get_book_item_based/?user=131&nbrecommendation=10&limit=10");
