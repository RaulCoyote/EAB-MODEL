document.addEventListener("DOMContentLoaded", function() {
    var registroButton = document.getElementById("registro");
    var sesionButton = document.getElementById("sesion");

    registroButton.addEventListener("click", function() {
        window.location.href = "/registroadmin";
    });

    sesionButton.addEventListener("click", function() {
        window.location.href = "/iniciar";
    });
});