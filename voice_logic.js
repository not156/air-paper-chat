// Агурец-чат: Voice Logic (Anti-RAT Edition) 🥒

async function startAguretsCall() {
    try {
        // Запрашиваем только аудио, никакой слежки!
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        console.log("Микрофон подключен. Хакеры не пройдут! 🛡️");
        
        // Тут будет логика WebRTC для прямой связи
        return stream;
    } catch (err) {
        console.error("Ошибка: Микрофон заблокирован или используется вирусом", err);
        alert("Эй! Кто-то мешает звонку. Проверь сеть!");
    }
}

// Кнопка вызова
const callButton = document.querySelector('#call-btn');
callButton.addEventListener('click', startAguretsCall);
