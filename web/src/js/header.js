const headerTemplate = document.createElement('template');

headerTemplate.innerHTML = `
   <style>
        /* Couleurs */
        :root {
            --col1: #1E2026;
            --blanc: #FFFFFF;
            --noir: #000000;
            --col2: #F2F2F2;
            --col3: #276BF2;
            --col4: #447EF2;
            --col5: #6393F2;
        }

        /* Fonts */
        @font-face {
            font-family: 'Poppins';
            src: url('../../fonts/Poppins-Regular.ttf') format('truetype');
            font-weight: 400;
            font-style: normal;
        }

        @font-face {
            font-family: 'Poppins';
            src: url('../../fonts/Poppins-Bold.ttf') format('truetype');
            font-weight: 700;
            font-style: normal;
        }

        @font-face {
            font-family: 'AbrilFatface';
            src: url('../../fonts/AbrilFatface-Regular.ttf') format('truetype');
            font-weight: 400;
            font-style: normal;
        }

        /* Header */
        header {
            position: fixed;
            top: 0;
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

        #sous {
            list-style-type: none;
            display: none;
            background-color: white;
            position: absolute;
            width: 100%;
            height: 100%;
            padding: 0;
            top: 100px;
        }

        nav > ul li:hover #sous {
            display: block;
        }

        #sous li {
            float: none;
            width: 100%;
            text-align: left;
            height: 50%;
        }

        #sous a {
            color: var(--noir);
        }

        #deroulant {
            position: sticky;
            color: var(--blanc);
            text-decoration: none;
            display: flex;
            align-items: center; 
            justify-content: center;
            width: 100%;
            height: 100%;
        }

        #BigBook{
            font-family: 'AbrilFatface';
            font-size: 4.5rem;
        }
    </style>

    <header>
        <nav>
          <ul>
              <li><a href="../html/rechercher.html">RECHERCHER</a></li>
              <li id="deroulant">MES LIVRES ▼
                <ul id="sous">
                    <li><a href="../html/meslivres.html">Livres à lire</a></li>
                    <li><a href="../html/meslivres.html">Livres lus</a></li>
                </ul>
              </li>
              <li><a id="BigBook" href="../../index.html">BigBook   </a></li>
              <li><a href="../html/apropos.html">A PROPOS</a></li>
              <li><a class="deconnexion" href="javascript:void(0);" onclick="localStorage.clear();refreshCarrousel()">DÉCONNEXION</a></li>
          </ul>
        </nav>
    </header>

    <script>
        const deroulant = document.getElementById('deroulant');
        const sous = document.getElementById('sous');
        deroulant.addEventListener('mouseover', function() {
            sous.style.display = 'block';
        });
    </script>
`;

class Header extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' }).appendChild(headerTemplate.content.cloneNode(true));
    }
  
    connectedCallback() {
        if (!this.shadowRoot) {
            const shadowRoot = this.attachShadow({ mode: 'open' });
        
            shadowRoot.appendChild(headerTemplate.content);
        }
    }
}

customElements.define('header-component', Header);

// Check if user is logged in, if not, replace "my profile" with "log in"

let token = localStorage.getItem('Token');

document.addEventListener("DOMContentLoaded", () => {
    const headerElement = document.querySelector("header-component");

    if (headerElement && headerElement.shadowRoot) {
        const navLinks = headerElement.shadowRoot.querySelectorAll("nav ul li");

        navLinks.forEach(li => {
            const link = li.querySelector("a");

            if (link && link.getAttribute("href") === "../html/profil.html" && !token) {
                li.innerHTML = `<a href="../html/connexion.html">CONNEXION</a>`;
            }
            if (link && link.getAttribute("href") === "../html/meslivres.html" && !token) {
                li.innerHTML = `<li><a href="../html/connexion.html">MES LIVRES</a></li>`;
            }
        });
    }
});