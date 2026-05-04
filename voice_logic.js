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
// Функция "Принять звонок" для нашего ровера
function acceptIncomingCall() {
    console.log("Соединение установлено через войс ровер... 🚀");
    
    // Запускаем проверку безопасности, которую мы писали
    if (checkConnectionSecurity()) {
        startAguretsCall(); // Включаем микрофон
    } else {
        alert("ОШИБКА: Обнаружена активность RAT! Соединение разорвано. 🛡️");
    }
}
// Функция для того самого *буууупбуууп*
function playIncomingBeep() {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(440, audioCtx.currentTime); // Тот самый буууп
    
    oscillator.connect(audioCtx.destination);
    oscillator.start();
    
    // Звучит коротко, чтобы не надоедать
    setTimeout(() => {
        oscillator.stop();
    }, 500);
}
