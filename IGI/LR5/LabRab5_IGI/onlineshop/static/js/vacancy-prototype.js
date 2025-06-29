function Vacancy(profession, salary, phone) {
    this.profession = profession;
    this.salary = salary;
    this.phone = phone;
}

Vacancy.prototype.getProfession = function() {
    return this.profession;
}

Vacancy.prototype.setProfession = function(profession) {
    this.profession = profession;
}

Vacancy.prototype.getSalary = function() {
    return this.salary;
}

Vacancy.prototype.setSalary = function(salary) {
    this.salary = salary;
}

Vacancy.prototype.getPhone = function() {
    return this.phone;
}

Vacancy.prototype.setPhone = function(phone) {
    this.phone = phone;
}

Vacancy.prototype.addVacancy = function(profession, salary, phone) {
    this.setProfession(profession);
    this.setSalary(salary);
    this.setPhone(phone);
}
function HighSalaryVacancy(profession, salary, phone, bonus) {
    Vacancy.call(this, profession, salary, phone);
    this.bonus = bonus;
}

HighSalaryVacancy.prototype = Object.create(Vacancy.prototype);
HighSalaryVacancy.prototype.constructor = HighSalaryVacancy;

HighSalaryVacancy.prototype.getBonus = function() {
    return this.bonus;
};

let vacancies = JSON.parse(localStorage.getItem('vacancies')) || [];

function filterHighSalaryVacancies() {
    const profession = document.getElementById('profession').value;
    const totalSalary = vacancies
        .filter(vacancy => vacancy.profession === profession)
        .reduce((sum, vacancy) => sum + vacancy.salary, 0);

    const avgSalary = totalSalary / vacancies.filter(vacancy => vacancy.profession === profession).length;
    const highSalaryVacancies = vacancies.filter(vacancy => vacancy.salary > avgSalary);

    const filteredList = document.getElementById('filtered-list');
    filteredList.innerHTML = '';

    highSalaryVacancies.forEach(vacancy => {
        const li = document.createElement('li');
        li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
        filteredList.appendChild(li);
    });
}

document.getElementById('vacancy-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const profession = document.getElementById('profession').value;
    const salary = parseFloat(document.getElementById('salary').value);
    const phone = document.getElementById('phone').value;

    const vacancy = new Vacancy(profession, salary, phone);
    vacancies.push(vacancy);

    localStorage.setItem('vacancies', JSON.stringify(vacancies));

    const vacancyList = document.getElementById('vacancy-list');
    const li = document.createElement('li');
    li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
    vacancyList.appendChild(li);

    filterHighSalaryVacancies();

    document.getElementById('vacancy-form').reset();
});

window.onload = function() {
    const vacancyList = document.getElementById('vacancy-list');
    vacancies.forEach(vacancy => {
        const li = document.createElement('li');
        li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
        vacancyList.appendChild(li);
    });
    filterHighSalaryVacancies();
};
