document.addEventListener("DOMContentLoaded", function () {
    function addSeparatorToField(fieldId) {
        let field = document.getElementById(fieldId);
        if (field) {
            field.value += "\n@@@\n";
        }
    }

    let entradasBtn = document.createElement("button");
    entradasBtn.type = "button";
    entradasBtn.classList.add("btn", "btn-primary", "btn-sm", "mt-1", "me-1", "px-2", "py-1");
    entradasBtn.textContent = "➕ Añadir @@@";
    entradasBtn.onclick = function () {
        addSeparatorToField("id_entradas_prueba");
    };

    let salidasBtn = document.createElement("button");
    salidasBtn.type = "button";
    salidasBtn.classList.add("btn", "btn-primary", "btn-sm", "mt-1", "me-1", "px-2", "py-1");
    salidasBtn.textContent = "➕ Añadir @@@";
    salidasBtn.onclick = function () {
        addSeparatorToField("id_salidas_esperadas");
    };

    let entradaField = document.getElementById("id_entradas_prueba");
    let salidaField = document.getElementById("id_salidas_esperadas");

    if (entradaField && salidaField) {
        entradaField.insertAdjacentElement("beforebegin", entradasBtn);
        salidaField.insertAdjacentElement("beforebegin", salidasBtn);
    }
});
