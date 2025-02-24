document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('https://example.com/api/books');
        
        if (!response.ok) throw new Error('Erreur lors de la récupération des données');
        
        const books = await response.json();
        const mainElement = document.querySelector('main');

        books.forEach(book => {
            const card = document.createElement('div');
            card.classList.add('card');

            card.innerHTML = `
                <img src="${book.image}" alt="Book Cover" class="card-img">
                <div class="card-content">
                    <h2 class="card-title">${book.title}</h2>
                    <h3 class="card-author">${book.author}</h3>
                    <p class="card-description">${book.description}</p>
                    <h4 class="card-editeur">${book.edition}</h4>
                    <h4 class="card-pages">${book.pages} pages</h4>
                    <h4 class="card-datesortie">Sortie ${new Date(book.release_date).toLocaleDateString()}</h4>
                    <button class="bouton-ajouter">Ajouter livre</button>
                </div>
            `;

            mainElement.appendChild(card);
        });

    } catch (error) {
        console.error('Erreur :', error);
    }
});
