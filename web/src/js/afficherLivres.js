// Fonction pour afficher une liste de livres dans un conteneur donné
function afficherLivres(livres, conteneur) {
    
    // D'abord, vider le conteneur
    conteneur.empty()

    // Itération sur le tableau des livres
    $.each(livres, function(index, livre) {
        // Création d'une div pour chaque livre avec un id unique et une classe
        var $livreItem = $('<div>', {
            id: 'book' + (index + 1),
            class: 'book-list-item'
        });

        // Construction de l'URL de l'image en utilisant la propriété isbn13
        
        var urlImage = 'https://covers.openlibrary.org/b/isbn/' + livre.isbn13 + '-L.jpg?default=false';
        // Création d'un élément img avec l'attribut src défini sur l'URL de l'image
        
        var $img = $('<img>', {
            src: urlImage,
            alt: livre.titre
        });
        
        // Ajout de l'image à la div du livre
        $livreItem.append($img);
        
        // Ajout de l'élément livre au conteneur
        conteneur.append($livreItem);
        console.log(conteneur.html())

    });
}
