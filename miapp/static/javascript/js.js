document.addEventListener("DOMContentLoaded", function () {
  const imagen = document.querySelector("#file");
  const imagenMostrada = document.querySelector("#imagenMostrada");
  const btnEnviar = document.querySelector("#btnEnviar");
  const selectOperador = document.querySelector("#selectOperador");
  const bordeCanny = document.querySelector("#bordeCanny");
  const btnEliminarImage = document.querySelector("#btnEliminarImage");
  const imagenProcesada = document.querySelector("#imagenProcesada");
  const umbral1 = document.querySelector("#umbral1");
  const umbral2 = document.querySelector("#umbral2");
  const valueRango = document.querySelector("#valueRango");
  const valueRango2 = document.querySelector("#valueRango2");
  let valores = {
    operador: "",
    canny: 0,
    umbral1: 0,
    umbral2: 0,
  };
  const reader = new FileReader();

  umbral1.addEventListener("input", function (e) {
    const valor = e.target.value;
    valueRango.textContent = valor;
    valores.umbral1 = valor;
    console.log(valores);
  });

  umbral2.addEventListener("input", function (e) {
    const valor = e.target.value;

    valueRango2.textContent = valor;
    valores.umbral2 = valor;
    console.log(valores);
  });

  selectOperador.addEventListener("change", function (e) {
    const operador = e.target.value;
    valores.operador = operador;

    umbral1.value = 0;
    umbral2.value = 0;
    valueRango.textContent = 0;
    valueRango2.textContent = 0;
    valores.umbral1 = 0;
    valores.umbral2 = 0;

    if (operador == "umbral" || operador == "invUmbral") {
      umbral1.classList.remove("d-none");
      umbral1.classList.add("d-block");
      umbral2.classList.add("d-none");
    } else if (operador == "umbrales" || operador == "umbralesInv") {
      umbral1.classList.remove("d-none");
      umbral1.classList.add("d-block");
      umbral2.classList.remove("d-none");
      umbral2.classList.add("d-block");
    } else {
      umbral1.classList.add("d-none");
      umbral2.classList.add("d-none");
    }

    console.log(valores);
  });

  bordeCanny.addEventListener("change", function (e) {
    if (bordeCanny.checked) {
      valores.canny = 1;
    } else {
      valores.canny = 0;
    }
  });

  btnEliminarImage.addEventListener("click", function (e) {
    if (imagenProcesada.style.display != "block") {
      return;
    }
    fetch("/eliminar/", {
      method: "POST",
      body: "",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        imagenProcesada.style.display = "none";
      });
    location.reload();
  });

  imagen.addEventListener("change", function (e) {
    if (imagenProcesada.style.display == "block") {
      alert("Debe eliminar la imagen procesada antes de subir otra");
      return;
    }

    const file = e.target.files[0];

    reader.onload = function () {
      imagenMostrada.src = reader.result;
      imagenMostrada.style.display = "block";
    };

    reader.readAsDataURL(file);

    btnEnviar.addEventListener("click", function (e) {
      const formData = new FormData();
      formData.append("imagen", file);
      formData.append("operador", valores.operador);
      formData.append("canny", valores.canny);
      formData.append("umbral1", valores.umbral1);
      formData.append("umbral2", valores.umbral2);
      console.log(formData);
      fetch("/prueba/", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          const timestamp = new Date().getTime();
          imagenProcesada.src = imagenProcesadaUrl + "?t=" + timestamp;
          imagenProcesada.style.display = "block";
        });
    });
  });
});
