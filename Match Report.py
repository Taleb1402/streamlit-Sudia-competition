import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch
import arabic_reshaper
import arabic_reshaper
from bidi.algorithm import get_display
import seaborn as sns
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
from PIL import Image
import urllib
from scipy.ndimage import gaussian_filter
import matplotlib.patheffects as path_effects

plt.rcParams['font.family'] = 'Arial'
# حجم الصفحة: متوسط لعرض أوضح


# دالة مصفوفة التمريرات
import arabic_reshaper
from bidi.algorithm import get_display
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from mplsoccer import Pitch
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
from PIL import Image
import urllib

from PIL import Image
import base64
from io import BytesIO
green = '#69f900'
red = '#ff4b44'
blue = '#00a0de'
violet = '#a369ff'
bg_color= "#f5f5f5"
line_color= '#000000'
col1 = '#ff4b44'
col2 = '#00a0de'
# تحميل الشعار

import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="centered")
# 📝 وصف تحليلي بعد عرض الرسومات
st.markdown("""
<div style='background-color:#1a2a3a; padding:15px; border-radius:10px; font-size:16px; color:#f5f5f5;'>

🔍 **تحليل مرئي شامل للمباراة بين الفريقين**:
<ul>
<li>📊 <strong>خريطة الإحصائيات العامة:</strong> توضح المؤشرات الرئيسية مثل الاستحواذ، التمريرات، التدخلات، الضغط، والمواجهات الهوائية.</li>
<li>🎯 <strong>خريطة التسديدات:</strong> تعكس مواقع التسديدات الناجحة والخاطئة والفرص الكبيرة، موزعة حسب الفريق.</li>
<li>🥅 <strong>خريطة المرمى:</strong> تحليل مرئي لفرص التسجيل وجودة التسديدات في مواجهة المرمى.</li>
<li>📈 <strong>تحليل الزخم:</strong> يوضح فترات السيطرة الهجومية والتهديد من كل فريق طوال زمن المباراة.</li>
</ul>
</div>
""", unsafe_allow_html=True)
st.markdown("""
    ### 📌 مؤشر PPDA (عدد التمريرات المسموح بها قبل التدخل الدفاعي)
    هو مقياس يُستخدم لتحديد مدى قوة الضغط الذي يمارسه الفريق. كلما قل الرقم، كان الضغط أعلى وأسرع على الخصم.

    ---

    ### 📌 التمريرات لكل استحواذ
    هو متوسط عدد التمريرات التي يُجريها الفريق خلال كل مرة يملك فيها الكرة. رقم مرتفع يعني لعب هادئ وتحكم بالرتم، ورقم منخفض يدل على اللعب المباشر.

    ---

    ### 📌 سلاسل تمرير +10
    هو عدد المرات التي نفذ فيها الفريق سلسلة تمريرات متواصلة مكونة من 10 تمريرات أو أكثر. هذا يعكس قدرة الفريق على الحفاظ على الكرة وبناء اللعب بشكل منظم.
    """)
# تغيير الخلفية بالكامل إلى أخضر زيتي وتعديل الشريط الجانبي وغيره

# محتوى توضيحي في الوسط



# دالة مصفوفة التمريرات

# إدخال مسار الملف يدويًا

# Stats
...

# دالة شبكة التمريرات
# اختيار ألوان شبكة التمريرات
# حساب الأهداف الحقيقية والعكسية

# Stats
        
#Possession%


