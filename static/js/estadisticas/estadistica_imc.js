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
        const respuestaUsuario = await fetch("http://localhost:5000/ver_id_usuario");
        const usuario = await respuestaUsuario.json();

        const respuestaEstadistica = await fetch(
            `http://localhost:5000/estadistica_general/${usuario.id_usuario}`
        );
        const datos = await respuestaEstadistica.json();

        if (!Array.isArray(datos) || datos.length === 0) {
            contenedorGrafico.innerHTML =
                "<h2>No tienes datos diarios, por favor registra datos</h2>";
            return;
        }

        const dias = [];
        const imcs = [];

        diasSemana.forEach((dia) => {
            const item = datos.find((d) => d.dia === dia);
            dias.push(diasTraduccion[dia]);
            imcs.push(item ? item.imc : null);
        });

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
                data: ["IMC"],
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
            animationDuration: 800,
        };

        grafico.setOption(opcion);
    } catch (error) {
        contenedorGrafico.innerHTML =
            "<h2>Ocurrió un error al cargar los datos</h2>";
        console.error("Error al cargar los datos:", error);
    }
};
