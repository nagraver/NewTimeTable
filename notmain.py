# from datetime import datetime
#
#
# def check_time_format(input_time):
#     try:
#         datetime.strptime(input_time, '%H:%M')
#         return True
#     except ValueError:
#         return False
#
#
# # Пример использования функции
# user_input = input("Введите время в формате XX:XX (24-часовой формат): ")
# if check_time_format(user_input):
#     print("Введенное время соответствует формату XX:XX в 24-часовом формате.")
# else:
#     print("Введенное время не соответствует формату XX:XX в 24-часовом формате.")
from datetime import datetime

current_time = datetime.now().time()
print(current_time)