def plotting_match_stats(ax, df, hteamName, ateamName, col1, col2, bg_color, line_color):
    import matplotlib.patheffects as path_effects
    from mplsoccer import Pitch
    import arabic_reshaper
    from bidi.algorithm import get_display

    # دالة تعريب
    def ar(text):
        return get_display(arabic_reshaper.reshape(text))

    # possession
    hpossdf = df[(df['teamName'] == hteamName) & (df['type'] == 'Pass')]
    apossdf = df[(df['teamName'] == ateamName) & (df['type'] == 'Pass')]
    hposs = round((len(hpossdf) / (len(hpossdf) + len(apossdf))) * 100, 2)
    aposs = round((len(apossdf) / (len(hpossdf) + len(apossdf))) * 100, 2)

    # field tilt
    hftdf = df[(df['teamName'] == hteamName) & (df['isTouch'] == 1) & (df['endX'] >= 70)]
    aftdf = df[(df['teamName'] == ateamName) & (df['isTouch'] == 1) & (df['endX'] >= 70)]
    hft = round((len(hftdf) / (len(hftdf) + len(aftdf)) * 100), 2)
    aft = round((len(aftdf) / (len(hftdf) + len(aftdf)) * 100), 2)

    # passes
    htotalPass = len(hpossdf)
    atotalPass = len(apossdf)
    hpass_acc = len(hpossdf[hpossdf['outcomeType'] == 'Successful'])
    apass_acc = len(apossdf[apossdf['outcomeType'] == 'Successful'])

    # long balls
    hLongB = len(df[(df['teamName'] == hteamName) & (df['type_value_Long ball'] == 1)])
    aLongB = len(df[(df['teamName'] == ateamName) & (df['type_value_Long ball'] == 1)])
    hlong_acc = len(df[(df['teamName'] == hteamName) & (df['type_value_Long ball'] == 1) & (df['outcomeType'] == 'Successful')])
    along_acc = len(df[(df['teamName'] == ateamName) & (df['type_value_Long ball'] == 1) & (df['outcomeType'] == 'Successful')])

    # defense
    htkl = len(df[(df['teamName'] == hteamName) & (df['type'] == 'Tackle')])
    atkl = len(df[(df['teamName'] == ateamName) & (df['type'] == 'Tackle')])
    hintc = len(df[(df['teamName'] == hteamName) & (df['type'] == 'Interception')])
    aintc = len(df[(df['teamName'] == ateamName) & (df['type'] == 'Interception')])
    hclr = len(df[(df['teamName'] == hteamName) & (df['type'] == 'Clearance')])
    aclr = len(df[(df['teamName'] == ateamName) & (df['type'] == 'Clearance')])
    harl = len(df[(df['teamName'] == hteamName) & (df['type'] == 'Aerial')])
    aarl = len(df[(df['teamName'] == ateamName) & (df['type'] == 'Aerial')])

    # PPDA
    home_def_acts = df[(df['teamName'] == hteamName) & (df['type'].str.contains('Interception|Foul|Challenge|BlockedPass|Tackle')) & (df['x'] > 35)]
    away_def_acts = df[(df['teamName'] == ateamName) & (df['type'].str.contains('Interception|Foul|Challenge|BlockedPass|Tackle')) & (df['x'] > 35)]
    home_pass = df[(df['teamName'] == hteamName) & (df['type'] == 'Pass') & (df['x'] < 70)]
    away_pass = df[(df['teamName'] == ateamName) & (df['type'] == 'Pass') & (df['x'] < 70)]
    home_ppda = round((len(away_pass) / len(home_def_acts)), 2) if len(home_def_acts) > 0 else 0
    away_ppda = round((len(home_pass) / len(away_def_acts)), 2) if len(away_def_acts) > 0 else 0

    # Passes per sequence
    pass_counts_home = df[(df['type'] == 'Pass') & (df['teamName'] == hteamName)].groupby('possession_id').size()
    PPS_home = pass_counts_home.mean() if not pass_counts_home.empty else 0
    pass_counts_away = df[(df['type'] == 'Pass') & (df['teamName'] == ateamName)].groupby('possession_id').size()
    PPS_away = pass_counts_away.mean() if not pass_counts_away.empty else 0
    pass_seq_10_more_home = pass_counts_home[pass_counts_home >= 10].count()
    pass_seq_10_more_away = pass_counts_away[pass_counts_away >= 10].count()

    # الرسم
    path_eff1 = [path_effects.Stroke(linewidth=1.5, foreground=line_color), path_effects.Normal()]
    path_eff = [path_effects.Stroke(linewidth=3, foreground=bg_color), path_effects.Normal()]
    pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=bg_color, linewidth=2)
    pitch.draw(ax=ax)
    ax.set_xlim(-0.5, 105.5)
    ax.set_ylim(-5, 68.5)
    ax.fill([0, 0, 105, 105], [62, 68, 68, 62], 'orange')
    ax.text(52.5, 64.5, ar("إحصائيات المباراة"), ha='center', va='center', color=line_color, fontsize=25, fontweight='bold', path_effects=path_eff)

    # بيانات التطبيع
    stats_y = [58 - i * 6 for i in range(11)]
    stats_home = [hposs, hft, htotalPass, hLongB, htkl, hintc, hclr, harl, home_ppda, PPS_home, pass_seq_10_more_home]
    stats_away = [aposs, aft, atotalPass, aLongB, atkl, aintc, aclr, aarl, away_ppda, PPS_away, pass_seq_10_more_away]
    stats_home_norm = [-val / (val + stats_away[i]) * 50 if (val + stats_away[i]) != 0 else 0 for i, val in enumerate(stats_home)]
    stats_away_norm = [val / (val + stats_home[i]) * 50 if (val + stats_home[i]) != 0 else 0 for i, val in enumerate(stats_away)]

    ax.barh(stats_y, stats_home_norm, height=4, color=col1, left=52.5)
    ax.barh(stats_y, stats_away_norm, height=4, color=col2, left=52.5)

    # عناوين بالعربي
    stat_labels = [
        "الاستحواذ", "ميل الملعب", "التمريرات (الناجحة)", "الكرات الطويلة (الناجحة)",
        "الافتكاكات (الناجحة)", "الافتكاك بالتمركز", "التشتيت", "الثنائيات الهوائية",
        "مؤشر PPDA", "تمريرات/استحواذ", "سلاسل 10+ تمريرة"
    ]

    stats_home_raw = [
        f"{int(round(hposs))}%", f"{int(round(hft))}%", f"{htotalPass} ({hpass_acc})", f"{hLongB} ({hlong_acc})",
        int(htkl), int(hintc), int(hclr), int(harl),
        int(round(home_ppda)), int(round(PPS_home)), int(pass_seq_10_more_home)
    ]
    stats_away_raw = [
        f"{int(round(aposs))}%", f"{int(round(aft))}%", f"{atotalPass} ({apass_acc})", f"{aLongB} ({along_acc})",
        int(atkl), int(aintc), int(aclr), int(aarl),
        int(round(away_ppda)), int(round(PPS_away)), int(pass_seq_10_more_away)
    ]

    for y, label in zip(stats_y, stat_labels):
        ax.text(52.5, y, ar(label), color=bg_color, fontsize=17, ha='center', va='center', fontweight='bold', path_effects=path_eff1)

    for i, y in enumerate(stats_y):
        ax.text(0, y, f"{stats_home_raw[i]}", color=line_color, fontsize=17, ha='right', va='center', fontweight='bold')
        ax.text(105, y, f"{stats_away_raw[i]}", color=line_color, fontsize=17, ha='left', va='center', fontweight='bold')

    # تنفيذ خريطة التسديد والتحليل
def draw_shotmap_both_teams(df, hteamName, ateamName):
    import matplotlib.pyplot as plt
    import numpy as np
    from mplsoccer import Pitch
    import arabic_reshaper
    from bidi.algorithm import get_display

    def ar(text):
        return get_display(arabic_reshaper.reshape(text))

    

    # الأهداف
    hgoal_count = len(df[(df['possession_team'] == hteamName) & (df['type'] == 'Goal')])
    agoal_count = len(df[(df['possession_team'] == ateamName) & (df['type'] == 'Goal')])

    # التسديدات
    Shotsdf = df[df['type'].isin(['Goal', 'MissedShots', 'SavedShot', 'ShotOnPost'])].reset_index(drop=True)
    hShotsdf = Shotsdf[Shotsdf['possession_team'] == hteamName]
    aShotsdf = Shotsdf[Shotsdf['possession_team'] == ateamName]
    hSavedf = hShotsdf[hShotsdf['type'] == 'SavedShot']
    aSavedf = aShotsdf[aShotsdf['type'] == 'SavedShot']
    hogdf = hShotsdf[hShotsdf.get('isOwnGoal', False) == True]
    aogdf = aShotsdf[aShotsdf.get('isOwnGoal', False) == True]

    # المسافة المتوسطة
    given_point = (105, 34)
    home_average_shot_distance = round(np.sqrt((hShotsdf['x'] - given_point[0])**2 + (hShotsdf['y'] - given_point[1])**2).mean(), 2)
    away_average_shot_distance = round(np.sqrt((aShotsdf['x'] - given_point[0])**2 + (aShotsdf['y'] - given_point[1])**2).mean(), 2)

    # الفرص الكبيرة والضائعة
    hBigC = len(hShotsdf[hShotsdf['type_value_Big Chance'] == 214])
    aBigC = len(aShotsdf[aShotsdf['type_value_Big Chance'] == 214])
    hBigCmiss = len(hShotsdf[(hShotsdf['type_value_Big Chance'] == 214) & (hShotsdf['type'] != 'Goal')])
    aBigCmiss = len(aShotsdf[(aShotsdf['type_value_Big Chance'] == 214) & (aShotsdf['type'] != 'Goal')])

    # رسم الملعب
    fig, ax = plt.subplots(figsize=(16, 10))
    pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color="w", linewidth=2, line_color="black")
    pitch.draw(ax=ax)
    ax.set_ylim(-0.5, 68.5)
    ax.set_xlim(-0.5, 105.5)

    def plot_events(df, x_flip=False, color='#000000', size=200, marker='o', edge='black', fill='full', hatch=None, z=2):
        x = 105 - df['x'] if x_flip else df['x']
        y = 68 - df['y'] if x_flip else df['y']
        facecolor = color if fill == 'full' else 'None'
        return pitch.scatter(x, y, ax=ax, s=size, edgecolors=edge, c=facecolor, marker=marker, hatch=hatch, zorder=z)

    # الفريق الأول
    plot_events(hShotsdf[hShotsdf['type'] == 'Goal'], True, 'None', 350, 'football', 'green', 'none', None, 3)
    plot_events(hShotsdf[hShotsdf['type'] == 'MissedShots'], True, col1, 200, 'o', col1)
    plot_events(hShotsdf[hShotsdf['type'] == 'ShotOnPost'], True, col1, 200, 'o', col1)
    plot_events(hShotsdf[hShotsdf['type'] == 'SavedShot'], True, 'None', 200, 'o', col1, 'none', '///////')
    plot_events(hogdf, True, 'None', 350, '*', 'orange', 'none', None, 3)

    # الفريق الثاني
    plot_events(aShotsdf[aShotsdf['type'] == 'Goal'], False, 'None', 350, 'football', 'green', 'none', None, 3)
    plot_events(aShotsdf[aShotsdf['type'] == 'MissedShots'], False, col2, 200, 'o', col2)
    plot_events(aShotsdf[aShotsdf['type'] == 'ShotOnPost'], False, col2, 200, 'o', col2)
    plot_events(aShotsdf[aShotsdf['type'] == 'SavedShot'], False, 'None', 200, 'o', col2, 'none', '///////')
    plot_events(aogdf, False, 'None', 350, '*', 'orange', 'none', None, 3)

    def norm(val, total): return (val / total * 20) if total > 0 else 10

    hTotalShots = len(hShotsdf)
    aTotalShots = len(aShotsdf)
    hShotsOnT = len(hSavedf) + hgoal_count
    aShotsOnT = len(aSavedf) + agoal_count

    stats_y = [52, 45, 38, 31, 24, 17]
    stats_names = [
        ar("الأهداف"), ar("التسديدات"), ar("على المرمى"),
        ar("فرص كبيرة"), ar("فرص كبيرة ضائعة"), ar("متوسط المسافة")
    ]
    home_vals = [hgoal_count, hTotalShots, hShotsOnT, hBigC, hBigCmiss, home_average_shot_distance]
    away_vals = [agoal_count, aTotalShots, aShotsOnT, aBigC, aBigCmiss, away_average_shot_distance]

    home_norm = [norm(val, home_vals[i] + away_vals[i]) for i, val in enumerate(home_vals)]
    away_norm = [norm(val, home_vals[i] + away_vals[i]) for i, val in enumerate(away_vals)]

    start_x = 42.5
    ax.barh(stats_y, home_norm, height=5, color=col1, left=start_x)
    ax.barh(stats_y, away_norm, height=5, color=col2, left=[x + start_x for x in home_norm])

    for i, y in enumerate(stats_y):
        ax.text(52.5, y, stats_names[i], color="black", fontsize=14, ha='center', va='center', weight='bold')
        ax.text(41.5, y, f"{home_vals[i]}", color="black", fontsize=14, ha='right', va='center', weight='bold')
        ax.text(63.5, y, f"{away_vals[i]}", color="black", fontsize=14, ha='left', va='center', weight='bold')

    ax.text(0, 70, f"{hteamName}\n<---", color=col1, size=20, ha='left', fontweight='bold')
    ax.text(105, 70, f"{ateamName}\n--->", color=col2, size=20, ha='right', fontweight='bold')

    plt.tight_layout()
    return fig
