const ctx = document.getElementById('expGraph').getContext('2d');

console.log(xValues);
console.log(expValues);
console.log(taylorValues);

new Chart(ctx, {
    type: 'line',
    data: {
        labels: xValues,
        datasets: [{
            label: 'Taylor Series Approximation',
            data: taylorValues,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false,
            tension: 0.1
        }, {
            label: 'Actual \( e^x \)',
            data: expValues,
            borderColor: 'rgba(153, 102, 255, 1)',
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            fill: false,
            tension: 0.1 //степень кривизны
        }]
    },
    options: {
        responsive: true, //адаптивность
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'x'
                },
                 ticks: {
                callback: function(value) {
                    return value.toFixed(2);
                }
            }
            },
            y: {
                title: {
                    display: true,
                    text: 'f(x)'
                },
                 ticks: {
                callback: function(value) {
                    return value.toFixed(2);
                }
            }
            }
        },
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart'
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toFixed(4);
                    }
                }
            }
        }
    }
});
