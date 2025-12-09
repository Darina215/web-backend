function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(resp => resp.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            films.forEach(film => {
                let tr = document.createElement('tr');

                let tdTitleRus = document.createElement('td');
                tdTitleRus.innerText = film.title_ru;

                let tdTitle = document.createElement('td');
                tdTitle.innerHTML = film.title ? `<i>(${film.title})</i>` : '';

                let tdYear = document.createElement('td');
                tdYear.innerText = film.year;

                let tdDescription = document.createElement('td');
                tdDescription.innerText = film.description;

                let tdAction = document.createElement('td');

                let editButton = document.createElement('button');
                editButton.innerText = "редактировать";
                editButton.onclick = () => editFilm(film.id);

                let delButton = document.createElement('button');
                delButton.innerText = "удалить";
                delButton.onclick = () => deleteFilm(film.id, film.title_ru);

                tdAction.append(editButton);
                tdAction.append(delButton);

                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdDescription);
                tr.append(tdAction);

                tbody.append(tr);
            });
        });
}


function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList());
}


function showModal() {
    document.querySelector('.modal').style.display = 'block';

    document.getElementById('description-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}


function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';

    showModal();
}


function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(resp => resp.json())
        .then(film => {
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;

            showModal();
        });
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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(resp => resp.json().then(data => ({ ok: resp.ok, data })))
    .then(result => {
        if (result.ok) {
            fillFilmList();
            hideModal();
        } else {
            const errors = result.data;

            if (errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
            if (errors.title_ru) {
                document.getElementById('title-ru-error').innerText = errors.title_ru;
            }
            if (errors.title) {
                document.getElementById('title-error').innerText = errors.title;
            }
            if (errors.year) {
                document.getElementById('year-error').innerText = errors.year;
            }
        }
    })
    .catch(err => console.error("Ошибка:", err));
}