# Goal Post Viz

# ShotMap
        

def plot_goalPost(ax, Shotsdf, hteamName, ateamName, col1, col2, bg_color, line_color):
            hShotsdf = Shotsdf[Shotsdf['teamName']==hteamName]
            aShotsdf = Shotsdf[Shotsdf['teamName']==ateamName]
            # converting the datapoints according to the pitch dimension, because the goalposts are being plotted inside the pitch using pitch's dimension
            hShotsdf['goalMouthZ_custom'] = hShotsdf['value_Goal mouth z coordinate']*0.75
            aShotsdf['goalMouthZ_custom'] = (aShotsdf['value_Goal mouth z coordinate']*0.75) + 38
        
            # hShotsdf['goalMouthY_custom'] = ((44 - hShotsdf['value_Goal mouth y coordinate'])*12.295) + 7.5
            # aShotsdf['goalMouthY_custom'] = ((44 - aShotsdf['value_Goal mouth y coordinate'])*12.295) + 7.5
        
            hShotsdf['goalMouthY_custom'] = ((55.5 - hShotsdf['value_Goal mouth y coordinate'])*8.5) + 7.5
            aShotsdf['goalMouthY_custom'] = ((55.5 - aShotsdf['value_Goal mouth y coordinate'])*8.5) + 7.5
        
            # plotting an invisible pitch using the pitch color and line color same color, because the goalposts are being plotted inside the pitch using pitch's dimension
            pitch = Pitch(pitch_type='uefa', corner_arcs=True, pitch_color=bg_color, line_color=bg_color, linewidth=2)
            pitch.draw(ax=ax)
            ax.set_ylim(-0.5,68.5)
            ax.set_xlim(-0.5,105.5)
            # ax.set_ylim(-200,200)
            # ax.set_xlim(-200,150)
        
            # away goalpost bars
            ax.plot([7.5, 7.5], [0, 30], color=line_color, linewidth=5)
            ax.plot([7.5, 97.5], [30, 30], color=line_color, linewidth=5)
            ax.plot([97.5, 97.5], [30, 0], color=line_color, linewidth=5)
            ax.plot([0, 105], [0, 0], color=line_color, linewidth=3)
            # plotting the away net
            y_values = np.arange(0, 6) * 6
            for y in y_values:
                ax.plot([7.5, 97.5], [y, y], color=line_color, linewidth=2, alpha=0.2)
            x_values = (np.arange(0, 11) * 9) + 7.5
            for x in x_values:
                ax.plot([x, x], [0, 30], color=line_color, linewidth=2, alpha=0.2)
            # home goalpost bars
            ax.plot([7.5, 7.5], [38, 68], color=line_color, linewidth=5)
            ax.plot([7.5, 97.5], [68, 68], color=line_color, linewidth=5)
            ax.plot([97.5, 97.5], [68, 38], color=line_color, linewidth=5)
            ax.plot([0, 105], [38, 38], color=line_color, linewidth=3)
            # plotting the home net
            y_values = (np.arange(0, 6) * 6) + 38
            for y in y_values:
                ax.plot([7.5, 97.5], [y, y], color=line_color, linewidth=2, alpha=0.2)
            x_values = (np.arange(0, 11) * 9) + 7.5
            for x in x_values:
                ax.plot([x, x], [38, 68], color=line_color, linewidth=2, alpha=0.2)
        
            # filtering different types of shots without BigChance
            hSavedf = hShotsdf[(hShotsdf['type']=='SavedShot') & (hShotsdf['type_value_Blocked']!=82) & (hShotsdf['type_value_Big Chance']!=214)]
            hGoaldf = hShotsdf[(hShotsdf['type']=='Goal') & (hShotsdf['type_value_Own goal']!=28) & (hShotsdf['type_value_Big Chance']!=214)]
            hPostdf = hShotsdf[(hShotsdf['type']=='ShotOnPost') & (hShotsdf['type_value_Big Chance']!=214)]
            aSavedf = aShotsdf[(aShotsdf['type']=='SavedShot') & (aShotsdf['type_value_Blocked']!=82) & (aShotsdf['type_value_Big Chance']!=214)]
            aGoaldf = aShotsdf[(aShotsdf['type']=='Goal') & (aShotsdf['type_value_Own goal']!=28) & (aShotsdf['type_value_Big Chance']!=214)]
            aPostdf = aShotsdf[(aShotsdf['type']=='ShotOnPost') & (aShotsdf['type_value_Big Chance']!=214)]
            # filtering different types of shots with BigChance
            hSavedf_bc = hShotsdf[(hShotsdf['type']=='SavedShot') & (hShotsdf['type_value_Blocked']!=82) & (hShotsdf['type_value_Big Chance']==214)]
            hGoaldf_bc = hShotsdf[(hShotsdf['type']=='Goal') & (hShotsdf['type_value_Own goal']!=28) & (hShotsdf['type_value_Big Chance']==214)]
            hPostdf_bc = hShotsdf[(hShotsdf['type']=='ShotOnPost') & (hShotsdf['type_value_Big Chance']==214)]
            aSavedf_bc = aShotsdf[(aShotsdf['type']=='SavedShot') & (aShotsdf['type_value_Blocked']!=82) & (aShotsdf['type_value_Big Chance']==214)]
            aGoaldf_bc = aShotsdf[(aShotsdf['type']=='Goal') & (aShotsdf['type_value_Own goal']!=28) & (aShotsdf['type_value_Big Chance']==214)]
            aPostdf_bc = aShotsdf[(aShotsdf['type']=='ShotOnPost') & (aShotsdf['type_value_Big Chance']==214)]
        
            # scattering those shots without BigChance
            sc1 = pitch.scatter(hSavedf.goalMouthY_custom, hSavedf.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolor=col2, hatch='/////', s=350, ax=ax)
            sc2 = pitch.scatter(hGoaldf.goalMouthY_custom, hGoaldf.goalMouthZ_custom, marker='football', c=bg_color, zorder=3, edgecolors='green', s=350, ax=ax)
            sc3 = pitch.scatter(hPostdf.goalMouthY_custom, hPostdf.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolors='orange', hatch='/////', s=350, ax=ax)
            sc4 = pitch.scatter(aSavedf.goalMouthY_custom, aSavedf.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolor=col1, hatch='/////', s=350, ax=ax)
            sc5 = pitch.scatter(aGoaldf.goalMouthY_custom, aGoaldf.goalMouthZ_custom, marker='football', c=bg_color, zorder=3, edgecolors='green', s=350, ax=ax)
            sc6 = pitch.scatter(aPostdf.goalMouthY_custom, aPostdf.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolors='orange', hatch='/////', s=350, ax=ax)
            # scattering those shots with BigChance
            sc1_bc = pitch.scatter(hSavedf_bc.goalMouthY_custom, hSavedf_bc.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolor=col2, hatch='/////', s=1000, ax=ax)
            sc2_bc = pitch.scatter(hGoaldf_bc.goalMouthY_custom, hGoaldf_bc.goalMouthZ_custom, marker='football', c=bg_color, zorder=3, edgecolors='green', s=1000, ax=ax)
            sc3_bc = pitch.scatter(hPostdf_bc.goalMouthY_custom, hPostdf_bc.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolors='orange', hatch='/////', s=1000, ax=ax)
            sc4_bc = pitch.scatter(aSavedf_bc.goalMouthY_custom, aSavedf_bc.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolor=col1, hatch='/////', s=1000, ax=ax)
            sc5_bc = pitch.scatter(aGoaldf_bc.goalMouthY_custom, aGoaldf_bc.goalMouthZ_custom, marker='football', c=bg_color, zorder=3, edgecolors='green', s=1000, ax=ax)
            sc6_bc = pitch.scatter(aPostdf_bc.goalMouthY_custom, aPostdf_bc.goalMouthZ_custom, marker='o', c=bg_color, zorder=3, edgecolors='orange', hatch='/////', s=1000, ax=ax)
        
            # Headlines and other texts
            ax.text(52.5, 70, f"{hteamName} GK saves", color=col1, fontsize=30, ha='center', fontweight='bold')
            ax.text(52.5, -2, f"{ateamName} GK saves", color=col2, fontsize=30, ha='center', va='top', fontweight='bold')
        
            ax.text(100, 68, f"Saves = {len(aSavedf)+len(aSavedf_bc)}",
                            color=col1, fontsize=16, va='top', ha='left')
            ax.text(100, 2, f"Saves = {len(hSavedf)+len(hSavedf_bc)}",
                            color=col2, fontsize=16, va='bottom', ha='left')
        
            return

