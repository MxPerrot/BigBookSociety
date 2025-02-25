const books = [
    { title: 'Book One', author: 'Author One', genre: 'fiction', rating: 4.5, cover: '../../public/img/goat.jpg' },
    { title: 'Book Two', author: 'Author Two', genre: 'non-fiction', rating: 3.8, cover: '../../public/img/cover.jpg' },
    { title: 'Book Three', author: 'Author Three', genre: 'fantasy', rating: 4.2, cover: '../../public/img/cover.jpg' },
    // Add more books as needed
];

function filterBooks() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const genreSelect = document.getElementById('genre-select').value;
    const minRating = parseFloat(document.getElementById('min-rating').value);
    const maxRating = parseFloat(document.getElementById('max-rating').value);
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';

    const filteredBooks = books.filter(book => 
        (book.title.toLowerCase().includes(searchInput) || 
        book.author.toLowerCase().includes(searchInput)) &&
        (genreSelect === '' || book.genre === genreSelect) &&
        book.rating >= minRating && book.rating <= maxRating
    );

    filteredBooks.forEach(book => {
        const bookCard = document.createElement('div');
        bookCard.className = 'book-card';

        const bookCover = document.createElement('img');
        bookCover.src = book.cover;
        bookCover.alt = book.title;

        const bookInfo = document.createElement('div');
        const bookTitle = document.createElement('h3');
        bookTitle.textContent = book.title;
        const bookAuthor = document.createElement('p');
        bookAuthor.textContent = `by ${book.author}`;
        const bookRating = document.createElement('p');
        bookRating.textContent = `Rating: ${book.rating}`;

        bookInfo.appendChild(bookTitle);
        bookInfo.appendChild(bookAuthor);
        bookInfo.appendChild(bookRating);
        bookCard.appendChild(bookCover);
        bookCard.appendChild(bookInfo);

        resultsContainer.appendChild(bookCard);
    });
}

function updateRatingRange() {
    const minRating = document.getElementById('min-rating').value;
    const maxRating = document.getElementById('max-rating').value;
    document.getElementById('rating-range').textContent = `${minRating} - ${maxRating}`;
    filterBooks();
}