document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll(".slide");
    const captions = document.querySelectorAll(".slide-caption");
    const slideNumber = document.getElementById("slide-number");
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const paginationButtons = document.querySelectorAll(".page");
    const slider = document.querySelector(".slides");
const slideDelayInput = document.getElementById("slide-delay");

    // Добавляем обработчик события для изменения значения
    slideDelayInput.addEventListener("change", updateAutoSlideInterval);
    let currentIndex = 0;
    let autoSlideInterval;

    // Дополнительные параметры
    const settings = {
        loop: true, // Переключение по кругу
        navs: true, // Стрелки
        pags: true, // Пагинация
        auto: true, // Автопереключение
        stopMouseHover: true, // Остановка при наведении мыши
        delay: 5 // Задержка между слайдами (сек.)
    };

    function showSlide(index) {
        slider.style.transform = `translateX(-${index * 100}%)`;
        slideNumber.textContent = `${index + 1}/${slides.length}`; // Обновление номера слайда

        // Скрываем все подписи
        captions.forEach(caption => {
            caption.style.visibility = 'hidden';
        });

        // Показываем подпись для текущего слайда
        document.getElementById(`caption-${index + 1}`).style.visibility = 'visible';

        // Обновление активной страницы в пагинации
        const pages = document.querySelectorAll(".page");
        pages.forEach(page => {
            page.classList.remove("active");
        });
        pages[index].classList.add("active");
    }

 function updateAutoSlideInterval() {
        const delay = parseInt(slideDelayInput.value, 10); // Получаем новое значение задержки
        console.log("New delay: ", delay);  // Выводим значение в консоль для отладки
        if (isNaN(delay) || delay <= 0) return; // Если значение некорректное, не обновляем

        settings.delay = delay; // Обновляем значение задержки в настройках
        stopAutoSlide(); // Останавливаем текущий интервал
        startAutoSlide(); // Запускаем новый интервал с новым значением задержки
    }

    function startAutoSlide() {
        if (settings.auto) {
            autoSlideInterval = setInterval(function() {
                currentIndex = (currentIndex + 1) % slides.length;
                showSlide(currentIndex);
            }, settings.delay * 1000); // Используем задержку из настроек
        }
    }

    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
        }
    }

    // Обработчик клика на стрелку "Prev"
    prevButton.addEventListener("click", function() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
        if (settings.auto) stopAutoSlide(); // Останавливаем автопереключение при ручном переключении
        if (settings.auto) startAutoSlide(); // Перезапускаем авто-слайдер
    });

    // Обработчик клика на стрелку "Next"
    nextButton.addEventListener("click", function() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
        if (settings.auto) stopAutoSlide();
        if (settings.auto) startAutoSlide();
    });

    // Обработчик клика на пагинацию
    paginationButtons.forEach((button, index) => {
        button.addEventListener("click", function() {
            currentIndex = index;
            showSlide(currentIndex);
            if (settings.auto) stopAutoSlide();
            if (settings.auto) startAutoSlide();
        });
    });

    // Автопереключение при наведении мыши
    if (settings.stopMouseHover && settings.auto) {
        slider.addEventListener("mouseover", function() {
            stopAutoSlide();
        });

        slider.addEventListener("mouseout", function() {
            startAutoSlide();
        });
    }

    // Инициализация слайдера
    if (settings.auto) {
        startAutoSlide();
    }

    if (!settings.navs) {
        prevButton.style.display = 'none';
        nextButton.style.display = 'none';
    }

    if (!settings.pags) {
        document.querySelector(".pagination").style.display = 'none';
    }

    // Инициализация первого слайда
    showSlide(currentIndex);
});


