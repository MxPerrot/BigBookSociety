function TokenError() {
  console.log("lancement TokenError");
  // Vider sessionStorage et localStorage
  sessionStorage.clear();
  clearMainContent();
  displayPopularBooksSection();

  fetchBooks("http://127.0.0.1:8000/get_tendance/20", "populaire-container");
}


// Fonction pour effacer le contenu de <main>
function clearMainContent() {
  let mainElement = document.querySelector("main");
  if (mainElement) {
    mainElement.innerHTML = '';  // Vide le contenu de <main>
  }
}

// Fonction pour afficher la section des livres populaires
function displayPopularBooksSection() {
  let popularSectionHTML = `
    <a class="refresh" href="javascript:void(0);" onclick="refreshCarrousel()">Rafraîchir</a>

    <section id="populaire-container" class="recommendation-section">
      <h2>Les plus populaires</h2>
      <div class="media-container">
        <button class="previous" aria-label="previous">
          <svg><use href="#previous"></use></svg>
        </button>
        <div class="media-scroller"></div>
        <button class="next" aria-label="next">
          <svg><use href="#next"></use></svg>
        </button>
      </div>
    </section>
    <svg style="display: none;">
      <symbol id="next" viewBox="0 0 256 512">
        <path fill="white" d="M224.3 273l-136 136c-9.4 9.4-24.6 9.4-33.9 0l-22.6-22.6c-9.4-9.4-9.4-24.6 0-33.9l96.4-96.4-96.4-96.4c-9.4-9.4-9.4-24.6 0-33.9L54.3 103c9.4-9.4 24.6-9.4 33.9 0l136 136c9.5 9.4 9.5 24.6.1 34z"/>
      </symbol>
      <symbol id="previous" viewBox="0 0 256 512">
        <path fill="white" d="M31.7 239l136-136c9.4-9.4 24.6-9.4 33.9 0l22.6 22.6c9.4 9.4 9.4 24.6 0 33.9L127.9 256l96.4 96.4c9.4 9.4 9.4 24.6 0 33.9L201.7 409c-9.4 9.4-24.6 9.4-33.9 0l-136-136c-9.5-9.4-9.5-24.6-.1-34z"/>
      </symbol>
    </svg>
    <div class="lien_connexion">
      <h1>Pour plus de recommandations, veuillez vous connecter ou créer un compte :</h1>
      <a class="bt_connex" href="./src/html/connexion.html"> Connexion</a>
    </div>
  `;
  
  let mainElement = document.querySelector("main");
  if (mainElement) {
    mainElement.innerHTML = popularSectionHTML;
  }
}

function fetchBooks(url, containerId) {
  let cachedData = sessionStorage.getItem(url);

  let token = localStorage.getItem('Token');

  if (cachedData) {
    try {
      let parsedData = JSON.parse(cachedData);

      // Vérification supplémentaire de l'intégrité des données
      if (parsedData?.detail === "Invalid token" || parsedData?.detail === "Token expired") {
        console.warn("Token invalide ou expiré. Seul le fetch des livres populaires sera effectué.");
        TokenError();
        return;
      }

      console.log("Données récupérées depuis sessionStorage.");
      carouselGenerateur(parsedData, containerId);
    } catch (error) {
      console.warn("Erreur lors du parsing des données depuis sessionStorage", error);
      console.warn("Token invalide ou expiré. Seul le fetch des livres populaires sera effectué.");
      TokenError();
      return;
    }
  } else {
    console.log("Lancement fetch");

    let headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    fetch(url, { method: 'GET', headers })
      .then(response => {
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error("Token expired");
          }
          throw new Error("Erreur réseau");
        }

        // Vérifie si le type de contenu de la réponse est du JSON
        let contentType = response.headers.get("Content-Type");
        if (contentType && contentType.includes("application/json")) {
          return response.json(); // Renvoie la réponse au format JSON
        } else {
          throw new Error("Réponse non JSON");
        }
      })
      .then(data => {
        if (data?.detail === "Token expired") {
          console.warn("Token expiré, nettoyage du sessionStorage...");
          TokenError();
          return;
        }
        
        // Vérification supplémentaire des données
        if (!data || typeof data !== 'object') {
          console.warn("Données récupérées non valides. Seul le fetch des livres populaires sera effectué.");
          TokenError();
          return;
        }

        console.log("Données récupérées depuis l'API.");
        sessionStorage.setItem(url, JSON.stringify(data));
        carouselGenerateur(data, containerId);
      })
      .catch(error => {
        console.error("Erreur lors de la récupération des données : ", error);
      });
  }
}


