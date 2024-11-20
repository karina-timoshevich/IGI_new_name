document.getElementById('settings-toggle').addEventListener('change', function () {
    const settingsPanel = document.getElementById('settings-panel');
    settingsPanel.style.display = this.checked ? 'block' : 'none';
});

document.getElementById('font-size').addEventListener('change', function () {
    document.body.style.fontSize = this.value;
});

document.getElementById('text-color').addEventListener('input', function () {
    document.body.style.color = this.value;
});

document.getElementById('background-color').addEventListener('input', function () {
    // Меняем цвет фона страницы
    document.body.style.backgroundColor = this.value;

    // Если фон с картинкой, сбрасываем картинку при изменении цвета
    document.body.style.backgroundImage = 'none';
});


