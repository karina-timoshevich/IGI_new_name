// Базовый класс Vacancy с использованием class/extends
class Vacancy {
    constructor(profession, salary, phone) {
        this.profession = profession;
        this.salary = salary;
        this.phone = phone;
    }

    getProfession() {
        return this.profession;
    }

    setProfession(profession) {
        this.profession = profession;
    }

    getSalary() {
        return this.salary;
    }

    setSalary(salary) {
        this.salary = salary;
    }

    getPhone() {
        return this.phone;
    }

    setPhone(phone) {
        this.phone = phone;
    }

    addVacancy(profession, salary, phone) {
        this.setProfession(profession);
        this.setSalary(salary);
        this.setPhone(phone);
    }
}

// Наследник класса HighSalaryVacancy
class HighSalaryVacancy extends Vacancy {
    constructor(profession, salary, phone, description) {
        super(profession, salary, phone);
        this.description = description;
    }

    getDescription() {
        return this.description;
    }

    setDescription(description) {
        this.description = description;
    }
}

// Массив для хранения вакансий
let vacanciesClass = JSON.parse(localStorage.getItem('vacanciesClass')) || [];

// Метод для фильтрации вакансий с высокой зарплатой
function filterHighSalaryVacanciesClass() {
    const profession = document.getElementById('profession').value;
    const totalSalary = vacanciesClass
        .filter(vacancy => vacancy.profession === profession)
        .reduce((sum, vacancy) => sum + vacancy.salary, 0);

    const avgSalary = totalSalary / vacanciesClass.filter(vacancy => vacancy.profession === profession).length;
    const highSalaryVacancies = vacanciesClass.filter(vacancy => vacancy.salary > avgSalary);

    const filteredList = document.getElementById('filtered-list');
    filteredList.innerHTML = '';

    highSalaryVacancies.forEach(vacancy => {
        const li = document.createElement('li');
        li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
        filteredList.appendChild(li);
    });
}

// Метод для добавления вакансии
document.getElementById('vacancy-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const profession = document.getElementById('profession').value;
    const salary = parseFloat(document.getElementById('salary').value);
    const phone = document.getElementById('phone').value;

    const vacancy = new Vacancy(profession, salary, phone);
    vacanciesClass.push(vacancy);

    // Сохраняем вакансии в localStorage
    localStorage.setItem('vacanciesClass', JSON.stringify(vacanciesClass));

    // Выводим все вакансии на страницу
    const vacancyList = document.getElementById('vacancy-list');
    const li = document.createElement('li');
    li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
    vacancyList.appendChild(li);

    // Фильтруем вакансии с высокой зарплатой
    filterHighSalaryVacanciesClass();

    // Очистка полей формы
    document.getElementById('vacancy-form').reset();
});

// Загружаем вакансии и выводим их на страницу при загрузке
window.onload = function() {
    const vacancyList = document.getElementById('vacancy-list');
    vacanciesClass.forEach(vacancy => {
        const li = document.createElement('li');
        li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
        vacancyList.appendChild(li);
    });
    // Фильтруем вакансии с высокой зарплатой
    filterHighSalaryVacanciesClass();
};
