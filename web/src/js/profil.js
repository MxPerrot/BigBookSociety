import { API_PATH } from "./config.js";

document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("Token");

    if (!token) {
        alert("Vous devez être connecté pour accéder à votre profil.");
        window.location.href = "../html/connexion.html"; // Redirige vers la page de connexion
        return;
    }

    // Sélection des éléments du DOM
    const profileName = document.querySelector(".profile-name");
    const profileDob = document.querySelector(".profile-email");
    const profileLanguages = document.querySelector(".profile-languages");

    // Récupération des données de l'utilisateur
    fetch(`${API_PATH}/users/me`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(user => {
        profileName.textContent = user.username || "Nom inconnu";
        profileDob.textContent = `Email: ${user.email || "Non renseigné"}`;
        profileLanguages.textContent = `Langues: ${user.languages || "Non renseigné"}`;
    })
    .catch(error => console.error("Erreur lors de la récupération du profil:", error));

    // Fonction pour modifier et enregistrer les informations du profil
    function updateUserData(field, value) {
        fetch(`${API_PATH}/users/update`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({'key':field,'value':value})
        })
        .then(response => response.json())
        .then(updatedUser => {
            console.log("Mise à jour réussie:", updatedUser);
        })
        .catch(error => console.error("Erreur lors de la mise à jour:", error));
    }

    // Modifier le nom
    window.editProfileName = function () {
        const newName = prompt("Entrez votre nouveau nom:", profileName.textContent);
        if (newName) {
            profileName.textContent = newName;
            updateUserData("username", newName);
        }
    };

    // Modifier la date de naissance
    window.editProfileEmail = function () {
        const newEmail = prompt("Entrez votre nouvel email:", profileDob.textContent.replace("Email: ", ""));
        if (newEmail) {
            profileDob.textContent = "Email: " + newEmail;
            updateUserData("email", newEmail);
        }
    };

    // Modifier les langues
    window.editProfileLanguages = function () {
        const newLanguages = prompt("Entrez vos langues parlées:", profileLanguages.textContent.replace("Langues: ", ""));
        if (newLanguages) {
            profileLanguages.textContent = "Langues: " + newLanguages;
            updateUserData("languages", newLanguages);
        }
    };

    // Modifier la photo de profil
    window.changeProfileImage = function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                profileImage.src = e.target.result;

                // Envoyer l'image au serveur
                const formData = new FormData();
                formData.append("profile_image", file);

                fetch(`${API_PATH}/users/update-image`, {
                    method: "PUT",
                    headers: { Authorization: `Bearer ${token}` },
                    body: formData
                })
                .then(response => response.json())
                .then(data => console.log("Image mise à jour:", data))
                .catch(error => console.error("Erreur lors du changement de l'image:", error));
            };
            reader.readAsDataURL(file);
        }
    };
});
