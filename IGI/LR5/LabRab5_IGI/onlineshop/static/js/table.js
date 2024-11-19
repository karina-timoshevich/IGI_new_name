function sortTable(columnIndex) {
    const table = document.getElementById("employee-table");
    const rows = Array.from(table.tBodies[0].rows);
    const direction = table.getAttribute("data-sort-direction") || "asc";

    // Очистка старых индикаторов
    document.querySelectorAll("[id^=sort-arrow-]").forEach(el => (el.innerHTML = ""));

    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].innerText.trim().toLowerCase();
        const bText = b.cells[columnIndex].innerText.trim().toLowerCase();
        return direction === "asc"
            ? aText.localeCompare(bText)
            : bText.localeCompare(aText);
    });

    rows.forEach(row => table.tBodies[0].appendChild(row));
    table.setAttribute("data-sort-direction", direction === "asc" ? "desc" : "asc");

    // Добавление индикатора
    const arrow = direction === "asc" ? "↑" : "↓";
    document.getElementById(`sort-arrow-${columnIndex}`).innerHTML = arrow;
}
function showDetails(row) {
    const detailsDiv = document.getElementById("details");
    const cells = row.cells;

    const details = `
        <p><strong>Name:</strong> ${cells[0].innerText} ${cells[1].innerText}</p>
        <p><strong>Position:</strong> ${cells[2].innerText}</p>
        <p><strong>Phone:</strong> ${cells[3].innerText}</p>
        <p><strong>Email:</strong> ${cells[4].innerText}</p>
    `;
    detailsDiv.innerHTML = details;
}
function filterTable() {
    const input = document.getElementById("filter-input").value.toLowerCase();
    const table = document.getElementById("employee-table");
    const rows = table.tBodies[0].rows;

    for (let row of rows) {
        const cellsText = Array.from(row.cells)
            .map(cell => cell.textContent.toLowerCase())
            .join(" ");

        // Показывать или скрывать строки в зависимости от текста
        if (cellsText.includes(input)) {
            row.style.display = ""; // Показать строку
        } else {
            row.style.display = "none"; // Скрыть строку
        }
    }
}
    document.getElementById('toggleForm').addEventListener('click', () => {
        const form = document.getElementById('employeeForm');
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    });

    const phoneInput = document.getElementById('phone');
    const urlInput = document.getElementById('url');
    const passwordInput = document.getElementById('password');
    const passwordConfirmationInput = document.getElementById('password_confirmation');
    const submitButton = document.getElementById('submitButton');

    const phoneError = document.getElementById('phoneError');
    const urlError = document.getElementById('urlError');
    const passwordError = document.getElementById('passwordError');

    const validatePhone = (phone) => {
        const phonePattern = /^(?:\+375|8)\s?\(?\d{2,3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/;
        return phonePattern.test(phone);
    };

    const validateURL = (url) => {
        const urlPattern = /^(https?:\/\/)[\w-]+\.[a-z]{2,6}(\.[a-z]{2})?(\/[\w\-\.]*)*(\.php|\.html)$/;
        return urlPattern.test(url);
    };

    const validateForm = () => {
        const isPhoneValid = validatePhone(phoneInput.value);
        const isURLValid = validateURL(urlInput.value);
        const arePasswordsMatching = passwordInput.value === passwordConfirmationInput.value;

        phoneError.style.display = isPhoneValid ? 'none' : 'block';
        urlError.style.display = isURLValid ? 'none' : 'block';
        passwordError.style.display = arePasswordsMatching ? 'none' : 'block';

        phoneInput.style.border = isPhoneValid ? '1px solid #ccc' : '1px solid red';
        urlInput.style.border = isURLValid ? '1px solid #ccc' : '1px solid red';
        passwordInput.style.border = arePasswordsMatching ? '1px solid #ccc' : '1px solid red';
        passwordConfirmationInput.style.border = arePasswordsMatching ? '1px solid #ccc' : '1px solid red';

        // Активируем кнопку только если все валидны
        submitButton.disabled = !(isPhoneValid && isURLValid && arePasswordsMatching);
    };

    // Привязываем обработчики к инпутам
    phoneInput.addEventListener('input', validateForm);
    urlInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);
    passwordConfirmationInput.addEventListener('input', validateForm)

// Сохранение выбранных сотрудников в localStorage
function saveSelectedEmployees() {
    const selectedCheckboxes = document.querySelectorAll('input[name="select_employee"]:checked');
    const selectedData = {};

    selectedCheckboxes.forEach(checkbox => {
        const row = checkbox.closest('tr');
        const lastName = row.cells[1].innerText; // Фамилия сотрудника (во втором столбце)
        selectedData[checkbox.value] = lastName; // Сохраняем ID и фамилию
    });

    localStorage.setItem("selectedEmployees", JSON.stringify(selectedData));
}

// Удаление сотрудника из localStorage
function deselectEmployee(employeeId) {
    const selectedData = JSON.parse(localStorage.getItem("selectedEmployees")) || {};
    delete selectedData[employeeId];
    localStorage.setItem("selectedEmployees", JSON.stringify(selectedData));
}

// Восстановление состояния чекбоксов
function restoreSelectedEmployees() {
    const selectedData = JSON.parse(localStorage.getItem("selectedEmployees")) || {};
    document.querySelectorAll('input[name="select_employee"]').forEach(checkbox => {
        if (selectedData.hasOwnProperty(checkbox.value)) {
            checkbox.checked = true;
        } else {
            checkbox.checked = false;
        }
    });
}

// Обработчик изменения чекбокса
document.addEventListener("change", event => {
    if (event.target.name === "select_employee") {
        const employeeId = event.target.value;
        const selectedData = JSON.parse(localStorage.getItem("selectedEmployees")) || {};

        if (event.target.checked) {
            // Если выбрано, добавляем сотрудника
            const row = event.target.closest('tr');
            const lastName = row.cells[1].innerText;
            selectedData[employeeId] = lastName;
        } else {
            // Если снята галочка, удаляем из localStorage
            delete selectedData[employeeId];
        }

        // Сохраняем изменения
        localStorage.setItem("selectedEmployees", JSON.stringify(selectedData));

        // Обновляем текст премирования
        rewardSelected();
    }
});

// Вызов восстановления состояния при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
    restoreSelectedEmployees();
    rewardSelected();
});

// Обновление текста премирования с фамилиями сотрудников
function rewardSelected() {
    const selectedData = JSON.parse(localStorage.getItem("selectedEmployees")) || {};
    const lastNames = Object.values(selectedData).filter(name => name && name.trim() !== "");

    const rewardTextDiv = document.getElementById("rewardText");
    if (lastNames.length > 0) {
        const namesList = lastNames.join(", "); // Формируем список через запятую
        rewardTextDiv.innerHTML = `<p>The following employees are rewarded: ${namesList}.</p>`;
    } else {
        rewardTextDiv.innerHTML = `<p>No employees selected for rewarding.</p>`;
    }
}
