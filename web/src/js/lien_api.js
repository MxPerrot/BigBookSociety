async function fetchBooks() {
    try {
        const response = await fetch("http://127.0.0.1:8000/get_book_item_based/?user=1&nbrecommendation=10&limit=10");
        const books = await response.json();
        generateCarousel(books);
    } catch (error) {
        console.error("Erreur lors de la récupération des livres :", error);
    }
}

function generateCarousel(books) {
    const scroller = document.querySelector(".media-scroller");
    scroller.innerHTML = "";
    
    let groupCount = Math.ceil(books.length / 3);
    
    for (let i = 0; i < groupCount; i++) {
        let group = document.createElement("div");
        group.classList.add("media-group");
        group.id = `group-${i + 1}`;
        
        if (i > 0) {
            let prevLink = document.createElement("a");
            prevLink.classList.add("previous");
            prevLink.href = `#group-${i}`;
            prevLink.innerHTML = `<svg><use href="#previous"></use></svg>`;
            group.appendChild(prevLink);
        }
        
        for (let j = 0; j < 3; j++) {
            let bookIndex = i * 3 + j;
            if (bookIndex >= books.length) break;
            
            let element = document.createElement("div");
            element.classList.add("media-element");
            
            let img = document.createElement("img");
            img.src = books[bookIndex].cover_url || "./public/img/cover.jpg";
            img.alt = books[bookIndex].titre;
            
            element.appendChild(img);
            group.appendChild(element);
        }
        
        if (i < groupCount - 1) {
            let nextLink = document.createElement("a");
            nextLink.classList.add("next");
            nextLink.href = `#group-${i + 2}`;
            nextLink.setAttribute("aria-label", "next");
            nextLink.innerHTML = `<svg><use href="#next"></use></svg>`;
            group.appendChild(nextLink);
        }
        
        scroller.appendChild(group);
    }
}

document.addEventListener("DOMContentLoaded", fetchBooks);


document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM chargé !");
});
