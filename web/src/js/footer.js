const footerTemplate = document.createElement('template');


footerTemplate.innerHTML = `
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

        /* Footer */
        footer {
            background-color: var(--col3);
            color: var(--blanc);
            text-align: center;
        }

        footer nav{
            height: 150px;
        }
        
        footer p {
            margin-bottom: 0px;
        }

      </style>

    <footer>
        <nav>
            <ul>
                <li><a href="#">Mention légales</a></li>
                <li><a href="#">Conditions générales d'utilisation</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>
        <p>© 2025  BigBook - Tous droits réservés</p>
    </footer>
`;


class Footer extends HTMLElement {
    constructor() {
      super();
    }
  
    connectedCallback() {
      const shadowRoot = this.attachShadow({ mode: 'closed' });
  
      shadowRoot.appendChild(footerTemplate.content);
    }
  }
  
  customElements.define('footer-component', Footer);