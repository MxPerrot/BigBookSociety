token = null;

document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();  // Prevent form refresh

    // Get the username and password input values
    const formData = new FormData();
    formData.append("username", document.getElementById("username").value);
    formData.append("password", document.getElementById("password").value);

    document.getElementById("loading-spinner").style.display = "block";


    // Make the POST request to the FastAPI login endpoint
    fetch('http://127.0.0.1:8000/token', {
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
            console.log(token);
            window.location.replace("http://127.0.0.1:5500/web/index.html");
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




// document.getElementById("getData").addEventListener("click", function () {

//     console.log(token);

//     if (!token) {
//         document.getElementById("dataOutput").textContent = "No token found. Please log in.";
//         return;
//     }

//     fetch('http://127.0.0.1:8000/users/me', {
//         method: 'GET',
//         headers: {
//             'Authorization': `Bearer ${token}`,  // Include the token in the request
//             'Content-Type': 'application/json'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById("dataOutput").textContent = JSON.stringify(data, null, 2);
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         document.getElementById("dataOutput").textContent = "Failed to fetch protected data.";
//     });
// });
