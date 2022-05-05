const url = 'https://integracionre.gastongrapu.repl.co/my-first-api';


fetch(url)
  .then(response => {
    return response.json();
  })
  .then(data => {
    console.log(data);

  // COMIENZO TODO EL HIGHCHART
  var chart = Highcharts.chart('container', {

  chart: {
    type: 'column'
  },

  title: {
    text: 'titulo del grafico'
  },

  subtitle: {
    text: data["serie1_nombre"]
  },

  legend: {
    align: 'right',
    verticalAlign: 'middle',
    layout: 'vertical'
  },

  xAxis: {
    categories: ['Apples', 'Oranges', 'Bananas'],
    labels: {
      x: -10
    }
  },

  yAxis: {
    allowDecimals: false,
    title: {
      text: 'Amount'
    }
  },

  series: [{
    name: 'Christmas Eve',
    data: [1, 4, 3]
  }, {
    name: 'Christmas Day before dinner',
    data: [6, 4, 2]
  }, {
    name: 'Christmas Day after dinner',
    data: [8, 4, 3]
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
    
    
    
 // TERMINO TODO EL HIGHCHART   
    
    return;
  })
  .catch(error => {
    console.error(error);
  });




