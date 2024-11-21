// Получаем контекст канваса
const ctx = document.getElementById('expGraph').getContext('2d');

// Проверим, что переменные xValues, expValues и taylorValues определены
console.log(xValues);  // Печать значений x
console.log(expValues);  // Печать значений exp(x)
console.log(taylorValues);  // Печать значений для ряда Тейлора

// Создаем график с двумя линиями: один для функции exp(x), другой для её приближения по ряду Тейлора
new Chart(ctx, {
    type: 'line',
    data: {
        labels: xValues,  // Подписи оси X
        datasets: [{
            label: 'Taylor Series Approximation',
            data: taylorValues,  // Данные для ряда Тейлора
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false,
            tension: 0.1
        }, {
            label: 'Actual \( e^x \)',
            data: expValues,  // Данные для функции exp(x)
            borderColor: 'rgba(153, 102, 255, 1)',
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            fill: false,
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'x'
                },
                 ticks: {
                callback: function(value) {
                    return value.toFixed(2);  // Округляем до 2 знаков после запятой
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
                    return value.toFixed(2);  // Округляем до 2 знаков после запятой
                }
            }
            }
        },
        animation: {
            duration: 2000,  // Анимация длится 2 секунды
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
