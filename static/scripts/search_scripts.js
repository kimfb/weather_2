let response;

/**
 * Функция отправки текста из input на /search, возвращает ответ сервера.
 * {str} rqst Текст запроса.
 * {json} result Ответ сервера.
 */
async function send_data(rqst) {
    let response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify(rqst)
    });
    if (response.ok) {
        let result = await response.json();
        return result;
    } else {
        console.error('Ошибка при отправке данных:', response.status);
    }
};

const dt = document.getElementById('suggest');
const input = document.getElementsByName('location')[0];

// Слушает input и отправляет данные на сервер.
input.addEventListener("input", async () => {
    var rqst = {
        "data": input.value,
        "type": "search"
    };
    response = await send_data(rqst);

    if (response) {
        dt.style.display = 'block';
        dt.innerHTML = '';

        // Добавляем подсказки из объекта response в формате "ключ, значение"
        for (const [key, value] of Object.entries(response)) {
            const option = document.createElement('p');
            option.className = 'spoint';
            option.innerHTML = `${key}, ${value}`;
            dt.appendChild(option);
            console.log(`${key}, ${value}`);
        }
        dt.style.border = '2px solid #009B95';

        //Отправка запроса по нажатию на подсказку
        Array.from(document.getElementsByClassName('spoint')).forEach(function(point) {
            point.addEventListener('click', function() {
                input.value = point.innerHTML;
                document.querySelector('.form-search').submit();
            });
        });
    }
});

// Скрывает панель подсказок когда поле ввода перестаёт быть в фокусе.
input.addEventListener('blur', function() {
    setTimeout(() => {
        dt.style.display = 'none';
    }, 200);
})