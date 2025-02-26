function fetchBooks() {
  const url = "http://127.0.0.1:8000/get_book_item_based/?user=131&nbrecommendation=10&limit=10";
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
        let groupCount = 1;
        let output = "";

        if (Array.isArray(books) && books.length > 0) {
          let groupHTML = ""; 
          books.forEach((book, index) => {
            const titre = book.titre || "Titre non disponible";
            const isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
            const auteur = book.nom_auteur && book.nom_auteur.length > 0 ? book.nom_auteur.join(", ") : "Auteur inconnu";
            const genre = book.libelle_genre && book.libelle_genre.length > 0 ? book.libelle_genre.join(", ") : "Genre inconnu";

            groupHTML += `
              <div class="media-element">
                <div>
                  <h3>${titre}</h3>
                  <p><strong>Auteur :</strong> ${auteur}</p>
                  <p><strong>ISBN :</strong> ${isbn}</p>
                  <p><strong>Genre :</strong> ${genre}</p>
                </div>
              </div>
            `;

            if ((index + 1) % 3 === 0 || index === books.length - 1) {
              output += `
                <div class="media-group" id="group-${groupCount}">
                  ${groupHTML}
                  <a class="next" href="#group-${groupCount + 1}" aria-label="next">
                    <svg>
                      <use href="#next"></use>
                    </svg>
                  </a>
                </div>
              `;
              groupCount++; 
              groupHTML = "";
            }
          });

          scroller.innerHTML = output;

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

fetchBooks();
