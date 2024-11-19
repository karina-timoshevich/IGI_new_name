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
