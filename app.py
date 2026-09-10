import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="中醫骨傷科病例追蹤", layout="wide")
st.title("病程與追蹤治療時序圖")

tab1, tab2 = st.tabs(["治療介入前 (時序圖)", "追蹤治療 (介入後)"])


def annotation_style(border_color, fill_color, **overrides):
    style = {
        "showarrow": False,
        "arrowhead": 1,
        "arrowcolor": "gray",
        "bordercolor": border_color,
        "bgcolor": fill_color,
        "font": {"size": 12, "color": "black"},
    }
    style.update(overrides)
    return style


yellow_anno = annotation_style("#D6B656", "#FFF2CC", font={"size": 12, "color": "black"})
blue_anno = annotation_style("#6C8EBF", "#DAE8FC")
gray_anno = annotation_style("#A6A6A6", "#F2F2F2", font={"size": 13, "color": "black"})

with tab1:
    st.subheader("治療介入前 - 病程時序與診斷")

    fig1 = go.Figure()
    x_pre = [0, 1, 2, 3]
    y_pre = [8, 9, 7, 8]

    fig1.add_trace(
        go.Scatter(
            x=x_pre,
            y=y_pre,
            mode="lines+markers+text",
            text=["<b>比賽受傷</b>", "<b>再比一場</b>", "<b>休息後</b>", "<b>門診就診</b>"],
            textposition="bottom center",
            textfont={"color": "#D62728", "size": 14},
            line={"color": "#D62728", "width": 3},
            marker={"size": 10},
            name="NRS 分數",
        )
    )

    fig1.add_annotation(x=0, y=7, text="右腳旋踢對手髂骨後，腳背疼痛<br>NRS達8分", **yellow_anno)
    fig1.add_annotation(x=1, y=7.9, text="右腳承重痛甚，走路時右腳拖行<br>無法上下樓梯<br>NRS增加為9分", **yellow_anno)
    fig1.add_annotation(x=2, y=6.2, text="休息後疼痛緩解至NRS 7分", **yellow_anno)

    clinic_text = (
        "<b>【07/13 門診評估】</b><br>"
        "• 中足腳背內側紅腫<br>"
        "• Ottawa Ankle Rules：陽性<br>"
        "• 內側楔形骨compression test(+)<br>"
        "• 針對楔形骨給上下剪力時疼痛，左右剪力也疼痛<br>"
        "• 腳踝ROM（Range Of Motion）測試 plantar flexion疼痛，<br>"
        "  dorsiflexion, inversion, eversion皆不痛<br>"
        "  ankle circumduction疼痛"
    )
    fig1.add_annotation(x=3, y=5.7, text=clinic_text, **blue_anno)

    imaging_text = (
        "<b>【07/13 影像檢查】</b><br>"
        "• 超音波檢查發現內側楔形附近瘀血，且骨邊不連續<br>"
        "• 進一步做X-ray檢查發現內側楔形骨輕微骨折(骨裂)"
    )
    fig1.add_annotation(x=3, y=3.0, text=imaging_text, **blue_anno)

    fig1.add_vline(x=2.5, line_width=1.5, line_dash="dash", line_color="gray", opacity=0.5)

    fig1.update_layout(
        height=600,
        margin={"t": 40, "b": 40},
        plot_bgcolor="#FAFAFA",
        xaxis={
            "tickmode": "array",
            "tickvals": [1, 3],
            "ticktext": ["<b>2026/07/12</b><br>(受傷當日)", "<b>2026/07/13</b><br>(初診日)"],
            "tickfont": {"size": 16},
            "showgrid": False,
        },
        yaxis={
            "title": "NRS 疼痛分數",
            "title_font": {"size": 16},
            "tickfont": {"size": 16},
            "range": [0, 10.5],
            "showgrid": True,
            "gridcolor": "lightgray",
        },
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("治療介入後 - 追蹤與 NRS 分數變化")

    fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])

    x_nrs = ["2026-07-13", "2026-07-15", "2026-07-20", "2026-07-21", "2026-07-28", "2026-07-29", "2026-07-31"]
    y_nrs = [8, 3.5, 3, 2, 7, 7, 4]

    fig2.add_trace(
        go.Scatter(
            x=x_nrs,
            y=y_nrs,
            mode="lines+markers",
            line={"color": "#C65911", "width": 3},
            marker={"symbol": "square", "size": 8},
            name="NRS 分數",
        ),
        row=1,
        col=1,
    )

    fig2.add_annotation(x="2026-07-13", y=8.7, text="NRS 8分<br>(冷熱交替浴結束消腫，剩5分)", row=1, col=1, **yellow_anno)
    fig2.add_annotation(x="2026-07-15", y=2.9, text="NRS 3.5分<br>腳踝可轉動，無法承重", row=1, col=1, **yellow_anno)
    fig2.add_annotation(x="2026-07-19 22:00", y=2.4, text="NRS 3分<br>可輕微承重，仍痛", row=1, col=1, ax=-20, ay=30, **yellow_anno)

    pe_0721 = "NRS 2分<br>可輕微承重，痛減<br>PE：中足腳背內側外觀無異常，<br>內側楔形骨compression test(+)；<br>針對楔形骨給上下或左右剪力時不痛；<br>腳踝ROM (Range Of Motion)<br>測試plantar flexion, dorsi flexion時疼痛，<br>inversion, eversion時不痛"
    fig2.add_annotation(x="2026-07-21 06:00", y=5, text=pe_0721, row=1, col=1, ax=50, ay=-130, **yellow_anno)

    fig2.add_annotation(x="2026-07-28", y=6.6, text="NRS 7分", row=1, col=1, ax=-20, ay=30, **yellow_anno)
    pe_0729 = "NRS 7分<br>PE：中足腳背內側稍腫，<br>Ottawa Ankle Rules(-)，<br>內側、中間楔形骨compression test(+)；<br>針對楔形骨給上下或左右剪力時不痛；<br>腳踝ROM (Range Of Motion)<br>測試plantar flexion, dorsi flexion時疼痛，<br>inversion, eversion時不痛"
    fig2.add_annotation(x="2026-07-29 08:00", y=8.8, text=pe_0729, row=1, col=1, ax=40, ay=-80, **yellow_anno)
    fig2.add_annotation(x="2026-07-31", y=3.6, text="NRS 4分", row=1, col=1, **yellow_anno)

    fig2.add_vrect(
        x0="2026-07-25",
        x1="2026-07-26",
        fillcolor="#B3B3B3",
        opacity=0.15,
        line_width=1,
        line_dash="dot",
        row=1,
        col=1,
    )
    fig2.add_annotation(x="2026-07-25 12:00", y=10, text="<b>跆拳道比賽兩日</b><br>Day 1: 中足腳背內側紅腫<br>Day 2: 症狀加劇", row=1, col=1, **gray_anno)

    fig2.add_trace(
        go.Scatter(
            x=["2026-07-13", "2026-07-31"],
            y=[0, 0],
            mode="lines",
            opacity=0,
            hoverinfo="skip",
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    fig2.add_shape(type="rect", x0="2026-07-13", x1="2026-07-31", y0=1.2, y1=1.8, fillcolor="#D5E8D4", line={"color": "white"}, opacity=0.8, row=2, col=1)
    fig2.add_annotation(x="2026-07-22", y=1.5, text="雷射針灸治療 (回診日施作)", showarrow=False, font={"size": 12, "color": "#274E13"}, row=2, col=1)

    fig2.add_shape(type="rect", x0="2026-07-13", x1="2026-07-15", y0=0.2, y1=0.8, fillcolor="#DAE8FC", line={"color": "white"}, opacity=0.8, row=2, col=1)
    fig2.add_annotation(x="2026-07-14", y=0.5, text="冷熱交替浴 (每日)", showarrow=False, font={"size": 12, "color": "#103667"}, row=2, col=1)

    fig2.add_shape(type="rect", x0="2026-07-16", x1="2026-07-31", y0=0.2, y1=0.8, fillcolor="#F8CECC", line={"color": "white"}, opacity=0.8, row=2, col=1)
    fig2.add_annotation(x="2026-07-23 12:00", y=0.5, text="泡熱水 (每日)", showarrow=False, font={"size": 12, "color": "#660000"}, row=2, col=1)

    fig2.update_layout(height=650, margin={"t": 40, "b": 40}, plot_bgcolor="white", showlegend=False)
    fig2.update_yaxes(title="NRS 分數", title_font=dict(size=16), range=[0, 10.5], showgrid=True, gridcolor="lightgray", row=1, col=1)
    fig2.update_yaxes(range=[0, 2], showgrid=False, showticklabels=False, zeroline=False, row=2, col=1)

    fig2.update_xaxes(
        tickmode="array",
        tickvals=["2026-07-13", "2026-07-14", "2026-07-15", "2026-07-16", "2026-07-17", "2026-07-18", "2026-07-19", "2026-07-20", "2026-07-21", "2026-07-22", "2026-07-23", "2026-07-24", "2026-07-25", "2026-07-26", "2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-07-31"],
        ticktext=["07/13", "07/14", "07/15", "07/16", "07/17", "07/18", "07/19", "07/20", "07/21", "07/22", "07/23", "07/24", "07/25", "07/26", "07/27", "07/28", "07/29", "07/30", "07/31"],
        range=["2026-07-12", "2026-08-01"],
        showgrid=True,
        gridcolor="lightgray",
        row=2,
        col=1,
    )

    st.plotly_chart(fig2, use_container_width=True)
