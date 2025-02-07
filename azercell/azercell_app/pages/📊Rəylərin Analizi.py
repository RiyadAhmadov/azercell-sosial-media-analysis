import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import calendar
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.set_page_config(page_title="📊Dashboard", layout="centered")

df = pd.read_excel(r'azercell/azercell_app/azercell_instagram_customer_reviews.xlsx')

st.sidebar.image(r"azercell/azercell_app/pages/azercell_telecom_llc_logo.png", use_container_width = True, width = 5)

df = df[df['hesab_adı'] != 'azercell']
df['post_tarix'] = pd.to_datetime(df['post_tarix'], format="%d.%m.%Y").dt.date
df['rəy_tarix'] = pd.to_datetime(df['rəy_tarix'], format="%d.%m.%Y").dt.date
df['post_saat'] = pd.to_datetime(df['post_saat'], format="%H:%M:%S").dt.time

st.sidebar.title("Filtrlər")

# 📅 **Post Tarixi Filter**
post_tarix_min, post_tarix_max = df['post_tarix'].min(), df['post_tarix'].max()
col1, col2 = st.sidebar.columns(2)
selected_post_start = col1.date_input("📅 Başlangıc", value=None, min_value=post_tarix_min, max_value=post_tarix_max)
selected_post_end = col2.date_input("📅 Son", value=None, min_value=post_tarix_min, max_value=post_tarix_max)

# 📆 **Rəy Tarixi Filter**
rəy_tarix_min, rəy_tarix_max = df['rəy_tarix'].min(), df['rəy_tarix'].max()
col3, col4 = st.sidebar.columns(2)
selected_rəy_start = col3.date_input("📆 Rəy Başlangıc", value=None, min_value=rəy_tarix_min, max_value=rəy_tarix_max)
selected_rəy_end = col4.date_input("📆 Rəy Son", value=None, min_value=rəy_tarix_min, max_value=rəy_tarix_max)

# ⏰ **Post Saatı Filter**
post_saat_min, post_saat_max = df['post_saat'].min(), df['post_saat'].max()
selected_post_saat_start = st.sidebar.time_input("⏰ Saat (Başlangıc)", value=post_saat_min)
selected_post_saat_end = st.sidebar.time_input("⏰ Saat (Son)", value=post_saat_max)

# 👍 **Bəyənmə Sayı Slider**
like_min, like_max = int(df['post_bəyənmə'].min()), int(df['post_bəyənmə'].max())
like_filter = st.sidebar.slider("👍🏻 Bəyənmə Sayı:", min_value=like_min, max_value=like_max, value=(like_min, like_max), format="%d")

# Filtering Data Based on Selections
filtered_data = df.copy()

# 🔥 **Date Filtering with Flexible Bounds**
if selected_post_start:
    filtered_data = filtered_data[filtered_data['post_tarix'] >= selected_post_start]
if selected_post_end:
    filtered_data = filtered_data[filtered_data['post_tarix'] <= selected_post_end]

if selected_rəy_start:
    filtered_data = filtered_data[filtered_data['rəy_tarix'] >= selected_rəy_start]
if selected_rəy_end:
    filtered_data = filtered_data[filtered_data['rəy_tarix'] <= selected_rəy_end]

# ⏰ **Filter by Time**
filtered_data = filtered_data[(filtered_data['post_saat'] >= selected_post_saat_start) & 
                              (filtered_data['post_saat'] <= selected_post_saat_end)]

# 👍 **Filter by Likes**
filtered_data = filtered_data[(filtered_data['post_bəyənmə'] >= like_filter[0]) & 
                              (filtered_data['post_bəyənmə'] <= like_filter[1])]

