document.addEventListener('DOMContentLoaded', function() {
  // Función para establecer el min date en los inputs de tipo date
  function setMinDate(input) {
    var today = new Date();
    var day = String(today.getDate()).padStart(2, '0');
    var month = String(today.getMonth() + 1).padStart(2, '0'); // Enero es 0
    var year = today.getFullYear();

    var minDate = year + '-' + month + '-' + day;

    input.setAttribute('min', minDate);
  }

  // Selecciona todos los inputs de tipo date con nombre diaH
  var dateInputs = document.querySelectorAll('input[type="date"][name="diaH"]');
  dateInputs.forEach(function(input) {
    setMinDate(input);
  });

  // Escucha el evento 'show.bs.modal' para los modales
  var exampleModal = document.getElementById('exampleModal');
  exampleModal.addEventListener('show.bs.modal', function(event) {
    var dateInput = exampleModal.querySelector('input[type="date"][name="diaH"]');
    setMinDate(dateInput);
  });
});
