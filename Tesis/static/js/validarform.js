// document.addEventListener('DOMContentLoaded', function() {
//   // Función para establecer el min date en los inputs de tipo date
//   function setMinDate(input) {
//     var today = new Date();
//     var day = String(today.getDate()).padStart(2, '0');
//     var month = String(today.getMonth() + 1).padStart(2, '0'); // Enero es 0
//     var year = today.getFullYear();
//
//     var minDate = year + '-' + month + '-' + day;
//
//     input.setAttribute('min', minDate);
//   }
//
//   // Selecciona todos los inputs de tipo date con el ID "fech_da"
//   var dateInput = document.getElementById('fech_da');
//   if (dateInput) {
//     setMinDate(dateInput);
//   }
//
//   // Escucha el evento 'show.bs.modal' para los modales
//   var exampleModal = document.getElementById('exampleModal');
//   exampleModal.addEventListener('show.bs.modal', function(event) {
//     var modalDateInput = exampleModal.querySelector('input[type="date"][name="fech_da"]');
//     if (modalDateInput) {
//       setMinDate(modalDateInput);
//     }
//   });
// });
