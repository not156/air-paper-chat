import flet as ft
import os 
DB_FILE = "users_db.txt"
 
#куку где изменен 
def get_all_users():
    users = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    u, p = line.strip().split(":")
                    users[u] = p
    return users

def save_user_to_file(username, password):
    # Добавляем юзера в конец файла: "логин:пароль"
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}:{password}\n")

def main(page: ft.Page):
    page.title = "Воздушная бумага"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FDFCF0"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
# 1. Создаем окно поиска (затемнение)
search_dialog = ft.AlertDialog(
    modal=True, # Нельзя закрыть просто так
    title=ft.Text("Поиск агурца... 🥒", text_align="center"),
    content=ft.Column([
        ft.ProgressRing(), # Крутилка как на серьезных сайтах
        ft.Text("Ищем безопасное соединение 111", size=12)
    ], tight=True, horizontal_alignment="center"),
)

# 2. Функция для кнопки (запуск поиска)
def start_search(e):
    page.dialog = search_dialog
    search_dialog.open = True
    page.update()
    print("Запущен поиск агурца! Ждем БУМ-БУМ... 🔊")
    # Тут сработает твой код на JavaScript с GitHub

    # Наша временная база данных (Логин: Пароль)
    users_db = {"admin": "1234"} 

    login_input = ft.TextField(label="Логин", width=300)
    pass_input = ft.TextField(label="Пароль", password=True, width=300)
    def register_user(e):
        current_users = get_all_users() # Читаем тех, кто уже есть
        if login_input.value and pass_input.value:
            if login_input.value in current_users:
                page.snack_bar = ft.SnackBar(ft.Text("Этот логин уже занят!"))
            else:
                save_user_to_file(login_input.value, pass_input.value)
                page.snack_bar = ft.SnackBar(ft.Text("Регистрация АГА! ✅"))
            page.snack_bar.open = True
            page.update()
            
    def login_user(e):
        current_users = get_all_users()
        # Проверяем пароль прямо из файла
        if login_input.value in current_users and current_users[login_input.value] == pass_input.value:
            show_chat(login_input.value)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Неверный логин или пароль! ❌"))
            page.snack_bar.open = True
            page.update()
    def show_chat(username):
        page.controls.clear()
        chat_history = ft.Column(expand=True, scroll="auto")
        
        def on_message(msg):
            chat_history.controls.append(
                ft.Container(content=ft.Text(msg), bgcolor="white", padding=10, border_radius=10)
            )
            page.update()

        page.pubsub.subscribe(on_message)

        def send_click(e):
            if msg_input.value:
                page.pubsub.send_all(f"{username}: {msg_input.value}")
                msg_input.value = ""
                page.update()

        msg_input = ft.TextField(expand=True, on_submit=send_click)
        page.add(
            ft.Text(f"Вы вошли как: {username}", size=12, italic=True),
            chat_history,
            ft.Row([msg_input, ft.IconButton(icon="#E2ADB2", on_click=send_click)])
        )
        page.update()

    page.add(
        ft.Text("Вход в систему", size=25, weight="bold"),
        login_input,
        pass_input,
        ft.Row([
            ft.ElevatedButton("Войти", on_click=login_user),
            ft.TextButton("Регистрация", on_click=register_user)
        ], alignment="center")
    )


    chat_display = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
    new_msg_field = ft.TextField(hint_text="Пиши сюда...", expand=True)
    friend_input = ft.TextField(label="Ник друга (например: Sanya)", width=250)

    # Функция добавления смайлика
    def add_emoji(e):
        new_msg_field.value += e.control.content.value
        page.update()

    # Ряд смайликов (тот самый выбор агурца)
    emoji_row = ft.Row([
        ft.TextButton(content=ft.Text("🥒", size=25), on_click=add_emoji),
        ft.TextButton(content=ft.Text("🤘", size=25), on_click=add_emoji),
        ft.TextButton(content=ft.Text("🔥", size=25), on_click=add_emoji),
        ft.TextButton(content=ft.Text("✅", size=25), on_click=add_emoji),
        ft.Container(
            content=ft.IconButton(
                icon=ft.icons.CALL,
                icon_color="red",
                icon_size=30,
            ),
            bgcolor="white", 
            border_radius=10,
            padding=2,
            on_click=start_search,
        ), # Закрыли контейнер
    ], alignment="center") # ЗАКРЫЛИ КВАДРАТНУЮ СКОБКУ ТУТ! ✅
 
    # 2. Функция для входящего звонка (Flet-way, без Tkinter)
    def incoming_call_popup():
        page.dialog = ft.AlertDialog(
            title=ft.Text("Входящий звонок"),
            content=ft.Text("Вам звонит 111\nОтветить ✅?"),
            actions=[
                ft.TextButton("✅ Ответить", on_click=lambda _: print("Принято!")),
                ft.TextButton("❌ Отклонить", on_click=close_dialog),
            ],
        )
        page.dialog.open = True
        page.update()

    # Строка отправки
    message_row = ft.Row([
        new_msg_field, 
        ft.IconButton(icon="send", on_click=lambda _: print("Отправлено!"))
    ])

