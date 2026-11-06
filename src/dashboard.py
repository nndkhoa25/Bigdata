from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(__import__('os').environ.get('REDDIT_DATA_DIR', ROOT / 'data' / 'processed'))
FILES = {
    'sentiment_monthly': 'sentiment_monthly.csv',
    'sentiment_subreddit': 'sentiment_by_subreddit.csv',
    'topic_monthly': 'topic_monthly_counts_v2.csv',
    'topic_subreddit': 'topic_subreddit_counts_v2.csv',
}
TOPIC_NAMES = {
    0: 'Thảo luận chung / pha trộn',
    1: 'Học Machine Learning và thuật toán',
    2: 'Data Science, học tập và nghề nghiệp',
    3: 'AI, ứng dụng và tương lai',
    4: 'Tuyển dụng Data Scientist / Data Engineer',
    5: 'Deep Learning và Reinforcement Learning',
    6: 'Thảo luận chung về AI/ML',
    7: 'Neural Networks',
    8: 'Liên kết phỏng vấn Couchbase lặp',
    9: 'Computer Science và học tập',
    10: 'Câu hỏi trợ giúp / bài tập thống kê',
    11: 'Linear và Logistic Regression',
}

st.set_page_config(page_title='Reddit Trends & Sentiment', page_icon='📊', layout='wide')
st.title('Xu hướng và cảm xúc trên Reddit')
st.caption('545.427 bài đăng thuộc 19 subreddit về Data Science/AI · VADER và TF-IDF + NMF')

@st.cache_data
def load_data(data_dir: str):
    d = Path(data_dir)
    missing = [name for name in FILES.values() if not (d / name).exists()]
    if missing:
        raise FileNotFoundError('Thiếu file trong ' + str(d) + ': ' + ', '.join(missing))
    monthly = pd.read_csv(d / FILES['sentiment_monthly'])
    by_sub = pd.read_csv(d / FILES['sentiment_subreddit'])
    topic_month = pd.read_csv(d / FILES['topic_monthly'])
    topic_sub = pd.read_csv(d / FILES['topic_subreddit'])
    monthly['month'] = pd.to_datetime(monthly['month'] + '-01', errors='coerce')
    topic_month['month'] = pd.to_datetime(topic_month['month'] + '-01', errors='coerce')
    for frame in (topic_month, topic_sub):
        frame['topic_id'] = pd.to_numeric(frame['topic_id'], errors='coerce').astype('Int64')
        frame['topic_name'] = frame['topic_id'].map(TOPIC_NAMES)
    monthly['neutral_share'] = (1 - monthly['positive_share'] - monthly['negative_share']).clip(0, 1)
    by_sub['neutral_share'] = (1 - by_sub['positive_share'] - by_sub['negative_share']).clip(0, 1)
    return monthly, by_sub, topic_month, topic_sub

try:
    monthly, by_sub, topic_month, topic_sub = load_data(str(DATA_DIR))
except Exception as exc:
    st.error(f'Chưa đọc được dữ liệu dashboard: {exc}')
    st.info('Tải 4 CSV tổng hợp vào thư mục data/processed. Hướng dẫn nằm trong README.')
    st.stop()

months = sorted(monthly['month'].dropna().unique())
subreddits = sorted(by_sub['subreddit'].dropna().unique())
if not months or not subreddits:
    st.error('Các bảng không có tháng hoặc subreddit hợp lệ.')
    st.stop()

with st.sidebar:
    st.header('Bộ lọc')
    start_month, end_month = st.select_slider(
        'Khoảng thời gian', options=months, value=(months[0], months[-1]),
        format_func=lambda x: x.strftime('%Y-%m')
    )
    selected_subs = st.multiselect('Subreddit', options=subreddits, default=subreddits)

month_mask = monthly['month'].between(start_month, end_month)
month_view = monthly.loc[month_mask].sort_values('month').copy()
if month_view.empty:
    st.warning('Không có dữ liệu trong khoảng tháng đã chọn.')
    st.stop()

posts_total = int(month_view['posts'].sum())
mean_compound = (month_view['mean_compound'] * month_view['posts']).sum() / max(posts_total, 1)
pos_share = (month_view['positive_share'] * month_view['posts']).sum() / max(posts_total, 1)
neg_share = (month_view['negative_share'] * month_view['posts']).sum() / max(posts_total, 1)
neutral_share = max(0, 1 - pos_share - neg_share)

k1, k2, k3, k4 = st.columns(4)
k1.metric('Số bài trong kỳ', f'{posts_total:,}')
k2.metric('Compound trung bình', f'{mean_compound:.3f}')
k3.metric('Tích cực theo VADER', f'{pos_share:.1%}')
k4.metric('Tiêu cực theo VADER', f'{neg_share:.1%}')
st.caption(f'Trung tính theo VADER: {neutral_share:.1%}. Tỷ lệ này được tính có trọng số theo số bài mỗi tháng.')

