const API_URL = "http://localhost:8080/film";

const form = document.getElementById("user-form");

form.addEventListener("submit", function (event) {
    event.preventDefault();
    checkUser();
});

function checkUser() {
    let email = document.getElementById("exampleInputEmail").value;
    let password = document.getElementById("exampleInputPassword").value;
    fetch(API_URL + "/" + email + "/" + password)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if(data != null) {
                console.log("Response JSON data:", data); 
                //datanın alanlarını kontrol et. eğer data.email ve data.password, ekrandan girilen değerlerle uyuşuyor ise içeriye yönlendirme yap.
                //window.location.href = "dashboard.html"
            }
        })
        .catch(error => {
            console.error("Bir hata oluştu:", error);
        });
}
