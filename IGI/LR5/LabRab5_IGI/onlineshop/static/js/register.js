document.getElementById("id_date_of_birth").addEventListener("change", function () {
    const dob = document.getElementById("id_date_of_birth").value; // ID поля даты
    const today = new Date();
    const dobParts = dob.split('.'); // Предполагается формат DD.MM.YYYY
    const dobDate = new Date(dobParts[2], dobParts[1] - 1, dobParts[0]); // Преобразование строки в дату

    if (dobDate > today) {
        alert("Дата рождения не может быть в будущем.");
        return;
    }

    let age = today.getFullYear() - dobDate.getFullYear();
    const monthDiff = today.getMonth() - dobDate.getMonth();
    const dayDiff = today.getDate() - dobDate.getDate();

    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--;
    }

    const weekday = dobDate.toLocaleString('en-US', { weekday: 'long' });
    const ageMessage = "You are " + age + " years old.";
    const weekdayMessage = "You were born on a " + weekday + ".";

    document.getElementById("dob-error").innerText = ageMessage + " " + weekdayMessage;

    if (age < 18) {
        alert("You are under 18. Parental consent is required to use this site.");
    }
});