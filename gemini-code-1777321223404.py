import flet as ft
import os 
DB_FILE = "users_db.txt"


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
    ], alignment="center")

    # Строка отправки
    message_row = ft.Row([
        new_msg_field, 
        ft.IconButton(icon="send", on_click=send_message)
    ])
    def start_private_chat(e):
        if friend_input.value:
            # Имя файла для сохранения (например: chat_Sanya.txt)
            chat_file = f"chat_with_{friend_input.value}.txt"
            
            page.clean()
            page.add(
                ft.Text(f"🔒 Личный чат с: {friend_input.value}", size=22, weight="bold", color="green"),
                chat_display,
                message_row,
                emoji_row
            )

            # Пробуем загрузить старые сообщения, если они есть
            if os.path.exists(chat_file):
                with open(chat_file, "r", encoding="utf-8") as f:
                    for line in f:
                        chat_display.controls.append(ft.Text(line.strip()))
            
            page.update()

    # А эту функцию привяжем к кнопке отправки
    def send_message(e):
        if new_msg_field.value:
            chat_file = f"chat_with_{friend_input.value}.txt"
            msg = f"Админ Семён: {new_msg_field.value}"
            
            # 1. Пишем в файл (сохраняем навсегда!)
            with open(chat_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
            
            # 2. Показываем на экране
            chat_display.controls.append(ft.Text(msg))
            new_msg_field.value = ""
            page.update()

# Запускаем!
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9001)