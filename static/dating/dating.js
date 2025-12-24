let offset = 0; // глобальное смещение
const limit = 3; // количество пользователей за раз

// Проверка, что мы на странице поиска
if (document.getElementById('search_results')) {

    const nextButton = document.getElementById('next_button');

    // Сброс и загрузка нового поиска
    window.loadSearch = function() {
        offset = 0;
        loadNext();
    }

    // Подгрузка следующих пользователей
    window.loadNext = function() {
        const name = document.getElementById('search_name').value;
        const ageMin = document.getElementById('search_age_min').value;
        const ageMax = document.getElementById('search_age_max').value;

        fetch(`/dating/api/search?offset=${offset}&name=${encodeURIComponent(name)}&age_min=${ageMin}&age_max=${ageMax}`)
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById('search_results');

                if (offset === 0) container.innerHTML = ''; // очистка при новом поиске

                if (data.length === 0 && offset === 0) {
                    container.innerHTML = '<p>Пользователи не найдены.</p>';
                    nextButton.style.display = 'none';
                    return;
                }

                if (data.error) {
                    container.innerHTML = `<p class="error">${data.error}</p>`;
                    nextButton.style.display = 'none';
                    return;
                }

                if (!data.results || data.results.length === 0) {
                    container.innerHTML = '<p>Пользователи не найдены.</p>';
                    nextButton.style.display = 'none';
                    return;
                }

                // Рендерим карточки
                data.results.forEach(user => {
                    const card = document.createElement('div');
                    card.classList.add('user_card');
                    card.innerHTML = `
                        ${user.photo ? `<img src="/static/uploads/${user.photo}" width="150">` : ''}
                        <div class="user_info">
                            <strong>${user.full_name}</strong>, ${user.age} лет<br>
                            ${user.about || ''}
                        </div>
                    `;
                    container.appendChild(card);
                });

                // Показываем кнопку "Следующие" только если вернулось limit результатов
                nextButton.style.display = data.length === limit ? 'inline-block' : 'none';

                offset += data.length;
            })
            .catch(err => console.error(err));
    }
}


