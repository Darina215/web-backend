function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdDescription = document.createElement('td');
            let tdAction = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;
            
            if (films[i].title) {
                tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
            } else {
                tdTitle.innerText = '';
            }

            tdYear.innerText = films[i].year;
            tdDescription.innerText = films[i].description; 

            let editButton = document.createElement('button');
            editButton.innerText = "редактировать";
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = "удалить";
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            tdAction.append(editButton);
            tdAction.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdDescription);
            tr.append(tdAction);

            tbody.append(tr);
        }
    })
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}


function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
    if (document.getElementById('title-error')) {
        document.getElementById('title-error').innerText = '';
    }
    if (document.getElementById('title-ru-error')) {
        document.getElementById('title-ru-error').innerText = '';
    }
    if (document.getElementById('year-error')) {
        document.getElementById('year-error').innerText = '';
    }
}
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    showModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const method = id === '' ? 'POST' : 'PUT';
    const url = id === '' 
        ? '/lab7/rest-api/films/' 
        : `/lab7/rest-api/films/${id}`;

    document.getElementById('description-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }    
         if (errors.title) {
            // Если ошибка в оригинальном названии, можно показать её
            let titleError = document.getElementById('title-error') || 
                document.getElementById('description-error');
            titleError.innerText = errors.title;
        }
        if (errors.title_ru) {
            // Создаем или находим элемент для ошибки русского названия
            let titleRuError = document.getElementById('title-ru-error');
            if (!titleRuError) {
                // Если элемента нет, создаем его
                titleRuError = document.createElement('div');
                titleRuError.id = 'title-ru-error';
                titleRuError.className = 'error-message';
                document.querySelector('label:nth-child(1)').appendChild(titleRuError);
            }
            titleRuError.innerText = errors.title_ru;
        }
        if (errors.year) {
            // Создаем или находим элемент для ошибки года
            let yearError = document.getElementById('year-error');
            if (!yearError) {
                yearError = document.createElement('div');
                yearError.id = 'year-error';
                yearError.className = 'error-message';
                document.querySelector('label:nth-child(3)').appendChild(yearError);
            }
            yearError.innerText = errors.year;
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    })
}