sent_tab, topic_tab = st.tabs(['Sentiment & xu hướng', 'Chủ đề'])
with sent_tab:
    st.subheader('Số bài theo tháng')
    # Reindex to full calendar but keep absent months missing; do not turn them into zero-volume months.
    calendar = pd.date_range(start_month, end_month, freq='MS')
    volume = month_view.set_index('month')['posts'].reindex(calendar)
    fig = go.Figure(go.Scatter(x=calendar, y=volume, mode='lines', name='Số bài', connectgaps=False))
    fig.update_layout(xaxis_title='Tháng (UTC)', yaxis_title='Bài đăng', height=360, margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.caption('Khoảng tháng không có dữ liệu được để trống, không xem là tháng có 0 bài.')

    st.subheader('Tỷ lệ sentiment theo tháng')
    sentiment_view = month_view.set_index('month').reindex(calendar).rename_axis('month').reset_index()
    sentiment_long = sentiment_view.melt(
        id_vars='month', value_vars=['negative_share','neutral_share','positive_share'],
        var_name='sentiment', value_name='share'
    )
    sentiment_long['sentiment'] = sentiment_long['sentiment'].map({
        'negative_share':'Tiêu cực','neutral_share':'Trung tính','positive_share':'Tích cực'
    })
    fig = px.line(sentiment_long, x='month', y='share', color='sentiment', markers=False,
                  labels={'month':'Tháng (UTC)','share':'Tỷ lệ','sentiment':'Nhãn'})
    fig.update_yaxes(tickformat='.0%')
    fig.update_layout(height=360, margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Sentiment theo subreddit (toàn giai đoạn)')
    sub_view = by_sub[by_sub['subreddit'].isin(selected_subs)].sort_values('posts', ascending=False).copy()
    if sub_view.empty:
        st.info('Chọn ít nhất một subreddit ở thanh bên.')
    else:
        sub_long = sub_view.melt(
            id_vars=['subreddit','posts'], value_vars=['negative_share','neutral_share','positive_share'],
            var_name='sentiment', value_name='share'
        )
        sub_long['sentiment'] = sub_long['sentiment'].map({
            'negative_share':'Tiêu cực','neutral_share':'Trung tính','positive_share':'Tích cực'
        })
        fig = px.bar(sub_long, x='share', y='subreddit', color='sentiment', orientation='h',
                     barmode='stack', hover_data=['posts'], labels={'share':'Tỷ lệ','subreddit':'Subreddit','sentiment':'Nhãn','posts':'Số bài'})
        fig.update_xaxes(tickformat='.0%')
        fig.update_layout(height=max(380, 28*len(sub_view)), margin=dict(l=10,r=10,t=20,b=10), legend_title_text='Sentiment')
        st.plotly_chart(fig, use_container_width=True)

with topic_tab:
    st.subheader('Tỷ trọng topic trong khoảng thời gian')
    selected_topic_month = topic_month[topic_month['month'].between(start_month, end_month)]
    if selected_topic_month.empty:
        st.info('Không có dữ liệu topic trong khoảng tháng đã chọn.')
    else:
        totals = selected_topic_month.groupby(['topic_id','topic_name'], dropna=False)['posts'].sum().reset_index()
        totals['share'] = totals['posts'] / totals['posts'].sum()
        totals = totals.sort_values('posts', ascending=False)
        fig = px.bar(totals, x='topic_name', y='posts', hover_data={'share':':.1%'},
                     labels={'topic_name':'Topic','posts':'Số bài','share':'Tỷ trọng'})
        fig.update_layout(height=420, xaxis_tickangle=-35, margin=dict(l=10,r=10,t=20,b=100))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(totals[['topic_id','topic_name','posts','share']].assign(share=lambda x:x['share'].map(lambda v:f'{v:.1%}')), hide_index=True, use_container_width=True)

        st.subheader('Topic theo thời gian')
        top_ids = totals.head(6)['topic_id'].dropna().astype(int).tolist()
        trend = selected_topic_month[selected_topic_month['topic_id'].isin(top_ids)].copy()
        if not trend.empty:
            trend['topic_name'] = trend['topic_id'].map(TOPIC_NAMES)
            fig = px.line(trend, x='month', y='posts', color='topic_name', markers=False,
                          labels={'month':'Tháng (UTC)','posts':'Số bài','topic_name':'Topic'})
            fig.update_layout(height=380, margin=dict(l=10,r=10,t=20,b=10))
            st.plotly_chart(fig, use_container_width=True)

    st.subheader('Topic theo subreddit (toàn giai đoạn)')
    topic_sub_view = topic_sub[topic_sub['subreddit'].isin(selected_subs)].copy()
    if not topic_sub_view.empty:
        ts = topic_sub_view.groupby(['subreddit','topic_name'], as_index=False)['posts'].sum()
        ts['share'] = ts['posts'] / ts.groupby('subreddit')['posts'].transform('sum')
        if len(selected_subs) > 1:
            keep_subs = ts.groupby('subreddit')['posts'].sum().nlargest(12).index
            ts = ts[ts['subreddit'].isin(keep_subs)]
        fig = px.bar(ts, x='share', y='subreddit', color='topic_name', orientation='h', barmode='stack',
                     labels={'share':'Tỷ lệ topic','subreddit':'Subreddit','topic_name':'Topic'})
        fig.update_xaxes(tickformat='.0%')
        fig.update_layout(height=max(400,28*ts['subreddit'].nunique()), margin=dict(l=10,r=10,t=20,b=10), legend_title_text='Topic')
        st.plotly_chart(fig, use_container_width=True)
    st.warning('Topic 0 là nhóm tổng quát/pha trộn (chiếm khoảng 61% toàn tập); topic 8 có nhiều liên kết phỏng vấn lặp. Diễn giải các tỷ trọng topic còn lại như kết quả khám phá, không phải nhãn chuẩn.')

st.divider()
st.caption('Nguồn: Reddit Data Science Posts trên Kaggle. Đơn vị phân tích là bài đăng; dữ liệu chỉ bao phủ 19 subreddit Data Science/AI và không đại diện toàn Reddit. VADER là baseline từ điển, không phải ground truth.')
