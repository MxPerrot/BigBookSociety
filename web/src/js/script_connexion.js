import { API_PATH } from "./config.js";

token = null;

document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();  // Prevent form refresh

    // Get the username and password input values
    const formData = new FormData();
    formData.append("username", document.getElementById("username").value);
    formData.append("password", document.getElementById("password").value);

    document.getElementById("loading-spinner").style.display = "block";


    // Make the POST request to the FastAPI login endpoint
    fetch(`${API_PATH}/token`, {
        method: 'POST',
        body: formData  // Send form data
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        const errorMessage = document.getElementById("error-message");
        document.getElementById("loading-spinner").style.display = "none";  
        if (data.access_token) {
            token=data.access_token;
            localStorage.setItem('Token', token);
            window.location.replace("../../index.html");
        } else {
            console.log("Login failed. Please check your credentials.");
            errorMessage.textContent = "Nom d'utilisateur ou mot de passe eronné.";
            errorMessage.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("loading-spinner").style.display = "none"; 
        document.getElementById("error-message").textContent = "An error occurred. Please try again.";
    });
});

