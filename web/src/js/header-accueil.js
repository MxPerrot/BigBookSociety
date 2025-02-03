const headerTemplate = document.createElement('template');


headerTemplate.innerHTML = `
   <style>
        /* Header */
        header {
            position: absolute;
            left: 0;
            width: 100%;
            height: 100px;
            background-color: var(--col3);
            color: var(--blanc);
            text-align: center;
            z-index: 1000;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
        }

        header-accueil {
            display: block; /* Pour que l'élément prenne toute la largeur */
            position: absolute;
            top: 100vh; /* Démarre juste sous l'image */
            left: 0;
            width: 100%;
            z-index: 1000;
        }

        /* Classe qui sera ajoutée dynamiquement */
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
        }

        /* Navigation */
        nav {
            width: 100%;
            height: 100px;
        }

        nav > ul {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
            list-style-type: none;
            padding: 0;
            margin: 0;
            height: 100%;
        }

        nav li {
            flex: 1;
            display: flex;
        }

        /* Liens de navigation */
        nav a {
            color: var(--blanc);
            text-decoration: none;
            display: flex;
            align-items: center; 
            justify-content: center;
            width: 100%;
            height: 100%;
        }

        /* Effet au survol */
        nav a:hover {
            background-color: var(--col5);
            color: var(--noir);
        }

        #BigBook{
            font-family: 'AbrilFatface';
            font-size: 4.5rem;
        }

      </style>

    <header>
        <nav>
          <ul>
              <li><a href="#">RECOMMENDATIONS</a></li>
              <li><a href="#">MES LIVRES</a></li>
              <li><a id="BigBook" href="#">BigBook   </a></li>
              <li><a href="#">A PROPOS</a></li>
              <li><a href="#">MON PROFIL</a></li>
          </ul>
        </nav>
    </header>
`;

class Header extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' }).appendChild(headerTemplate.content.cloneNode(true));
    }

    connectedCallback() {
        // Attendre que le shadowRoot soit attaché avant d'ajouter l'écouteur de scroll
        window.addEventListener("scroll", () => {
            if (!this.shadowRoot) return; // 🔥 Sécurité pour éviter une erreur
            
            const header = this.shadowRoot.querySelector("header"); // ✅ Sélectionne <header> à l'intérieur du Shadow DOM
            if (!header) return; // 🔥 Vérification supplémentaire
            
            const threshold = document.getElementById("background").getBoundingClientRect().bottom;

            if (threshold <= 0) {
                header.classList.add("fixed-header"); // ✅ Ajoute la classe à <header>
            } else {
                header.classList.remove("fixed-header"); // ✅ Supprime la classe si on remonte
            }
        });
    }
}

customElements.define('header-accueil', Header);
