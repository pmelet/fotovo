let chart = null;

function render(array){
    if (!chart) {
        chart = draw()
    }
    data = array.production.map(x => [x.time*1000, x.watts])
    yesterday = array.yesterday.map(x => [x.time*1000, x.watts])
    avg = array.stats.map(x => [x.time*1000, x.avg])
    min = array.stats.map(x => [x.time*1000, x.min])
    max = array.stats.map(x => [x.time*1000, x.max])
    stats = array.stats.map(x => [x.time*1000, x.min, x.max])

    chart.series[0].update({data: stats});
    chart.series[1].update({data: avg });
    chart.series[2].update({data: yesterday });
    chart.series[3].update({data: data });
}

function draw(){

    Highcharts.setOptions(
        {
            time : {
                timezone: 'Europe/Paris',
            },
        }
    )

    return Highcharts.chart('container', {
        chart: {
            animation: false,
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
        series: [{
            type: 'areasplinerange',
            name: 'Min/Max',
            data: [],
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
            data: [],
            color: '#aaf',
            marker: { enabled: false }
        },{
            type: 'scatter',
            name: "Hier",
            data: [],
            color: '#ccf',
            marker: {
                symbol: 'circle',
                fillColor: '#FFFFFF',
                enabled: true,
                radius: 2,
                lineWidth: 1,
                lineColor: null
            }
        },{
            type: 'spline',
            name: 'Production',
            data: [],
            marker: { enabled: false },
            color: 'red',
        }]
    });
}

document.addEventListener('DOMContentLoaded', load)

function load(){
    let url = "production"
    const options = { method: 'GET' };
    fetch(url, options)
        .then(res => res.json())
        .then(out => render(out))
        .catch(err => { throw err });

    setTimeout(load, 30000);
}