var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

var total_hours_config = {
    type: 'line',
    data: {
        labels: MONTHS,
        datasets: [{
            label: 'Hours',
            backgroundColor: 'rgb(242,125,60, 0.1)',
            borderColor: '#f27d3c',
            data: window.total_hours,
            fill: true
        }]
    },
    options: {
        legend: {
            display: false
        },
        responsive: true,
        tooltips: {
            mode: 'index',
            intersect: false
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true
            }],
            yAxes: [{
                display: true,
                ticks: {
                    min: 0,
                    max: 80,
                    stepSize: 10
                }
            }]
        }
    }
};