# --- 1. ФУНКЦИЯ ОТПРАВКИ (чтобы писать в файл) ---
    def send_message(e):
        if new_msg_field.value:
            # Имя файла на основе ника друга
            chat_file = f"chat_{friend_input.value}.txt"
            msg = f"Семён: {new_msg_field.value}"
            
            # Пишем в файл
            with open(chat_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
            
            # Добавляем на экран и очищаем поле
            chat_display.controls.append(ft.Text(msg, color="white"))
            new_msg_field.value = ""
            page.update()

    # --- 2. ФУНКЦИЯ ВХОДА В ЛИЧКУ ---
    def start_private_chat(e):
        if friend_input.value:
            chat_file = f"chat_{friend_input.value}.txt"
            page.clean() # Очищаем экран входа
            
 #Собираем экран лички
            page.add(
                ft.Text(f"🔒 Чат с {friend_input.value}", size=25, color="green", weight="bold"),
                chat_display,
                ft.Row([
                    new_msg_field, 
                    ft.ElevatedButton("ОТПРАВИТЬ 🚀", on_click=send_message)
                ]),
                emoji_row
            )
            # Если файл уже был, загружаем историю
            if os.path.exists(chat_file):
                with open(chat_file, "r", encoding="utf-8") as f:
                    for line in f:
                        chat_display.controls.append(ft.Text(line.strip()))
            page.update()

    # --- 3. КНОПКА ЗАПУСКА (на главном экране) ---
    start_btn = ft.ElevatedButton("Войти в личку 🚀", on_click=start_private_chat)
    page.add(friend_input, start_btn) # Это то, что мы видим в начале
        
    def start_drawing(e):
        page.clean()
        page.add(ft.Text("🎨 ТУТ БУДЕТ ХОЛСТ (Скоро...)", size=30, color="blue"))
        # Сюда мы потом вставим код для рисования пальцем/мышкой
        page.update()

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    # Функция для вызова окна (тот самый ДЗИНЬ)
    def show_invite():
        page.dialog = ft.AlertDialog(
            title=ft.Text("🎨 Вызов от 111!"),
            content=ft.Text("Саня пишет: мяу. Погнали рисовать?"),
            actions=[
                ft.TextButton("✅ Принять", on_click=start_drawing),
                ft.TextButton("❌ Отклонить", on_click=close_dialog),
            ],
        )
        page.dialog.open = True
        page.update()
        # --- БЛОК СОЗДАНИЯ КНОПОК ---

# 1. Сначала создаем функцию, которая сработает при нажатии
def start_pomidor_call():
    print("Звонок через Агурец-чат запущен! 🍅")
    # Здесь пойдет связь с твоим кодом на GitHub

# 2. А теперь сама кнопка (ставим её под остальными кнопками)
pomidor_btn = tk.Button(
    text="🍅 ПОЗВОНИТЬ", 
    command=start_pomidor_call, 
    bg="red",          # Красный как помидор!
    fg="white",        # Белый текст, чтобы было видно
    font=("Arial", 12, "bold") # Чтобы кнопка была заметной
)

# 3. Размещаем её на экране
pomidor_btn.pack(pady=10)
# --- ОТДЕЛЬНАЯ КНОПКА СВЯЗИ (Линия 242 и далее) ---
    def start_call_logic(e):
        page.dialog = search_dialog
        search_dialog.open = True
        page.update()
        print("Буууп-буууп запущен! 🔊")

    # Создаем большую, красивую кнопку
    main_call_btn = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.icons.CALL, color="white"), ft.Text("УСТАНОВИТЬ СВЯЗЬ 111")],
            alignment="center",
        ),
        bgcolor="red",
        color="white",
        on_click=start_call_logic,
        width=300,
        height=50,
    )

    # Добавляем её в самый низ страницы
    page.add(ft.Divider(), main_call_btn) 
    page.update()
    # --- КОНЕЦ БЛОКА --

# Запускаем!
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9001)
