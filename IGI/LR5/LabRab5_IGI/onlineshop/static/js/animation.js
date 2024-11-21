let lastScrollTop = 0;

window.addEventListener("scroll", () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const isScrollingDown = scrollTop > lastScrollTop;
  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;

  const products = document.querySelectorAll(".product-animation-scroll");
  const cart = document.getElementById("cart-animation-scroll");
  const cartRect = cart.getBoundingClientRect();

  products.forEach((product, index) => {
    const productRect = product.getBoundingClientRect();
    const threshold = window.innerHeight / 2;

    // Проверяем, если продукт уже в корзине
    const isInCart = product.dataset.inCart === "true";

    if (isScrollingDown && productRect.top < threshold && !isInCart) {
      // Корректируем смещение по X и Y
      const offsetX = index * 26; // Смещение вправо
      const offsetY = 0; // Смещение вниз для каждого продукта в корзине

      // Перемещаем продукт в корзину с учетом смещения
      product.style.transform = `translate(${
        cartRect.left - productRect.left + offsetX
      }px, ${cartRect.top - productRect.top + offsetY}px)`;

      product.dataset.inCart = "true"; // Отмечаем, что продукт в корзине

      // Синтез речи: объявление о добавлении в корзину
      const synth = window.speechSynthesis;
      const utterance = new SpeechSynthesisUtterance(`${product.textContent} added to cart`);
      synth.speak(utterance);
    } else if (!isScrollingDown && productRect.top < threshold && isInCart) {
      // При скролле вверх возвращаем на место
      product.style.transform = "none";
      product.dataset.inCart = "false"; // Сбрасываем состояние
    }
  });
});
