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

  const cannyumbral1 = document.querySelector("#cannyumbral1");
  const cannyumbral2 = document.querySelector("#cannyumbral2");
  const valueUmbral1 = document.querySelector("#valueUmbral1");
  const valueUmbral2 = document.querySelector("#valueUmbral2");

  let valores = {
    operador: "",
    canny: 0,
    umbral1: 0,
    umbral2: 0,
    cannyMin: 0,
    cannyMax: 0,
  };
  const reader = new FileReader();

  cannyumbral1.addEventListener("input", function (e) {
    const valor = e.target.value;
    valores.cannyMin = parseInt(valor);
    valueUmbral1.textContent = valor;
    console.log(valores);
  });

  cannyumbral2.addEventListener("input", function (e) {
    const valor = e.target.value;
    valores.cannyMax = parseInt(valor);
    valueUmbral2.textContent = valor;
    console.log(valores);
  });

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

    cannyumbral1.value = 0;
    cannyumbral2.value = 0;
    valueUmbral1.textContent = 0;
    valueUmbral2.textContent = 0;
    valores.cannyMin = 0;
    valores.cannyMax = 0;

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
      console.log("checked");
      valores.canny = 1;
      cannyumbral1.classList.remove("d-none");
      cannyumbral1.classList.add("d-block");
      cannyumbral2.classList.remove("d-none");
      cannyumbral2.classList.add("d-block");
    } else {
      valores.canny = 0;
      cannyumbral1.classList.remove("d-block");
      cannyumbral1.classList.add("d-none");
      cannyumbral2.classList.remove("d-block");
      cannyumbral2.classList.add("d-none");
      cannyumbral1.value = 0;
      cannyumbral2.value = 0;
      valueUmbral1.textContent = 0;
      valueUmbral2.textContent = 0;
      valores.cannyMin = 0;
      valores.cannyMax = 0;
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
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Debe eliminar la imagen procesada antes de subir otra",
      });
      return;
    }

    const file = e.target.files[0];

    reader.onload = function () {
      imagenMostrada.src = reader.result;
      imagenMostrada.style.display = "block";
    };

    reader.readAsDataURL(file);

    btnEnviar.addEventListener("click", function (e) {
      if (valores.canny == 1) {
        if (valores.cannyMax < valores.cannyMin || valores.cannyMin == 0) {
          console.log(valores.cannyMax, valores.cannyMin);
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "El valor del umbral minimo debe de ser menor que el valor del umbral maximo",
          });

          return;
        }
      }
      console.log(valores.cannyMax, valores.cannyMin);
      const formData = new FormData();
      formData.append("imagen", file);
      formData.append("operador", valores.operador);
      formData.append("canny", valores.canny);
      formData.append("umbral1", valores.umbral1);
      formData.append("umbral2", valores.umbral2);
      formData.append("cannyMin", valores.cannyMin);
      formData.append("cannyMax", valores.cannyMax);
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
