import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="中醫骨傷科病例追蹤", layout="wide")
st.title("病程與追蹤治療時序圖")

# 建立頁籤 (對應你要求的第三頁、第四頁)
tab1, tab2 = st.tabs(["治療介入前 (時序圖)", "追蹤治療 (介入後)"])

# 共用的註解方塊樣式
yellow_anno = dict(showarrow=True, arrowhead=1, arrowcolor="gray", bordercolor="#D6B656", bgcolor="#FFF2CC", font=dict(size=11, color="black"))
blue_anno = dict(showarrow=True, arrowhead=1, arrowcolor="gray", bordercolor="#6C8EBF", bgcolor="#DAE8FC", font=dict(size=11, color="black"))

# ==========================================
# 第三頁：治療介入前的時序圖 (更新 X 軸日期顯示)
# ==========================================
with tab1:
    st.subheader("治療介入前 - 病程時序與診斷")
    
    fig1 = go.Figure()
    
    # 將 X 軸改為數字索引 (0, 1, 2, 3)，確保點與點之間等距排列
    x_pre = [0, 1, 2, 3]
    y_pre = [8, 9, 7, 8] 
    
    # 畫出 NRS 變化線，並在點的下方加上「事件名稱」
    fig1.add_trace(go.Scatter(
        x=x_pre, y=y_pre, mode='lines+markers+text',
        text=['<b>比賽受傷</b>', '<b>再比一場</b>', '<b>休息後</b>', '<b>門診就診</b>'],
        textposition="bottom center",
        textfont=dict(color="#D62728", size=13),
        line=dict(color='#D62728', width=3), marker=dict(size=10), name='NRS 分數'
    ))
    
    # 加入各階段的黃色便利貼備註 (對應 x=0, 1, 2)
    fig1.add_annotation(x=0, y=8.3, text="右腳旋踢對手hip後，腳背疼痛<br>NRS達8分", **yellow_anno)
    fig1.add_annotation(x=1, y=9.3, text="右腳無法承重，走路時右腳拖行<br>無法上下樓梯<br>NRS增加為9分", **yellow_anno)
    fig1.add_annotation(x=2, y=7.3, text="休息後疼痛緩解至NRS 7分", **yellow_anno)
    
    # 07/13 的詳細門診與影像評估 (對應 x=3)
    clinic_text = (
        "<b>【07/13 門診評估】</b><br>"
        "• 中足腳背內側紅腫<br>"
        "• Ottawa Ankle Rules：陰性<br>"
        "• 內側楔形骨compression test(+)<br>"
        "• 針對楔形骨給上下剪力時疼痛，左右剪力也疼痛<br>"
        "• 腳踝ROM（Range Of Motion）測試plantar flexion疼痛，<br>"
        "  dorsi flexion, inversion, eversion皆不痛"
    )
    fig1.add_annotation(x=3, y=6.5, text=clinic_text, **blue_anno)
    
    imaging_text = (
        "<b>【07/13 影像檢查】</b><br>"
        "• 超音波檢查發現內側楔形附近瘀血，且骨邊不連續<br>"
        "• 進一步做X-ray檢查發現內側楔形骨輕微骨折(骨裂)"
    )
    
    blue_anno_no_arrow = dict(showarrow=False, arrowhead=1, arrowcolor="gray", bordercolor="#6C8EBF", bgcolor="#DAE8FC", font=dict(size=11, color="black"))

    
    # 因為沒有箭頭，方塊會直接置中於座標點。可以將 y 往下調一點避免跟上面的門診評估擠在一起
    #fig3.add_annotation(x='2026-07-13 09:00', y=2, text=imaging_text, **blue_anno_no_arrow)
    fig1.add_annotation(x=3, y=3.0, text=imaging_text, **blue_anno_no_arrow)
    
    # ★ 加上一條垂直虛線，將 07/12 與 07/13 視覺上切開
    fig1.add_vline(x=2.5, line_width=1.5, line_dash="dash", line_color="gray", opacity=0.5)

    fig1.update_layout(
        height=600, margin=dict(t=40, b=40), plot_bgcolor="#FAFAFA",
        # ★ 重新設定 X 軸，讓日期置中顯示，不再重複
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 3], # 1 是 07/12 三個事件的正中間，3 是 07/13
            ticktext=['<b>2026/07/12</b><br>(受傷當日)', '<b>2026/07/13</b><br>(初診日)'],
            tickfont=dict(size=14),
            showgrid=False # 關閉垂直網格線，讓畫面更乾淨
        ),
        yaxis=dict(title="NRS 疼痛分數", range=[0, 10.5], showgrid=True, gridcolor='lightgray')
    )
    st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# 第四頁：追蹤治療 (介入後) - 回復原本飄浮便利貼樣式