##################################

def generate_and_plot_momentum(df, hteamName, ateamName, col1, col2, bg_color, line_color):
    u_df = df.copy()
    u_df = u_df[(u_df['type_value_Corner taken'] != 6)]
    u_df = u_df[['x', 'minute', 'period', 'type', 'teamName']]
    u_df = u_df[~u_df['type'].isin([
        'Start', 'OffsidePass', 'OffsideProvoked', 'Card', 'CornerAwarded', 'End',
        'OffsideGiven', 'SubstitutionOff', 'SubstitutionOn', 'FormationChange', 'FormationSet'
    ])].reset_index(drop=True)

    u_df.loc[u_df['teamName'] == ateamName, 'x'] = 105 - u_df.loc[u_df['teamName'] == ateamName, 'x']

    Momentumdf = u_df.groupby('minute')['x'].mean().reset_index()
    Momentumdf.columns = ['minute', 'average_x']
    Momentumdf['average_x'] -= 52.5

    u_df_1 = u_df[u_df['period'] == 'FirstHalf']
    u_df_2 = u_df[u_df['period'] == 'SecondHalf']

    Momentumdf1 = u_df_1.groupby('minute')['x'].mean().reset_index()
    Momentumdf1.columns = ['minute', 'average_x']
    Momentumdf1['average_x'] -= 52.5

    Momentumdf2 = u_df_2.groupby('minute')['x'].mean().reset_index()
    Momentumdf2.columns = ['minute', 'average_x']
    Momentumdf2['average_x'] -= 52.5

    def plot_Momentum(ax):
        colors1 = [col1 if x > 0 else col2 for x in Momentumdf1['average_x']]
        colors2 = [col1 if x > 0 else col2 for x in Momentumdf2['average_x']]

        homedf = df[df['teamName'] == hteamName]
        awaydf = df[df['teamName'] == ateamName]
        hxT = homedf['xT'].sum().round(2)
        axT = awaydf['xT'].sum().round(2)

        hgoal_list = homedf[(homedf['type'] == 'Goal') & (homedf['type_value_Own goal'] != 28)]['minute'].tolist()
        agoal_list = awaydf[(awaydf['type'] == 'Goal') & (awaydf['type_value_Own goal'] != 28)]['minute'].tolist()
        hog_list = homedf[(homedf['type'] == 'Goal') & (homedf['type_value_Own goal'] == 28)]['minute'].tolist()
        aog_list = awaydf[(awaydf['type'] == 'Goal') & (awaydf['type_value_Own goal'] == 28)]['minute'].tolist()

        highest_x = Momentumdf['average_x'].max()
        lowest_x = Momentumdf['average_x'].min()
        highest_minute = Momentumdf['minute'].max()
        hscatter_y = [highest_x] * len(hgoal_list)
        ascatter_y = [lowest_x] * len(agoal_list)
        hogscatter_y = [highest_x] * len(aog_list)
        aogscatter_y = [lowest_x] * len(hog_list)
        extra_time = Momentumdf1['minute'].max() - 45

        ax.text((45 / 2), lowest_x, 'First Half', color='gray', fontsize=20, alpha=0.25, va='center', ha='center')
        ax.text((45 + (45 / 2)), lowest_x, 'Second Half', color='gray', fontsize=20, alpha=0.25, va='center', ha='center')

        ax.scatter(hgoal_list, hscatter_y, s=250, c='None', edgecolor='green', hatch='////', marker='o')
        ax.scatter(agoal_list, ascatter_y, s=250, c='None', edgecolor='green', hatch='////', marker='o')
        ax.scatter(hog_list, aogscatter_y, s=250, c='None', edgecolor='orange', hatch='////', marker='o')
        ax.scatter(aog_list, hogscatter_y, s=250, c='None', edgecolor='orange', hatch='////', marker='o')

        ax.bar(Momentumdf1['minute'], Momentumdf1['average_x'], width=1, color=colors1)
        ax.bar(Momentumdf2['minute'] + extra_time, Momentumdf2['average_x'], width=1, color=colors2)

        ax.set_xticks(range(0, len(Momentumdf['minute']), 5))
        ax.axvline(45, color='gray', linewidth=2, linestyle='dotted')
        ax.set_facecolor(bg_color)
        for spine in ['top', 'right', 'left', 'bottom']:
            ax.spines[spine].set_visible(False)
        ax.tick_params(axis='both', which='both', length=0)
        ax.tick_params(axis='x', colors=line_color)
        ax.tick_params(axis='y', colors=bg_color)
        ax.set_xlabel('Minute', color=line_color, fontsize=20)
        ax.axhline(y=0, color=line_color, alpha=1, linewidth=2)
        ax.text(highest_minute + 1, highest_x, f"{hteamName}\nxT: {hxT}", color=col1, fontsize=20, va='bottom', ha='left')
        ax.text(highest_minute + 1, lowest_x, f"{ateamName}\nxT: {axT}", color=col2, fontsize=20, va='top', ha='left')
        ax.set_title('Match Momentum', color=line_color, fontsize=30, fontweight='bold')

    return plot_Momentum
 



