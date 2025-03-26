import { API_PATH } from "./config.js";

document.addEventListener("DOMContentLoaded", function () {
    const list_populaires = document.getElementById("list_populaires");
    const list_whish = document.getElementById("list_whish");

    fetchBooksWish(list_whish);
    fetchBooksTendance(list_populaires);
})

function calcul_demande(noteMoyenne, nbCritiques, nbNotes) {
    const poidsNotes = 0.45 * Math.log(nbNotes) - 0.8;
    const poidsNoteMoyenne = noteMoyenne < 3 ? 0.2 : (noteMoyenne >= 3 && noteMoyenne <= 4.5) ? 0.8 : 1.2;  // Moins de 3 = faible demande, plus de 4 = forte demande
    const poidsCritiques = nbCritiques > 50000 ? 1.2 : 1;  // Plus de 100 critiques, livre populaire

    const indiceDemande = poidsNotes * poidsNoteMoyenne * poidsCritiques;
    const baseStock = 5;  // Stock de base pour un livre "standard"
    return Math.round(baseStock * indiceDemande);
}

function tri_books(books, val) {
    books.forEach(book => {
        book['indice_succes'] = calcul_demande(book['note_moyenne'], book['nb_critiques'], book['nb_notes']);
    });
    books.sort((a, b) => {
        return b['indice_succes'] - a['indice_succes']
    });
    books = books.slice(0, val);
    return books;
}

function fetchBooksTendance(list_populaires) {
    console.log("Chargement des tendances...");
    const url = `${API_PATH}/get_tendance/2000`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("Token")}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(books => {
        console.log('Réponse de l\'API :', books);

        books = tri_books(books, 20);
        let infos = "<ul>";
        books.forEach(book => {
            infos += "<li>" + book['titre'];
            if (book['nom_auteur'].length > 0) infos += ", de " + book['nom_auteur'][0];
            infos += " (" + book['indice_succes'] + ")</li>";
        });
        infos += "</ul>";
        list_populaires.innerHTML = infos;
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des livres :", error);
        document.getElementById('books-container').innerHTML = "<p>Erreur lors de la récupération des livres.</p>";
    });
}

function fetchBooksWish(list_whish) {
    console.log("Chargement de la whislist...");
    const url = `${API_PATH}/get_whislist/20`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("Token")}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(books => {
        console.log('Réponse de l\'API :', books);
        let infos = "<ul>";
        books.forEach(book => {
            infos += "<li>" + book['titre'];
            if (book['nom_auteur'].length > 0) infos += ", de " + book['nom_auteur'][0];
            infos += " (" + book['count'] +" voeux)</li>";
        });
        infos += "</ul>";
        list_whish.innerHTML = infos;
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des livres :", error);
        document.getElementById('books-container').innerHTML = "<p>Erreur lors de la récupération des livres.</p>";
    });
}

