const API_URL = "http://localhost:8080/film";

let username;
let email;
let password;
const form = document.getElementById("user")

function createJson() {
    username = document.getElementById("name").value;
    email = document.getElementById("email").value;
    password = document.getElementById("password").value;
    console.log(username)
    return {
        "name": username,
        "email": email,
        "password": password
    }
}

form.addEventListener("submit", function (event) {
    event.preventDefault();
    saveUser();
});

function saveUser() {
    const jsonBody = createJson()
    console.log(jsonBody)
    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonBody),
    })
        .then((response) => {
            if (!response.ok) {
                alert("Something wrong. Please try again later.")
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            window.location.href = "login.html"
        })
        .catch((error) => {
            console.error("Hata:", error);
        });
}