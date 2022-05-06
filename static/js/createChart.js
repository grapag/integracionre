// COMIENZO TODO EL HIGHCHART
function createChart() {
  
    var chart = Highcharts.chart('container', {
  
    chart: {
      type: 'column'
    },
  
    title: {
      text: 'Evolucion de Integración de RE'
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
                   'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
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
      data: [1, 4, 3]
    }, {
      name: 'Ampliación',
      data: [6, 4, 2]
    }, {
      name: 'Reemplazo',
      data: [8, 4, 3]
    }, {
      name: 'Cliente',
      data: [2, 3, 4]
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
}
module.export = createChart;

 // TERMINO TODO EL HIGHCHART   
    