
function render(array){

data = array.production.map(x => [x.time*1000, x.watts])

console.log(data)

Highcharts.chart('container', {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Production',
        align: 'left'
    },
    xAxis: {
        type: 'datetime',
        //dateTimeLabelFormats: {
            //month: '%e. %b',
            //year: '%b',
        //},
        title: {
            text: 'Time'
        }
    },
    yAxis: {
        title: {
            text: 'Watts'
        },
        min: 0
    },
    plotOptions: {
        series: {
            //marker: {
            //    symbol: 'circle',
            //    fillColor: '#FFFFFF',
            //    enabled: true,
            //    radius: 2.5,
            //    lineWidth: 1,
            //    lineColor: null
            //}
        }
    },

    colors: ['#6CF', '#39F', '#06C', '#036', '#000'],
    series: [
        {
            name: 'Production',
            data: data
        }
    ]
});
}

document.addEventListener('DOMContentLoaded', function(){
    let url = "http://192.168.1.25:8000"
    const options = { method: 'GET' };
    fetch(url, options)
        .then(res => res.json())
        .then(out => render(out))
        .catch(err => { throw err });
})

