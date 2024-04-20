document.addEventListener("DOMContentLoaded", function() {
  var cancelarButton = document.getElementById("cancelar");
  var userForm = document.getElementById("userForm");
  var sesionButton = document.getElementById("admin");

  // Función para validar el formulario
  function validarFormulario() {
      var nombre = document.getElementsByName("nombre")[0].value;
      var matricula = document.getElementsByName("matricula")[0].value;
      var contrasena = document.getElementsByName("contrasena")[0].value;
      var usuario = document.getElementsByName("usuario")[0].value;

      if (nombre.trim() === "" || matricula.trim() === "" || contrasena.trim() === "" || usuario.trim() === "") {
          Swal.fire("Error", "Por favor, completa todos los campos.", "error");
          return false;
      }

      if (contrasena.length < 6 || contrasena.length > 10) {
          Swal.fire("Error", "La contraseña debe tener entre 6 y 10 caracteres.", "error");
          return false;
      }

      if (nombre.length < 5 || nombre.length > 15 || usuario.length < 5 || usuario.length > 15) {
          Swal.fire("Error", "La longitud del nombre y usuario debe estar entre 5 y 15 caracteres.", "error");
          return false;
      }

      if (!/^\d{8}$/.test(matricula)) {
          Swal.fire("Error", "La matrícula debe tener exactamente 8 dígitos numéricos.", "error");
          return false;
      }

      // Realizar una solicitud AJAX para verificar si la matrícula ya existe
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/verificarMatricula", true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.onreadystatechange = function() {
          if (xhr.readyState === 4) {
              if (xhr.status === 200) {
                  var response = JSON.parse(xhr.responseText);
                  if (response.existe) {
                      Swal.fire("Error", "La matrícula ya está registrada", "error");
                  } else {
                      // Si la matrícula no existe, enviar el formulario
                      userForm.submit();
                  }
              } else {
                  Swal.fire("Error", "Ocurrió un error al verificar la matrícula.", "error");
              }
          }
      };
      xhr.send(JSON.stringify({ matricula: matricula }));

      // Evitar que el formulario se envíe automáticamente
      return false;
  }

  // Evento para validar el formulario al enviar
  userForm.addEventListener("submit", function(event) {
      event.preventDefault(); // Evitar enviar el formulario automáticamente
      validarFormulario(); // Llamar a la función de validación
  });

  // Evento para limpiar el formulario al hacer clic en "Cancelar"
  cancelarButton.addEventListener("click", function() {
      var inputs = document.querySelectorAll("input[name]");
      var tieneDatos = false; // Variable para verificar si algún campo tiene datos
      
      inputs.forEach(function(input) {
          if (input.value.trim() !== "") {
              tieneDatos = true; // Cambiar a true si encuentra algún campo con datos
          }
          input.value = ""; // Limpiar el valor de los campos de entrada
      });

      // Mostrar el mensaje de Sweet Alert solo si algún campo tenía datos
      if (tieneDatos) {
          Swal.fire("Cancelado", "El registro ha sido cancelado.", "info");
      }
  });

  // Evento para redirigir a la página de administración al hacer clic en "Administración"
  if (sesionButton) {
      sesionButton.addEventListener("click", function() {
          window.location.href = "/administracion";
      });
  }
});