// Affichage des livres dans le carrousel
function carouselGenerateur(data, containerId) {
  try {
    let books = data;
    
    let container = document.querySelector(`#${containerId} .media-container`);
    if (!container) {
      console.error("Erreur : Élément contenant le carrousel introuvable !");
      return;
    }

    let scroller = document.createElement('div');
    scroller.classList.add("media-scroller");

    container.appendChild(scroller);

    scroller.innerHTML = "";

    if (Array.isArray(books) && books.length > 0) {
      let fragment = document.createDocumentFragment();

      books.forEach(book => {
        let id = book.id_livre || "ID non disponible";
        let titre = book.titre || "Titre non disponible";
        let isbn = book.isbn13 || book.isbn || "Aucun ISBN disponible";
        let auteur = book.nom_auteur && book.nom_auteur.length > 0 ? book.nom_auteur.join(", ") : "Auteur inconnu";
        let genre = book.libelle_genre && book.libelle_genre.length > 0 ? 
          book.libelle_genre[0].includes(',') ? book.libelle_genre[0].split(',')[0] : book.libelle_genre[0] : 
          "Genre inconnu";

          let coverUrl = (isbn !== "Aucun ISBN disponible") 
          ? `https://covers.openlibrary.org/b/isbn/${isbn}-M.jpg?default=false` 
          : "public/img/couverture.jpg";

          let bookElement = document.createElement('div');
        bookElement.classList.add("media-element");
        bookElement.setAttribute("data-id", id);

        bookElement.innerHTML = `
          <div>
            <div class="isbn">
              <img src="${coverUrl}" alt="Couverture du livre ${titre}" onerror="this.onerror=null;this.src='public/img/couverture.jpg';" />
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
      addClickEventToBooks();
    } else {
      scroller.innerHTML = "<p>Aucun livre trouvé.</p>";
    }
  } catch (error) {
    console.error("Erreur lors de l'analyse des données : ", error);
  }
}

// Permet de se déplacer à l'infini dans le caroussel, peu importe le sens
function setupInfiniteScroll(scroller) {
  let prevButton = scroller.closest('.recommendation-section').querySelector(".previous");
  let nextButton = scroller.closest('.recommendation-section').querySelector(".next");

  if (!prevButton || !nextButton) {
    console.error("Boutons next/previous introuvables !");
    return;
  }

  // Attribuer la fonction addClickEventToBooks (lien pour les détails d'un livre) quand on se déplace dans le carrousel
  prevButton.addEventListener("click", () => {
    shiftCarousel(scroller, "prev");
    addClickEventToBooks();
  });
  
  nextButton.addEventListener("click", () => {
    shiftCarousel(scroller, "next");
    addClickEventToBooks(); 
  });
}

function shiftCarousel(scroller, direction) {
  let firstElement = scroller.firstElementChild;
  let lastElement = scroller.lastElementChild;

  if (direction === "next") {
    scroller.appendChild(firstElement.cloneNode(true));
    scroller.removeChild(firstElement);
  } else if (direction === "prev") {
    scroller.prepend(lastElement.cloneNode(true));
    scroller.removeChild(lastElement);
  }
}

// Lien entre les livres du carrousel et la page de détail du livre
function addClickEventToBooks() {
  let books = document.querySelectorAll(".media-element");
  
  books.forEach(book => {
    book.addEventListener("click", (e) => {
      let id = book.getAttribute('data-id');
      if (id) {
        window.location.href = `src/html/livres.html?id=${id}`;
      } else {
        console.error("ID non trouvé pour ce livre.");
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  let token = localStorage.getItem('Token');

  // Si le token est absent
  if (!token) {
    console.warn("TOKEN ABSENT dans le localStorage. Seul le fetch des livres populaires sera effectué.");
    TokenError();
    return;
  } else {
    // Si le token est présent, exécuter tous les fetch
    fetchBooks("http://127.0.0.1:8000/get_book_item_based/?nbrecommendation=20", "item-based-container");
    fetchBooks("http://127.0.0.1:8000/get_book_item_based_tendance/?nbrecommendation=20", "item-based-tendance-container");
    fetchBooks("http://127.0.0.1:8000/get_book_user_based/?nbrecommendation=20", "user-based-container");
    fetchBooks("http://127.0.0.1:8000/get_tendance/20", "populaire-container");
  }
});


function refreshCarrousel() {
  // Efface données sessionStorage (le cache)
  sessionStorage.clear();
  
  var script = document.createElement('script');
  script.src = './src/js/carrousel.js';
  script.type = 'text/javascript';
  
  document.head.appendChild(script);
  window.location.href = `./index.html`;
}
