
function render(array){

    data = array.production.map(x => [x.time*1000, x.watts])

    Highcharts.setOptions(
        {
            time : {
                timezone: 'Europe/Paris',
            },
        }
    )

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
            title: {
                text: 'Time'
            },
        },
        yAxis: {
            title: {
                text: 'Watts'
            },
            min: 0
        },
        colors: ['#6CF', '#39F', '#06C', '#036', '#000'],
        series: [{
            name: 'Production',
            data: data
        }]
    });
}

document.addEventListener('DOMContentLoaded', function(){
    let url = "production"
    const options = { method: 'GET' };
    fetch(url, options)
        .then(res => res.json())
        .then(out => render(out))
        .catch(err => { throw err });
})

