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

        diasSemana.forEach((dia) => {
            const item = datos.find((d) => d.dia === dia);
            dias.push(diasTraduccion[dia]);
            pesos.push(item ? item.peso : null);  // Obtener solo el peso
        });

        // 4. Configuración del gráfico
        const grafico = echarts.init(contenedorGrafico);

        const opcion = {
            title: {
                left: "center",
                textStyle: {
                    fontSize: 24,
                    fontWeight: 'bold',
                    color: '#333',  // Color oscuro para el título
                },
                subtextStyle: {
                    fontSize: 14,
                    color: '#666',
                },
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'cross' },
                backgroundColor: '#fff',  // Fondo blanco para el tooltip
                borderColor: '#ccc',
                borderWidth: 1,
                textStyle: {
                    color: '#333',
                },
            },
            legend: {
                data: ["Peso"],  // Solo mostrar "Peso"
                orient: "horizontal",
                left: "center",
                textStyle: {
                    fontSize: 16,
                    color: '#333',  // Color de la leyenda
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
                        color: "#ccc",  // Color de la línea del eje X
                    },
                },
            },
            yAxis: {
                type: "value",
                name: "kg",  // Indicar que el eje Y representa peso en kg
                axisLabel: {
                    fontSize: 14,
                    color: "#333",
                },
                axisLine: {
                    lineStyle: {
                        color: "#ccc",  // Color de la línea del eje Y
                    },
                },
            },
            series: [
                {
                    name: "Peso",
                    type: "line",
                    data: pesos,
                    itemStyle: {
                        color: "#4e92d8",  // Color azul para la línea
                        borderWidth: 3,
                        borderColor: "#1c6db2",
                    },
                    lineStyle: {
                        width: 4,
                        type: 'solid',
                    },
                    smooth: true,  // Suavizar la línea
                    symbol: 'circle',  // Forma de los puntos
                    symbolSize: 8,  // Tamaño de los puntos
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
