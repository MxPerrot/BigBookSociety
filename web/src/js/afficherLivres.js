// Fonction pour afficher une liste de livres dans un conteneur donné
function afficherLivres(livres, conteneur) {
    
    // D'abord, vider le conteneur
    conteneur.empty()

    // // Convertir livres en array si ce n'est pas fait

    // livres = JSON.parse(livres)

    // Ensuite, vérifier qu'il y a bien des livres à afficher
    if (livres.length > 0) {

        // Itération sur le tableau des livres
        $.each(livres, function(index, livre) {
            // Création d'une div pour chaque livre avec un id unique et une classe
            var $livreItem = $('<div>', {
                id: livre.id_livre,
                class: 'book-list-item'
            });

            // Construction de l'URL de l'image en utilisant la propriété isbn13
            
            var urlImage = 'https://covers.openlibrary.org/b/isbn/' + livre.isbn13 + '-L.jpg?default=false';
            // Création d'un élément img avec l'attribut src défini sur l'URL de l'image
            
            var $img = $('<img>', {
                src: urlImage,
                alt: livre.titre,
                onerror: "this.onerror=null;this.src='../../public/img/couverture.jpg';"
            });
            
            // Ajout de l'image à la div du livre
            $livreItem.append($img);
            
            var $info = $('<div>', {
            });
            $info.html(`
                <h3 class="card-title">${livre.titre || "Titre non disponible"}</h3>
                <p class="card-author">De ${livre.nom_auteur || "Auteur inconnu"}</p>
            `);

            $livreItem.append($info);
            
            // Ajout de l'élément livre au conteneur
            conteneur.append($livreItem);
        });
        
    } else {

        conteneur.append("Pas de livres.")
    }

    addClickEventToBooks()
}

function addClickEventToBooks() {
    const books = document.querySelectorAll(".book-list-item");

    books.forEach(book => {
        book.addEventListener("click", (e) => {
            const id = book.getAttribute('id');
            if (id) {
                window.location.href = `./livres.html?id=${id}`;
            } else {
                console.error("ID non trouvé pour ce livre.");
            }
        });
    });
}