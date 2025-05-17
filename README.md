# Telegram Bot для отображения расписания СевГУ

Этот бот предназначен для получения расписания с сайта [https://sevsu.samrzhevsky.ru/schedule](https://sevsu.samrzhevsky.ru/schedule) и отображения его в удобном формате через интерфейс Telegram.

## 📦 Использование

/start — запуск бота  
<img width="333" alt="image" src="https://github.com/user-attachments/assets/28c71a79-e585-42be-b7a1-aa4238b2d1f9" />
<br><br>
/settings – настройки  
<img width="416" alt="image" src="https://github.com/user-attachments/assets/d28403ca-5baf-4abb-a897-8190bb515de6" />


## 🧠 Логика работы

1. Бот отправляет запрос к серверу [https://sevsu.samrzhevsky.ru/schedule](https://sevsu.samrzhevsky.ru/schedule).
2. В ответ приходит JSON-документ, содержащий структурированные данные расписания.
3. Бот обрабатывает этот JSON, извлекая нужную информацию (группы, преподаватели, дни, пары и т.д.).
4. Полученные данные форматируются и адаптируются под интерфейс Telegram — в виде текстовых сообщений, кнопок и навигации.
