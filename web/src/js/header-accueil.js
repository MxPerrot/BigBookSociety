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
    }
  
    connectedCallback() {
      const shadowRoot = this.attachShadow({ mode: 'closed' });
  
      shadowRoot.appendChild(headerTemplate.content);
    }
  }
  
  customElements.define('header-accueil', Header);