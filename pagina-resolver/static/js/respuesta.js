function respuesta_funcion() {
    
    let valor = document.getElementById("valor_html").value;
    let id = document.getElementById("id_html").value;

    fetch("../../agregar_respuesta/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `valor=${valor}&id=${id}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.correcto) {
                alert("Respuesta correcta y registrada");
            } else {
                alert("Respuesta incorrecta y registrada");
            }
            window.location.href = data.redirect_url + id;
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
