main_flow = ['Создание заявки', 'Покупка']
demo_flow = ['Переход на ДУ (ДУ начался)', 'ДУ завершен']
intro_lesson_flow = ['Назначение ВУ', 'Выход МВУ на ВУ', 'Успешный ВУ']
operator_1_flow = ['Назначение задачи на звонок 1Л', 'Ученик ответил на звонок оператора 1л']
operator_2_flow = ['Назначена задача на вторую линию', 'Дозвон 2Л']
wa_flow = ['Отправка сообщения WA', 'У ответил на сообщение WA']

main_events = [*main_flow, *intro_lesson_flow, *operator_1_flow, *operator_2_flow]
