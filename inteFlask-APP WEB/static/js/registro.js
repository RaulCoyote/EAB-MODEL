document.addEventListener("DOMContentLoaded", function() {
    var registroButton = document.getElementById("cancel");
    var sesionButton = document.getElementById("regis");

    registroButton.addEventListener("click", function() {
        window.location.href = "/";
    });

    sesionButton.addEventListener("click", function() {
        window.location.href = "/iniciar";
    });
});