# ==========================================
with tab2:
    st.subheader("治療介入後 - 追蹤與 NRS 分數變化")
    
    fig2 = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.8, 0.2] 
    )
    
    x_nrs = ['2026-07-13', '2026-07-15', '2026-07-20', '2026-07-21', '2026-07-28', '2026-07-29', '2026-07-31']
    y_nrs = [8, 3.5, 3, 2, 7, 7, 4]
    
    # 1. 畫上層的折線圖
    fig2.add_trace(go.Scatter(
        x=x_nrs, y=y_nrs, mode='lines+markers',
        line=dict(color='#C65911', width=3), marker=dict(symbol='square', size=8), name='NRS 分數'
    ), row=1, col=1)
    
    # ==========================================
    # 2. 標註每次回診的臨床狀況 (拔掉硬梆梆的箭頭，回復懸浮設定)
    # ==========================================
    fig2.add_annotation(x='2026-07-13', y=8.5, text="NRS 8分<br>(冷熱交替浴結束消腫，剩5分)", row=1, col=1, **yellow_anno)
    fig2.add_annotation(x='2026-07-15', y=3.8, text="NRS 3.5分<br>腳踝可轉動，無法承重", row=1, col=1, **yellow_anno)
    
    # 07/20 移到下方 (設定在 y=1.5，讓便利貼自動浮在折線下方)
    fig2.add_annotation(x='2026-07-19 22:00', y=2.8, text="NRS 3分<br>可輕微承重，仍痛", row=1, col=1, ax=-20, ay=30, **yellow_anno)
    
    # 07/21 字很多，移到上方 (設定在 y=7.0，給它超大空間)
    pe_0721 = "NRS 2分<br>可輕微承重，痛減<br>PE：中足腳背內側外觀無異常，<br>Ottawa Ankle Rules(-)，<br>內側楔形骨compression test(+)；<br>針對楔形骨給上下或左右剪力時不痛；<br>腳踝ROM (Range Of Motion)<br>測試plantar flexion, dorsi flexion時疼痛，<br>inversion, eversion時不痛"
    fig2.add_annotation(x='2026-07-21 02:00', y=2.3, text=pe_0721, row=1, col=1, ax=50, ay=-130, **yellow_anno)

    fig2.add_annotation(x='2026-07-28', y=6.8, text="NRS 7分", row=1, col=1, ax=-20, ay=30, **yellow_anno)
    pe_0729 = "NRS 7分<br>PE：中足腳背內側稍腫，<br>Ottawa Ankle Rules(-)，<br>內側、中間楔形骨compression test(+)；<br>針對楔形骨給上下或左右剪力時不痛；<br>腳踝ROM (Range Of Motion)<br>測試plantar flexion, dorsi flexion時疼痛，<br>inversion, eversion時不痛"
    fig2.add_annotation(x='2026-07-29 02:00', y=7.3, text=pe_0729, row=1, col=1, ax=40, ay=-80, **yellow_anno)
    fig2.add_annotation(x='2026-07-31', y=4.5, text="NRS 4分", row=1, col=1, **yellow_anno)
    
    # 3. 關鍵事件：跆拳道比賽 (灰色陰影 + 灰色文字框)
    fig2.add_vrect(
        x0='2026-07-25', x1='2026-07-26', fillcolor="#B3B3B3", opacity=0.15, line_width=1, line_dash="dot",
        row=1, col=1
    )
    gray_anno = dict(showarrow=False, arrowhead=1, arrowcolor="gray", bordercolor="#A6A6A6", bgcolor="#F2F2F2", font=dict(size=11, color="black"))
    fig2.add_annotation(x='2026-07-25 12:00', y=10, text="<b>跆拳道比賽兩日</b><br>Day 1: 中足腳背內側紅腫<br>Day 2: 症狀加劇", row=1, col=1, **gray_anno)

    # 隱形軌道，強制啟動時間軸
    fig2.add_trace(go.Scatter(
        x=['2026-07-13', '2026-07-31'], y=[0, 0], 
        mode='lines', opacity=0, hoverinfo='skip', showlegend=False
    ), row=2, col=1)

    # 4. 底部治療橫條
    # 雷射針灸
    fig2.add_shape(type="rect", x0='2026-07-13', x1='2026-07-31', y0=1.2, y1=1.8, fillcolor="#D5E8D4", line=dict(color="white"), opacity=0.8, row=2, col=1)
    fig2.add_annotation(x='2026-07-22', y=1.5, text="雷射針灸治療 (回診日施作)", showarrow=False, font=dict(size=12, color="#274E13"), row=2, col=1)
    
    # 冷熱交替浴
    fig2.add_shape(type="rect", x0='2026-07-13', x1='2026-07-15', y0=0.2, y1=0.8, fillcolor="#DAE8FC", line=dict(color="white"), opacity=0.8, row=2, col=1)
    fig2.add_annotation(x='2026-07-14', y=0.5, text="冷熱交替浴", showarrow=False, font=dict(size=12, color="#103667"), row=2, col=1)
    
    # 泡熱水
    fig2.add_shape(type="rect", x0='2026-07-16', x1='2026-07-31', y0=0.2, y1=0.8, fillcolor="#F8CECC", line=dict(color="white"), opacity=0.8, row=2, col=1)
    fig2.add_annotation(x='2026-07-23 12:00', y=0.5, text="泡熱水 (每日)", showarrow=False, font=dict(size=12, color="#660000"), row=2, col=1)

    # 5. 版面與座標軸整理
    fig2.update_layout(
        height=650, margin=dict(t=40, b=40), 
        plot_bgcolor="white", 
        showlegend=False
    )
    
    fig2.update_yaxes(title="NRS 分數", range=[0, 10.5], showgrid=True, gridcolor='lightgray', row=1, col=1)
    fig2.update_yaxes(range=[0, 2], showgrid=False, showticklabels=False, zeroline=False, row=2, col=1)

    # 統一的 X 軸設定
    fig2.update_xaxes(
        tickmode='array',
        tickvals=['2026-07-13', '2026-07-15', '2026-07-16', '2026-07-20', '2026-07-21', '2026-07-25', '2026-07-26', '2026-07-28', '2026-07-29', '2026-07-31'],
        ticktext=['07/13', '07/15', '07/16', '07/20', '07/21', '07/25', '07/26', '07/28', '07/29', '07/31'],
        range=['2026-07-12', '2026-08-01'],
        showgrid=True, gridcolor='lightgray', row=2, col=1
    )

    st.plotly_chart(fig2, use_container_width=True)