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

      // Verificar si los datos son válidos
      if (!Array.isArray(datos) || datos.length === 0) {
          contenedorGrafico.innerHTML =
              "<h2>No tienes datos diarios, por favor registra datos</h2>";
          return;
      }

      // 3. Organizar los datos
      const dias = [];
      const pesos = [];
      const grasas = [];
      const masasMusculares = [];
      const imcs = [];

      diasSemana.forEach((dia) => {
          const item = datos.find((d) => d.dia === dia);
          dias.push(diasTraduccion[dia]);
          pesos.push(item ? item.peso : null);
          grasas.push(item ? item.grasa_corporal : null);
          masasMusculares.push(item ? item.masa_muscular : null);  // Obtener la masa muscular
          imcs.push(item ? item.imc : null);
      });

      // 4. Configuración del gráfico
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
              data: ["Peso", "Grasa Corporal", "Masa Muscular", "IMC"],
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
                  name: "Peso",
                  type: "line",
                  data: pesos,
                  itemStyle: {
                      color: "#4e92d8",
                      borderWidth: 3,
                      borderColor: "#1c6db2",
                  },
                  lineStyle: {
                      width: 4,
                      type: 'solid',
                  },
                  smooth: true,
                  symbol: 'circle',
                  symbolSize: 8,
              },
              {
                  name: "Grasa Corporal",
                  type: "line",
                  data: grasas,
                  itemStyle: {
                      color: "#e74c3c",
                      borderWidth: 3,
                      borderColor: "#c0392b",
                  },
                  lineStyle: {
                      width: 4,
                      type: 'solid',
                  },
                  smooth: true,
                  symbol: 'circle',
                  symbolSize: 8,
              },
              {
                  name: "Masa Muscular",
                  type: "line",
                  data: masasMusculares,
                  itemStyle: {
                      color: "#28a745",  // Verde para la masa muscular
                      borderWidth: 3,
                      borderColor: "#1c7430",
                  },
                  lineStyle: {
                      width: 4,
                      type: 'solid',
                  },
                  smooth: true,
                  symbol: 'circle',
                  symbolSize: 8,
              },
              {
                  name: "IMC",
                  type: "line",
                  data: imcs,
                  itemStyle: {
                      color: "#f1c40f",
                      borderWidth: 3,
                      borderColor: "#d4ac0d",
                  },
                  lineStyle: {
                      width: 4,
                      type: 'solid',
                  },
                  smooth: true,
                  symbol: 'circle',
                  symbolSize: 8,
              },
          ],
          animationDuration: 800, // Animación más suave
      };

      grafico.setOption(opcion);

      // Calcular calorías semanales
      const respuestaCal = await fetch(
          `http://localhost:5000/estadistica_calorias/${usuario.id_usuario}`
      );
      const datosCal = await respuestaCal.json();
      if (Array.isArray(datosCal)) {
          const totalSemana = datosCal.reduce((acc, d) => acc + (d.calorias || 0), 0);
          const elemSemana = document.getElementById("calorias-semana");
          if (elemSemana) {
              elemSemana.innerHTML = `
                <h3>Calorías Semana</h3>
                <p>${totalSemana.toFixed(2)} kcal</p>
              `;
          }
      }
  } catch (error) {
      contenedorGrafico.innerHTML =
          "<h2>Ocurrió un error al cargar los datos</h2>";
      console.error("Error al cargar los datos:", error);
  }
};