import numpy as np
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

import numpy as np
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

def draw_static_passing_network(df_match, team_name, opponent_name,
                                bg_color='white', line_color='gray',
                                highlight_color='red', node_edge_color='b'):

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.colors import to_rgba
    from matplotlib.lines import Line2D
    from mplsoccer import Pitch

    df_match['pass_receiver'] = df_match.get('pass_recipient', np.where(
        (df_match['type'] == 'Pass') &
        (df_match['outcomeType'] == 'Successful') &
        (df_match['teamName'] == df_match['teamName'].shift(-1)),
        df_match['name'].shift(-1),
        np.nan
    ))
    df_match['pass_receiver'] = df_match['pass_receiver'].fillna('No')
    df_match['minute'] = df_match['minute'].astype(int)
    df_match['interval'] = pd.cut(
        df_match['minute'],
        bins=[0, 15, 30, 45, 60, 75, 90],
        labels=["0-15'", "15-30'", "30-45'", "45-60'", "60-75'", "75-90'"],
        right=False
    )

    interval_labels = ["0-15'", "15-30'", "30-45'", "45-60'", "60-75'", "75-90'"]
    subs_dict = df_match[(df_match['type'] == 'SubstitutionOn') & 
                         (df_match['teamName'] == team_name)][['name', 'minute']]
    subs_dict = dict(zip(subs_dict['name'], subs_dict['minute']))

    fig, axes = plt.subplots(2, 3, figsize=(24, 15), facecolor=bg_color)
    axes = axes.flatten()

    passes_team_all = df_match[
        (df_match['type'] == 'Pass') & 
        (df_match['outcomeType'] == 'Successful') & 
        (df_match['teamName'] == team_name)
    ]

    sent = passes_team_all['name'].value_counts()
    received = passes_team_all['pass_receiver'].value_counts()
    involvement = (sent + received).fillna(0).sort_values(ascending=False).head(5)
    top_involved_players = involvement.index.tolist()

    interval_comments = []

    for i, interval in enumerate(interval_labels):
        ax = axes[i]
        interval_max = int(interval.split('-')[1].replace("'", ""))

        if 'isFirstEleven' in df_match.columns:
            starting_players = df_match[
                (df_match['teamName'] == team_name) & 
                (df_match['isFirstEleven'] == True)
            ]['name'].unique().tolist()
        else:
            starting_players = df_match[
                (df_match['teamName'] == team_name) & 
                (df_match['minute'] <= 5)
            ]['name'].unique().tolist()

        substitutes_on = df_match[
            (df_match['teamName'] == team_name) & 
            (df_match['type'] == 'SubstitutionOn') & 
            (df_match['minute'] <= interval_max)
        ]['name'].tolist()

        valid_players = set(starting_players + substitutes_on)

        subs_off = df_match[
            (df_match['teamName'] == team_name) & 
            (df_match['type'] == 'SubstitutionOff') & 
            (df_match['minute'] <= interval_max)
        ]['name'].tolist()

        valid_players = valid_players - set(subs_off)
        valid_players = list(valid_players)

        pass_df_full = passes_team_all[(passes_team_all['interval'] == interval)]
        if pass_df_full.empty:
            ax.set_facecolor(bg_color)
            ax.set_title(interval, color=line_color)
            ax.axis('off')
            interval_comments.append(f"🕒 {interval}: لا توجد تمريرات في هذه الفترة.")
            continue

        pass_df = pass_df_full[['name', 'pass_receiver']].reset_index(drop=True)
        pass_counts_df = pass_df.groupby(['name', 'pass_receiver']).size().reset_index(name='pass_count')

        player_positions = df_match[
            (df_match['teamName'] == team_name) &
            (df_match['interval'] == interval)
        ].groupby('name')[['x', 'y']].median().rename(columns={'x': 'avg_x', 'y': 'avg_y'})

        top11 = df_match[
            (df_match['teamName'] == team_name) &
            (df_match['interval'] == interval)
        ]['name'].value_counts().head(11).index.tolist()

        avg_locs_df = pd.DataFrame({'name': top11})
        avg_locs_df = avg_locs_df.merge(player_positions, on='name', how='left')
        avg_locs_df['avg_x'] = avg_locs_df['avg_x'].fillna(60)
        avg_locs_df['avg_y'] = avg_locs_df['avg_y'].fillna(40)
        avg_locs_df['short_name'] = avg_locs_df['name'].apply(lambda x: ''.join([n[0] for n in str(x).split()]) if pd.notnull(x) else '')

        player_pass_counts = pass_counts_df.groupby('name')['pass_count'].sum().reset_index()
        player_pass_counts.rename(columns={'pass_count': 'total_passes'}, inplace=True)
        avg_locs_df = avg_locs_df.merge(player_pass_counts, on='name', how='left')
        avg_locs_df['total_passes'] = avg_locs_df['total_passes'].fillna(0)
        avg_locs_df['marker_size'] = avg_locs_df['total_passes'].apply(lambda x: 100 + 500 * np.log1p(x))

        pitch = Pitch(pitch_type='uefa', pitch_color=bg_color, line_color='black')
        pitch.draw(ax=ax)

        pass_counts_df = pd.merge(pass_counts_df, avg_locs_df, on='name', how='inner')
        pass_counts_df = pd.merge(pass_counts_df, avg_locs_df, left_on='pass_receiver', right_on='name',
                                  how='inner', suffixes=('', '_receiver'))

        pass_counts_df = pass_counts_df[pass_counts_df['pass_count'] >= 2]

        if not pass_counts_df.empty:
            pass_counts_df.rename(columns={'avg_x_receiver': 'receiver_avg_x', 'avg_y_receiver': 'receiver_avg_y'}, inplace=True)
            pass_counts_df['width'] = pass_counts_df.pass_count / pass_counts_df.pass_count.max() * 20
            top_pairs = pass_counts_df.sort_values(by='pass_count', ascending=False).head(5)
            top_pairs_list = list(zip(top_pairs['name'], top_pairs['pass_receiver']))
            colors = []

            for _, row in pass_counts_df.iterrows():
                if (row['name'], row['pass_receiver']) in top_pairs_list:
                    color_rgba = np.array(to_rgba(highlight_color)); color_rgba[3] = 0.9
                else:
                    color_rgba = np.array(to_rgba(line_color)); color_rgba[3] = 0.4
                colors.append(color_rgba)

            pitch.lines(pass_counts_df.avg_x, pass_counts_df.avg_y,
                        pass_counts_df.receiver_avg_x, pass_counts_df.receiver_avg_y,
                        lw=pass_counts_df.width, color=colors, zorder=2, ax=ax)

        for _, row in avg_locs_df.iterrows():
            marker = 's' if 0 < subs_dict.get(row['name'], 0) <= interval_max else 'o'
            fontsize = 14 if row['name'] in top_involved_players else 10
            pitch.scatter(row['avg_x'], row['avg_y'], s=row['marker_size'], marker=marker,
                          color=bg_color, edgecolor=node_edge_color, zorder=3, linewidth=2, ax=ax)
            pitch.annotate(row['short_name'], xy=(row.avg_x, row.avg_y), c='black',
                           ha='center', va='center', size=fontsize, ax=ax)

        ax.set_title(interval, fontsize=16, color='black', pad=10)

        if not pass_counts_df.empty:
            top_passes_text = "\n".join([
                f"{row['name']} → {row['pass_receiver']}: {row['pass_count']}" 
                for _, row in top_pairs.iterrows()
            ])
            ax.text(75, -10, top_passes_text, color='black', ha='right', va='center', fontsize=12)
            interval_comments.append(f"🕒 {interval}: عدد التمريرات >2: {len(pass_counts_df)} | أفضل ثنائي: {top_pairs.iloc[0]['name']} → {top_pairs.iloc[0]['pass_receiver']} ({top_pairs.iloc[0]['pass_count']})")
        else:
            interval_comments.append(f"🕒 {interval}: لم تتجاوز أي علاقة تمريرية الحد المطلوب (3 تمريرات).")

    fig.suptitle(f"{team_name} vs {opponent_name} - Passing Network by 15-Minute Intervals\n(Node Size = Pass Volume, Line Width = Pass Link)",
                 color='black', fontsize=20)

    # --- تدرج الحجم High → Low تحت العنوان ---
    legend_sizes = [100, 300, 600, 1000]
    legend_x_positions = [0.35, 0.42, 0.49, 0.56]

    for size, xpos in zip(legend_sizes, legend_x_positions):
        ax_circle = fig.add_axes([xpos, 0.88, 0.03, 0.06])
        ax_circle.set_xlim(0, 1)
        ax_circle.set_ylim(0, 1)
        ax_circle.axis('off')
        ax_circle.scatter(0.5, 0.5, s=size, facecolor='none', edgecolors=node_edge_color, linewidths=2)

    fig.text(0.34, 0.915, "Low pass count", color='black',
             ha='right', va='center', fontsize=15, fontweight='bold')

    fig.text(0.615, 0.915, "High pass count", color='black',
             ha='left', va='center', fontsize=15, fontweight='bold')

    
    
    
    fig.text(0.8, 0.035, "○ Starter | □ Substitute", color='black', ha='center', fontsize=30)

    line = Line2D([0.26, 0.36], [0.045, 0.045], color=highlight_color, linewidth=3, transform=fig.transFigure, figure=fig)
    fig.add_artist(line)
    fig.text(0.37, 0.043, "Top pass combinations by volume", color='black', fontsize=30, ha='left', va='center')
    
    fig.text(0.98, 0.01, '@Turadi_7', color='gray', fontsize=25, ha='right', va='bottom', style='italic')

    ai_comment = "### 🧠 تحليل AI لشبكة التمريرات:\n\n" + "\n\n".join(interval_comments)
    return fig, ai_comment

 





