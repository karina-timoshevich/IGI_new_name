// countdown.js
document.addEventListener("DOMContentLoaded", function () {
    const timerElement = document.getElementById("countdown-timer");
    const COOKIE_NAME = "countdown_start_time";
    const countdownDuration = 3600 * 1000; // 1 час в миллисекундах

    // Получаем сохраненное время начала из cookies или создаем новое
    let startTime = document.cookie.split('; ').find(row => row.startsWith(COOKIE_NAME + "="));
    startTime = startTime ? parseInt(startTime.split('=')[1]) : null;

    if (!startTime) {
        // Устанавливаем новое значение в cookies
        startTime = Date.now(); // Текущее время в миллисекундах
        document.cookie = `${COOKIE_NAME}=${startTime}; path=/; max-age=3600`;
    }

    // Обратный отсчет
    const endTime = startTime + countdownDuration;

    function updateCountdown() {
        const now = Date.now();
        const timeLeft = endTime - now;

        if (timeLeft <= 0) {
            timerElement.textContent = "Time's up!";
            clearInterval(interval);
        } else {
            const hours = Math.floor((timeLeft / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((timeLeft / (1000 * 60)) % 60);
            const seconds = Math.floor((timeLeft / 1000) % 60);
            timerElement.textContent = `Time left: ${hours}h ${minutes}m ${seconds}s`;
        }
    }

    // Обновляем каждые 1000 мс
    updateCountdown();
    const interval = setInterval(updateCountdown, 1000);
});
