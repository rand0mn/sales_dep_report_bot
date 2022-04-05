import pandas as pd

import reports.workflows as flow
from reports.utils import get_daily_pivot

pipelines = {
    'Открытые заявки': {
        'start': 'Создание заявки',
        'end': [*flow.intro_lesson_flow, *flow.operator_1_flow, *flow.operator_2_flow],
    },
    'Первая линия': {
        'start': 'Назначение задачи на звонок 1Л',
        'end': ['Ученик ответил на звонок оператора 1л'],
    },
    'Вторая линия': {
        'start': 'Назначена задача на вторую линию',
        'end': ['Дозвон 2Л'],
    },
    'Оплата ВУ': {
        'start': 'Успешный ВУ',
        'end': ['Покупка', 'Назначена задача на вторую линию'],
    },
}


def get_plot(df, date):
    """
    Формирует отчет по незавершенным бизнес процессам
    :param df: Фрейм с пользовательскими событиями
    :param date: День на кторый формируется отчет ('2022-03-14')
    :return: Путь к файлу с графиком отчета
    """
    full_report = {}
    for name, pipeline in pipelines.items():
        pivot = get_daily_pivot(df, date, columns=flow.main_events)

        start_event, end_events = pipelines[name].values()

        start_mask = pivot[start_event].notna()
        any_end_mask = pivot[end_events].notna().any(axis=1)

        full_report[name] = len(pivot[start_mask & ~any_end_mask])

    ax = pd.DataFrame(full_report, index=[0]).T.sort_values([0]).plot.barh(
        title=f'Незакрытые бизнес процессы, {date}', legend=False)

    path = 'hanging_workflows.jpeg'
    ax.get_figure().savefig(path, bbox_inches='tight')

    return path
