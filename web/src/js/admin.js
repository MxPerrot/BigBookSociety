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
    .then(books_all => {
        console.log('Réponse de l\'API :', books_all);

        let books = tri_books(books_all, 20);
        let infos = "<ul>";
        books.forEach(book => {
            infos += "<li>" + book['titre'];
            if (book['nom_auteur'].length > 0) infos += ", de " + book['nom_auteur'][0];
            infos += " (" + book['indice_succes'] + ")</li>";
        });
        infos += "</ul>";
        list_populaires.innerHTML = infos;
        let graph = document.getElementById('populareChart').getContext('2d');
        fetchData(books_all, graph);
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
        let graph = document.getElementById('wishChart').getContext('2d');
        fetchData(books, graph);
    })
    .catch(error => {
        console.error("Erreur lors de la récupération des livres :", error);
        document.getElementById('books-container').innerHTML = "<p>Erreur lors de la récupération des livres.</p>";
    });
}

async function fetchData(books_infos, graph) {
    console.log(graph);
    let genreCounts = {};
    books_infos.forEach(book => {
        const count = book.count;
        let genres = book.libelle_genre || [];
        genres.forEach(genre => {
            if (genreCounts[genre]) {
                genreCounts[genre] += count;
            } else {
                genreCounts[genre] = count;
            }
        });
    });
    let filteredGenres = filter_max(genreCounts, 20);
    console.log(filteredGenres);
    let labels = Object.keys(filteredGenres);
    let data = Object.values(filteredGenres);
    createPieChart(labels, data, graph);
}

function filter_max(genreCounts, val) {
    let filteredGenres = {};
    let sortedGenres = Object.entries(genreCounts).sort((a, b) => b[1] - a[1])
    sortedGenres.slice(0, val).forEach(([genre, count]) => {
        filteredGenres[genre] = count;
    });
    return filteredGenres;
}

function generateUniqueColor(x) {
    const startColor = [255, 78, 78];
    const endColor = [255, 255, 78];
    let colors = [];
    for (let i = 0; i < x; i++) {
        let t = i / (x - 1); 
        let r = Math.round((1 - t) * startColor[0] + t * endColor[0]);
        let g = Math.round((1 - t) * startColor[1] + t * endColor[1]);
        let b = Math.round((1 - t) * startColor[2] + t * endColor[2]);
        let hexColor = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
        colors.push(hexColor);
    }
    return colors;
}

function createPieChart(labels, data, ctx) {
    const backgroundColors = generateUniqueColor(labels.length);
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,  // Couleurs générées dynamiquement
                borderColor: '#fff',
                borderWidth: 1
            }]
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    let titre = document.getElementById("form-titre");
    let auteur = document.getElementById("form-auteur");
    let editeur = document.getElementById("form-edition");
    let nb_pages = document.getElementById("form-nb_pages");
    let date_sortie = document.getElementById("form-date_sortie");
    let description = document.getElementById("form-description");
    let isbn = document.getElementById("form-isbn");
    let form = document.getElementById("uploadForm");
    let preview = document.getElementById("preview");

    // Prévisualisation avant l'envoi
    isbn.addEventListener("change", function() {
        console.log("change");
        let url = 'https://covers.openlibrary.org/b/isbn/' + isbn.value + '-M.jpg?default=false';
        preview.src = url;
        preview.style.display = "block";
    });

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Empêche le rechargement de la page

        book_exist(isbn, titre, editeur, auteur, nb_pages, date_sortie, description);
    });
});

function book_exist(isbn, titre, editeur, auteur, nb_pages, date_sortie, description) {
    if (isbn.value) {            
        fetch(`${API_PATH}/search_book_isbn/?isbn=${isbn.value}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                'Content-Type': 'application/json'
            }                  
        }).then(response => response.json())
        .then(answer => {
            if (answer.length > 0) {
                alert("Un livre de cet ISBN existe déjà !")
            }
            else {
                fetch(`${API_PATH}/register_book/?isbn13=${isbn.value}&titre=${titre.value}&editeur=${editeur.value}&auteur=${auteur.value}
                    &nb_pages=${nb_pages.value}&date_sortie=${date_sortie.value}&description=${description.value}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }
                    })
                .then(response => response.json())  // Parse response as JSON
                .then(data => {
                        console.log('Response:', data);
                        alert(`Le livre ${titre.value} a été créé !`);
                    }) // Log the response
                .catch(error => console.error('Error:', error));
            }
        });
    } 
    else if (titre.value && editeur.value) {
        fetch(`${API_PATH}/search_book_titre_editeur/?titre=${titre.value}&editeur=${editeur.value}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                'Content-Type': 'application/json'
            }                  
        }).then(response => response.json())
        .then(answer => {
            if (answer.length > 0) {
                alert("Un livre de ce titre/editeur existe déjà !")
            }
            else {
                fetch(`${API_PATH}/register_book/?titre=${titre.value}&editeur=${editeur.value}&auteur=${auteur.value}
                    &nb_pages=${nb_pages.value}&date_sortie=${date_sortie.value}&description=${description.value}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }                  
                    })
                .then(response => response.json())  // Parse response as JSON
                .then(data => {
                    console.log('Response:', data);
                    alert(`Le livre ${titre.value} a été créé !`);
                })  // Log the response
                .catch(error => console.error('Error:', error));
            }
        });
    }
    
    else {
        alert("Les valeurs entrées sont insuffisantes");
    }
}