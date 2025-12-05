function fillFilmList() {
    fetch(BASE_API_URL)
        .then(resp => resp.json())
        .then(films => {
            const tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            films.forEach(film => {
                const tr = document.createElement('tr');

                tr.innerHTML = `
                    <td>${film.title_ru}</td>
                    <td>${film.title ? `<i>(${film.title})</i>` : ''}</td>
                    <td>${film.year}</td>
                    <td>${film.description}</td>
                    <td>
                        <button onclick="editFilm(${film.id})">редактировать</button>
                        <button onclick="deleteFilm(${film.id}, '${film.title_ru}')">удалить</button>
                    </td>
                `;
                tbody.append(tr);
            });
        })
        .catch(err => console.error("Ошибка при загрузке списка фильмов:", err));
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    fetch(`${BASE_API_URL}${id}`, { method: 'DELETE' })
        .then(resp => {
            if (resp.ok) fillFilmList();
            else alert("Ошибка при удалении фильма");
        })
        .catch(err => console.error("Ошибка удаления:", err));
}

function showModal() {
    const modal = document.querySelector('.modal');
    modal.style.display = 'block';

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
    fetch(`${BASE_API_URL}${id}`)
        .then(resp => resp.json())
        .then(film => {
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        })
        .catch(err => console.error("Ошибка при получении фильма:", err));
}

function sendFilm() {
    const id = document.getElementById('id').value;

    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const url = id === '' ? BASE_API_URL : `${BASE_API_URL}${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    // Сброс ошибок
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
            if (errors.description) document.getElementById('description-error').innerText = errors.description;
            if (errors.title_ru) document.getElementById('title-ru-error').innerText = errors.title_ru;
            if (errors.title) document.getElementById('title-error').innerText = errors.title;
            if (errors.year) document.getElementById('year-error').innerText = errors.year;
        }
    })
    .catch(err => console.error("Ошибка при отправке фильма:", err));
}
