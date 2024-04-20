document.addEventListener("DOMContentLoaded", function() {
    var registroButton = document.getElementById("regi");
    var sesionButton = document.getElementById("can");
    var adminButton = document.getElementById("adm");

    if (registroButton) {
        registroButton.addEventListener("click", function() {
            window.location.href = "/registroadmin";
        });
    }

    if (sesionButton) {
        sesionButton.addEventListener("click", function() {
            window.location.href = "/";
        });
    }

    if (adminButton) {
        adminButton.addEventListener("click", function() {
            window.location.href = "/añadirusuario";
        });
    }
});
