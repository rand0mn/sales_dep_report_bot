import reports.workflows as flow
from reports.utils import get_daily

import retentioneering

retentioneering.config.update({
    'user_col': 'user_id',
    'event_col': 'event_type',
    'event_time_col': 'event_time',
})

targets = ['Создание заявки', *flow.operator_1_flow, *flow.intro_lesson_flow, 'Покупка']


def get_plot(df, date):
    df = get_daily(df, date)

    n_clusters = 2

    df.rete.get_clusters(method='kmeans',
                         feature_type='tfidf',
                         n_clusters=n_clusters,
                         ngram_range=(1, 2),
                         targets=targets)

    clusters_ids = [df.rete.cluster_mapping[i] for i in range(n_clusters)]
    fig = df.rete.funnel(targets=targets, groups=clusters_ids)

    path = 'conversion_funnel.jpeg'
    fig.write_image(path, engine='kaleido', width=1000, height=1000, scale=2)

    return path
