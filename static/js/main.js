const url = 'https://integracionre.gastongrapu.repl.co/api';
const refreshButton = document.querySelector('#refreshButton')
//const createChart = require('./createChart.js');



//window.addEventlistener('load', () => {
  fetch(url)
    .then(response => response.json())
    .then(data => {
      //Calculo de valores para liberacion mensual agrupada
      var liberacionxmes = [];
      for(i = 0; i < 12; i++){
        liberacionxmes[i] = data["ebarbero_prodxmes"][i] + data["jvilar_prodxmes"][i] + data["alorenzo_prodxmes"][i] + data["jschmukler_prodxmes"][i];
      }
      
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
        
          yAxis: [{
            allowDecimals: false,
            title: {
              text: 'Cant de RE'
            }
          },
                 {
            allowDecimals: false,
            title: {
              text: null
            }
          }],
        
          series: [{
            yAxis: 0,
            name: 'Alta',
            data: data["valores_alta"]
          }, {
            yAxis: 0,
            name: 'Ampliacion',
            data: data["valores_ampliacion"]
          }, {
            yAxis: 0,
            name: 'Ampliacion Placas',
            data: data["valores_ampliacion_placas"]
          }, {
            yAxis: 0,
            name: 'Reemplazo',
            data: data["valores_reemplazo"]
          }, {
            yAxis: 0,
            name: 'Cliente',
            data: data["valores_cliente"]
          }, {
            yAxis: 1,
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
        text: 'Produccion x Integrador'
      },
      xAxis: {
        categories: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
      },
      labels: {
        items: [{
          html: 'Integ Total x Persona',
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
        name: 'A.Lorenzo',
        data: data["alorenzo_prodxmes"]
      }, {
        type: 'column',
        name: 'E.Barbero',
        data: data["ebarbero_prodxmes"]
      }, {
        type: 'column',
        name: 'J.Vilar',
        data: data["jvilar_prodxmes"]
      }, {
        type: 'column',
        name: 'J.Schmukler',
        data: data["jschmukler_prodxmes"]
      }, {
        type: 'spline',
        name: 'Liberado x mes',
        data: liberacionxmes,
        marker: {
          lineWidth: 2,
          lineColor: Highcharts.getOptions().colors[3],
          fillColor: 'red'
        }
      }, {
        type: 'pie',
        name: 'Total',
        data: [{
          name: 'A.Lorenzo',
          y: data["valor_alorenzo_prod"],
          color: Highcharts.getOptions().colors[0] // A.Lorenzo color
        }, {
          name: 'E.Barbero',
          y: data["valor_ebarbero_prod"],
          color: Highcharts.getOptions().colors[1] // E.Barbero color
        }, {
          name: 'J.Vilar',
          y: data["valor_jvilar_prod"],
          color: Highcharts.getOptions().colors[2] // J.Vilar color
        }, {
          name: 'J.Schmukler',
          y: data["valor_jschmukler_prod"],
          color: Highcharts.getOptions().colors[3] // J.Schmukler color
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


