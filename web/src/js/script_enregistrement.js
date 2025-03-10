import { API_PATH } from "./config.js";

token = null;

// Assuming API_PATH is defined globally or imported elsewhere
var token = null;

$(document).ready(function() {
    $("#registerForm").on("submit", function(event) {
        event.preventDefault(); // Prevent form refresh

        // Serialize the form data into a URL-encoded string
        var data = $(this).serialize();

        $.ajax({
        url: API_PATH + "/register",
        type: "POST",
        data: data, // Data is sent in the request body
        success: function(response) {
            console.log(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
        }
        });
    });
});
  
  