// adci_dias Inicio

// // <!-- VALIDACIONES -->
//
//   // Definir el método fechaNoPasada
//   $.validator.addMethod("fechaNoPasada", function(value, element) {
//     var selectedDate = new Date(value);
//     var currentDate = new Date();
//     currentDate.setHours(0, 0, 0, 0);
//
//     return selectedDate >= currentDate;
//   }, "No se pueden seleccionar fechas pasadas.");
//
//   $.validator.addMethod("fechaCorrespondeDia", function(value, element) {
//     var selectedDate = new Date(value);
//     var selectedDayIndex = selectedDate.getDay(); // Obtener el índice del día de la semana (0 para Domingo, 1 para Lunes, ..., 6 para Sábado)
//
//     // Obtener el día de la semana seleccionado en el campo id_cita
//     var selectedDay = $("#id_cita option:selected").text().toUpperCase(); // Obtener el texto de la opción seleccionada y convertirlo a mayúsculas
//
//     // Mapeo de los días de la semana en español a sus índices (0 para Domingo, 1 para Lunes, ..., 6 para Sábado)
//     var daysOfWeek = {
//         "DOMINGO": 6,
//         "LUNES": 0,
//         "MARTES": 1,
//         "MIERCOLES": 2,
//         "JUEVES": 3,
//         "VIERNES": 4,
//         "SÁBADO": 5
//     };
//
//     // Validar que la fecha coincida con el día de la semana especificado
//     return selectedDayIndex === daysOfWeek[selectedDay]; // Devuelve true si el día de la fecha seleccionada coincide con el día especificado en id_cita
// }, "La fecha seleccionada no corresponde al día de la semana especificado.");
//
//   // Configurar la validación del formulario
//   $(document).ready(function() {
//     $("#vldt_dias").validate({
//       rules: {
//         "id_cita": {
//           required: true,
//         },
//         "fechaCita": {
//           required: true,
//           fechaNoPasada: true,
//           fechaCorrespondeDia: true
//         }
//       },
//       messages: {
//         "id_cita": {
//           required: "Debe ingresar el día de la semana.",
//         },
//         "fechaCita": {
//           required: "Debe ingresar la fecha a configurar.",
//           fechaNoPasada: "No se pueden seleccionar fechas pasadas.",
//           fechaCorrespondeDia: "La fecha no coincide con el día seleccionado."
//         }
//       }
//     });
//   });



//adci_dias FINAL
