document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll(".slide");
    const captions = document.querySelectorAll(".slide-caption");
    const slideNumber = document.getElementById("slide-number");
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const paginationButtons = document.querySelectorAll(".page");
    const slider = document.querySelector(".slides");
const slideDelayInput = document.getElementById("slide-delay");

    slideDelayInput.addEventListener("change", updateAutoSlideInterval);
    let currentIndex = 0;
    let autoSlideInterval;

    const settings = {
        loop: true,
        navs: true,
        pags: true,
        auto: true,
        stopMouseHover: true,
        delay: 5
    };

    function showSlide(index) {
        slider.style.transform = `translateX(-${index * 100}%)`;
        slideNumber.textContent = `${index + 1}/${slides.length}`;

        captions.forEach(caption => {
            caption.style.visibility = 'hidden';
        });

        document.getElementById(`caption-${index + 1}`).style.visibility = 'visible';

        const pages = document.querySelectorAll(".page");
        pages.forEach(page => {
            page.classList.remove("active");
        });
        pages[index].classList.add("active");
    }

 function updateAutoSlideInterval() {
        const delay = parseInt(slideDelayInput.value, 10);
        console.log("New delay: ", delay);
        if (isNaN(delay) || delay <= 0) return;

        settings.delay = delay;
        stopAutoSlide();
        startAutoSlide();
    }

    function startAutoSlide() {
        if (settings.auto) {
            autoSlideInterval = setInterval(function() {
                currentIndex = (currentIndex + 1) % slides.length;
                showSlide(currentIndex);
            }, settings.delay * 1000);
        }
    }

    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
        }
    }

    prevButton.addEventListener("click", function() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
        if (settings.auto) stopAutoSlide();
        if (settings.auto) startAutoSlide();
    });

    nextButton.addEventListener("click", function() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
        if (settings.auto) stopAutoSlide();
        if (settings.auto) startAutoSlide();
    });

    paginationButtons.forEach((button, index) => {
        button.addEventListener("click", function() {
            currentIndex = index;
            showSlide(currentIndex);
            if (settings.auto) stopAutoSlide();
            if (settings.auto) startAutoSlide();
        });
    });

    if (settings.stopMouseHover && settings.auto) {
        slider.addEventListener("mouseover", function() {
            stopAutoSlide();
        });

        slider.addEventListener("mouseout", function() {
            startAutoSlide();
        });
    }

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

    showSlide(currentIndex);
});


