import { API_PATH } from "./config.js";

document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const bookId = params.get("id");

    console.log("ID du livre récupéré :", bookId); // DEBUG

    if (bookId) {
        fetchBookById(bookId);
    } else {
        console.error("Aucun ID de livre trouvé dans l'URL.");
        document.querySelector(".card").innerHTML = "<p>Aucun livre trouvé.</p>";
    }
});
   
function fetchBookById(id) {
    const url = `${API_PATH}/get_book_data_by_id/${id}`;
    
    fetch(url)
        .then(response => response.json())
        .then(book => {
            console.log("Données récupérées :", book); // DEBUG

            // Vérifie si la réponse est un tableau ou un objet
            if (!book || (Array.isArray(book) && book.length === 0)) {
                console.error("Erreur : Aucun livre trouvé ou réponse invalide.");
                document.querySelector(".card").innerHTML = "<p>Aucun livre trouvé.</p>";
                return;
            }

            const bookData = Array.isArray(book) ? book[0] : book;
            const bookContainer = document.querySelector(".card");
            const isbn = bookData.isbn13 || bookData.isbn || "Aucun ISBN disponible";
            const coverUrl = (isbn !== "Aucun ISBN disponible") 
                ? `https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg?default=false` 
                : "../../public/img/couverture.jpg";
            bookData.note_moyenne = bookData.note_moyenne ? bookData.note_moyenne.toFixed(1) : "";  

            bookContainer.innerHTML = `
                <img class="card-img" src="${coverUrl}" alt="Couverture du livre ${bookData.titre}" onerror="this.onerror=null;this.src='../../public/img/couverture.jpg';" />
                <div class="card-content">
                    <h2 class="card-title">${bookData.titre || "Titre non disponible"}</h2>
                    <h3 class="card-author">${bookData.nom_auteur || "Auteur inconnu"}</h3>
                    <p class="card-description">${bookData.description || "Description non disponible"}</p>
                    <h4 class="card-editeur">Edition: ${bookData.nom_editeur || "Éditeur inconnu"}</h4>
                    <h4 class="card-pages">Pages: ${bookData.nombre_pages || "Nombre de pages inconnu"}</h4>
                    <h4 class="card-datesortie">Date de sortie: ${bookData.date_publication || "Non disponible"}</h4>
                    <div class="card-avis">
                        <div id="noneEtat">
                            <button id="noneLikeButton" class="like-button">Like</button>
                            <button id="noneLuButton" class="like-button">Marquer comme lu</button>
                        </div>
                        <div id="likeEtat">
                            <button id="likeNoneButton" class="like-button">Liked</button>
                            <button id="likeLuButton" class="like-button">Marquer comme lu</button>
                        </div>
                        <div id="luEtat">
                            <button id="luLikeButton" class="like-button">Mettre dans la whislist</button>
                            <button id="luNoneButton" class="like-button">Retirer de la liste</button>
                        </div>
                        <div id="average-section">
                            <p>Note moyenne : ${bookData.note_moyenne} </p>
                            <div id="average-stars" class="group_stars"></div>
                        </div>
                        <div id="rating-section" style="display: none;">
                            <button id="validate-btn" class="note-button">Valider</button>
                            <div id="rating-stars" class="group_stars"></div>
                        </div>
                        <div id="display-section" style="display: none;">
                            <button id="modify-btn" class="note-button">Modifier</button>
                            <div id="display-stars" class="group_stars"></div>
                        </div>
                    </div>
                </div>
            `;

            ///// CONSTANTES /////

            const noneEtat = document.getElementById("noneEtat");
            const likeEtat = document.getElementById("likeEtat");
            const luEtat = document.getElementById("luEtat");

            const noneLikeButton = document.getElementById("noneLikeButton");
            const noneLuButton = document.getElementById("noneLuButton");
            const likeNoneButton = document.getElementById("likeNoneButton");
            const likeLuButton = document.getElementById("likeLuButton");
            const luLikeButton = document.getElementById("luLikeButton");
            const luNoneButton = document.getElementById("luNoneButton");

            const averageSection = document.getElementById('average-section');
            const averageStars = document.getElementById('average-stars');
            const ratingStars = document.getElementById("rating-stars");
            const validateBtn = document.getElementById("validate-btn");
            const displaySection = document.getElementById("display-section");
            const displayStars = document.getElementById("display-stars");
            const modifyBtn = document.getElementById("modify-btn");
            const ratingSection = document.getElementById("rating-section");
            let selectedRating = 0;

            ///// FETCH /////

            noneEtat.style.display = "block";
            likeEtat.style.display = "none";
            luEtat.style.display = "none";
            displayAverageRating(bookData.note_moyenne);

            fetch(`${API_PATH}/is_liked/?bookID=${id}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                    'Content-Type': 'application/json'
                }                  
            }).then(response => response.json())
            .then(answer => {
                if (answer=="True"){
                    noneEtat.style.display = "none";
                    likeEtat.style.display = "block";
                    luEtat.style.display = "none";
                }
            });

            fetch(`${API_PATH}/get_lu/?bookID=${id}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                    'Content-Type': 'application/json'
                }                  
            }).then(response => response.json())
            .then(answer => {
                if (answer==true || answer==1){
                    noneEtat.style.display = "none";
                    likeEtat.style.display = "none";
                    luEtat.style.display = "block";
                    createStars(displaySection, displayStars, null);
                }
            });

            fetch(`${API_PATH}/get_note/?bookID=${id}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                    'Content-Type': 'application/json'
                }                  
            }).then(response => response.json())
            .then(answer => {
                selectedRating = 0;
                answer = answer[0][0];
                if (answer) {
                    selectedRating = answer;
                }
            });

            

            ///// LISTENERS /////

            noneLikeButton.addEventListener("click", function () {
                fetch(`${API_PATH}/like/?bookID=${id}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }                  
                    })
                .then(response => response.json())  // Parse response as JSON
                .then(data => console.log('Response:', data))  // Log the response
                .catch(error => console.error('Error:', error));
                noneEtat.style.display = "none";
                likeEtat.style.display = "block";
                luEtat.style.display = "none";
                console.log("none to like");
                displaySection.style.display = "none";
                ratingSection.style.display = "none";
            });

            noneLuButton.addEventListener("click", function () {
                fetch(`${API_PATH}/like/?bookID=${id}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())  // Parse response as JSON
                .then(data => console.log('Response:', data))  // Log the response
                .catch(error => console.error('Error:', error));

                fetch(`${API_PATH}/yes_lu/?bookID=${id}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())  // Parse response as JSON
                .then(data => console.log('Response:', data))  // Log the response
                .catch(error => console.error('Error:', error));
                noneEtat.style.display = "none";
                likeEtat.style.display = "none";
                luEtat.style.display = "block";
                console.log("none to lu");
                displaySection.style.display = "block";
                ratingSection.style.display = "none";
            });

            likeNoneButton.addEventListener("click", function () {
                fetch(`${API_PATH}/unlike/?bookID=${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())  // Parse response as JSON
                .then(data => console.log('Response:', data))  // Log the response
                .catch(error => console.error('Error:', error));
                noneEtat.style.display = "block";
                likeEtat.style.display = "none";
                luEtat.style.display = "none";
                console.log("like to none");
                displaySection.style.display = "none";
                ratingSection.style.display = "none";
            });

            likeLuButton.addEventListener("click", function () {
                fetch(`${API_PATH}/yes_lu/?bookID=${id}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())  // Parse response as JSON
                .then(data => console.log('Response:', data))  // Log the response
                .catch(error => console.error('Error:', error));
                noneEtat.style.display = "none";
                likeEtat.style.display = "none";
                luEtat.style.display = "block";
                console.log("like to lu");
                displaySection.style.display = "block";
                ratingSection.style.display = "none";
            });

            luLikeButton.addEventListener("click", function () {
                fetch(`${API_PATH}/no_lu/?bookID=${id}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())  // Parse response as JSON
                .then(data => console.log('Response:', data))  // Log the response
                .catch(error => console.error('Error:', error));
                noneEtat.style.display = "none";
                likeEtat.style.display = "block";
                luEtat.style.display = "none";
                console.log("lu to like");
                displaySection.style.display = "none";
                ratingSection.style.display = "none";
            });

            luNoneButton.addEventListener("click", function () {
                fetch(`${API_PATH}/unlike/?bookID=${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())  // Parse response as JSON
                .then(data => console.log('Response:', data))  // Log the response
                .catch(error => console.error('Error:', error));       
                noneEtat.style.display = "block";
                likeEtat.style.display = "none";
                luEtat.style.display = "none"; 
                console.log("lu to none");
                displaySection.style.display = "none";
                ratingSection.style.display = "none";       
            });

            /*
            luButton.addEventListener("click", function () {
                luButton.classList.toggle("lu");
                luButton.textContent = luButton.classList.contains("lu") ? "Marquer comme non-lu" : "Marquer comme lu";

                var estlu = luButton.textContent.trim() == "Marquer comme non-lu";
                if (estlu) {
                    fetch(`${API_PATH}/yes_lu/?bookID=${id}`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                            'Content-Type': 'application/json'
                        }                  
                        })
                    .then(response => response.json())  // Parse response as JSON
                    .then(data => console.log('Response:', data))  // Log the response
                    .catch(error => console.error('Error:', error));
                    likeButton.style.display = "none";
                    displaySection.style.display = "block";
                    ratingSection.style.display = "none";
                } else {
                    fetch(`${API_PATH}/no_lu/?bookID=${id}`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                            'Content-Type': 'application/json'
                        }                  
                        })
                    .then(response => response.json())  // Parse response as JSON
                    .then(data => console.log('Response:', data))  // Log the response
                    .catch(error => console.error('Error:', error));
                    likeButton.style.display = "block";
                    displaySection.style.display = "none";
                    ratingSection.style.display = "none";
                }
            });
            */

            ///// NOTATIONS /////

            console.log("s : " + selectedRating);

            /* Modification du nombre d'étoiles affichées dans la moyenne */
            function displayAverageRating(average) {
                averageStars.innerHTML = "";
                for (let i = 1; i <= 5; i++) {
                    if (i <= Math.floor(average)) {
                        let star = createFullStar();
                        star.classList.add("red");
                        averageStars.appendChild(star);
                    } else if (i - 1 < average && average % 1 !== 0) {
                        let halfStar = createHalfStar(average % 1);
                        averageStars.appendChild(halfStar);
                    } else {
                        let star = createFullStar();
                        star.classList.add("empty");
                        averageStars.appendChild(star);
                    }
                }
            }

            /* Créé une étoile entière */
            function createFullStar() {
                const star = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                star.setAttribute("viewBox", "0 0 24 24");
                star.setAttribute("class", "star");
                star.innerHTML = '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.86L12 17.77l-6.18 3.23L7 14.14l-5-4.87 6.91-1.01z"/>';
                return star;
            }

            /* Créé une étoile partielle */
            function createHalfStar(percentage) {
                const div = document.createElement("div");
                div.classList.add("half-star");

                const emptyStar = createFullStar();
                emptyStar.classList.add("empty");

                const fullStar = createFullStar();
                fullStar.classList.add("full");
                fullStar.style.clipPath = `inset(0 ${(1 - percentage) * 100}% 0 0)`;

                div.appendChild(emptyStar);
                div.appendChild(fullStar);

                return div;
            }

            /* Créer un bloc d'étoiles */
            function createStars(section, container, clickHandler) {
                ratingSection.style.display = "none";
                displaySection.style.display = "none";
                section.style.display = "block";

                container.innerHTML = "";
                for (let i = 1; i <= 5; i++) {
                    const star = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                    star.setAttribute("viewBox", "0 0 24 24");
                    star.setAttribute("class", "star");
                    star.innerHTML = '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.86L12 17.77l-6.18 3.23L7 14.14l-5-4.87 6.91-1.01z"/>';
                    container.appendChild(star);
                    if (i <= selectedRating) {
                        star.classList.add("red");
                    }

                    if (clickHandler) {
                        star.addEventListener("mouseover", () => updateStarColors(i));
                        star.addEventListener("mouseleave", () => updateStarColors(selectedRating));
                        star.addEventListener("click", () => {
                            selectedRating = i;
                            updateStarColors(selectedRating);
                        });
                    }
                }
            }

            /* fonction update couleur de l'étoile */
            function updateStarColors(rating) {
                createStars(ratingSection, ratingStars, true);
                const stars = ratingStars.querySelectorAll(".star");
                stars.forEach((star, index) => {
                    if (index < rating) {
                        star.classList.add("red");
                        star.classList.remove("beige");
                    } else {
                        star.classList.remove("red");
                        if (index < selectedRating) {
                            star.classList.add("beige");
                        } else {
                            star.classList.remove("beige");
                        }
                    }
                });
                
            }

            validateBtn.addEventListener("click", () => {
                if (selectedRating >= 0) {
                    ratingSection.style.display = "none";
                    displaySection.style.display = "block";
                    updateDisplayStars(selectedRating);
                    fetch(`${API_PATH}/update_note/?bookID=${id}&note=${selectedRating}`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('Token')}`,  // Include the token in the request
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ bookID: id, note: selectedRating })
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! Status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('enregistrement réussi');
                    })
                    .catch(error => {
                        console.error('Fetch error:', error);
                    });
                }
            });

            modifyBtn.addEventListener("click", () => {
                displaySection.style.display = "none";
                ratingSection.style.display = "block";
                updateStarColors(selectedRating);
            });

            function updateDisplayStars(rating) {
                createStars(displaySection, displayStars, null);
                displayStars.querySelectorAll(".star").forEach((star, index) => {
                    if (index < rating) {
                        star.classList.add("red");
                    }
                });
            }
        })
        .catch(error => {
            console.error("Erreur lors de la récupération du livre :", error);
        });
}
