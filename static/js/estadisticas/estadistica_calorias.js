window.onload = async function () {
  const contenedorGrafico = document.getElementById("chart");

  const dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"];

  try {
    const respuestaUsuario = await fetch("http://localhost:5000/ver_id_usuario");
    const usuario = await respuestaUsuario.json();

    const respuestaEstadistica = await fetch(
      `http://localhost:5000/estadistica_calorias/${usuario.id_usuario}`
    );
    const datos = await respuestaEstadistica.json();

    if (!Array.isArray(datos) || datos.length === 0) {
      contenedorGrafico.innerHTML =
        "<h2>No tienes datos registrados, por favor añade comidas</h2>";
      return;
    }

    const calorias = [];
    dias.forEach((dia) => {
      const item = datos.find((d) => d.dia === dia);
      calorias.push(item ? item.calorias : null);
    });

    const grafico = echarts.init(contenedorGrafico);

    const opcion = {
      title: {
        left: "center",
        textStyle: {
          fontSize: 24,
          fontWeight: "bold",
          color: "#333",
        },
      },
      tooltip: {
        trigger: "axis",
      },
      legend: {
        data: ["Calorías"],
        orient: "horizontal",
        left: "center",
        textStyle: {
          fontSize: 16,
          color: "#333",
        },
      },
      grid: {
        left: "5%",
        right: "5%",
        bottom: "10%",
        top: "20%",
      },
      xAxis: {
        type: "category",
        data: dias,
        axisLabel: {
          fontSize: 14,
          color: "#333",
        },
        axisLine: {
          lineStyle: {
            color: "#ccc",
          },
        },
      },
      yAxis: {
        type: "value",
        name: "kcal",
        axisLabel: {
          fontSize: 14,
          color: "#333",
        },
        axisLine: {
          lineStyle: {
            color: "#ccc",
          },
        },
      },
      series: [
        {
          name: "Calorías",
          type: "line",
          data: calorias,
          itemStyle: {
            color: "#FF5722",
            borderWidth: 3,
            borderColor: "#E64A19",
          },
          lineStyle: {
            width: 4,
            type: "solid",
          },
          smooth: true,
          symbol: "circle",
          symbolSize: 8,
        },
      ],
      animationDuration: 800,
    };

    grafico.setOption(opcion);
  } catch (error) {
    contenedorGrafico.innerHTML =
      "<h2>Ocurrió un error al cargar los datos</h2>";
    console.error("Error al cargar los datos:", error);
  }
};
