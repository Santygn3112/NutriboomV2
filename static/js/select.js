// Función principal para convertir los selects múltiples en dropdowns personalizados
function DropdownMultiselect() {
  // Selecciona todos los elementos <select> con el atributo 'multiple'
  document.querySelectorAll("select[multiple]").forEach((select) => {
    
    // Ocultar el select original, ya que vamos a reemplazarlo por un dropdown personalizado
    select.style.display = "none";

    // Crear el contenedor del dropdown
    const contenedor = document.createElement("div");
    contenedor.classList.add("multiselect-dropdown");

    // Crear la lista de opciones que se mostrarán en el dropdown
    const lista = document.createElement("div");
    lista.classList.add("multiselect-dropdown-list");

    // Insertar el contenedor del dropdown después del select original
    select.after(contenedor);
    contenedor.appendChild(lista);

    // Función para actualizar las opciones seleccionadas que se muestran arriba del dropdown
    function refrescar() {
      // Eliminar las opciones previas seleccionadas
      contenedor.querySelectorAll(".optext, .placeholder").forEach(el => el.remove());
      
      // Obtener las opciones seleccionadas
      const seleccionados = Array.from(select.selectedOptions);

      // Si no hay opciones seleccionadas, mostrar un texto de placeholder
      if (seleccionados.length === 0) {
        contenedor.prepend(createElement("span", { class: "placeholder", text: "seleccionar" }));
      } else {
        // Si hay opciones seleccionadas, mostrar cada una de ellas como un 'tag'
        seleccionados.forEach((opcion) => {
          const tag = createElement("span", { class: "optext", text: opcion.text });
          const eliminar = createElement("span", {
            class: "optdel",
            text: "🗙", // El icono para eliminar la opción
            onclick: () => {
              opcion.selected = false; // Desmarcar la opción
              refrescar(); // Actualizar la vista
            }
          });
          tag.appendChild(eliminar); // Agregar el botón de eliminar a cada tag
          contenedor.insertBefore(tag, lista); // Insertar el tag arriba de la lista
        });
      }
    }

    // Función para cargar las opciones dentro del dropdown
    function cargarOpciones() {
      lista.innerHTML = ""; // Limpiar la lista antes de cargar las opciones
      Array.from(select.options).forEach((opcion) => {
        const item = document.createElement("div");
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = opcion.selected; // Marcar si la opción está seleccionada

        item.appendChild(checkbox); // Agregar el checkbox
        item.append(" " + opcion.text); // Agregar el texto de la opción

        // Manejar el clic en cada opción para marcar o desmarcar el checkbox
        item.addEventListener("click", () => {
          opcion.selected = checkbox.checked; // Actualizar el estado de selección de la opción
          refrescar(); // Actualizar la vista
          select.dispatchEvent(new Event("change")); // Disparar el evento 'change' para actualizar el select original
        });

        lista.appendChild(item); // Agregar el item de opción al dropdown
      });
    }

    // Mostrar u ocultar la lista de opciones al hacer clic en el contenedor
    contenedor.addEventListener("click", () => {
      lista.style.display = lista.style.display === "block" ? "none" : "block"; // Alternar la visibilidad de la lista
    });

    // Si se hace clic fuera del contenedor, ocultar la lista
    document.addEventListener("click", (e) => {
      if (!contenedor.contains(e.target)) {
        lista.style.display = "none"; // Ocultar la lista si se hace clic fuera
      }
    });

    cargarOpciones(); // Llamar a la función para cargar las opciones
    refrescar(); // Actualizar la vista inicial
  });
}

// Ejecutar la función 'DropdownMultiselect' cuando la página se haya cargado completamente
window.addEventListener("load", DropdownMultiselect);

// Función auxiliar para crear elementos HTML con atributos dinámicos
function createElement(tag, attrs = {}) {
  const el = document.createElement(tag); // Crear el elemento HTML
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") el.classList.add(value); // Agregar clase al elemento
    else if (key === "text") el.innerHTML = value; // Agregar texto al elemento
    else el[key] = value; // Asignar otros atributos al elemento
  }
  return el; // Devolver el elemento creado
}
