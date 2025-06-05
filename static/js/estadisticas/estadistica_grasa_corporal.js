window.onload = async function () {
    const contenedorGrafico = document.getElementById("chart");
  
    const diasTraduccion = {
      Monday: "Lunes",
      Tuesday: "Martes",
      Wednesday: "Miércoles",
      Thursday: "Jueves",
      Friday: "Viernes",
      Saturday: "Sábado",
      Sunday: "Domingo",
    };
  
    const diasSemana = Object.keys(diasTraduccion);
  
    try {
      // 1. Obtener ID del usuario
      const respuestaUsuario = await fetch("http://localhost:5000/ver_id_usuario");
      const usuario = await respuestaUsuario.json();
  
      // 2. Obtener datos estadísticos
      const respuestaEstadistica = await fetch(
        `http://localhost:5000/estadistica_general/${usuario.id_usuario}`
      );
      const datos = await respuestaEstadistica.json();
  
      if (!Array.isArray(datos) || datos.length === 0) {
        contenedorGrafico.innerHTML =
          "<h2>No tienes datos diarios, por favor registra datos</h2>";
        return;
      }
  
      // 3. Organizar datos
      const dias = [];
      const grasas = [];
  
      diasSemana.forEach((dia) => {
        const item = datos.find((d) => d.dia === dia);
        dias.push(diasTraduccion[dia]);
        grasas.push(item ? item.grasa_corporal : null);
      });
  
      // 4. Mostrar gráfico
      const grafico = echarts.init(contenedorGrafico);
  
      const opcion = {
        title: {
          left: "center",
          textStyle: {
            fontSize: 24,
            fontWeight: 'bold',
            color: '#333',
          },
          subtextStyle: {
            fontSize: 14,
            color: '#666',
          },
        },
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: ["Grasa Corporal"],
          orient: "horizontal",
          left: "center",
          textStyle: {
            fontSize: 16,
            color: '#333',
          },
        },
        grid: {
          left: '5%',
          right: '5%',
          bottom: '10%',
          top: '20%',
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
            name: "Grasa Corporal",
            type: "line",
            data: grasas,
            itemStyle: {
              color: "#e74c3c", // Color rojo para la línea de grasa corporal
              borderWidth: 3,
              borderColor: "#c0392b",
            },
            lineStyle: {
              width: 4,
              type: 'solid',
            },
            smooth: true, // Suavizar la línea
            symbol: 'circle', // Forma de los puntos en la línea
            symbolSize: 8, // Tamaño de los puntos
          },
        ],
        animationDuration: 800, // Animación más suave
      };
  
      grafico.setOption(opcion);
    } catch (error) {
      contenedorGrafico.innerHTML =
        "<h2>Ocurrió un error al cargar los datos</h2>";
      console.error("Error al cargar los datos:", error);
    }
  };
  