import reports.workflows as flow
from db import query
import pandas as pd


def load_data():
    sql = """
    select 
        e._user_id as user_id,
        e.happened_at as event_time,
        ed._description as event_type 
    from events e
    left join events_dict ed
        on e.event_id = ed.id

    union all

    select 
        p._user_id as user_id,
        p.transaction_created_at as happened_at,
        'Покупка' as event_type
    from
    payments p
    """

    df = query(sql)

    df['is_ab'] = df.event_type.isin([*flow.demo_flow, *flow.wa_flow])
    users = df.groupby('user_id').is_ab.max()
    users_not_ab = users[users == False].index
    df = df[df.user_id.isin(users_not_ab)][['user_id', 'event_time', 'event_type']]
    df.event_time = pd.to_datetime(df.event_time)

    return df


def get_day_boundaries(date):
    template = '%Y-%m-%d %H:%M:%S'
    t1 = pd.to_datetime(f'{date} 00:00:00', format=template)
    t2 = pd.to_datetime(f'{date} 23:59:59', format=template)

    return t1, t2


def get_daily(data, date):
    t1, t2 = get_day_boundaries(date)
    time_mask = (data['event_time'] > t1) & (data['event_time'] < t2)

    return data[time_mask]


def get_daily_pivot(data, date, columns=None):
    data = get_daily(data, date)
    data = data.groupby(['user_id', 'event_type']).event_time.agg(max).unstack()

    for col_name in columns:
        if col_name not in data.columns:
            data[col_name] = pd.NaT

    return data
