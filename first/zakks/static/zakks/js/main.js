'use strict'

document.addEventListener('DOMContentLoaded', function() {
    const passwordFields = document.querySelectorAll('input[type="password"]')

    passwordFields.forEach(function(field) {
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'password-toggle';
        toggleBtn.innerHTML = '🙉';
        toggleBtn.setAttribute('aria-label', 'Показать пароль');

        const wrapper = document.createElement('div');
        wrapper.className = 'password-wrapper';
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        wrapper.appendChild(toggleBtn);

        toggleBtn.addEventListener('click', function() {
            if (field.type === 'password') {
                field.type = 'text';
                toggleBtn.innerHTML = '🙈';
                toggleBtn.setAttribute('aria-label', 'Скрыть пароль');
            } else {
                field.type = 'password';
                toggleBtn.innerHTML = '🙉';
                toggleBtn.setAttribute('aria-label', 'Показать пароль');
            }
        })
    })
})


// Показать/скрыть комментарии
function toggleComments(zakkId) {
    const hiddenBlock = document.getElementById('hidden-comments-' + zakkId);
    const button = event.target;

    if (hiddenBlock.style.display === 'none') {
        hiddenBlock.style.display = 'block';
        button.textContent = 'Свернуть комментарии';
    } else {
        hiddenBlock.style.display = 'none';
        button.textContent = 'Показать все комментарии';
    }
}


function toggleLike(zakkId) {
    const button = document.getElementById('like-btn-' + zakkId);
    const counter = document.getElementById('like-count-' + zakkId);

    console.log('zakkId:', zakkId);
    console.log('button:', button);
    console.log('counter:', counter);

    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

    fetch('/like/' + zakkId + '/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        }
    })

    .then(response => response.json())
    .then(data => {
        if (data.success) {
            counter.textContent = data.likes_count;

            if (data.liked) {
                button.classList.add('liked');
                button.textContent = '❤️';

                showToast('Сердечко поставлено! ❤️');
            } else {
                button.classList.remove('liked');
                button.textContent = '🤍';
            }
        } else {
            alert(data.error || 'Что-то пошло не так');
        }
    })

    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка соединения');
    });
}


/* ===== ФУНКЦИЯ ПОКАЗА УВЕДОМЛЕНИЙ ===== */
function showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    // Создаем элемент уведомления
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;

    // Добавляем на страницу
    container.appendChild(toast);

    // Удаляем через 3 секунды
    setTimeout(() => {
        toast.classList.add('hide');
        // Удаляем из DOM после анимации
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