st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://seeklogo.com/images/A/azercell-logo-119FFF6347-seeklogo.com.png" width="80">
        <h1 style="margin-left: 10px; margin-bottom: 10px;">Müştəri Rəylər Analizi</h1>
    </div>
    """,
    unsafe_allow_html=True
)

user_count = f"👤 {df['hesab_adı'].nunique()}"   
comment_count = f"💭 {df['rəy'].shape[0]}"    
average_like = f"❤ {df['post_bəyənmə'].mean():.2f}"

def metric_card(label, value):
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 10px; background-color:rgb(66, 26, 94);">
            <p style="font-size: 18px; color:rgb(255, 255, 255); font-weight: bold; margin: 0;">{label}</p>
            <p style="font-size: 24px; color:rgb(255, 223, 223); margin: 0;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

col1, col2, col3 = st.columns(3)

with col1:
    metric_card("İzləyici Sayı", user_count)

with col2:
    metric_card("Rəy Sayı", comment_count)

with col3:
    metric_card("Ortalama Bəyənmə Sayı", average_like)


# Bar chart
def create_bar_chart_45(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='#6A0DAD',
                line=dict(color='white', width=0.2)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.03,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=90, b=90)
    )
    return fig

def create_barh_chart(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=y_data,  
            y=x_data,  
            orientation='h',  
            marker=dict(
                color='#6A0DAD',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.1,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=120, r=50, t=90, b=90)  
    )
    return fig

def create_barh_chart_short(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=y_data,  
            y=x_data,  
            orientation='h',  
            marker=dict(
                color='#6A0DAD',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.2,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=120, r=50, t=90, b=90)  
    )
    return fig


def create_bar_chart(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='#6A0DAD',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.1,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=90, b=90)
    )
    return fig

def create_bar_chart_head(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='#6A0DAD',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=22, family='Verdana', color='white'),
        title_x=0.04,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=90, b=90)
    )
    return fig

def create_bar_chart_head1(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='#6A0DAD',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=22, family='Verdana', color='white'),
        title_x=0.085,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=90, b=90)
    )
    return fig

def create_bar_chart_short(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='#6A0DAD',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.2,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=90, b=90)
    )
    return fig

def create_line_chart(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(go.Scatter(
        x=x_data, 
        y=y_data, 
        mode='lines', 
        fill='tozeroy', 
        fillcolor='rgba(106, 13, 173, 0.3)', 
        line=dict(color='purple')
    ))

    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.2,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=90, b=90)
    )

    return fig

def create_line_chart_head(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(go.Scatter(
        x=x_data, 
        y=y_data, 
        mode='lines', 
        fill='tozeroy', 
        fillcolor='rgba(106, 13, 173, 0.3)', 
        line=dict(color='purple')
    ))

    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.1,
        xaxis=dict(
            title=dict(text=x_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(size=17, family='Arial', color='white')),
            tickfont=dict(size=14, family='Arial', color='white')
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=90, b=90)
    )

    return fig


# ----

st.header('📅 Tarix Üzrə Analiz')
st.subheader('📆 Tarix Üzrə Paylaşılan Post Sayı')
st.write(f""">Aşağıdakı <strong style='color: purple;'>xətti qrafikdə</strong> post sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['post_tarix'] = pd.to_datetime(filtered_data['post_tarix'])
date_counts = filtered_data.groupby(filtered_data['post_tarix'].dt.date)['post_şəkil'].nunique()

fig0 = create_line_chart(date_counts.index, date_counts.values,'Tarix Üzrə Paylaşılan Post Sayı','Tarix','Post Sayı')
st.plotly_chart(fig0)

st.write(f""">Sample data olduğunu nəzərə alsaq, post paylaşımları <strong style='color: purple;'>uniform</strong> paylanmaya yaxındır.  
Lakin bəzi günlərdə <strong style='color: purple;'>1-dən çox</strong> paylaşım edilib. Siyahını aşağıda görə bilərsiniz.""", unsafe_allow_html=True)

date_counts = date_counts.to_frame().reset_index()
date_counts = date_counts[date_counts['post_şəkil'] > 1] 
date_counts.columns = ['Postun Paylaşılma Tarixi','Paylaşılan Post Sayı']
date_counts= date_counts.sort_values(by = 'Paylaşılan Post Sayı', ascending = False)
date_counts.reset_index(drop = True, inplace = True) 

st.dataframe(date_counts)

# ---

