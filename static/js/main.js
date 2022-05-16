const url = 'https://integracionre.gastongrapu.repl.co/api';
const refreshButton = document.querySelector('#refreshButton')
//const createChart = require('./createChart.js');

//window.addEventlistener('load', () => {
  fetch(url)
    .then(response => response.json())
    .then(data => {
      //createChart(data); //Funcion que crea el gráfico con los datos actualizados
      //CREACION DE BAR CHART PROGRAMACION
          Highcharts.chart('container_barChart', {
  
          chart: {
            type: 'column',
          },
        
          title: {
            text: 'Programación de Integración de RE'
          },
        
          subtitle: {
            text: null
          },
        
          legend: {
            align: 'right',
            verticalAlign: 'middle',
            layout: 'vertical'
          },
        
          xAxis: {
            categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 
                         'Mayo', 'Junio', 'Julio', 'Agosto', 
                         'Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'A Programar'],
            labels: {
              x: -10
            }
          },
        
          yAxis: {
            allowDecimals: false,
            title: {
              text: 'Cant de RE'
            }
          },
        
          series: [{
            name: 'Alta',
            data: data["valores_alta"]
          }, {
            name: 'Ampliación',
            data: data["valores_ampliacion"]
          }, {
            name: 'Reemplazo',
            data: data["valores_reemplazo"]
          }, {
            name: 'Cliente',
            data: data["valores_cliente"]
          }, {
            name: 'Sin Programar',
            data: data["valores_pendientes"]
          }],
        
          responsive: {
            rules: [{
              condition: {
                maxWidth: 500
              },
              chartOptions: {
                legend: {
                  align: 'center',
                  verticalAlign: 'bottom',
                  layout: 'horizontal'
                },
                yAxis: {
                  labels: {
                    align: 'left',
                    x: 0,
                    y: -5
                  },
                  title: {
                    text: null
                  }
                },
                subtitle: {
                  text: null
                },
                credits: {
                  enabled: false
                }
              }
            }]
          }
        });
            
        document.getElementById('small').addEventListener('click', function () {
          chart.setSize(400);
        });
        
        document.getElementById('large').addEventListener('click', function () {
          chart.setSize(600);
        });
        
        document.getElementById('auto').addEventListener('click', function () {
          chart.setSize(null);
        });
      //FIN DE BAR CHART PROGRAMACION

      //INICIO BAR CHART X INTEGRADOR
      Highcharts.chart('container_barChartxIntegrador', {
      title: {
        text: 'Combination chart'
      },
      xAxis: {
        categories: ['Apples', 'Oranges', 'Pears', 'Bananas', 'Plums']
      },
      labels: {
        items: [{
          html: 'Total fruit consumption',
          style: {
            left: '50px',
            top: '18px',
            color: ( // theme
              Highcharts.defaultOptions.title.style &&
              Highcharts.defaultOptions.title.style.color
            ) || 'black'
          }
        }]
      },
      series: [{
        type: 'column',
        name: 'Jane',
        data: [3, 2, 1, 3, 4]
      }, {
        type: 'column',
        name: 'John',
        data: [2, 3, 5, 7, 6]
      }, {
        type: 'column',
        name: 'Joe',
        data: [4, 3, 3, 9, 0]
      }, {
        type: 'spline',
        name: 'Average',
        data: [3, 2.67, 3, 6.33, 3.33],
        marker: {
          lineWidth: 2,
          lineColor: Highcharts.getOptions().colors[3],
          fillColor: 'white'
        }
      }, {
        type: 'pie',
        name: 'Total consumption',
        data: [{
          name: 'Jane',
          y: 13,
          color: Highcharts.getOptions().colors[0] // Jane's color
        }, {
          name: 'John',
          y: 23,
          color: Highcharts.getOptions().colors[1] // John's color
        }, {
          name: 'Joe',
          y: 19,
          color: Highcharts.getOptions().colors[2] // Joe's color
        }],
        center: [100, 80],
        size: 100,
        showInLegend: false,
        dataLabels: {
          enabled: false
        }
      }]
    });
      //FIN BAR CHART X INTEGRADOR
      
      //CREACION DE PIE CHART
      Highcharts.chart('container_pieChart', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
      },
      title: {
        text: 'Estado General'
      },
      accessibility: {
        point: {
          valueSuffix: 'decimals'
        }
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Cantidad',
        colorByPoint: true,
        data: [{
          name: 'No Iniciado',
          y: data["estadoGral_NI"],
          sliced: true,
          selected: true
        }, {
          name: 'En Construccion',
          y: data["estadoGral_EC"]
        }, {
          name: 'En Liberacion',
          y: data["estadoGral_EL"]
        }, {
          name: 'Liberado',
          y: data["estadoGral_LI"]
        }, {
          name: 'Pendiente',
          y: data["estadoGral_PE"]
        }]
      }]
    });

    })
    //Fin graficos
    .catch(err => console.log(err));
//})


