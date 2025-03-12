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
              <li><a href="./src/html/rechercher.html">RECHERCHER</a></li>
              <li><a href="./src/html/meslivres.html">MES LIVRES</a></li>
              <li><a id="BigBook" href="./index.html">BigBook   </a></li>
              <li><a href="./src/html/apropos.html">A PROPOS</a></li>
              <li><a class="deconnexion" href="javascript:void(0);" onclick="localStorage.clear();refreshCarrousel()">DÉCONNEXION</a></li>
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
     
        window.addEventListener("scroll", () => {
            if (!this.shadowRoot) return; 
            
            const header = this.shadowRoot.querySelector("header"); 
            if (!header) return; 
            
            const threshold = document.getElementById("background").getBoundingClientRect().bottom;

            if (threshold <= 0) {
                header.classList.add("fixed-header"); 
            } else {
                header.classList.remove("fixed-header"); 
            }
        });

        this.shadowRoot.querySelectorAll("nav a").forEach(link => {
            link.addEventListener("click", (event) => {
                event.preventDefault(); 
                const targetPage = link.getAttribute("href");

                if (targetPage && targetPage !== "#") {
                    window.location.href = targetPage; 
                }
            });
        });
    }
}

customElements.define('header-accueil', Header);

// Check if user is logged in, if not, replace "my profile" with "log in"

let token = localStorage.getItem('Token');

document.addEventListener("DOMContentLoaded", () => {
    const headerElement = document.querySelector("header-accueil");

    if (headerElement && headerElement.shadowRoot) {
        const navLinks = headerElement.shadowRoot.querySelectorAll("nav ul li");

        navLinks.forEach(li => {
            const link = li.querySelector("a");

            if (link) {
                const href = link.getAttribute("href");
                if ((!token || token === "Invalid token" || token === "Token expired") && href === "./src/html/profil.html") {
                    li.innerHTML = `<a href="./src/html/connexion.html">CONNEXION</a>`;
                }
                if ((!token || token === "Invalid token" || token === "Token expired") && href === "./src/html/meslivres.html") {
                    li.innerHTML = `<a href="./src/html/connexion.html">MES LIVRES</a>`;
                }
            }
        });
    }
});