st.subheader('📆 Aylar və İllər Üzrə Paylaşılan Post Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>bar qrafikdə</strong> ay və illər üzrə paylaşılan post sayını görə bilərsiniz.""", unsafe_allow_html=True)

monthly_counts = filtered_data.groupby(filtered_data['post_tarix'].dt.to_period("M"))['post_şəkil'].nunique()
months = monthly_counts.index.astype(str)
values = monthly_counts.values

fig1 = create_bar_chart(months, values, 'Aylar və İllər Üzrə Paylaşılan Post Sayı', 'Ay', 'Post Sayı')
st.plotly_chart(fig1)

st.write(f""">Adətən, <strong style='color: purple;'>qış aylarında (yanvar / fevral)</strong> paylaşılan postların sayının daha az olduğunu görə bilərsiniz.""", unsafe_allow_html=True)

# ---

st.subheader('📅 Aylar Üzrə Ortalama Paylaşılan Post Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>bar qrafikdə</strong> aylar üzrə paylaşılan post sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['post_tarix_year'] = filtered_data['post_tarix'].dt.year
filtered_data['post_tarix_month'] = filtered_data['post_tarix'].dt.month

monthly_mean = filtered_data.groupby(by=['post_tarix_year', 'post_tarix_month'])['post_şəkil'].nunique().reset_index()
monthly_mean = monthly_mean.groupby(by=['post_tarix_month'])['post_şəkil'].mean()
months = monthly_mean.index
values = monthly_mean.values.round(2)

fig2 = create_bar_chart_head1(months, values, 'Aylar Üzrə Paylaşılan Post Sayının Ortalaması', 'Ay', 'Post Sayının Ortalaması')
st.plotly_chart(fig2)   

st.write(f""">Ümumilikdə, <strong style='color: purple;'>yanvar, fevral və noyabr</strong> aylarında daha az post sayı olduğu müşahidə edilir. Ətraflı məlumatı aşağıdakı cədvəldə görə bilərsiniz.""", unsafe_allow_html=True)

monthly_mean = monthly_mean.to_frame().reset_index()
min = monthly_mean['post_şəkil'].min()
monthly_mean['post_şəkil'] = monthly_mean['post_şəkil'].round(1)
monthly_mean['Minimumdan neçə dəfə çox'] = monthly_mean['post_şəkil'].apply(lambda x: str(round(x/min,1))+ 'x')
monthly_mean.columns = ['Ayın İndeksi','Ortalama Paylaşılan Post Sayı','Minimumdan neçə dəfə çox']
st.dataframe(monthly_mean)

# --- 

st.subheader('📅 İllər Üzrə Toplam Paylaşılan Post Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>pie qrafikdə</strong> illər üzrə paylaşılan post sayını görə bilərsiniz.""", unsafe_allow_html=True)

new = filtered_data.groupby(by=['post_tarix_year'])['post_şəkil'].nunique().reset_index()
fig3 = px.pie(new, values='post_şəkil', names='post_tarix_year', 
              title='İllər Üzrə Toplam Paylaşılan Post Sayı', hole=0.3,
              color_discrete_sequence=['#4B0082', '#6A0DAD', '#8A2BE2', '#9370DB', '#BA55D3', '#D8BFD8'])

fig3.update_layout(title_font=dict(size=24))
st.plotly_chart(fig3)
    
st.write(f""">Qrafikdən aydındır ki, ildən-ilə paylaşılan post sayı artıb. Ətraflı məlumatı aşağıdakı cədvəldə görə bilərsiniz.""", unsafe_allow_html=True)

new['post_tarix_year'] = new['post_tarix_year'].apply(lambda x: str(x)) 
min = new['post_şəkil'].min()
new['Minimumdan neçə dəfə çox'] = new['post_şəkil'].apply(lambda x: str(round(x/min,1))+ 'x')
new.columns = ['İl','Paylaşılan Post Sayı','Minimumdan neçə dəfə çox']
st.dataframe(new)

# ---

st.subheader('📅 Həftənin Günləri Üzrə Ortalama Paylaşılan Post Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> həftənin günləri üzrə paylaşılan post sayının ortalamasını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['post_day_name'] = filtered_data['post_tarix'].dt.day_name()
new = filtered_data.groupby(by=['post_tarix_year', 'post_tarix_month', 'post_day_name'])['post_şəkil'].nunique().reset_index()

week_mean = new.groupby(by = 'post_day_name')['post_şəkil'].mean()
weekdays = week_mean.index
values = week_mean.values.round(2)

fig4 = create_bar_chart_head1(weekdays, values, 'Həftə Üzrə Paylaşılan Post Sayının Ortalaması', 'Həftənin Günü', 'Post Sayının Ortalaması')
st.plotly_chart(fig4)

st.write(f""">Qrafikdən aydın olur ki, həftə sonuna yaxınlaşdıqca <strong style='color: purple;'>(1-5)</strong> günlərində paylaşılan post sayının ortalamasında azalma müşahidə edilir.""", unsafe_allow_html=True)

# ---

st.subheader('📅 Həftə İçi və Həftə Sonu Günlər Üzrə Ortalama Paylaşılan Post Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> həftə içi və həftə sonu günlər üzrə paylaşılan post sayının ortalamasını görə bilərsiniz.""", unsafe_allow_html=True)

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
weekends = ['Saturday', 'Sunday']

week_mean = week_mean.reset_index() 
week_mean['week_type'] = np.where(week_mean['post_day_name'].isin(weekdays), 'Weekday', 'Weekend')
week_mean = week_mean.groupby(by='week_type')['post_şəkil'].mean()

weekdays = week_mean.index
values = week_mean.values.round(2)

fig5 = create_bar_chart_head1(weekdays, values, 'Həftə Üzrə Paylaşılan Post Sayısının Ortalaması', 'Həftə İçi/ Həftə Sonu', 'Post Sayısının Ortalaması')
st.plotly_chart(fig5)

st.write(f""">Qrafikdən aydın olur ki, <strong style='color: purple;'>həftə içi və həftə sonu</strong> günlər üzrə paylaşılan post sayının ortalamasında nəzərəçarpan fərq yoxdur.""", unsafe_allow_html=True)

# ---

st.subheader('🗯 Tarix Üzrə Rəy Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>xətti qrafikdə</strong> ümumi tarix üzrə rəy sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data = filtered_data.sort_values(by='rəy_tarix')
date_counts = filtered_data['rəy_tarix'].value_counts().sort_index()
fig8 = create_line_chart(date_counts.index, date_counts.values,'Tarix Üzrə İzləyicilərin Rəy Sayı','Tarix','Rəy Sayı')
st.plotly_chart(fig8)

# ---

st.subheader('📅 Aylar və İllər Üzrə Rəy Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> aylar və illər üzrə rəy sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['rəy_tarix'] = pd.to_datetime(filtered_data['rəy_tarix'])
monthly_counts = filtered_data.groupby(filtered_data['rəy_tarix'].dt.to_period("M"))['rəy'].count()
months = monthly_counts.index.astype(str)
values = monthly_counts.values
fig9 = create_bar_chart_short(months, values, 'Tarix Üzrə İzləyicilərin Rəy Sayı', 'Ay', 'Rəy Sayı')
st.plotly_chart(fig9)

st.write(f""">Məlumatın nümunə olduğunu nəzərə alaraq, məlumatda <strong style='color: purple;'>uniform</strong> tendensiya müşahidə edilir.""", unsafe_allow_html=True)

# ---

st.subheader('📅 Aylar Üzrə Ortalama Rəy Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> aylar üzrə ortalama rəy sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['rəy_tarix_year'] = filtered_data['rəy_tarix'].dt.year
filtered_data['rəy_tarix_month'] = filtered_data['rəy_tarix'].dt.month
new = filtered_data.groupby(by=['rəy_tarix_year', 'rəy_tarix_month']).agg(rəy_count=('rəy', 'count')).reset_index()
monthly_mean = new.groupby(by = 'rəy_tarix_month')['rəy_count'].mean()
months = monthly_mean.index
values = monthly_mean.values.round(2)
fig10 = create_bar_chart_head1(months, values, 'Aylar Üzrə İzləyicilərin Rəy Sayısının Ortalaması', 'Ay', 'Rəy Sayısının Ortalaması')
st.plotly_chart(fig10)  

# ---

st.subheader('📅 İllər Üzrə Toplam Rəy Paylanması')

st.write(f""">Aşağıdakı <strong style='color: purple;'>pie qrafikdə</strong> illər üzrə rəy sayını görə bilərsiniz.""", unsafe_allow_html=True)

new = filtered_data.groupby(by=['rəy_tarix_year']).agg(rəy_count=('rəy', 'count')).reset_index()
fig11 = px.pie(new, values='rəy_count', names='rəy_tarix_year', 
              title='İllər Üzrə Rəy Paylanması', hole=0.3,
              color_discrete_sequence=['#4B0082', '#6A0DAD', '#8A2BE2', '#9370DB', '#BA55D3', '#D8BFD8'])
fig11.update_layout(title_font=dict(size=24))
st.plotly_chart(fig11)

st.write(f""">Qrafikdən aydın olur ki, məlumat daxilində əksərən <strong style='color: purple;'>2022 (29.8%)</strong> ilinə aid qeydlər mövcuddur.""", unsafe_allow_html=True)

# ---

st.subheader('📅 Həftənin Günləri Üzrə Ortalama Rəy Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> həftənin günləri üzrə ortalama rəy sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['rəy_day_name'] = filtered_data['rəy_tarix'].dt.day_name()
new = filtered_data.groupby(by=['rəy_tarix_year', 'rəy_tarix_month','rəy_day_name']).agg(rəy_count=('rəy', 'count')).reset_index()
week_mean = new.groupby(by = 'rəy_day_name')['rəy_count'].mean()
weekdays = week_mean.index
values = week_mean.values.round(2)
fig12 = create_bar_chart_head1(weekdays, values, 'Həftə Üzrə İzləyicilərin Rəy Sayısının Ortalaması', 'Həftənin Günü', 'Rəy Sayının Ortalaması')
st.plotly_chart(fig12)

st.write(f""">Qrafikdən görünür ki, həftəiçi günlərdə <strong style='color: purple;'>(1-5)</strong> istifadəçilər rəy yazmağa daha çox meylli olurlar. 
Təbii ki, burada həmçinin postların həftə içi daha çox paylaşılma faktoru da mövcuddur.""", unsafe_allow_html=True)

# ---

st.subheader('📅 Həftə İçi və Həftə Sonu Günlər Üzrə Ortalama Rəy Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> həftə içi və həftə sonu günlər üzrə ortalama rəy sayını görə bilərsiniz.""", unsafe_allow_html=True)

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
weekends = ['Saturday', 'Sunday']

week_mean = week_mean.reset_index() 
week_mean['week_type'] = np.where(week_mean['rəy_day_name'].isin(weekdays), 'Weekday', 'Weekend')
week_mean = week_mean.groupby(by='week_type')['rəy_count'].mean()

weekdays = week_mean.index
values = week_mean.values.round(2)

fig13 = create_bar_chart_head(weekdays, values, 'Həftə Üzrə İzləyicilərin Rəy Sayısının Ortalaması', 'Həftə İçi/Sonu', 'Rəy Sayısının Ortalaması')
st.plotly_chart(fig13)

st.write(f""">Bu qrafikdən aydın görünür ki, həftəiçi günlərdə <strong style='color: purple;'>(1-5)</strong> istifadəçilər daha çox rəy yazırlar.""", unsafe_allow_html=True)

# ---

st.header('⏲ Zaman Üzrə Analiz')
st.subheader('⏰ Zaman Üzrə Paylaşılan Post Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>xətti qrafikdə</strong> zaman üzrə paylaşılan post sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['post_saat'] = pd.to_datetime(filtered_data['post_saat'], format="%H:%M:%S")
time_counts = filtered_data.groupby(filtered_data['post_saat'].dt.hour)['post_şəkil'].nunique()

fig6 = create_line_chart(time_counts.index, time_counts.values, 'Zaman Üzrə Paylaşılan Post Sayı', 'Saat', 'Post Sayı')
st.plotly_chart(fig6)

st.write(f""">Bu qrafikdən aydın görünür ki, postlar adətən <strong style='color: purple;'>səhər saatlarında</strong> və 
<strong style='color: purple;'>axşam (iş çıxışı)</strong> saatlarında paylaşılır. (Təbii ki, burada həftənin günü və həftə içi/sonu faktoru da rol oynayır.)""", unsafe_allow_html=True)

# --- 

st.subheader('⏰ Günün Müxtəlif Hissələri Üzrə Paylaşılan Post Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> günün müxtəlif hissələri üzrə paylaşılan post sayını görə bilərsiniz.""", unsafe_allow_html=True)

filtered_data['post_saat'] = pd.to_datetime(filtered_data['post_saat'], format="%H:%M:%S").dt.hour

filtered_data['time_segment'] = pd.cut(
    filtered_data['post_saat'],
    bins=[2, 11, 15, 20],
    labels=['Səhər', 'Günorta', 'Axşam'],
)

time_segment_counts = filtered_data.groupby(by = ['time_segment'])['post_şəkil'].nunique()

fig7 = create_bar_chart(time_segment_counts.index, time_segment_counts.values, 'Günün Hissələri Üzrə Paylaşılan Post Sayı', 'Günün Hissələri', 'Post Sayı')
st.plotly_chart(fig7)

st.write(f""">Bu qrafikdən aydın görünür ki, <strong style='color: purple;'>günorta saatlarında</strong>, 
<strong style='color: purple;'>səhər və axşam (iş çıxışı)</strong> saatlarına nisbətən daha az post paylaşılır.""", unsafe_allow_html=True)

# --- 

st.header('📊 Instagram Hesabları Üzrə Analiz')

st.subheader('📅 Tarix Üzrə Unikal Hesab Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> tarix üzrə unikal istifadəçi sayını görə bilərsiniz.""", unsafe_allow_html=True)

new = filtered_data.groupby(by=['rəy_tarix_year', 'rəy_tarix_month'])['hesab_adı'].nunique().reset_index()
new['Tarix'] = new['rəy_tarix_year'].astype(str) + "-" + new['rəy_tarix_month'].astype(str)

weekdays = new['Tarix']
values = new['hesab_adı']

fig13 = create_bar_chart_short(weekdays, values, 'Tarix Üzrə Unikal Hesab Sayısı', 'Tarix', 'Unikal Hesab Sayı')
st.plotly_chart(fig13)

# --- 

st.subheader('📊 Tarix Üzrə Kumulativ Unikal Hesab Sayı')

st.write(f""">Aşağıdakı <strong style='color: purple;'>sütun qrafikdə</strong> isə istifadəçi sayının kumulativ cəmini görə bilərsiniz.""", unsafe_allow_html=True)

new = filtered_data.groupby(by=['rəy_tarix_year', 'rəy_tarix_month'])['hesab_adı'].nunique().reset_index()
new['Tarix'] = new['rəy_tarix_year'].astype(str) + "-" + new['rəy_tarix_month'].astype(str)

new['Kumulativ_Hesab_Sayı'] = new['hesab_adı'].cumsum()

tarixlər = new['Tarix']
kumulativ_dəyərlər = new['Kumulativ_Hesab_Sayı']

fig14 = create_line_chart_head(tarixlər, kumulativ_dəyərlər, 'Tarix Üzrə Kumulativ Unikal Hesab Sayısı', 'Tarix', 'Kumulativ Unikal Hesab Sayı')
st.plotly_chart(fig14)

# --- 

st.subheader('👥 Rəy Sayına Görə Top Hesablar')

st.write(f""">Aşağıdakı <strong style='color: purple;'>horizontal sütun qrafikdə</strong> top n ən çox comment yazan istifadəçiləri görə bilərsiniz.""", unsafe_allow_html=True)

top_n = st.number_input("Top neçə  hesab göstərilsin?", min_value=1, value=5, step=1)
new = filtered_data.groupby(by=['hesab_adı']).agg(rəy_count=('rəy', 'count')).reset_index()
new.sort_values(by='rəy_count', ascending=False, inplace=True)
new = new.head(top_n)
new.sort_values(by='rəy_count', ascending=False, inplace=True)

fig15 = create_barh_chart_short(new['hesab_adı'], new['rəy_count'], 
                          'Rəy Sayına Görə Top Hesablar', 'Instagram Hesabı', 'Rəy Sayı')
st.plotly_chart(fig15)

# --- 

st.subheader('👍 Rəylərin Bəyənmə Sayına Görə Top Hesablar')

st.write(f""">Aşağıdakı <strong style='color: purple;'>horizontal sütun qrafikdə</strong> ən çox bəyənilən top n kommentlərini və onları yazan istifadəçiləri görə bilərsiniz.""", unsafe_allow_html=True)

top_n1 = st.number_input("Bəyənilmə sayına görə top neçə hesab göstərilsin?", min_value=1, value=5, step=1)

new = filtered_data.groupby(by=['hesab_adı']).agg(bəyənmə_max =('rəy_bəyənmə', 'max')).reset_index()
new.sort_values(by='bəyənmə_max', ascending=False, inplace=True)
new = new.head(top_n1)
new.sort_values(by='bəyənmə_max', ascending=False, inplace=True)

fig16 = create_barh_chart(new['hesab_adı'], new['bəyənmə_max'], 
                          'Rəylərin Bəyənilmə Sayına Görə Hesablar', 'Instagram Hesabı', 'Rəyin Bəyənilmə Sayı')
st.plotly_chart(fig16)

# --- 

emoji = filtered_data[~pd.isna(filtered_data['emoji'])]
emoji_sentiment_mapping = {
    'Positive': [
        '🎊', '🙌', '🔥', '🧨', '🤩', '💐', '🎸', '♥', '💓', '😄', '💗',
        '🎈', '🌺', '😁', '👌', '🍀', '🍂', '🤤', '😍', '💫', '✨', '🫶',
        '✔', '🥋', '🎁', '🎆', '🧡', '🤯', '❤', '🎉', '😀', '👬', '🌹',
        '🙂', '🥰', '🤗', '💚', '👋', '💃', '🤣', '😎', '💯', '🚀', '✅',
        '💞', '💖', '🦄', '💜', '💘', '💵', '💙', '🥳','❤️','👏','🙏','😂','😃','😊'
    ],
    'Negative': [
        '😞', '👎', '😡', '🤧', '😒', '🥀', '💔', '😱', '😢', '💔', '😭',
        '😓', '😔', '😰', '😱', '😑', '😐', '😆', '🤢', '🤮', '🥲', '😿',
        '💥', '❌', '👿', '😕', '😤', '⚠️', '😣', '🙄', '⚡', '🥴', '😴'
    ],
    'Neutral': [
        '👅', '😮', '🏐', '🙃', '𝑨', '𝗿', '🖨', '𝒎', '🏾', '🇱', '🫡',
        '🖖', '𝚆', '𝙽', '𝚕', '𝗲', '🛼', '👈', '𝗸', '𝙷', '📍', '📤',
        '⠀', '☝', '🌾', '🏞', '𝒓', '𝐍', '⤵', '🧑', '🏽', '𝚍', '𝒊',
        '𝙸', '📝', '🇷', '🏃', '💂', '🖤', '🔷', '🛑', '🏘', '📱', '📝',
        '😐', '🧾', '🎇', '💫', '💪', '💚', '💰', '📉', '🖐', '📩', '💼',
        '🚗', '📃', '💸', '📝', '📲', '📊', '📝', '📚', '✍', '📒', '✏',
        '🍁', '📝', '🌸', '📌', '📦', '🏀', '📍', '📞', '📝', '🏆', '⬆',
        '🏞', '📱', '🗓', '🛋', '🎸', '⚽', '⏳', '🍃', '📑', '🦾'
    ]
}


emojies = ['🎊', '🙌', '🔥', '🧨', '🤩', '💐', '🎸', '♥', '💓','😂','😃','😊', '😄', '💗',
        '🎈', '🌺', '😁', '👌', '🍀', '🍂', '🤤', '😍', '💫', '✨', '🫶',
        '✔', '🥋', '🎁', '🎆', '🧡', '🤯', '❤', '🎉', '😀', '👬', '🌹',
        '🙂', '🥰', '🤗', '💚', '👋', '💃', '🤣', '😎', '💯', '🚀', '✅',
        '💞', '💖', '🦄', '💜', '💘', '💵', '💙', '🥳','❤️','👏','🙏',
        '😞', '👎', '😡', '🤧', '😒', '🥀', '💔', '😱', '😢', '💔', '😭',
        '😓', '😔', '😰', '😱', '😑', '😐', '😆', '🤢', '🤮', '🥲', '😿',
        '💥', '❌', '👿', '😕', '😤', '⚠️', '😣', '🙄', '⚡', '🥴', '😴',
        '👅', '😮', '🏐', '🙃', '𝑨', '𝗿', '🖨', '𝒎', '🏾', '🇱', '🫡',
        '🖖', '𝚆', '𝙽', '𝚕', '𝗲', '🛼', '👈', '𝗸', '𝙷', '📍', '📤',
        '⠀', '☝', '🌾', '🏞', '𝒓', '𝐍', '⤵', '🧑', '🏽', '𝚍', '𝒊',
        '𝙸', '📝', '🇷', '🏃', '💂', '🖤', '🔷', '🛑', '🏘', '📱', '📝',
        '😐', '🧾', '🎇', '💫', '💪', '💚', '💰', '📉', '🖐', '📩', '💼',
        '🚗', '📃', '💸', '📝', '📲', '📊', '📝', '📚', '✍', '📒', '✏',
        '🍁', '📝', '🌸', '📌', '📦', '🏀', '📍', '📞', '📝', '🏆', '⬆',
        '🏞', '📱', '🗓', '🛋', '🎸', '⚽', '⏳', '🍃', '📑', '🦾']
    

def get_sentiment_for_emoji(emoji):
    emoji_list = list(emoji)
    for i in emoji_list:
        if i in emojies: 
            emoji = i
            break
        else:
            continue

    for sentiment, emojis in emoji_sentiment_mapping.items():
        if emoji in emojis:
            return sentiment
    return 'Neutral'


emoji['emoji_sentiment'] = emoji['emoji'].apply(lambda x: get_sentiment_for_emoji(x))
all_emojis = "".join(emoji['emoji'])
st.subheader("😊 İstifadə Edilən Emojilər")
emoji.reset_index(inplace = True, drop = True)

st.write(f""">Aşağıdakı <strong style='color: purple;'>cədvəldə</strong> emoji istifadə edilən rəyləri və onların sentiment kateqoriyasını görə bilərsiniz.""", unsafe_allow_html=True)

sentiment_choice = st.radio("Filter by Sentiment:", ["All", "Positive", "Negative", "Neutral"])

if sentiment_choice != "All":
    df_filtered = emoji[emoji['emoji_sentiment'] == sentiment_choice]
else:
    df_filtered = emoji

st.dataframe(df_filtered[['hesab_adı','rəy','emoji','emoji_sentiment']])

# ---

st.subheader("😊 Emoji İstifadə Edilən Rəylərin Sentiment Paylanması")

st.write(f""">Aşağıdakı <strong style='color: purple;'>pie qrafikdə</strong> emoji istifadə edilən rəylərin sentiment paylanmasını görə bilərsiniz.""", unsafe_allow_html=True)

new = emoji.groupby(by=['emoji_sentiment']).agg(rəy_count=('rəy', 'count')).reset_index()
fig17 = px.pie(new, values='rəy_count', names='emoji_sentiment', 
              title='Rəylərin Sentiment üzrə Paylanması', hole=0.3,
              color_discrete_sequence=['#4B0082', '#8A2BE2', '#9370DB', '#D8BFD8'])
fig17.update_layout(title_font=dict(size=24))
st.plotly_chart(fig17)

# ---

st.subheader("🧠 Semantik Analiz")

st.write(f""">Aşağıdakı <strong style='color: purple;'>cədvəldə</strong> istifadəçi rəylərinin semantik kateqoriyasını görə bilərsiniz.""", unsafe_allow_html=True)

semantic_choice = st.radio("Filter by Sentiment:", ["All", "Tərif", "Şikayət", "Sual", 'Başqa'])

if semantic_choice != "All":
    semantik = filtered_data[filtered_data['rəyin_kateqoriyası_z_s_c'] == semantic_choice]
    semantik.reset_index(inplace = True, drop = True)
else:
    semantik = filtered_data
    semantik.reset_index(inplace = True, drop = True)

semantik = semantik[['hesab_adı','rəy', 'Tərif','Başqa','Sual','Şikayət','rəyin_kateqoriyası_z_s_c']]
semantik.columns = ['Hesab Adı','Rəy', 'Tərif Ehtimalı','Başqa Ehtimalı','Sual Ehtimalı','Şikayət Ehtimalı','Rəyin Kateqoriyası']
st.dataframe(semantik)

# ---

st.subheader('📊 Ümumi Rəylər Üzrə Semantik Kateqoriya ilə Paylanma')

st.write(f""">Aşağıdakı <strong style='color: purple;'>pie qrafikdə</strong> istifadəçi rəylərinin semantik paylanmasını görə bilərsiniz.""", unsafe_allow_html=True)

new = filtered_data.groupby(by=['rəyin_kateqoriyası_z_s_c']).agg(rəy_count=('rəy', 'count')).reset_index()
fig18 = px.pie(new, values='rəy_count', names='rəyin_kateqoriyası_z_s_c', 
              title='Rəylərin Semantik Kateqoriya üzrə Paylanması', hole=0.3,
              color_discrete_sequence=['#4B0082', '#8A2BE2', '#9370DB', '#D8BFD8'])
fig18.update_layout(title_font=dict(size=24))
st.plotly_chart(fig18)

# ---

st.subheader('💬 Şikayətlər Kateqoriyası Üzrə Ən Çox Bəyənilən Rəylər')

st.write(f""">Aşağıdakı <strong style='color: purple;'>cədvəldə</strong> isə semantik kateqoriyası şikayət olan, ən çox bəyənilən top rəyləri görə bilərsiniz.""", unsafe_allow_html=True)

top_sikayet = st.number_input("Top neçə rəy göstərilsin?", min_value=1, value=5, step=1)

new = filtered_data.loc[
    (filtered_data['rəyin_kateqoriyası_z_s_c'] == 'Şikayət') & 
    (filtered_data['emoji'].isna())
]
new = new.groupby(by=['hesab_adı','rəy']).agg(Bəyənmə_Sayı =('rəy_bəyənmə', 'max')).reset_index()
new.sort_values(by='Bəyənmə_Sayı', ascending=False, inplace=True)
new = new.head(top_sikayet)
new.sort_values(by='Bəyənmə_Sayı', ascending=False, inplace=True)
new.reset_index(inplace = True, drop = True)
st.dataframe(new)

st.subheader('⚠️ Şikayətlər Arasında Fərqli Hallar')

st.write(f""">Aşağıdakı <strong style='color: purple;'>cədvəldə</strong> fərqli hesablardan eyni məzmunda olan <strong style='color: purple;'>(boykot xarakterli)</strong> şikayət rəylərini görə bilərsiniz.""", unsafe_allow_html=True)

case = df[df['rəy'].str.contains('qınayır', case=False, na=False)]
case = case.reset_index(drop = True)
st.dataframe(case)

st.markdown("---")

st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="https://olaylar.az/media/2019/11/09/loqo_yeni-azercell.png" width="280">
    </div>
    """, unsafe_allow_html=True)


# ✅Done
