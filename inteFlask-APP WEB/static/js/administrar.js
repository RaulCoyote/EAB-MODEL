document.addEventListener("DOMContentLoaded", function() {
    // Obtener referencia al botón de registro
    var registroButton = document.getElementById("registro");

    // Verificar si el botón de registro existe
    if (registroButton) {
        // Agregar un event listener para el botón de registro
        registroButton.addEventListener('click', function() {
            // código del event listener
            window.location.href = "/registro";
        });
    }

    // Obtener referencia al botón de inicio de sesión
    var sesionButton = document.getElementById("sesion");

    // Verificar si el botón de inicio de sesión existe
    if (sesionButton) {
        // Agregar un event listener para el botón de inicio de sesión
        sesionButton.addEventListener("click", function() {
            // Redirigir a la página de inicio de sesión al hacer clic en el botón
            window.location.href = "/iniciar";
        });
    }
});