# دالة مصفوفة التمريرات


    

def draw_pass_matrix_arabic(df_match, team1, color_low='#b5ffe1', color_high='#ff8fab'):
    df_match['minute'] = df_match['minute'].astype(int)
    df_match['pass_receiver'] = np.where(
        (df_match['type'] == 'Pass') & 
        (df_match['outcomeType'] == 'Successful') & 
        (df_match['teamName'] == df_match['teamName'].shift(-1)),
        df_match['name'].shift(-1),
        np.nan
    )
    df_match['pass_receiver'] = df_match['pass_receiver'].fillna('No')

    passes_team1 = df_match[
        (df_match['type'] == 'Pass') &
        (df_match['outcomeType'] == 'Successful') &
        (df_match['teamName'] == team1) &
        (df_match['pass_receiver'] != 'No')
    ]
    matrix = passes_team1.groupby(['name', 'pass_receiver']).size().unstack(fill_value=0)

    matrix.index = matrix.index.map(lambda x: get_display(arabic_reshaper.reshape(x)))
    matrix.columns = matrix.columns.map(lambda x: get_display(arabic_reshaper.reshape(x)))

    # استخدام الألوان التي اخترتها
    custom_cmap = LinearSegmentedColormap.from_list("custom_map", [color_low, color_high])
    
    fig, ax = plt.subplots(figsize=(15, 13))
    sns.heatmap(matrix, annot=True, fmt="d", cmap=custom_cmap, cbar=True,
                linewidths=0.7, linecolor='gray', annot_kws={"fontsize": 10}, ax=ax)

    title_text = get_display(arabic_reshaper.reshape("خريطة التمريرات بين لاعبي الفريق"))
    xlabel = get_display(arabic_reshaper.reshape("اللاعب المستقبل"))
    ylabel = get_display(arabic_reshaper.reshape("اللاعب المرسل"))

    ax.set_title(title_text, fontsize=20)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)

    # عنوان علوي
    arabic_header = get_display(arabic_reshaper.reshape("مصفوفة التمريرات للفريق المختار"))
    fig.text(0.5, 0.98, arabic_header, ha='center', va='top', fontsize=18, fontweight='bold', color='black')

    # تحريك الرموز البصرية
    
        # ✅ تحليل AI بعد رسم المصفوفة
    total_passes = matrix.values.sum()
    top_pair = matrix.stack().idxmax()
    top_value = matrix.stack().max()

    comment = f"""
    ###  تعليق AI على مصفوفة التمريرات:

    - عدد التمريرات الكلي للفريق هو **{int(total_passes)}** تمريرة.
    - أكثر تمريرات بين لاعبين كانت من **{top_pair[0]}** إلى **{top_pair[1]}** بعدد **{int(top_value)}** تمريرة.
    - {"هناك توازن جيد بين اللاعبين." if matrix.values.std() < 5 else "هناك تفاوت واضح في توزيع التمريرات بين اللاعبين."}
    """
    
    return fig, comment
    

    



