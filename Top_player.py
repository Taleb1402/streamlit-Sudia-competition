# ✅ Import Packages
import os
import re
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
from matplotlib import rcParams
from matplotlib.colors import to_rgba, LinearSegmentedColormap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mplsoccer import Pitch, VerticalPitch, add_image
from highlight_text import ax_text, fig_text
from PIL import Image
from urllib.request import urlopen
from unidecode import unidecode
from scipy.spatial import ConvexHull
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

# ✅ إعداد الصفحة

# ✅ إعداد الصفحة
st.set_page_config(page_title="تقرير أفضل اللاعبين", layout="wide")
st.markdown(
    """
    <div style='text-align: center; margin-top: 30px; margin-bottom: 30px; direction: rtl;'>
        <h1 style='font-size: 36px; color: #0f172a; font-weight: bold;'>📊 أفضل المساهمين في التمرير والدفاع وصناعة الفرص</h1>
        <p style='font-size: 18px; color: #444;'>تحليل لأكثر اللاعبين تأثيرًا في بناء الهجمات والدفاع وخلق التهديدات الهجومية</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        max-width: 400px;
        margin: auto;
    }
    textarea {
        max-width: 400px;
        margin: auto;
        display: block;
    }
    button[kind="primary"] {
        max-width: 400px;
        margin: auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# ✅ اختيار الألوان يدويًا من القائمة الجانبية
st.sidebar.title("🎨 إعدادات الألوان اليدوية")
col1 = st.sidebar.color_picker("🎨 لون الفريق المستضيف", "#1f77b4")
col2 = st.sidebar.color_picker("🎨 لون الفريق الضيف", "#ff7f0e")
line_color = st.sidebar.color_picker("🖊️ لون خطوط الملعب", "#000000")
bg_color = st.sidebar.color_picker("🪵 لون خلفية الملعب", "#f5f5f5")
# ✅ إعداد تعريب النصوص
def ar(text):
    return get_display(arabic_reshaper.reshape(text))

# ✅ إعداد الألوان

violet = '#9467bd'

# ✅ إعداد session state
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False
import streamlit as st
import pandas as pd
import os

import streamlit as st
import pandas as pd
import os

import streamlit as st
import pandas as pd
import os
import streamlit as st
import pandas as pd
import os

import streamlit as st
import pandas as pd
import os

# 🔄 دالة إعادة تأكيد المدخلات
import streamlit as st
import pandas as pd
import os

def reset_confirmed():
    st.session_state['confirmed'] = False

# 📁 تحميل البيانات من مسار ثابت
file_path = r"C:\Users\aalturaidi\OneDrive - Ittihad Club Company\Desktop\merged_events_with_competition_all.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # 🔍 تصحيح أسماء اللاعبين في حمل الكرة
    df.loc[
        (df['type'] == 'Carry') & (df['name'].isna()) & (df['playerId'] == df['playerId'].shift(-1)),
        'name'
    ] = df['name'].shift(-1)

    # ⚠️ معالجة الأهداف العكسية إن وُجد العمود
    if 'type_value_Own goal' in df.columns:
        df['type_value_Own goal'] = pd.to_numeric(df['type_value_Own goal'], errors='coerce').fillna(0)
    else:
        df['type_value_Own goal'] = 0

    # ✅ التأكد من وجود عمود البطولة
    if 'competition' not in df.columns:
        df['competition'] = "Saudi Pro League"
    df['competition'] = df['competition'].astype(str).str.strip()

    # ✅ اختيار البطولة
    
    st.markdown("<h5 style='text-align: center;'>🏆 اختر اسم البطولة</h5>", unsafe_allow_html=True)

    competitions = sorted(df['competition'].dropna().unique().tolist())
    selected_competition = st.selectbox("", competitions, key="competition_select")
    
    df = df[df['competition'] == selected_competition].copy()

    # 🗂️ استخراج أعمدة الجولات
    week_columns = [col for col in df.columns if col.lower().startswith("week")]

    if week_columns:
        # 🔁 تصحيح القيم النصية وتحويلها إلى أرقام
        for col in week_columns:
            df[col] = df[col].replace('WEEK1', 1)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 🏷️ توليد عمود الفريق ضد الفريق
        if {'teamName', 'oppositionTeamName'}.issubset(df.columns):
            df['team_vs'] = df.apply(
                lambda row: " vs ".join(sorted([str(row['teamName']), str(row['oppositionTeamName'])])),
                axis=1
            )

        # 🕵️‍♂️ أخذ صف واحد فقط لكل مباراة
        match_info_df = df.sort_values(by=['team_vs', 'minute']).drop_duplicates(subset='team_vs', keep='first')

        # 🔄 تحويل الجولات إلى صفوف لمطابقة كل مباراة بجولتها
        match_week_df = match_info_df.melt(
            id_vars=['team_vs'],
            value_vars=week_columns,
            var_name='Week',
            value_name='in_week'
        )

        # 📌 عرض قائمة الجولات للاختيار
        available_weeks = match_week_df['Week'].unique().tolist()
        st.markdown("<h5 style='text-align: center;'>🗓️ اختر الجولة</h5>", unsafe_allow_html=True)
        selected_week = st.selectbox("", available_weeks, key="week_selection")

        # ✅ استخراج مباريات الجولة المحددة فقط
        matches_in_week = match_week_df[
            (match_week_df['Week'] == selected_week) & (match_week_df['in_week'] == 1)
        ]['team_vs'].unique().tolist()

        # 🎯 تصفية البيانات الأصلية للمباريات المحددة
        df = df[df['team_vs'].isin(matches_in_week)].copy()

        # 🎮 اختيار المباراة
        matches = sorted(df['team_vs'].dropna().unique().tolist())
        st.markdown("<h5 style='text-align: center;'>🌍 اختر المواجهة (الفريق ضد الفريق)</h5>", unsafe_allow_html=True)
        selected_match = st.selectbox("", matches, key="match_selectbox")
        
        if selected_match:
            df = df[df['team_vs'] == selected_match].copy()
            hteam, ateam = selected_match.split(" vs ")

            # 🏠 تحديد الفريقين المضيف والضيف
            if 'h_a' in df.columns:
                home_away_df = df.head(2)[['teamName', 'h_a']].sort_values(by='h_a').reset_index(drop=True)
                hteamName = home_away_df['teamName'][1]
                ateamName = home_away_df['teamName'][0]
            else:
                hteamName, ateamName = hteam, ateam

            homedf = df[df['teamName'] == hteamName]
            awaydf = df[df['teamName'] == ateamName]



           



        # 🎯 تحليل الأهداف
        score_df = df[df['type'] == 'Goal'][['type', 'minute', 'type_value_Own goal', 'name', 'teamName']].fillna(0)

        h_goal = score_df[(score_df['teamName'] == hteamName) & (score_df['type_value_Own goal'] == 0)]
        h_og = score_df[(score_df['teamName'] == hteamName) & (score_df['type_value_Own goal'] != 0)]
        a_goal = score_df[(score_df['teamName'] == ateamName) & (score_df['type_value_Own goal'] == 0)]
        a_og = score_df[(score_df['teamName'] == ateamName) & (score_df['type_value_Own goal'] != 0)]

        hgoal_count = len(h_goal) + len(a_og)
        agoal_count = len(a_goal) + len(h_og)

        # 👥 استخراج أسماء اللاعبين
        hpnames = homedf['name'].dropna().unique()
        apnames = awaydf['name'].dropna().unique()

        # 🧠 اختيارات المهاجمين
        st.markdown("<h5 style='text-align: center;'>اختر مهاجم الفريق المستضيف</h5>", unsafe_allow_html=True)
        home_Forward = st.selectbox("", hpnames, key='home_fwd', index=None, on_change=reset_confirmed)
        st.markdown("<h5 style='text-align: center;'>اختر مهاجم الفريق الضيف</h5>", unsafe_allow_html=True)
        away_Forward = st.selectbox("", apnames, key='away_fwd', index=None, on_change=reset_confirmed)

        if home_Forward and away_Forward:
            # 🧤 اختيار الحراس
            st.markdown("<h5 style='text-align: center;'>اختر حارس الفريق المستضيف</h5>", unsafe_allow_html=True)
            homeGK = st.selectbox("", hpnames, key='home_gk', index=None, on_change=reset_confirmed)

            st.markdown("<h5 style='text-align: center;'>اختر حارس الفريق الضيف</h5>", unsafe_allow_html=True)
            awayGK = st.selectbox("", apnames, key='away_gk', index=None, on_change=reset_confirmed)
   
            
            if homeGK and awayGK:
                # 🏆 اسم البطولة
                league_name = st.text_area('📝 اكتب اسم البطولة', on_change=reset_confirmed)
                match_input = st.button('✅ تأكيد المدخلات', on_click=lambda: st.session_state.update({'confirmed': True}))

                if st.session_state.get('confirmed', False):
                    # ✂️ دالة اختصار الاسم
                    def get_short_name(full_name):
                        if pd.isna(full_name):
                            return full_name
                        parts = full_name.split()
                        if len(parts) == 1:
                            return full_name
                        elif len(parts) == 2:
                            return parts[0][0] + ". " + parts[1]
                        else:
                            return parts[0][0] + ". " + parts[1][0] + ". " + " ".join(parts[2:])

                    df['short_name'] = df['name'].apply(get_short_name)

                    # 📌 تحديد مستقبل التمريرة
                    df = df.sort_values(by=['teamName', 'minute', 'second']).reset_index(drop=True)
                    df['pass_receiver'] = (
                        df[df['type'] == 'Pass']
                        .sort_values(by=['teamName', 'minute', 'second'])
                        .groupby('teamName')['name']
                        .shift(-1)
                    )
                    df['pass_receiver'] = df['pass_receiver'].fillna('No')

                    




    if home_Forward and away_Forward and homeGK and awayGK and league_name and st.session_state.confirmed:
        
        # ShortName s
         
        def get_short_name(full_name):
            if pd.isna(full_name):
                return full_name
            parts = full_name.split()
            if len(parts) == 1:
                return full_name  # No need for short name if there's only one word
            elif len(parts) == 2:
                return parts[0][0] + ". " + parts[1]
            else:
                return parts[0][0] + ". " + parts[1][0] + ". " + " ".join(parts[2:])
            
            
        df['pass_receiver'] = df.loc[(df['type'] == 'Pass') & (df['outcomeType'] == 'Successful'), 'name'].shift(-1)
        df['pass_receiver'] = df['pass_receiver'].fillna('No')
        
        
        
        def plot_congestion(ax):
            pcmap = LinearSegmentedColormap.from_list("Pearl Earring - 10 colors",  [col2, 'gray', col1], N=20)
            df1 = df[(df['teamName']==hteamName) & (~df['type'].str.contains('SubstitutionOff|SubstitutionOn|Challenge|Card')) &
                     (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)]
            df2 = df[(df['teamName']==ateamName) & (~df['type'].str.contains('SubstitutionOff|SubstitutionOn|Challenge|Card')) & 
                     (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)]
            df2['x'] = 105-df2['x']
            df2['y'] =  68-df2['y']
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2, line_zorder=6)
            pitch.draw(ax=ax)
            ax.set_ylim(-0.5,68.5)
            ax.set_xlim(-0.5,105.5)
        
            bin_statistic1 = pitch.bin_statistic(df1.x, df1.y, bins=(6,5), statistic='count', normalize=False)
            bin_statistic2 = pitch.bin_statistic(df2.x, df2.y, bins=(6,5), statistic='count', normalize=False)
        
            # Assuming 'cx' and 'cy' are as follows:
            cx = np.array([[ 8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                       [ 8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                       [ 8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                       [ 8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                       [ 8.75, 26.25, 43.75, 61.25, 78.75, 96.25]])
        
            cy = np.array([[61.2, 61.2, 61.2, 61.2, 61.2, 61.2],
                       [47.6, 47.6, 47.6, 47.6, 47.6, 47.6],
                       [34.0, 34.0, 34.0, 34.0, 34.0, 34.0],
                       [20.4, 20.4, 20.4, 20.4, 20.4, 20.4],
                       [ 6.8,  6.8,  6.8,  6.8,  6.8,  6.8]])
        
            # Flatten the arrays
            cx_flat = cx.flatten()
            cy_flat = cy.flatten()
        
            # Create a DataFrame
            df_cong = pd.DataFrame({'cx': cx_flat, 'cy': cy_flat})
        
            hd_values = []
        
        
            # Loop through the 2D arrays
            for i in range(bin_statistic1['statistic'].shape[0]):
                for j in range(bin_statistic1['statistic'].shape[1]):
                    stat1 = bin_statistic1['statistic'][i, j]
                    stat2 = bin_statistic2['statistic'][i, j]
                
                    if (stat1 / (stat1 + stat2)) > 0.55:
                        hd_values.append(1)
                    elif (stat1 / (stat1 + stat2)) < 0.45:
                        hd_values.append(0)
                    else:
                        hd_values.append(0.5)
        
            df_cong['hd']=hd_values
            bin_stat = pitch.bin_statistic(df_cong.cx, df_cong.cy, bins=(6,5), values=df_cong['hd'], statistic='sum', normalize=False)
            pitch.heatmap(bin_stat, ax=ax, cmap=pcmap, edgecolors='#000000', lw=0, zorder=3, alpha=0.85)
        
            ax_text(52.5, 71, s=f"<{hteamName}>  |  Contested  |  <{ateamName }>", highlight_textprops=[{'color':col1}, {'color':col2}],
                    color='gray', fontsize=18, ha='center', va='center', ax=ax)
            ax.set_title("Team's Dominating Zone", color=line_color, fontsize=30, fontweight='bold', y=1.075)
            ax.text(0,  -3, 'Attacking Direction--->', color=col1, fontsize=13, ha='left', va='center')
            ax.text(105,-3, '<---Attacking Direction', color=col2, fontsize=13, ha='right', va='center')
        
            ax.vlines(1*(105/6), ymin=0, ymax=68, color=bg_color, lw=2, ls='--', zorder=5)
            ax.vlines(2*(105/6), ymin=0, ymax=68, color=bg_color, lw=2, ls='--', zorder=5)
            ax.vlines(3*(105/6), ymin=0, ymax=68, color=bg_color, lw=2, ls='--', zorder=5)
            ax.vlines(4*(105/6), ymin=0, ymax=68, color=bg_color, lw=2, ls='--', zorder=5)
            ax.vlines(5*(105/6), ymin=0, ymax=68, color=bg_color, lw=2, ls='--', zorder=5)
        
            ax.hlines(1*(68/5), xmin=0, xmax=105, color=bg_color, lw=2, ls='--', zorder=5)
            ax.hlines(2*(68/5), xmin=0, xmax=105, color=bg_color, lw=2, ls='--', zorder=5)
            ax.hlines(3*(68/5), xmin=0, xmax=105, color=bg_color, lw=2, ls='--', zorder=5)
            ax.hlines(4*(68/5), xmin=0, xmax=105, color=bg_color, lw=2, ls='--', zorder=5)
            
            return
            
            
        # Player Stats Counting
        
        # Get unique players
        home_unique_players = homedf['name'].unique()
        away_unique_players = awaydf['name'].unique()
        
        
        # Top Ball Progressor
        # Initialize an empty dictionary to store home players different type of pass counts
        home_progressor_counts = {'name': home_unique_players, 'Progressive Passes': [], 'Progressive Carries': []}
        for name in home_unique_players:
            home_progressor_counts['Progressive Passes'].append(len(df[(df['name'] == name) & (df['prog_pass'] >= 9.144) & (df['x']>=35) & (df['outcomeType']=='Successful') & (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)]))
            home_progressor_counts['Progressive Carries'].append(len(df[(df['name'] == name) & (df['prog_carry'] >= 9.144) & (df['endX']>=35)]))
            
        home_progressor_df = pd.DataFrame(home_progressor_counts)
        home_progressor_df['total'] = home_progressor_df['Progressive Passes']+home_progressor_df['Progressive Carries']
        home_progressor_df = home_progressor_df.sort_values(by='total', ascending=False)
        home_progressor_df.reset_index(drop=True, inplace=True)
        home_progressor_df = home_progressor_df.head(5)
        home_progressor_df['shortName'] = home_progressor_df['name'].apply(get_short_name)
        
        # Initialize an empty dictionary to store away players different type of pass counts
        away_progressor_counts = {'name': away_unique_players, 'Progressive Passes': [], 'Progressive Carries': []}
        for name in away_unique_players:
            away_progressor_counts['Progressive Passes'].append(len(df[(df['name'] == name) & (df['prog_pass'] >= 9.144) & (df['x']>=35) & (df['outcomeType']=='Successful') & (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)]))
            away_progressor_counts['Progressive Carries'].append(len(df[(df['name'] == name) & (df['prog_carry'] >= 9.144) & (df['endX']>=35)]))
            
        away_progressor_df = pd.DataFrame(away_progressor_counts)
        away_progressor_df['total'] = away_progressor_df['Progressive Passes']+away_progressor_df['Progressive Carries']
        away_progressor_df = away_progressor_df.sort_values(by='total', ascending=False)
        away_progressor_df.reset_index(drop=True, inplace=True)
        away_progressor_df = away_progressor_df.head(5)
        away_progressor_df['shortName'] = away_progressor_df['name'].apply(get_short_name)
        
        
        # Top Threate Creators
        # Initialize an empty dictionary to store home players different type of Carries counts
        home_xT_counts = {'name': home_unique_players, 'xT from Pass': [], 'xT from Carry': []}
        for name in home_unique_players:
            home_xT_counts['xT from Pass'].append((df[(df['name'] == name) & (df['type'] == 'Pass') & (df['xT']>=0) & (df['outcomeType']=='Successful') & (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)])['xT'].sum().round(2))
            home_xT_counts['xT from Carry'].append((df[(df['name'] == name) & (df['type'] == 'Carry') & (df['xT']>=0)])['xT'].sum().round(2))
        home_xT_df = pd.DataFrame(home_xT_counts)
        home_xT_df['total'] = home_xT_df['xT from Pass']+home_xT_df['xT from Carry']
        home_xT_df = home_xT_df.sort_values(by='total', ascending=False)
        home_xT_df.reset_index(drop=True, inplace=True)
        home_xT_df = home_xT_df.head(5)
        home_xT_df['shortName'] = home_xT_df['name'].apply(get_short_name)
        
        # Initialize an empty dictionary to store home players different type of Carries counts
        away_xT_counts = {'name': away_unique_players, 'xT from Pass': [], 'xT from Carry': []}
        for name in away_unique_players:
            away_xT_counts['xT from Pass'].append((df[(df['name'] == name) & (df['type'] == 'Pass') & (df['xT']>=0) & (df['outcomeType']=='Successful') & (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)])['xT'].sum().round(2))
            away_xT_counts['xT from Carry'].append((df[(df['name'] == name) & (df['type'] == 'Carry') & (df['xT']>=0)])['xT'].sum().round(2))
        away_xT_df = pd.DataFrame(away_xT_counts)
        away_xT_df['total'] = away_xT_df['xT from Pass']+away_xT_df['xT from Carry']
        away_xT_df = away_xT_df.sort_values(by='total', ascending=False)
        away_xT_df.reset_index(drop=True, inplace=True)
        away_xT_df = away_xT_df.head(5)
        away_xT_df['shortName'] = away_xT_df['name'].apply(get_short_name)
        
        
        # Shot Sequence Involvement
        df_no_carry = df[df['type']!='Carry']
        # Initialize an empty dictionary to store home players different type of shot sequence counts
        home_shot_seq_counts = {'name': home_unique_players, 'Shots': [], 'Shot Assist': [], 'Buildup to shot': []}
        # Putting counts in those lists
        for name in home_unique_players:
            home_shot_seq_counts['Shots'].append(len(df[(df['name'] == name) & ((df['type']=='MissedShots') | (df['type']=='SavedShot') | (df['type']=='ShotOnPost') | (df['type']=='Goal'))]))
            home_shot_seq_counts['Shot Assist'].append(len(df[(df['name'] == name) & (df['type'] == 'Pass') & (df['type_value_Assist']==210)]))
            home_shot_seq_counts['Buildup to shot'].append(len(df_no_carry[(df_no_carry['name'] == name) & (df_no_carry['type'] == 'Pass') & (df['type_value_Assist'].shift(-1)==210)]))
        # converting that list into a dataframe
        home_sh_sq_df = pd.DataFrame(home_shot_seq_counts)
        home_sh_sq_df['total'] = home_sh_sq_df['Shots']+home_sh_sq_df['Shot Assist']+home_sh_sq_df['Buildup to shot']
        home_sh_sq_df = home_sh_sq_df.sort_values(by='total', ascending=False)
        home_sh_sq_df.reset_index(drop=True, inplace=True)
        home_sh_sq_df = home_sh_sq_df.head(5)
        home_sh_sq_df['shortName'] = home_sh_sq_df['name'].apply(get_short_name)
        
        # Initialize an empty dictionary to store away players different type of shot sequence counts
        away_shot_seq_counts = {'name': away_unique_players, 'Shots': [], 'Shot Assist': [], 'Buildup to shot': []}
        for name in away_unique_players:
            away_shot_seq_counts['Shots'].append(len(df[(df['name'] == name) & ((df['type']=='MissedShots') | (df['type']=='SavedShot') | (df['type']=='ShotOnPost') | (df['type']=='Goal'))]))
            away_shot_seq_counts['Shot Assist'].append(len(df[(df['name'] == name) & (df['type'] == 'Pass') & (df['type_value_Assist']==210)]))
            away_shot_seq_counts['Buildup to shot'].append(len(df_no_carry[(df_no_carry['name'] == name) & (df_no_carry['type'] == 'Pass') & (df['type_value_Assist'].shift(-1)==210)]))
        away_sh_sq_df = pd.DataFrame(away_shot_seq_counts)
        away_sh_sq_df['total'] = away_sh_sq_df['Shots']+away_sh_sq_df['Shot Assist']+away_sh_sq_df['Buildup to shot']
        away_sh_sq_df = away_sh_sq_df.sort_values(by='total', ascending=False)
        away_sh_sq_df.reset_index(drop=True, inplace=True)
        away_sh_sq_df = away_sh_sq_df.head(5)
        away_sh_sq_df['shortName'] = away_sh_sq_df['name'].apply(get_short_name)
        
        
        # Top Defenders
        # Initialize an empty dictionary to store home players different type of defensive actions counts
        home_defensive_actions_counts = {'name': home_unique_players, 'Tackles': [], 'Interceptions': [], 'Clearance': []}
        for name in home_unique_players:
            home_defensive_actions_counts['Tackles'].append(len(df[(df['name'] == name) & (df['type'] == 'Tackle') & (df['outcomeType']=='Successful')]))
            home_defensive_actions_counts['Interceptions'].append(len(df[(df['name'] == name) & (df['type'] == 'Interception')]))
            home_defensive_actions_counts['Clearance'].append(len(df[(df['name'] == name) & (df['type'] == 'Clearance')]))
        home_defender_df = pd.DataFrame(home_defensive_actions_counts)
        home_defender_df['total'] = home_defender_df['Tackles']+home_defender_df['Interceptions']+home_defender_df['Clearance']
        home_defender_df = home_defender_df.sort_values(by='total', ascending=False)
        home_defender_df.reset_index(drop=True, inplace=True)
        home_defender_df = home_defender_df.head(5)
        home_defender_df['shortName'] = home_defender_df['name'].apply(get_short_name)
        
        # Initialize an empty dictionary to store away players different type of defensive actions counts
        away_defensive_actions_counts = {'name': away_unique_players, 'Tackles': [], 'Interceptions': [], 'Clearance': []}
        for name in away_unique_players:
            away_defensive_actions_counts['Tackles'].append(len(df[(df['name'] == name) & (df['type'] == 'Tackle') & (df['outcomeType']=='Successful')]))
            away_defensive_actions_counts['Interceptions'].append(len(df[(df['name'] == name) & (df['type'] == 'Interception')]))
            away_defensive_actions_counts['Clearance'].append(len(df[(df['name'] == name) & (df['type'] == 'Clearance')]))
        away_defender_df = pd.DataFrame(away_defensive_actions_counts)
        away_defender_df['total'] = away_defender_df['Tackles']+away_defender_df['Interceptions']+away_defender_df['Clearance']
        away_defender_df = away_defender_df.sort_values(by='total', ascending=False)
        away_defender_df.reset_index(drop=True, inplace=True)
        away_defender_df = away_defender_df.head(5)
        away_defender_df['shortName'] = away_defender_df['name'].apply(get_short_name)
        
        # Get unique players
        unique_players = df['name'].unique()
        
        
        # Top Ball Progressor
        # Initialize an empty dictionary to store home players different type of pass counts
        progressor_counts = {'name': unique_players, 'Progressive Passes': [], 'Progressive Carries': []}
        for name in unique_players:
            progressor_counts['Progressive Passes'].append(len(df[(df['name'] == name) & (df['prog_pass'] >= 9.144) & (df['x']>=35) & (df['outcomeType']=='Successful') & (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)]))
            progressor_counts['Progressive Carries'].append(len(df[(df['name'] == name) & (df['prog_carry'] >= 9.144) & (df['endX']>=35)]))
        
        progressor_df = pd.DataFrame(progressor_counts)
        progressor_df['total'] = progressor_df['Progressive Passes']+progressor_df['Progressive Carries']
        progressor_df = progressor_df.sort_values(by='total', ascending=False)
        progressor_df.reset_index(drop=True, inplace=True)
        progressor_df = progressor_df.head(10)
        progressor_df['shortName'] = progressor_df['name'].apply(get_short_name)
        
        
        
        
        # Top Threate Creators
        # Initialize an empty dictionary to store home players different type of Carries counts
        xT_counts = {'name': unique_players, 'xT from Pass': [], 'xT from Carry': []}
        for name in unique_players:
            xT_counts['xT from Pass'].append((df[(df['name'] == name) & (df['type'] == 'Pass') & (df['xT']>=0) & (df['outcomeType']=='Successful') & (df['type_value_Corner taken']!=6) & (df['type_value_Free kick taken']!=5)])['xT'].sum().round(2))
            xT_counts['xT from Carry'].append((df[(df['name'] == name) & (df['type'] == 'Carry') & (df['xT']>=0)])['xT'].sum().round(2))
        xT_df = pd.DataFrame(xT_counts)
        xT_df['total'] = xT_df['xT from Pass']+xT_df['xT from Carry']
        xT_df = xT_df.sort_values(by='total', ascending=False)
        xT_df.reset_index(drop=True, inplace=True)
        xT_df = xT_df.head(10)
        xT_df['shortName'] = xT_df['name'].apply(get_short_name)
        
        
        
        
        # Shot Sequence Involvement
        df_no_carry = df[df['type']!='Carry']
        # Initialize an empty dictionary to store home players different type of shot sequence counts
        shot_seq_counts = {'name': unique_players, 'Shots': [], 'Shot Assist': [], 'Buildup to shot': []}
        # Putting counts in those lists
        for name in unique_players:
            shot_seq_counts['Shots'].append(len(df[(df['name'] == name) & ((df['type']=='MissedShots') | (df['type']=='SavedShot') | (df['type']=='ShotOnPost') | (df['type']=='Goal'))]))
            shot_seq_counts['Shot Assist'].append(len(df[(df['name'] == name) & (df['type'] == 'Pass') & (df['type_value_Assist']==210)]))
            shot_seq_counts['Buildup to shot'].append(len(df_no_carry[(df_no_carry['name'] == name) & (df_no_carry['type'] == 'Pass') & (df['type_value_Assist'].shift(-1)==210)]))
        # converting that list into a dataframe
        sh_sq_df = pd.DataFrame(shot_seq_counts)
        sh_sq_df['total'] = sh_sq_df['Shots']+sh_sq_df['Shot Assist']+sh_sq_df['Buildup to shot']
        sh_sq_df = sh_sq_df.sort_values(by='total', ascending=False)
        sh_sq_df.reset_index(drop=True, inplace=True)
        sh_sq_df = sh_sq_df.head(10)
        sh_sq_df['shortName'] = sh_sq_df['name'].apply(get_short_name)
        
        
        
        
        # Top Defenders
        # Initialize an empty dictionary to store home players different type of defensive actions counts
        defensive_actions_counts = {'name': unique_players, 'Tackles': [], 'Interceptions': [], 'Clearance': []}
        for name in unique_players:
            defensive_actions_counts['Tackles'].append(len(df[(df['name'] == name) & (df['type'] == 'Tackle') & (df['outcomeType']=='Successful')]))
            defensive_actions_counts['Interceptions'].append(len(df[(df['name'] == name) & (df['type'] == 'Interception')]))
            defensive_actions_counts['Clearance'].append(len(df[(df['name'] == name) & (df['type'] == 'Clearance')]))
        defender_df = pd.DataFrame(defensive_actions_counts)
        defender_df['total'] = defender_df['Tackles']+defender_df['Interceptions']+defender_df['Clearance']
        defender_df = defender_df.sort_values(by='total', ascending=False)
        defender_df.reset_index(drop=True, inplace=True)
        defender_df = defender_df.head(10)
        defender_df['shortName'] = defender_df['name'].apply(get_short_name)
        
        
        
        # Top Passer's PassMap
        
        def home_player_passmap(ax):
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-0.5, 68.5)
        
            # taking the top home passer and plotting his passmap
            home_player_name = home_progressor_df['name'].iloc[0]
        
            acc_pass = df[(df['name']==home_player_name) & (df['type']=='Pass') & (df['outcomeType']=='Successful')]
            pro_pass = acc_pass[(acc_pass['prog_pass']>=9.11) & (acc_pass['x']>=35) & (acc_pass['type_value_Corner taken']!=6) & (acc_pass['type_value_Free kick taken']!=5)]
            pro_carry = df[(df['name']==home_player_name) & (df['prog_carry']>=9.11) & (df['endX']>=35)]
            key_pass = acc_pass[acc_pass['type_value_Assist']==210]
            g_assist = acc_pass[acc_pass['assist']==1]
        
            pitch.lines(acc_pass.x, acc_pass.y, acc_pass.endX, acc_pass.endY, color=line_color, lw=2, alpha=0.15, comet=True, zorder=2, ax=ax)
            pitch.lines(pro_pass.x, pro_pass.y, pro_pass.endX, pro_pass.endY, color=col1, lw=3, alpha=1,    comet=True, zorder=3, ax=ax)
            pitch.lines(key_pass.x, key_pass.y, key_pass.endX, key_pass.endY, color=violet,     lw=4, alpha=1,    comet=True, zorder=4, ax=ax)
            pitch.lines(g_assist.x, g_assist.y, g_assist.endX, g_assist.endY, color='green',      lw=4, alpha=1,    comet=True, zorder=5, ax=ax)
        
            ax.scatter(acc_pass.endX, acc_pass.endY, s=30, color=bg_color,    edgecolor='gray', alpha=1, zorder=2)
            ax.scatter(pro_pass.endX, pro_pass.endY, s=40, color=bg_color,  edgecolor= col1,  alpha=1, zorder=3)
            ax.scatter(key_pass.endX, key_pass.endY, s=50, color=bg_color,  edgecolor=violet, alpha=1, zorder=4)
            ax.scatter(g_assist.endX, g_assist.endY, s=50, color=bg_color,  edgecolor= 'green', alpha=1, zorder=5)
        
            for index, row in pro_carry.iterrows():
                arrow = patches.FancyArrowPatch((row['x'], row['y']), (row['endX'], row['endY']), arrowstyle='->', color=col1, zorder=4, mutation_scale=20, 
                                                alpha=0.9, linewidth=2, linestyle='--')
                ax.add_patch(arrow) 
        
        
            home_name_show = home_progressor_df['shortName'].iloc[0]
            ax.set_title(f"{home_name_show} PassMap", color=col1, fontsize=25, fontweight='bold', y=1.03)
            ax.text(0,-3, f'Prog. Pass: {len(pro_pass)}          Prog. Carry: {len(pro_carry)}', fontsize=15, color=col1, ha='left', va='center')
            ax_text(105,-3, s=f'Key Pass: {len(key_pass)}          <Assist: {len(g_assist)}>', fontsize=15, color=violet, ha='right', va='center',
                    highlight_textprops=[{'color':'green'}], ax=ax)
        
        def away_player_passmap(ax):
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-0.5, 68.5)
            ax.invert_xaxis()
            ax.invert_yaxis()
        
            # taking the top away passer and plotting his passmap
            away_player_name = away_progressor_df['name'].iloc[0]
            
            acc_pass = df[(df['name']==away_player_name) & (df['type']=='Pass') & (df['outcomeType']=='Successful')]
            pro_pass = acc_pass[(acc_pass['prog_pass']>=9.11) & (acc_pass['x']>=35) & (acc_pass['type_value_Corner taken']!=6) & (acc_pass['type_value_Free kick taken']!=5)]
            pro_carry = df[(df['name']==away_player_name) & (df['prog_carry']>=9.11) & (df['endX']>=35)]
            key_pass = acc_pass[acc_pass['type_value_Assist']==210]
            g_assist = acc_pass[acc_pass['assist']==1]
        
            pitch.lines(acc_pass.x, acc_pass.y, acc_pass.endX, acc_pass.endY, color=line_color, lw=2, alpha=0.15, comet=True, zorder=2, ax=ax)
            pitch.lines(pro_pass.x, pro_pass.y, pro_pass.endX, pro_pass.endY, color=col2      , lw=3, alpha=1,    comet=True, zorder=3, ax=ax)
            pitch.lines(key_pass.x, key_pass.y, key_pass.endX, key_pass.endY, color=violet,     lw=4, alpha=1,    comet=True, zorder=4, ax=ax)
            pitch.lines(g_assist.x, g_assist.y, g_assist.endX, g_assist.endY, color='green',      lw=4, alpha=1,    comet=True, zorder=5, ax=ax)
        
            ax.scatter(acc_pass.endX, acc_pass.endY, s=30, color=bg_color,    edgecolor='gray', alpha=1, zorder=2)
            ax.scatter(pro_pass.endX, pro_pass.endY, s=40, color=bg_color,  edgecolor= col2,  alpha=1, zorder=3)
            ax.scatter(key_pass.endX, key_pass.endY, s=50, color=bg_color,  edgecolor=violet, alpha=1, zorder=4)
            ax.scatter(g_assist.endX, g_assist.endY, s=50, color=bg_color,  edgecolor= 'green', alpha=1, zorder=5)
        
            for index, row in pro_carry.iterrows():
                arrow = patches.FancyArrowPatch((row['x'], row['y']), (row['endX'], row['endY']), arrowstyle='->', color=col2, zorder=4, mutation_scale=20, 
                                                alpha=0.9, linewidth=2, linestyle='--')
                ax.add_patch(arrow) 
        
        
            away_name_show = away_progressor_df['shortName'].iloc[0]
            ax.set_title(f"{away_name_show} PassMap", color=col2, fontsize=25, fontweight='bold', y=1.03)
            ax.text(0,71, f'Prog. Pass: {len(pro_pass)}          Prog. Carry: {len(pro_carry)}', fontsize=15, color=col2, ha='right', va='center')
            ax_text(105,71, s=f'Key Pass: {len(key_pass)}          <Assist: {len(g_assist)}>', fontsize=15, color=violet, ha='left', va='center',
                    highlight_textprops=[{'color':'green'}], ax=ax)
            
            
        # Forward Pass Receiving
        
        def home_passes_recieved(ax):
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-0.5, 68.5)
        
            # plotting the home center forward pass receiving
            name = home_Forward
            name_show = get_short_name(name)
            filtered_rows = df[(df['type'] == 'Pass') & (df['outcomeType'] == 'Successful') & (df['name'].shift(-1) == name)]
            keypass_recieved_df = filtered_rows[filtered_rows['type_value_Assist']==210]
            assist_recieved_df = filtered_rows[filtered_rows['assist']==1]
            pr = len(filtered_rows)
            kpr = len(keypass_recieved_df)
            ar = len(assist_recieved_df)
        
            lc1 = pitch.lines(filtered_rows.x, filtered_rows.y, filtered_rows.endX, filtered_rows.endY, lw=3, transparent=True, comet=True,color=col1, ax=ax, alpha=0.5)
            lc2 = pitch.lines(keypass_recieved_df.x, keypass_recieved_df.y, keypass_recieved_df.endX, keypass_recieved_df.endY, lw=4, transparent=True, comet=True,color=violet, ax=ax, alpha=0.75)
            lc3 = pitch.lines(assist_recieved_df.x, assist_recieved_df.y, assist_recieved_df.endX, assist_recieved_df.endY, lw=4, transparent=True, comet=True,color='green', ax=ax, alpha=0.75)
            sc1 = pitch.scatter(filtered_rows.endX, filtered_rows.endY, s=30, edgecolor=col1, linewidth=1, color=bg_color, zorder=2, ax=ax)
            sc2 = pitch.scatter(keypass_recieved_df.endX, keypass_recieved_df.endY, s=40, edgecolor=violet, linewidth=1.5, color=bg_color, zorder=2, ax=ax)
            sc3 = pitch.scatter(assist_recieved_df.endX, assist_recieved_df.endY, s=50, edgecolors='green', linewidths=1, marker='football', c=bg_color, zorder=2, ax=ax)
        
            avg_endY = filtered_rows['endY'].median()
            avg_endX = filtered_rows['endX'].median()
            ax.axvline(x=avg_endX, ymin=0, ymax=68, color='gray', linestyle='--', alpha=0.6, linewidth=2)
            ax.axhline(y=avg_endY, xmin=0, xmax=105, color='gray', linestyle='--', alpha=0.6, linewidth=2)
            ax.set_title(f"{name_show} Passes Recieved", color=col1, fontsize=25, fontweight='bold', y=1.03)
            highlight_text=[{'color':violet}, {'color':'green'}]
            ax_text(52.5,-3, f'Passes Recieved:{pr+kpr} | <Keypasses Recieved:{kpr}> | <Assist Received: {ar}>', color=line_color, fontsize=15, ha='center', 
                    va='center', highlight_textprops=highlight_text, ax=ax)
        
            return
        
        def away_passes_recieved(ax):
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-0.5, 68.5)
            ax.invert_xaxis()
            ax.invert_yaxis()
        
            # plotting the away center forward pass receiving
            name = away_Forward
            name_show = get_short_name(name)
            filtered_rows = df[(df['type'] == 'Pass') & (df['outcomeType'] == 'Successful') & (df['name'].shift(-1) == name)]
            keypass_recieved_df = filtered_rows[filtered_rows['type_value_Assist']==210]
            assist_recieved_df = filtered_rows[filtered_rows['assist']==1]
            pr = len(filtered_rows)
            kpr = len(keypass_recieved_df)
            ar = len(assist_recieved_df)
        
            lc1 = pitch.lines(filtered_rows.x, filtered_rows.y, filtered_rows.endX, filtered_rows.endY, lw=3, transparent=True, comet=True,color=col2, ax=ax, alpha=0.5)
            lc2 = pitch.lines(keypass_recieved_df.x, keypass_recieved_df.y, keypass_recieved_df.endX, keypass_recieved_df.endY, lw=4, transparent=True, comet=True,color=violet, ax=ax, alpha=0.75)
            lc3 = pitch.lines(assist_recieved_df.x, assist_recieved_df.y, assist_recieved_df.endX, assist_recieved_df.endY, lw=4, transparent=True, comet=True,color='green', ax=ax, alpha=0.75)
            sc1 = pitch.scatter(filtered_rows.endX, filtered_rows.endY, s=30, edgecolor=col2, linewidth=1, color=bg_color, zorder=2, ax=ax)
            sc2 = pitch.scatter(keypass_recieved_df.endX, keypass_recieved_df.endY, s=40, edgecolor=violet, linewidth=1.5, color=bg_color, zorder=2, ax=ax)
            sc3 = pitch.scatter(assist_recieved_df.endX, assist_recieved_df.endY, s=50, edgecolors='green', linewidths=1, marker='football', c=bg_color, zorder=2, ax=ax)
        
            avg_endX = filtered_rows['endX'].median()
            avg_endY = filtered_rows['endY'].median()
            ax.axvline(x=avg_endX, ymin=0, ymax=68, color='gray', linestyle='--', alpha=0.6, linewidth=2)
            ax.axhline(y=avg_endY, xmin=0, xmax=105, color='gray', linestyle='--', alpha=0.6, linewidth=2)
            ax.set_title(f"{name_show} Passes Recieved", color=col2, fontsize=25, fontweight='bold', y=1.03)
            highlight_text=[{'color':violet}, {'color':'green'}]
            ax_text(52.5,71, f'Passes Recieved:{pr+kpr} | <Keypasses Recieved:{kpr}> | <Assist Received: {ar}>', color=line_color, fontsize=15, ha='center', 
                    va='center', highlight_textprops=highlight_text, ax=ax)
        
            return
        
        
        # Top Defenders
        
        def home_player_def_acts(ax):
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, line_zorder=2, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-12,68.5)
        
            # taking the top home defender and plotting his defensive actions
            home_player_name = home_defender_df['name'].iloc[0]
            home_playerdf = df[(df['name']==home_player_name)]
        
            hp_tk = home_playerdf[home_playerdf['type']=='Tackle']
            hp_intc = home_playerdf[(home_playerdf['type']=='Interception') | (home_playerdf['type']=='BlockedPass')]
            hp_br = home_playerdf[home_playerdf['type']=='BallRecovery']
            hp_cl = home_playerdf[home_playerdf['type']=='Clearance']
            hp_fl = home_playerdf[(home_playerdf['type']=='Foul') & (home_playerdf['outcomeType']=='Unsuccessful')]
            hp_ar = home_playerdf[(home_playerdf['type']=='Aerial')]
        
            sc1 = pitch.scatter(hp_tk.x, hp_tk.y, s=250, c=col1, lw=2.5, edgecolor=col1, marker='+', hatch='/////', ax=ax)
            sc2 = pitch.scatter(hp_intc.x, hp_intc.y, s=250, c='None', lw=2.5, edgecolor=col1, marker='s', hatch='/////', ax=ax)
            sc3 = pitch.scatter(hp_br.x, hp_br.y, s=250, c='None', lw=2.5, edgecolor=col1, marker='o', hatch='/////', ax=ax)
            sc4 = pitch.scatter(hp_cl.x, hp_cl.y, s=250, c='None', lw=2.5, edgecolor=col1, marker='d', hatch='/////', ax=ax)
            sc5 = pitch.scatter(hp_fl.x, hp_fl.y, s=250, c=col1, lw=2.5, edgecolor=col1, marker='x', hatch='/////', ax=ax)
            sc6 = pitch.scatter(hp_ar.x, hp_ar.y, s=250, c='None', lw=2.5, edgecolor=col1, marker='^', hatch='/////', ax=ax)
        
            sc7 =  pitch.scatter(2, -4, s=150, c=col1, lw=2.5, edgecolor=col1, marker='+', hatch='/////', ax=ax)
            sc8 =  pitch.scatter(2, -10, s=150, c='None', lw=2.5, edgecolor=col1, marker='s', hatch='/////', ax=ax)
            sc9 =  pitch.scatter(41, -4, s=150, c='None', lw=2.5, edgecolor=col1, marker='o', hatch='/////', ax=ax)
            sc10 = pitch.scatter(41, -10, s=150, c='None', lw=2.5, edgecolor=col1, marker='d', hatch='/////', ax=ax)
            sc11 = pitch.scatter(103, -4, s=150, c=col1, lw=2.5, edgecolor=col1, marker='x', hatch='/////', ax=ax)
            sc12 = pitch.scatter(103, -10, s=150, c='None', lw=2.5, edgecolor=col1, marker='^', hatch='/////', ax=ax)
        
            ax.text(5, -3, f"Tackle: {len(hp_tk)}\n\nInterception: {len(hp_intc)}", color=col1, ha='left', va='top', fontsize=13)
            ax.text(43, -3, f"BallRecovery: {len(hp_br)}\n\nClearance: {len(hp_cl)}", color=col1, ha='left', va='top', fontsize=13)
            ax.text(100, -3, f"{len(hp_fl)} Fouls\n\n{len(hp_ar)} Aerials", color=col1, ha='right', va='top', fontsize=13)
        
            home_name_show = home_defender_df['shortName'].iloc[0]
            ax.set_title(f"{home_name_show} Defensive Actions", color=col1, fontsize=25, fontweight='bold')
        
        def away_player_def_acts(ax):
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, line_zorder=2, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-0.5,80)
            ax.invert_xaxis()
            ax.invert_yaxis()
        
            # taking the top home defender and plotting his defensive actions
            away_player_name = away_defender_df['name'].iloc[0]
            away_playerdf = df[(df['name']==away_player_name)]
        
            ap_tk = away_playerdf[away_playerdf['type']=='Tackle']
            ap_intc = away_playerdf[(away_playerdf['type']=='Interception') | (away_playerdf['type']=='BlockedPass')]
            ap_br = away_playerdf[away_playerdf['type']=='BallRecovery']
            ap_cl = away_playerdf[away_playerdf['type']=='Clearance']
            ap_fl = away_playerdf[(away_playerdf['type']=='Foul') & (away_playerdf['outcomeType']=='Unsuccessful')]
            ap_ar = away_playerdf[(away_playerdf['type']=='Aerial')]
        
            sc1 = pitch.scatter(ap_tk.x, ap_tk.y, s=250, c=col2, lw=2.5, edgecolor=col2, marker='+', hatch='/////', ax=ax)
            sc2 = pitch.scatter(ap_intc.x, ap_intc.y, s=250, c='None', lw=2.5, edgecolor=col2, marker='s', hatch='/////', ax=ax)
            sc3 = pitch.scatter(ap_br.x, ap_br.y, s=250, c='None', lw=2.5, edgecolor=col2, marker='o', hatch='/////', ax=ax)
            sc4 = pitch.scatter(ap_cl.x, ap_cl.y, s=250, c='None', lw=2.5, edgecolor=col2, marker='d', hatch='/////', ax=ax)
            sc5 = pitch.scatter(ap_fl.x, ap_fl.y, s=250, c=col2, lw=2.5, edgecolor=col2, marker='x', hatch='/////', ax=ax)
            sc6 = pitch.scatter(ap_ar.x, ap_ar.y, s=250, c='None', lw=2.5, edgecolor=col2, marker='^', hatch='/////', ax=ax)
        
            sc7 =  pitch.scatter(2, 72, s=150, c=col2, lw=2.5, edgecolor=col2, marker='+', hatch='/////', ax=ax)
            sc8 =  pitch.scatter(2, 78, s=150, c='None', lw=2.5, edgecolor=col2, marker='s', hatch='/////', ax=ax)
            sc9 =  pitch.scatter(41, 72, s=150, c='None', lw=2.5, edgecolor=col2, marker='o', hatch='/////', ax=ax)
            sc10 = pitch.scatter(41, 78, s=150, c='None', lw=2.5, edgecolor=col2, marker='d', hatch='/////', ax=ax)
            sc11 = pitch.scatter(103, 72, s=150, c=col2, lw=2.5, edgecolor=col2, marker='x', hatch='/////', ax=ax)
            sc12 = pitch.scatter(103, 78, s=150, c='None', lw=2.5, edgecolor=col2, marker='^', hatch='/////', ax=ax)
        
            ax.text(5, 71, f"Tackle: {len(ap_tk)}\n\nInterception: {len(ap_intc)}", color=col2, ha='right', va='top', fontsize=13)
            ax.text(43, 71, f"BallRecovery: {len(ap_br)}\n\nClearance: {len(ap_cl)}", color=col2, ha='right', va='top', fontsize=13)
            ax.text(100, 71, f"{len(ap_fl)} Fouls\n\n{len(ap_ar)} Aerials", color=col2, ha='left', va='top', fontsize=13)
        
            away_name_show = away_defender_df['shortName'].iloc[0]
            ax.set_title(f"{away_name_show} Defensive Actions", color=col2, fontsize=25, fontweight='bold')
            
            
        # GoalKeeper PassMap
        
        def home_gk(ax):
            df_gk = df[(df['name']==homeGK) & (df['shortName'].notna())]
            gk_pass = df_gk[df_gk['type']=='Pass']
            op_pass = df_gk[(df_gk['type']=='Pass') & (df_gk['type_value_Goal Kick']!=124) & (df_gk['type_value_Free kick taken']!=5)]
            sp_pass = df_gk[(df_gk['type']=='Pass') & ((df_gk['type_value_Goal Kick']==124) | (df_gk['type_value_Free kick taken']==5))]
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-0.5, 68.5)
            gk_name = df_gk['shortName'].unique()[0]
            op_succ = sp_succ = 0
            for index, row in op_pass.iterrows():
                if row['outcomeType']=='Successful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=col1, lw=4, comet=True, alpha=0.5, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=col1, edgecolor=line_color, zorder=3)
                    op_succ += 1
                if row['outcomeType']=='Unsuccessful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=col1, lw=4, comet=True, alpha=0.5, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=bg_color, edgecolor=col1, zorder=3)
            for index, row in sp_pass.iterrows():
                if row['outcomeType']=='Successful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=violet, lw=4, comet=True, alpha=0.5, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=violet, edgecolor=line_color, zorder=3)
                    sp_succ += 1
                if row['outcomeType']=='Unsuccessful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=violet, lw=4, comet=True, alpha=0.35, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=bg_color, edgecolor=violet, zorder=3)
        
            op_pass['length'] = np.sqrt((op_pass['x']-op_pass['endX'])**2 + (op_pass['y']-op_pass['endY'])**2)
            sp_pass['length'] = np.sqrt((sp_pass['x']-sp_pass['endX'])**2 + (sp_pass['y']-sp_pass['endY'])**2)
            avg_len_op = round(op_pass['length'].median(), 2)
            avg_len_sp = round(sp_pass['length'].median(), 2)
            
            ax.set_title(f'{gk_name} PassMap', color=col1, fontsize=25, fontweight='bold', y=1.07)
            ax.text(52.5, -3, f'Avg. OpenPlay Pass Length: {avg_len_op}m     |     Avg. SetPiece Pass Length: {avg_len_sp}m', color=line_color, fontsize=14, ha='center', va='center')
            ax_text(52.5, 70, s=f'<Open-play Pass (Acc.): {len(op_pass)} ({op_succ})>     |     <GoalKick/Freekick (Acc.): {len(sp_pass)} ({sp_succ})>', 
                    fontsize=15, highlight_textprops=[{'color':col1}, {'color':violet}], ha='center', va='center', ax=ax)
        
            return
        
        def away_gk(ax):
            df_gk = df[(df['name']==awayGK) & (df['shortName'].notna())]
            gk_pass = df_gk[df_gk['type']=='Pass']
            op_pass = df_gk[(df_gk['type']=='Pass') & (df_gk['type_value_Goal Kick']!=124) & (df_gk['type_value_Free kick taken']!=5)]
            sp_pass = df_gk[(df_gk['type']=='Pass') & ((df_gk['type_value_Goal Kick']==124) | (df_gk['type_value_Free kick taken']==5))]
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_xlim(-0.5, 105.5)
            ax.set_ylim(-0.5, 68.5)
            ax.invert_xaxis()
            ax.invert_yaxis()
            gk_name = df_gk['shortName'].unique()[0]
            op_succ = sp_succ = 0
            for index, row in op_pass.iterrows():
                if row['outcomeType']=='Successful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=col2, lw=4, comet=True, alpha=0.5, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=col2, edgecolor=line_color, zorder=3)
                    op_succ += 1
                if row['outcomeType']=='Unsuccessful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=col2, lw=4, comet=True, alpha=0.5, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=bg_color, edgecolor=col2, zorder=3)
            for index, row in sp_pass.iterrows():
                if row['outcomeType']=='Successful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=violet, lw=4, comet=True, alpha=0.5, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=violet, edgecolor=line_color, zorder=3)
                    sp_succ += 1
                if row['outcomeType']=='Unsuccessful':
                    pitch.lines(row['x'], row['y'], row['endX'], row['endY'], color=violet, lw=4, comet=True, alpha=0.35, zorder=2, ax=ax)
                    ax.scatter(row['endX'], row['endY'], s=40, color=bg_color, edgecolor=violet, zorder=3)
        
            op_pass['length'] = np.sqrt((op_pass['x']-op_pass['endX'])**2 + (op_pass['y']-op_pass['endY'])**2)
            sp_pass['length'] = np.sqrt((sp_pass['x']-sp_pass['endX'])**2 + (sp_pass['y']-sp_pass['endY'])**2)
            avg_len_op = round(op_pass['length'].median(), 2)
            avg_len_sp = round(sp_pass['length'].median(), 2)
        
            ax.set_title(f'{gk_name} PassMap', color=col2, fontsize=25, fontweight='bold', y=1.07)
            ax.text(52.5, 71, f'Avg. OpenPlay Pass Length: {avg_len_op}m     |     Avg. SetPiece Pass Length: {avg_len_sp}m', color=line_color, fontsize=14, ha='center', va='center')
            ax_text(52.5, -2, s=f'<Open-play Pass (Acc.): {len(op_pass)} ({op_succ})>     |     <GoalKick/Freekick (Acc.): {len(sp_pass)} ({sp_succ})>', 
                    fontsize=15, highlight_textprops=[{'color':col2}, {'color':violet}], ha='center', va='center', ax=ax)
        
            return
        
        
        from matplotlib.ticker import MaxNLocator
        def sh_sq_bar(ax):
          top10_sh_sq = sh_sq_df.nsmallest(10, 'total')['shortName'].tolist()
        
          shsq_sh = sh_sq_df.nsmallest(10, 'total')['Shots'].tolist()
          shsq_sa = sh_sq_df.nsmallest(10, 'total')['Shot Assist'].tolist()
          shsq_bs = sh_sq_df.nsmallest(10, 'total')['Buildup to shot'].tolist()
        
          left1 = [w + x for w, x in zip(shsq_sh, shsq_sa)]
        
          ax.barh(top10_sh_sq, shsq_sh, label='Shot', color=col1, left=0)
          ax.barh(top10_sh_sq, shsq_sa, label='Shot Assist', color=violet, left=shsq_sh)
          ax.barh(top10_sh_sq, shsq_bs, label='Buildup to Shot', color=col2, left=left1)
        
          # Add counts in the middle of the bars (if count > 0)
          for i, player in enumerate(top10_sh_sq):
              for j, count in enumerate([shsq_sh[i], shsq_sa[i], shsq_bs[i]]):
                  if count > 0:
                      x_position = sum([shsq_sh[i], shsq_sa[i]][:j]) + count / 2
                      ax.text(x_position, i, str(count), ha='center', va='center', color=bg_color, fontsize=18, fontweight='bold')
        
          max_x = sh_sq_df['total'].iloc()[0]
          x_coord = [2 * i for i in range(1, int(max_x/2))]
          for x in x_coord:
              ax.axvline(x=x, color='gray', linestyle='--', zorder=2, alpha=0.5)
        
          ax.set_facecolor(bg_color)
          ax.tick_params(axis='x', colors=line_color, labelsize=15)
          ax.tick_params(axis='y', colors=line_color, labelsize=15)
          ax.xaxis.label.set_color(line_color)
          ax.yaxis.label.set_color(line_color)
          for spine in ax.spines.values():
            spine.set_edgecolor(bg_color)
        
          ax.set_title(f"Shot Sequence Involvement", color=line_color, fontsize=25, fontweight='bold')
          ax.legend(fontsize=13)
        
        def passer_bar(ax):
          top10_passers = progressor_df.nsmallest(10, 'total')['shortName'].tolist()
        
          passers_pp = progressor_df.nsmallest(10, 'total')['Progressive Passes'].tolist()
          passers_tp = progressor_df.nsmallest(10, 'total')['Progressive Carries'].tolist()
        
          left1 = [w + x for w, x in zip(passers_pp, passers_tp)]
        
          ax.barh(top10_passers, passers_pp, label='Prog. Pass', color=col1, left=0)
          ax.barh(top10_passers, passers_tp, label='Prog. Carries', color=col2, left=passers_pp)
        
          # Add counts in the middle of the bars (if count > 0)
          for i, player in enumerate(top10_passers):
              for j, count in enumerate([passers_pp[i], passers_tp[i]]):
                  if count > 0:
                      x_position = sum([passers_pp[i], passers_tp[i]][:j]) + count / 2
                      ax.text(x_position, i, str(count), ha='center', va='center', color=bg_color, fontsize=18, fontweight='bold')
        
          max_x = progressor_df['total'].iloc()[0]
          x_coord = [2 * i for i in range(1, int(max_x/2))]
          for x in x_coord:
              ax.axvline(x=x, color='gray', linestyle='--', zorder=2, alpha=0.5)
        
          ax.set_facecolor(bg_color)
          ax.tick_params(axis='x', colors=line_color, labelsize=15)
          ax.tick_params(axis='y', colors=line_color, labelsize=15)
          ax.xaxis.label.set_color(line_color)
          ax.yaxis.label.set_color(line_color)
          for spine in ax.spines.values():
            spine.set_edgecolor(bg_color)
        
          ax.set_title(f"Top10 Ball Progressors", color=line_color, fontsize=25, fontweight='bold')
          ax.legend(fontsize=13)
        
        
        def defender_bar(ax):
          top10_defenders = defender_df.nsmallest(10, 'total')['shortName'].tolist()
        
          defender_tk = defender_df.nsmallest(10, 'total')['Tackles'].tolist()
          defender_in = defender_df.nsmallest(10, 'total')['Interceptions'].tolist()
          defender_ar = defender_df.nsmallest(10, 'total')['Clearance'].tolist()
        
          left1 = [w + x for w, x in zip(defender_tk, defender_in)]
        
          ax.barh(top10_defenders, defender_tk, label='Tackle', color=col1, left=0)
          ax.barh(top10_defenders, defender_in, label='Interception', color=violet, left=defender_tk)
          ax.barh(top10_defenders, defender_ar, label='Clearance', color=col2, left=left1)
        
          # Add counts in the middle of the bars (if count > 0)
          for i, player in enumerate(top10_defenders):
              for j, count in enumerate([defender_tk[i], defender_in[i], defender_ar[i]]):
                  if count > 0:
                      x_position = sum([defender_tk[i], defender_in[i]][:j]) + count / 2
                      ax.text(x_position, i, str(count), ha='center', va='center', color=bg_color, fontsize=18, fontweight='bold')
        
          max_x = defender_df['total'].iloc()[0]
          x_coord = [2 * i for i in range(1, int(max_x/2))]
          for x in x_coord:
              ax.axvline(x=x, color='gray', linestyle='--', zorder=2, alpha=0.5)
        
          ax.set_facecolor(bg_color)
          ax.tick_params(axis='x', colors=line_color, labelsize=15)
          ax.tick_params(axis='y', colors=line_color, labelsize=15)
          ax.xaxis.label.set_color(line_color)
          ax.yaxis.label.set_color(line_color)
          for spine in ax.spines.values():
            spine.set_edgecolor(bg_color)
        
        
          ax.set_title(f"Top10 Defenders", color=line_color, fontsize=25, fontweight='bold')
          ax.legend(fontsize=13)
        
        
        def threat_creators(ax):
          top10_xT = xT_df.nsmallest(10, 'total')['shortName'].tolist()
        
          xT_pass = xT_df.nsmallest(10, 'total')['xT from Pass'].tolist()
          xT_carry = xT_df.nsmallest(10, 'total')['xT from Carry'].tolist()
        
          left1 = [w + x for w, x in zip(xT_pass, xT_carry)]
        
          ax.barh(top10_xT, xT_pass, label='xT from pass', color=col1, left=0)
          ax.barh(top10_xT, xT_carry, label='xT from carry', color=violet, left=xT_pass)
        
          # Add counts in the middle of the bars (if count > 0)
          for i, player in enumerate(top10_xT):
              for j, count in enumerate([xT_pass[i], xT_carry[i]]):
                  if count > 0:
                      x_position = sum([xT_pass[i], xT_carry[i]][:j]) + count / 2
                      ax.text(x_position, i, str(count), ha='center', va='center', color=line_color, fontsize=15, rotation=45)
        
          # max_x = xT_df['total'].iloc()[0]
          # x_coord = [2 * i for i in range(1, int(max_x/2))]
          # for x in x_coord:
          #     ax.axvline(x=x, color='gray', linestyle='--', zorder=2, alpha=0.5)
        
          ax.set_facecolor(bg_color)
          ax.tick_params(axis='x', colors=line_color, labelsize=15)
          ax.tick_params(axis='y', colors=line_color, labelsize=15)
          ax.xaxis.label.set_color(line_color)
          ax.yaxis.label.set_color(line_color)
          for spine in ax.spines.values():
            spine.set_edgecolor(bg_color)
        
        
          ax.set_title(f"Top10 Threatening Players", color=line_color, fontsize=25, fontweight='bold')
          ax.legend(fontsize=13)
          
          
          
        
            
            
            
        fig, axs = plt.subplots(4,3, figsize=(35,35), facecolor=bg_color)
        
        home_player_passmap(axs[0,0])
        passer_bar(axs[0,1])
        away_player_passmap(axs[0,2])
        home_passes_recieved(axs[1,0])
        sh_sq_bar(axs[1,1])
        away_passes_recieved(axs[1,2])
        home_player_def_acts(axs[2,0])
        defender_bar(axs[2,1])
        away_player_def_acts(axs[2,2])
        home_gk(axs[3,0])
        threat_creators(axs[3,1])
        away_gk(axs[3,2])
        
        highlight_text = [{'color':col1}, {'color':col2}]
        fig_text(0.5, 0.98, f"<{hteamName} {hgoal_count}> - <{agoal_count} {ateamName}>", color=line_color, fontsize=30, fontweight='bold',
                    highlight_textprops=highlight_text, ha='center', va='center', ax=fig)
        
        
        # fig.text(0.5, 0.95, f"Primera Division Femenina 2024-25 |  Top Players of the Match", color=line_color, fontsize=30, ha='center', va='center')
        fig.text(0.5, 0.95, f"{league_name} |  Top Players of the Match", color=line_color, fontsize=30, ha='center', va='center')
        fig.text(0.5, 0.93, f"Data from: Opta  |  made by: @Turadi_7", color=line_color, fontsize=22.5, ha='center', va='center')
        fig.text(0.125,0.097, 'Attacking Direction ------->', color=col1, fontsize=25, ha='left', va='center')
        fig.text(0.9,0.097, '<------- Attacking Direction', color=col2, fontsize=25, ha='right', va='center')
        
        st.write('Top Players of the Match') 
        st.pyplot(fig)


        def offensive_actions(ax, pname):
            # Viz Dfs:
            playerdf = df[df['name']==pname]
            passdf = playerdf[playerdf['type']=='Pass']
            succ_passdf = passdf[passdf['outcomeType']=='Successful']
            prg_pass = playerdf[(playerdf['prog_pass']>9.144) & (playerdf['outcomeType']=='Successful') & (playerdf['x']>35) &
                                (playerdf['type_value_Corner taken']!=6) & (playerdf['type_value_Free kick taken']!=5)]
            prg_carry = playerdf[(playerdf['prog_carry']>9.144) & (playerdf['endX']>35)]
            cc = playerdf[(playerdf['type_value_Assist']==210)]
            ga = playerdf[(playerdf['assist']==1)]
            goal = playerdf[(playerdf['type']=='Goal') & (playerdf['isOwnGoal'].isna())]
            owngoal = playerdf[(playerdf['type']=='Goal') & (playerdf['isOwnGoal'].notna())]
            ontr = playerdf[(playerdf['type']=='SavedShot')]
            oftr = playerdf[playerdf['type'].isin(['MissedShots', 'ShotOnPost'])]
            takeOns = playerdf[(playerdf['type']=='TakeOn') & (playerdf['outcomeType']=='Successful')]
            takeOnu = playerdf[(playerdf['type']=='TakeOn') & (playerdf['outcomeType']=='Unsuccessful')]

            # Pitch Plot
            pitch = VerticalPitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, line_zorder=2, linewidth=2, pad_bottom=27)
            pitch.draw(ax=ax)

            # line, arrow, scatter Plots
            pitch.lines(succ_passdf.x, succ_passdf.y, succ_passdf.endX, succ_passdf.endY, color='gray', comet=True, lw=2, alpha=0.65, zorder=1, ax=ax)
            pitch.scatter(succ_passdf.endX, succ_passdf.endY, color=bg_color, ec='gray', s=20, zorder=2, ax=ax)
            pitch.lines(prg_pass.x, prg_pass.y, prg_pass.endX, prg_pass.endY, color=col2, comet=True, lw=3, zorder=2, ax=ax)
            pitch.scatter(prg_pass.endX, prg_pass.endY, color=bg_color, ec=col2, s=40, zorder=3, ax=ax)
            pitch.lines(cc.x, cc.y, cc.endX, cc.endY, color=violet, comet=True, lw=3.5, zorder=3, ax=ax)
            pitch.scatter(cc.endX, cc.endY, color=bg_color, ec=violet, s=50, lw=1.5, zorder=4, ax=ax)
            pitch.lines(ga.x, ga.y, ga.endX, ga.endY, color='green', comet=True, lw=4, zorder=4, ax=ax)
            pitch.scatter(ga.endX, ga.endY, color=bg_color, ec='green', s=60, lw=2, zorder=5, ax=ax)

            for index, row in prg_carry.iterrows():
                arrow = patches.FancyArrowPatch((row['y'], row['x']), (row['endY'], row['endX']), arrowstyle='->', color=col2, zorder=2, mutation_scale=20, 
                                                linewidth=2, linestyle='--')
                ax.add_patch(arrow)

            pitch.scatter(goal.x, goal.y, c=bg_color, edgecolors='green', linewidths=1.2, s=300, marker='football', zorder=10, ax=ax)
            pitch.scatter(owngoal.x, owngoal.y, c=bg_color, edgecolors='orange', linewidths=1.2, s=300, marker='football', zorder=10, ax=ax)
            pitch.scatter(ontr.x, ontr.y, c=col1, edgecolors=line_color, linewidths=1.2, s=200, alpha=0.75, zorder=9, ax=ax)
            pitch.scatter(oftr.x, oftr.y, c=bg_color, edgecolors=col1, linewidths=1.2, s=200, alpha=0.75, zorder=8, ax=ax)

            pitch.scatter(takeOns.x, takeOns.y, c='orange', edgecolors=line_color, marker='h', s=200, alpha=0.75, zorder=7, ax=ax)
            pitch.scatter(takeOnu.x, takeOnu.y, c=bg_color, edgecolors='orange', marker='h', lw=1.2, hatch='//////', s=200, alpha=0.85, zorder=7, ax=ax)

            # Stats:
            pitch.scatter(-5, 68, c=bg_color, edgecolors='green', linewidths=1.2, s=300, marker='football', zorder=10, ax=ax)
            pitch.scatter(-10, 68, c=col1, edgecolors=line_color, linewidths=1.2, s=300, alpha=0.75, zorder=9, ax=ax)
            pitch.scatter(-15, 68, c=bg_color, edgecolors=col1, linewidths=1.2, s=300, alpha=0.75, zorder=8, ax=ax)
            pitch.scatter(-20, 68, c='orange', edgecolors=line_color, marker='h', s=300, alpha=0.75, zorder=7, ax=ax)
            pitch.scatter(-25, 68, c=bg_color, edgecolors='orange', marker='h', lw=1.2, hatch='//////', s=300, alpha=0.85, zorder=7, ax=ax)
            if len(owngoal)>0:
                ax_text(64, -4.5, f'Goals: {len(goal)} | <OwnGoal: {len(owngoal)}>', fontsize=12, highlight_textprops=[{'color':'orange'}], ax=ax)
            else:
                ax.text(64, -5.5, f'Goals: {len(goal)}', fontsize=12)
            ax.text(64, -10.5, f'Shots on Target: {len(ontr)}', fontsize=12)
            ax.text(64, -15.5, f'Shots off Target: {len(oftr)}', fontsize=12)
            ax.text(64, -20.5, f'TakeOn (Succ.): {len(takeOns)}', fontsize=12)
            ax.text(64, -25.5, f'TakeOn (Unsucc.): {len(takeOnu)}', fontsize=12)

            pitch.lines(-5, 34, -5, 24, color='gray', comet=True, lw=2, alpha=0.65, zorder=1, ax=ax)
            pitch.scatter(-5, 24, color=bg_color, ec='gray', s=20, zorder=2, ax=ax)
            pitch.lines(-10, 34, -10, 24, color=col2, comet=True, lw=3, zorder=2, ax=ax)
            pitch.scatter(-10, 24, color=bg_color, ec=col2, s=40, zorder=3, ax=ax)
            arrow = patches.FancyArrowPatch((34, -15), (23, -15), arrowstyle='->', color=col2, zorder=2, mutation_scale=20, 
                                                linewidth=2, linestyle='--')
            ax.add_patch(arrow)
            pitch.lines(-20, 34, -20, 24, color=violet, comet=True, lw=3.5, zorder=3, ax=ax)
            pitch.scatter(-20, 24, color=bg_color, ec=violet, s=50, lw=1.5, zorder=4, ax=ax)
            pitch.lines(-25, 34, -25, 24, color='green', comet=True, lw=4, zorder=4, ax=ax)
            pitch.scatter(-25, 24, color=bg_color, ec='green', s=60, lw=2, zorder=5, ax=ax)

            ax.text(21, -5.5, f'Successful Pass: {len(succ_passdf)}', fontsize=12)
            ax.text(21, -10.5, f'Porgressive Pass: {len(prg_pass)}', fontsize=12)
            ax.text(21, -15.5, f'Porgressive Carry: {len(prg_carry)}', fontsize=12)
            ax.text(21, -20.5, f'Key Passes: {len(cc)}', fontsize=12)
            ax.text(21, -25.5, f'Assists: {len(ga)}', fontsize=12)

            ax.text(34, 110, 'Offensive Actions', fontsize=20, fontweight='bold', ha='center', va='center')
            return
        

        def pass_receiving_and_touchmap(ax, pname):
            # Viz Dfs:
            playerdf = df[df['name']==pname]
            touch_df = playerdf[(playerdf['x']>0) & (playerdf['y']>0)]
            pass_rec = df[(df['type']=='Pass') & (df['outcomeType']=='Successful') & (df['name'].shift(-1)==pname)]
            # touch_df = pd.concat([acts_df, pass_rec], ignore_index=True)
            actual_touch = playerdf[playerdf['isTouch']==1]

            fthd_tch = actual_touch[actual_touch['x']>=70]
            penbox_tch = actual_touch[(actual_touch['x']>=88.5) & (actual_touch['y']>=13.6) & (actual_touch['y']<=54.4)]

            fthd_rec = pass_rec[pass_rec['endX']>=70]
            penbox_rec = pass_rec[(pass_rec['endX']>=88.5) & (pass_rec['endY']>=13.6) & (pass_rec['endY']<=54.4)]

            pitch = VerticalPitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2, pad_bottom=27)
            pitch.draw(ax=ax)

            ax.scatter(touch_df.y, touch_df.x, marker='o', s=30, c='None', edgecolor=col2, lw=2)
            if len(touch_df)>3:
                # Calculate mean point
                mean_point = np.mean(touch_df[['y', 'x']].values, axis=0)
                
                # Calculate distances from the mean point
                distances = np.linalg.norm(touch_df[['y', 'x']].values - mean_point[None, :], axis=1)
                
                # Compute the interquartile range (IQR)
                q1, q3 = np.percentile(distances, [20, 80])  # Middle 75%: 12.5th to 87.5th percentile
                iqr_mask = (distances >= q1) & (distances <= q3)
                
                # Filter points within the IQR
                points_within_iqr = touch_df[['y', 'x']].values[iqr_mask]
                
                # Check if we have enough points for a convex hull
                if len(points_within_iqr) >= 3:
                    hull = ConvexHull(points_within_iqr)
                    for simplex in hull.simplices:
                        ax.plot(points_within_iqr[simplex, 0], points_within_iqr[simplex, 1], color=col2, linestyle='--')
                    ax.fill(points_within_iqr[hull.vertices, 0], points_within_iqr[hull.vertices, 1], 
                            facecolor='none', edgecolor=col2, alpha=0.3, hatch='/////', zorder=1)
                else:
                    pass
            else:
                pass

            ax.scatter(pass_rec.endY, pass_rec.endX, marker='o', s=30, c='None', edgecolor=col1, lw=2)
            if len(touch_df)>4:
                # Calculate mean point
                mean_point = np.mean(pass_rec[['endY', 'endX']].values, axis=0)
                
                # Calculate distances from the mean point
                distances = np.linalg.norm(pass_rec[['endY', 'endX']].values - mean_point[None, :], axis=1)
                
                # Compute the interquartile range (IQR)
                q1, q3 = np.percentile(distances, [25, 75])  # Middle 75%: 12.5th to 87.5th percentile
                iqr_mask = (distances >= q1) & (distances <= q3)
                
                # Filter points within the IQR
                points_within_iqr = pass_rec[['endY', 'endX']].values[iqr_mask]
                
                # Check if we have enough points for a convex hull
                if len(points_within_iqr) >= 3:
                    hull = ConvexHull(points_within_iqr)
                    for simplex in hull.simplices:
                        ax.plot(points_within_iqr[simplex, 0], points_within_iqr[simplex, 1], color=col1, linestyle='--')
                    ax.fill(points_within_iqr[hull.vertices, 0], points_within_iqr[hull.vertices, 1], 
                            facecolor='none', edgecolor=col1, alpha=0.3, hatch='/////', zorder=1)
                else:
                    pass
            else:
                pass

            ax_text(34, 110, '<Touches> & <Pass Receiving> Points', fontsize=20, fontweight='bold', ha='center', va='center', 
                    highlight_textprops=[{'color':col2}, {'color':col1}])
            ax.text(34, -5, f'Total Touches: {len(actual_touch)} | at Final Third: {len(fthd_tch)} | at Penalty Box: {len(penbox_tch)}', color=col2, fontsize=13, ha='center', va='center')
            ax.text(34, -9, f'Total Pass Received: {len(pass_rec)} | at Final Third: {len(fthd_rec)} | at Penalty Box: {len(penbox_rec)}', color=col1, fontsize=13, ha='center', va='center')
            ax.text(34, -17, '*blue area = middle 75% touches area', color=col2, fontsize=13, fontstyle='italic', ha='center', va='center')
            ax.text(34, -21, '*red area = middle 75% pass receiving area', color=col1, fontsize=13, fontstyle='italic', ha='center', va='center')
            return
        

        def defensive_actions(ax, pname):
            # Viz Dfs:
            playerdf = df[df['name']==pname]
            tackles = playerdf[(playerdf['type']=='Tackle') & (playerdf['outcomeType']=='Successful')]
            tackleu = playerdf[(playerdf['type']=='Tackle') & (playerdf['outcomeType']=='Unsuccessful')]
            ballrec = playerdf[playerdf['type']=='BallRecovery']
            intercp = playerdf[playerdf['type']=='Interception']
            clearnc = playerdf[playerdf['type']=='Clearance']
            passbkl = playerdf[playerdf['type']=='BlockedPass']
            shotbkl = playerdf[playerdf['type']=='Save']
            chalnge = playerdf[playerdf['type']=='Challenge']
            aerialw = playerdf[(playerdf['type']=='Aerial') & (playerdf['outcomeType']=='Successful')]
            aerialu = playerdf[(playerdf['type']=='Aerial') & (playerdf['outcomeType']=='Unsuccessful')]

            # Pitch Plot
            pitch = VerticalPitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=line_color, linewidth=2, pad_bottom=27)
            pitch.draw(ax=ax)

            # Scatter Plots
            sns.scatterplot(x=tackles.y, y=tackles.x, marker='X', s=300, color=col2, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            sns.scatterplot(x=tackleu.y, y=tackleu.x, marker='X', s=300, color=col1, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            pitch.scatter(ballrec.x, ballrec.y, marker='o', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(intercp.x, intercp.y, marker='*', lw=1.25, s=600, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(clearnc.x, clearnc.y, marker='h', lw=1.5, s=400, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(passbkl.x, passbkl.y, marker='s', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(shotbkl.x, shotbkl.y, marker='s', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(chalnge.x, chalnge.y, marker='+', lw=5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(aerialw.x, aerialw.y, marker='^', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(aerialu.x, aerialu.y, marker='^', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)

            # Stats
            sns.scatterplot(x=[65], y=[-5], marker='X', s=300, color=col2, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            sns.scatterplot(x=[65], y=[-10], marker='X', s=300, color=col1, edgecolor=line_color, linewidth=1.5, alpha=0.8, ax=ax)
            pitch.scatter(-15, 65, marker='o', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-20, 65, marker='*', lw=1.25, s=600, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-25, 65, marker='h', lw=1.5, s=400, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            
            pitch.scatter(-5, 26, marker='s', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-10, 26, marker='s', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-15, 26, marker='+', lw=5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-20, 26, marker='^', lw=1.5, s=300, c=col2, edgecolors=line_color, ax=ax, alpha=0.8)
            pitch.scatter(-25, 26, marker='^', lw=1.5, s=300, c=col1, edgecolors=line_color, ax=ax, alpha=0.8)

            ax.text(60, -5.5, f'Tackle (Succ.): {len(tackles)}', fontsize=12)
            ax.text(60, -10.5, f'Tackle (Unsucc.): {len(tackleu)}', fontsize=12)
            ax.text(60, -15.5, f'Ball Recoveries: {len(ballrec)}', fontsize=12)
            ax.text(60, -20.5, f'Interceptions: {len(intercp)}', fontsize=12)
            ax.text(60, -25.5, f'Clearance: {len(clearnc)}', fontsize=12)

            ax.text(21, -5.5, f'Passes Blocked: {len(passbkl)}', fontsize=12)
            ax.text(21, -10.5, f'Shots Blocked: {len(shotbkl)}', fontsize=12)
            ax.text(21, -15.5, f'Dribble Past: {len(chalnge)}', fontsize=12)
            ax.text(21, -20.5, f'Aerials Won: {len(aerialw)}', fontsize=12)
            ax.text(21, -25.5, f'Aerials Lost: {len(aerialu)}', fontsize=12)

            ax.text(34, 110, 'Defensive Actions', fontsize=20, fontweight='bold', ha='center', va='center')
            return
        

        def generate_player_dahsboard(pname):
            fig, axs = plt.subplots(1, 3, figsize=(27, 17), facecolor='#f5f5f5')
            
            # Generate individual plots
            offensive_actions(axs[0], pname)
            defensive_actions(axs[1], pname)
            pass_receiving_and_touchmap(axs[2], pname)
            fig.subplots_adjust(wspace=0.025)
            
            # Add text and images to the figure
            fig.text(0.5, 0.995, pname, fontsize=34, fontweight='bold', ha='center', va='center', color='black')

            fig.text(0.14, 0.97, f'in {hteamName} {hgoal_count} - {agoal_count} {ateamName}', 
                    fontsize=30, ha='left', va='center')
            
            
            
            st.pyplot(fig)
            

        player_list = df['name'].unique().tolist()
        pname = st.selectbox('Select Player', player_list, index=0)
        generate_player_dahsboard(pname)