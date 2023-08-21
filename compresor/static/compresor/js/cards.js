document.getElementById("archivoInput").addEventListener("change", function () {
    const listaArchivos = document.getElementById("listaArchivos");
    listaArchivos.innerHTML = ""; // Limpia la lista anterior

    for (const archivo of this.files) {
        // Crea un div con clases CSS específicas
        const divCard = document.createElement("div");
        divCard.classList.add("card");

        const divContent = document.createElement("div");
        divContent.classList.add("content");

        const divHeader = document.createElement("div");
        divHeader.classList.add("header");
        divHeader.textContent = archivo.name;

        const divDescription = document.createElement("div");
        divDescription.classList.add("description");
        divDescription.textContent = `Tipo de archivo: ${archivo.type}`;

        const botonEliminar = document.createElement("button");
        botonEliminar.classList.add("ui", "teal", "button");
        botonEliminar.textContent = "Eliminar";
        botonEliminar.addEventListener("click", function () {
            // Eliminar este archivo de la lista
            divCard.remove();
        });

        // Agrega los elementos al div listaArchivos
        divContent.appendChild(divHeader);
        divContent.appendChild(divDescription);
        divCard.appendChild(divContent);
        divContent.appendChild(botonEliminar);
        listaArchivos.appendChild(divCard);
    }
});