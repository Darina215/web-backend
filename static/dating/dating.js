let offset = 0;

function loadSearch() {
    offset = 0;  // сбрасываем смещение при новом поиске
    loadNext();
}

function loadNext() {
    const name = document.getElementById('search_name').value;
    const ageMin = document.getElementById('search_age_min').value;
    const ageMax = document.getElementById('search_age_max').value;

    fetch(`/api/search?offset=${offset}&name=${name}&age_min=${ageMin}&age_max=${ageMax}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('search_results');

            if (offset === 0) {
                resultsDiv.innerHTML = '';  // очищаем при новом поиске
            }

            if (data.length === 0 && offset === 0) {
                resultsDiv.innerHTML = '<p>Пользователи не найдены.</p>';
                document.getElementById('next_button').style.display = 'none';
                return;
            }

            data.forEach(user => {
                const userDiv = document.createElement('div');
                userDiv.classList.add('user_card');
                userDiv.innerHTML = `
                    <strong>${user.full_name}</strong>, ${user.age} лет<br>
                    ${user.about || ''}<br>
                    ${user.photo ? `<img src="/static/uploads/${user.photo}" width="100">` : ''}
                    <hr>
                `;
                resultsDiv.appendChild(userDiv);
            });

            // Показываем кнопку «Следующие» только если результат = 3
            document.getElementById('next_button').style.display = data.length === 3 ? 'inline-block' : 'none';
            offset += 3;
        });
}