# واجهة التطبيق
# واجهة التطبيق في Streamlit
# ✅ خيارات الألوان للمصفوفة (يجب أن تكون قبل استدعاء الدالة)


# ✅ رفع الملف وتحديد الفريق

     
     # ✅ خيارات الألوان للمصفوفة (يجب أن تكون قبل استدعاء الدالة)



# ✅ خيارات الألوان للمصفوفة (يجب أن تكون قبل استدعاء الدالة)



# ✅ مشروع تحليل المباراة باستخدام Streamlit




# ✅ دالة تعريب النصوص
import os
import pandas as pd
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

# ✅ دالة تعريب النصوص
import os
import pandas as pd
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

# ✅ تعريب النصوص
import os
import pandas as pd
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

# ✅ تعريب النصوص
import os
import pandas as pd
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

# ✅ تعريب النصوص
import os
import pandas as pd
import streamlit as st
import arabic_reshaper
from bidi.algorithm import get_display

# ✅ تعريب النصوص (للرسومات فقط، وليس Streamlit)
def ar(text):
    return get_display(arabic_reshaper.reshape(text))

def reset_confirmed():
    st.session_state['confirmed'] = False

# 📁 تحميل البيانات
file_path = r"C:\Users\aalturaidi\OneDrive - Ittihad Club Company\Desktop\merged_events_with_competition_all.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # 🔍 تصحيح أسماء اللاعبين في حمل الكرة
    df.loc[
        (df['type'] == 'Carry') & (df['name'].isna()) & (df['playerId'] == df['playerId'].shift(-1)),
        'name'
    ] = df['name'].shift(-1)

    # ⚠️ معالجة الأهداف العكسية
    if 'type_value_Own goal' in df.columns:
        df['type_value_Own goal'] = pd.to_numeric(df['type_value_Own goal'], errors='coerce').fillna(0)
    else:
        df['type_value_Own goal'] = 0

    # ✅ إدخال اسم البطولة يدويًا إذا لم يكن موجودًا
    if 'competition' not in df.columns:
        st.warning("⚠️ لا يوجد عمود لاسم البطولة، يرجى إدخاله يدويًا")
        manual_comp = st.text_input("📌 أدخل اسم البطولة", value="Saudi Pro League")
        df['competition'] = manual_comp
    df['competition'] = df['competition'].astype(str).str.strip()

    # ✅ اختيار البطولة
    st.markdown("<h5 style='text-align: center;'>🏆 اختر اسم البطولة</h5>", unsafe_allow_html=True)
    competitions = sorted(df['competition'].dropna().unique().tolist())
    selected_competition = st.selectbox("", competitions, key="competition_select", on_change=reset_confirmed)
    df = df[df['competition'] == selected_competition].copy()

    # 🗂️ استخراج أعمدة الجولات
    week_columns = [col for col in df.columns if col.lower().startswith("week")]

    if week_columns:
        for col in week_columns:
            df[col] = df[col].replace('WEEK1', 1)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 🏷️ توليد team_vs
        if {'teamName', 'oppositionTeamName'}.issubset(df.columns):
            df['team_vs'] = df.apply(
                lambda row: " vs ".join(sorted([str(row['teamName']), str(row['oppositionTeamName'])])),
                axis=1
            )

        match_info_df = df.sort_values(by=['team_vs', 'minute']).drop_duplicates(subset='team_vs', keep='first')

        match_week_df = match_info_df.melt(
            id_vars=['team_vs'],
            value_vars=week_columns,
            var_name='Week',
            value_name='in_week'
        )

        available_weeks = match_week_df['Week'].unique().tolist()
        st.markdown("<h5 style='text-align: center;'>🗓️ اختر الجولة</h5>", unsafe_allow_html=True)
        selected_week = st.selectbox("", available_weeks, key="week_selection", on_change=reset_confirmed)

        matches_in_week = match_week_df[
            (match_week_df['Week'] == selected_week) & (match_week_df['in_week'] == 1)
        ]['team_vs'].unique().tolist()

        df = df[df['team_vs'].isin(matches_in_week)].copy()

        matches = sorted(df['team_vs'].dropna().unique().tolist())
        st.markdown("<h5 style='text-align: center;'>🌍 اختر المواجهة (الفريق ضد الفريق)</h5>", unsafe_allow_html=True)
        selected_match = st.selectbox("", matches, key="match_selectbox", on_change=reset_confirmed)

        if selected_match:
            df_match = df[df['team_vs'] == selected_match].copy()
            hteam, ateam = selected_match.split(" vs ")

            # 🏠 تحديد الفريقين المضيف والضيف
            if 'h_a' in df_match.columns:
                home_away_df = df_match.head(2)[['teamName', 'h_a']].sort_values(by='h_a').reset_index(drop=True)
                hteamName = home_away_df['teamName'][1]
                ateamName = home_away_df['teamName'][0]
            else:
                hteamName, ateamName = hteam, ateam

            homedf = df_match[df_match['teamName'] == hteamName]
            awaydf = df_match[df_match['teamName'] == ateamName]

            # ✅ اختيار الفريق للتحليل

            # ✅ مثال: تحليل شبكة التمريرات
            
           


# حفظ الكود الكامل الذي يتضمن:
# - خريطة التسديدات وتحليل الزخم
# - تحليل تمريرات فريق محدد
# - Heatmap وتمريرات لاعب

