function fetchBooks(url, containerId) {
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
        
        const container = document.querySelector(`#${containerId} .media-container`);
        if (!container) {
          console.error("Erreur : Élément contenant le carrousel introuvable !");
          return;
        }

        const scroller = document.createElement('div');
        scroller.classList.add("media-scroller");

        container.appendChild(scroller);

        scroller.innerHTML = "";

        if (Array.isArray(books) && books.length > 0) {
          const fragment = document.createDocumentFragment();

          books.forEach(book => {
            const id = book.id_livre || "ID non disponible";
            const titre = book.titre || "Titre non disponible";
            const isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
            const auteur = book.nom_auteur && book.nom_auteur.length > 0 ? book.nom_auteur.join(", ") : "Auteur inconnu";
            const genre = book.libelle_genre && book.libelle_genre.length > 0 ? 
              book.libelle_genre[0].includes(',') ? book.libelle_genre[0].split(',')[0] : book.libelle_genre[0] : 
              "Genre inconnu";

            const coverUrl = (isbn !== "Aucun ISBN disponible") 
              ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg?default=false` 
              : "public/img/couverture.jpg";

            const bookElement = document.createElement('div');
            bookElement.classList.add("media-element");
            bookElement.setAttribute("data-id", id);

            bookElement.innerHTML = `
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
            `;

            fragment.appendChild(bookElement);
          });

          scroller.appendChild(fragment);
          
          setupInfiniteScroll(scroller);
          addClickEventToBooks(containerId); // Passer containerId pour ajouter l'événement de clic
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
  const prevButton = scroller.closest('.recommendation-section').querySelector(".previous");
  const nextButton = scroller.closest('.recommendation-section').querySelector(".next");

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
    scroller.appendChild(firstElement.cloneNode(true));
    scroller.removeChild(firstElement);
  } else if (direction === "prev") {
    scroller.prepend(lastElement.cloneNode(true));
    scroller.removeChild(lastElement);
  }
}

// Fonction pour ajouter l'événement de clic sur chaque élément du carrousel
function addClickEventToBooks(containerId) {
  const scroller = document.querySelector(`#${containerId} .media-scroller`);

  if (!scroller) {
    console.error("Erreur : Élément .media-scroller introuvable !");
    return;
  }

  scroller.addEventListener("click", (event) => {
    let bookElement = event.target.closest(".media-element");

    if (bookElement) {
      const id = bookElement.getAttribute("data-id");
      if (id) {
        window.location.href = `src/html/livres.html?id=${id}`;
      } else {
        console.error("ID non trouvé pour ce livre.");
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // item based :
  fetchBooks("http://127.0.0.1:8000/get_book_item_based/?user=131&nbrecommendation=15", "item-based-container");

  // item based tendance :
  fetchBooks("http://127.0.0.1:8000/get_book_item_based_tendance/?user=131&nbrecommendation=15", "item-based-tendance-container");

  // user based :
  fetchBooks("http://127.0.0.1:8000/get_book_user_based/?user=131&nbrecommendation=15", "user-based-container");

  //tendance
  //fetchBooks("http://127.0.0.1:8000/get_tendance/10");

});
