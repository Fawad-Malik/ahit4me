var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

var fulfilment_config = {
    type: 'line',
    data: {
        labels: MONTHS,
        datasets: [{
            label: 'Fulfilment',
            backgroundColor: 'rgb(78,137,183, 0.1)',
            borderColor: '#4E89B7',
            data: window.average_fulfilments,
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
                    max: 5,
                    stepSize: 1
                }
            }]
        }
    }
};