with st.expander("⚽️ خريطة التسديدات وتحليل الزخم للفريقين", expanded=True):
    col1 = st.color_picker("🎨 لون الفريق الأول", '#0099ff')
    col2 = st.color_picker("🎨 لون الفريق الثاني", '#ff4d4d')
    bg_color = st.color_picker("🎨 لون الخلفية", "#F2F3F3")
    line_color = st.color_picker("🎨 لون الخط", '#000000')

    if st.button("📊 عرض خريطة الاحصائيات والتسديدات وتحليل الزخم للفريقين"):
        try:
            # ✅ عرض خريطة التسديدات
            fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
            ax.set_facecolor('white')
            plotting_match_stats(ax, df_match, hteam, ateam, col1, col2, bg_color, line_color)
            st.pyplot(fig)

            fig = draw_shotmap_both_teams(df_match, hteam, ateam)
            st.pyplot(fig)

            # ✅ خريطة المرمى وتحليل فرص التسجيل
            st.subheader("🥅 خريطة المرمى وتحليل فرص التسجيل")
            Shotsdf = df_match[df_match['type'].isin(['Goal', 'SavedShot', 'ShotOnPost', 'MissedShots'])].reset_index(drop=True)
            fig2, ax2 = plt.subplots(figsize=(14, 8), facecolor=bg_color)
            plot_goalPost(ax2, Shotsdf, hteam, ateam, col1, col2, bg_color, line_color)
            st.pyplot(fig2)

            # ✅ تحليل الزخم
            st.subheader("📈 تحليل الزخم (Momentum) خلال المباراة")
            fig3, ax = plt.subplots(figsize=(12, 5), facecolor=bg_color)
            plot_momentum = generate_and_plot_momentum(df_match, hteam, ateam, col1, col2, bg_color, line_color)
            plot_momentum(ax)
            st.pyplot(fig3)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء عرض التحليلات: {e}")

with st.expander("🧠 تحليل تمريرات شيكة التمريرات فريق محدد"):
    selected_team = st.selectbox("🎯 اختر الفريق الذي ترغب في عرض تحليله", [hteam, ateam])
    matrix_color_low = st.color_picker("🔵 لون مصفوفة التمريرات (قيمة منخفضة)", '#b5ffe1')
    matrix_color_high = st.color_picker("🔴 لون مصفوفة التمريرات (قيمة مرتفعة)", '#ff8fab')
    line_color = st.color_picker("⚫ لون التمريرات العادية", '#808080')
    highlight_color = st.color_picker("🟡 لون التمريرات البارزة", '#ff0000')
    node_edge_color = st.color_picker("🟢 لون حواف الدوائر (اللاعبين)", '#00ccff')
    opponent = ateam if selected_team == hteam else hteam

    st.markdown(f"## 📊 تحليل المصفوفة: {selected_team}")
    fig_matrix, ai_comment = draw_pass_matrix_arabic(df_match, selected_team, matrix_color_low, matrix_color_high)
    st.pyplot(fig_matrix)
    st.markdown(ai_comment, unsafe_allow_html=True)

    st.markdown(f"## 🕸️ شبكة التمريرات: {selected_team}")
    fig_net, ai_comment_net = draw_static_passing_network(
        df_match, selected_team, opponent,
        line_color=line_color,
        highlight_color=highlight_color,
        node_edge_color=node_edge_color
    )
    st.pyplot(fig_net)
    st.markdown(ai_comment_net, unsafe_allow_html=True)


with st.expander("🔥 الخريطة الحرارية وتمريرات اللاعب المحدد", expanded=True):
    player_options = df_match[df_match['teamName'] == selected_team]['shortName'].dropna().unique().tolist()
    selected_player = st.selectbox("اختر اللاعب", player_options, key="heatmap_pass_player")

    if st.button("📊 عرض الخريطة الحرارية وتمريرات اللاعب المحدد"):
        player_data = df_match[
            (df_match['shortName'] == selected_player) & df_match['x'].notnull() & df_match['y'].notnull()
        ]

        if player_data.empty:
            st.warning(f"⚠️ لا توجد تحركات مسجلة للاعب: {selected_player}")
        else:
            # رسم Heatmap
            pitch = Pitch(pitch_type='uefa', pitch_color='#22312b', line_color='#efefef', line_zorder=2)
            fig, ax = pitch.draw(figsize=(10, 7))
            fig.set_facecolor('#22312b')
            ax.annotate(xy=(0.42, 0.001), xytext=(0.60, 0.001), text='',
                        arrowprops=dict(arrowstyle='<|-, head_length=0.2, head_width=0.12',
                                        linewidth=0.7, color='w', fc='#f2f2f2', zorder=4),
                        xycoords='axes fraction')
            ax.annotate(xy=(0.44, -0.031), text='Attacking direction', xycoords='axes fraction',
                        size=8.2, color='w', weight="bold")
            bin_statistic = pitch.bin_statistic(player_data.x, player_data.y, statistic='count', bins=(25, 25))
            bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], sigma=1.5)
            heatmap = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
            cbar = fig.colorbar(heatmap, ax=ax, shrink=0.6)
            cbar.outline.set_edgecolor('#efefef')
            cbar.ax.yaxis.set_tick_params(color='#efefef')
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#efefef')
            title = f"الخريطة الحرارية وتحليل تمريرات {selected_player}"
            ax.set_title(ar(title), fontsize=16, color='white', weight='bold')
            st.pyplot(fig)

            # خريطة تمريرات اللاعب
            st.markdown("📌 *خريطة تمريرات اللاعب*")
            player_passes = player_data[player_data['type'] == 'Pass']
            success = player_passes[player_passes['outcomeType'] == 'Successful']
            fail = player_passes[player_passes['outcomeType'] == 'Unsuccessful']
            label_success = ar("✅ تمريرات ناجحة")
            label_fail = ar("❌ تمريرات خاطئة")

            pitch = Pitch(pitch_type='uefa', pitch_color='white', line_color='black', line_zorder=2)
            fig2, ax2 = pitch.draw(figsize=(10, 7))
            ax2.annotate(xy=(0.42, 0.001), xytext=(0.60, 0.001), text='',
                         arrowprops=dict(arrowstyle='<|-, head_length=0.2, head_width=0.12',
                                         linewidth=0.7, color='black', fc='black', zorder=4),
                         xycoords='axes fraction')
            ax2.annotate(xy=(0.44, -0.015), text='Attacking direction', xycoords='axes fraction',
                         size=8.2, color='black', weight="bold")
            pitch.arrows(success['x'], success['y'], success['endX'], success['endY'],
                         ax=ax2, color='green', width=2, headwidth=3, label=label_success)
            pitch.arrows(fail['x'], fail['y'], fail['endX'], fail['endY'],
                         ax=ax2, color='red', width=2, headwidth=3, alpha=0.6, label=label_fail)

            ax2.set_title(ar(f"تحليل تمريرات {selected_player}"), fontsize=14, weight='bold')
            total_passes = len(player_passes)
            successful_passes = len(success)
            failed_passes = len(fail)
            accuracy = (successful_passes / total_passes * 100) if total_passes > 0 else 0
            stats_text = f"✅ عدد التمريرات الناجحة: {successful_passes}    ❌ الخاطئة: {failed_passes}    📊 المجموع: {total_passes}    🎯 الدقة: {accuracy:.1f}%"
            ax2.text(0.5, 0.97, ar(stats_text), transform=ax2.transAxes,
                     ha='center', va='bottom', fontsize=11, color='black', fontweight='bold')
            ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), ncol=2, fontsize=12,
                       frameon=False, handlelength=2.5)
            st.pyplot(fig2)



              

            #