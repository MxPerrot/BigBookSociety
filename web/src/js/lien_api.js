function fetchBooks() {
  const url = "http://127.0.0.1:8000/get_book_item_based/?user=131&nbrecommendation=10&limit=10";
  fetch(url)
    .then(response => response.text())  // Récupérer la réponse en texte brut
    .then(data => {
      console.log("Réponse brute de l'API : ", data); // Afficher la réponse brute dans la console

      // Si la réponse commence et se termine par des guillemets simples, on les enlève
      if (data.startsWith("'") && data.endsWith("'")) {
        data = data.slice(1, -1);
      }

      try {
        // Analyser la chaîne de texte JSON
        const books = JSON.parse(data);

        console.log("Réponse analysée (books) : ", books); // Afficher l'objet après parsing
        
        const resultElement = document.getElementById("result");
        let output = ""; // Variable pour stocker les informations à afficher

        if (Array.isArray(books) && books.length > 0) {
          books.forEach(book => {
            // Extraire les informations du livre avec une vérification pour les valeurs manquantes
            const titre = book.titre || "Titre non disponible";
            const isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
            const auteur = book.nom_auteur && book.nom_auteur.length > 0 ? book.nom_auteur.join(", ") : "Auteur inconnu";
            const genre = book.libelle_genre && book.libelle_genre.length > 0 ? book.libelle_genre.join(", ") : "Genre inconnu";
            const description = book.description || "Description non disponible";
            const datePublication = book.date_publication || "Date de publication non disponible";
            const nbPages = book.nombre_pages || "Nombre de pages non disponible";

            // Ajouter ces informations dans l'output
            output += `
              <div>
                <h3>${titre}</h3>
                <p><strong>Auteur :</strong> ${auteur}</p>
                <p><strong>ISBN :</strong> ${isbn}</p>
                <p><strong>Genre :</strong> ${genre}</p>
              </div>
              <hr>
            `;
          });
        } else {
          output = "<p>Aucun livre trouvé.</p>";
        }

        resultElement.innerHTML = output; // Affiche le résultat dans le div avec l'id "result"
      } catch (error) {
        const resultElement = document.getElementById("result");
        resultElement.textContent = "Erreur lors de l'analyse des données.";
        console.error("Erreur de parsing JSON : ", error);
      }
    })
    .catch(error => {
      const resultElement = document.getElementById("result");
      resultElement.textContent = "Impossible de récupérer les données.";
      console.error("Erreur lors de la récupération des données : ", error);
    });
}

fetchBooks();
