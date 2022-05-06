const url = 'https://integracionre.gastongrapu.repl.co/my-first-api';
const refreshButton = document.querySelector('#refreshButton')
//const createChart = require('./createChart.js');

//window.addEventlistener('load', () => {
  fetch(url)
    .then(response => response.json())
    .then(data => {
      //createChart(data); //Funcion que crea el gráfico con los datos actualizados
        var chart = Highcharts.chart('container', {
  
          chart: {
            type: 'column'
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
    })
    //Fin graficos
    .catch(err => console.log(err));
//})


