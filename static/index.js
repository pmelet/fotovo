
function render(array){

    data = array.production.map(x => [x.time*1000, x.watts])
    yesterday = array.yesterday.map(x => [x.time*1000, x.watts])
    avg = array.stats.map(x => [x.time*1000, x.avg])
    min = array.stats.map(x => [x.time*1000, x.min])
    max = array.stats.map(x => [x.time*1000, x.max])
    stats = array.stats.map(x => [x.time*1000, x.min, x.max])

    Highcharts.setOptions(
        {
            time : {
                timezone: 'Europe/Paris',
            },
        }
    )

    Highcharts.chart('container', {
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
        colors: ['#6CF', '#aaF', '#aaF', '#aaF'],
        series: [{
            type: 'areasplinerange',
            name: 'Min/Max',
            data: stats,
            opacity: .5,
            color: {
                linearGradient: {
                    x1: 0,
                    x2: 0,
                    y1: 0,
                    y2: 1
                },
                stops: [
                    [0, '#ffcccc'],
                    [1, '#ccccff']
                ]
            },
            marker: { enabled: false }
        },{
            type: 'spline',
            name: "Moyenne",
            data: avg,
            dashStyle: "dot",
            marker: { enabled: false }
        },{
            type: 'spline',
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

