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

let vacanciesClass = JSON.parse(localStorage.getItem('vacanciesClass')) || [];

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

document.getElementById('vacancy-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const profession = document.getElementById('profession').value;
    const salary = parseFloat(document.getElementById('salary').value);
    const phone = document.getElementById('phone').value;

    const vacancy = new Vacancy(profession, salary, phone);
    vacanciesClass.push(vacancy);

    localStorage.setItem('vacanciesClass', JSON.stringify(vacanciesClass));

    const vacancyList = document.getElementById('vacancy-list');
    const li = document.createElement('li');
    li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
    vacancyList.appendChild(li);

    filterHighSalaryVacanciesClass();

    document.getElementById('vacancy-form').reset();
});

window.onload = function() {
    const vacancyList = document.getElementById('vacancy-list');
    vacanciesClass.forEach(vacancy => {
        const li = document.createElement('li');
        li.textContent = `Profession: ${vacancy.profession}, Salary: ${vacancy.salary}, Phone: ${vacancy.phone}`;
        vacancyList.appendChild(li);
    });
    filterHighSalaryVacanciesClass();
};
