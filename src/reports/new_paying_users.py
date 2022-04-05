from reports.utils import get_day_boundaries, get_daily


def get_report(df, date):
    today_df = get_daily(df, date)

    report_date, _ = get_day_boundaries(date)

    today_payed_users = today_df[today_df.event_type == 'Покупка'].user_id.unique()
    before_payed_users = df[(df.event_type == 'Покупка') & (df.event_time < report_date)].user_id.unique()
    new_payed_users = [x for x in today_payed_users if x not in before_payed_users]

    return len(new_payed_users)
