/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

    var randomScalingFactor = function() {
        return Math.round(Math.random() * 100);
    };
    var color = Chart.helpers.color;

    // Graphs
    var ctx1 = document.getElementById('chart1')

    // eslint-disable-next-line no-unused-vars
    var myChart = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# test',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

    var ctx2 = document.getElementById('chart2')
    var myChart = new Chart(ctx2, {
    type: 'pie',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green'],
        datasets: [{
            data: [12, 19, 3, 5],
            backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    }
    });

    var ctx3 = document.getElementById('chart3')
    var myChart = new Chart(ctx3, {
        type: 'line',
        data: {
            labels: [0,10,20,30],
            datasets: [{
                data: [60,85,106,4],
                label: "#1",
                borderColor: "#3e95cd",
                fill: false
            }, {
                data: [411,282,350,502],
                label: "#2",
                borderColor: "#8e5ea2",
                fill: false
            }, {
                data: [-4,78,302,24],
                label: "#3",
                borderColor: "#3cba9f",
                fill: false
            }]
        }
    });


    /*var myRadarChart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: [['Eating', 'Dinner'], ['Drinking', 'Water'], 'Sleeping', ['Designing', 'Graphics'], 'Coding', 'Cycling', 'Running'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(244 67 54 / 0.2)',
            borderColor: 'red',
            pointBackgroundColor: 'red',
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor()
            ]
        }, {
            label: 'My Second dataset',
            backgroundColor: 'rgb(13 110 252 / 0.2)',
            borderColor: 'blue',
            pointBackgroundColor: 'blue',
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor()
            ]
        }]
    },
    options: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Chart.js Radar Chart'
        },
        scale: {
            ticks: {
                beginAtZero: true
            }
        }
    }
    });*/
})()