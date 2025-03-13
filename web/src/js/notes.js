document.addEventListener("DOMContentLoaded", function () {
    /* Variables */
    const ratingStars = document.getElementById("rating-stars");
    const validateBtn = document.getElementById("validate-btn");
    const displaySection = document.getElementById("display-section");
    const displayStars = document.getElementById("display-stars");
    const modifyBtn = document.getElementById("modify-btn");
    const ratingSection = document.getElementById("rating-section");
    const averageStars = document.getElementById("average-stars");

    console.log()

    /* Note de l'user */
    let selectedRating = 0;

    /* Créer un bloc d'étoiles */
    function createStars(container, clickHandler) {
        container.innerHTML = "";
        for (let i = 1; i <= 5; i++) {
            /* Dessin d'une étoile */
            const star = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            star.setAttribute("viewBox", "0 0 24 24");
            star.setAttribute("class", "star");
            star.innerHTML = '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.86L12 17.77l-6.18 3.23L7 14.14l-5-4.87 6.91-1.01z"/>';
            container.appendChild(star);

            /* events survol / click des étoiles */
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

    /* Valider : noter -> afficher ma note */
    validateBtn.addEventListener("click", () => {
        if (selectedRating > 0) {
            ratingSection.style.display = "none";
            displaySection.style.display = "block";
            updateDisplayStars(selectedRating);
        }
    });

    /* Modifier : afficher ma note -> noter */
    modifyBtn.addEventListener("click", () => {
        displaySection.style.display = "none";
        ratingSection.style.display = "block";
        updateStarColors(selectedRating);
    });

    /* Modification du nombre d'étoiles affichées selon la note */
    function updateDisplayStars(rating) {
        createStars(displayStars, null);
        displayStars.querySelectorAll(".star").forEach((star, index) => {
            if (index < rating) {
                star.classList.add("red");
            }
        });
    }

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

    createStars(ratingStars, true);
});