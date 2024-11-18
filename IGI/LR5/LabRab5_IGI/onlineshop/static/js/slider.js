document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll(".slide");
    const captions = document.querySelectorAll(".slide-caption");
    const slideNumber = document.getElementById("slide-number");
    let currentIndex = 0;

    function showSlide(index) {
        const slider = document.querySelector(".slides");
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

    document.getElementById("next").addEventListener("click", function() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    });

    document.getElementById("prev").addEventListener("click", function() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
    });

   // Обработчик клика на элементы пагинации
    const paginationButtons = document.querySelectorAll(".page");
    paginationButtons.forEach((button) => {
        button.addEventListener("click", function() {
            const slideIndex = parseInt(button.getAttribute("data-slide"));
            currentIndex = slideIndex;
            showSlide(currentIndex);
        });
    });
    // Инициализация первого слайда
    showSlide(currentIndex);
});
