"""
Pul Hisobchi - Loan & Deposit calculator (UZS)
Run locally:  streamlit run app.py
"""
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pul Hisobchi | Loan & Deposit Calculator",
    page_icon="💠",
    layout="wide",
)

TURQUOISE = "#2EC4B6"   # principal / deposits
SAFFRON = "#F2B84B"     # interest
INK = "#0C1424"
PANEL = "#131E35"
MUTED = "#8FA0C0"
TEXT = "#E8EDF7"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Plus Jakarta Sans', sans-serif;
}}
.stApp {{
    background:
        radial-gradient(900px 400px at 85% -10%, rgba(46,196,182,0.14), transparent 60%),
        radial-gradient(700px 400px at 0% 0%, rgba(242,184,75,0.08), transparent 55%),
        {INK};
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; max-width: 1200px; }}

.brand {{ display:flex; align-items:baseline; gap:14px; margin-bottom:4px; }}
.brand h1 {{ font-size:2.1rem; font-weight:800; letter-spacing:-0.02em; margin:0; color:{TEXT}; }}
.brand span {{ color:{TURQUOISE}; }}
.tagline {{ color:{MUTED}; margin-bottom:1.4rem; font-size:1rem; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 1px solid rgba(143,160,192,0.18); }}
.stTabs [data-baseweb="tab"] {{
    height: 46px; padding: 0 20px; border-radius: 12px 12px 0 0;
    color: {MUTED}; font-weight: 600;
}}
.stTabs [aria-selected="true"] {{ color: {TURQUOISE} !important; background: rgba(46,196,182,0.08); }}

/* Inputs */
.stNumberInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] > div {{
    background: {PANEL} !important; border-radius: 12px !important;
    border: 1px solid rgba(143,160,192,0.22) !important; color: {TEXT} !important;
    font-weight: 600;
}}
label, .stRadio label {{ color: {MUTED} !important; font-weight: 600 !important; }}

/* KPI cards */
.kpi {{
    background: {PANEL}; border: 1px solid rgba(143,160,192,0.16);
    border-radius: 18px; padding: 20px 22px; height: 100%;
}}
.kpi .label {{ color: {MUTED}; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px; }}
.kpi .value {{ color: {TEXT}; font-size: 1.55rem; font-weight: 800; letter-spacing: -0.01em; }}
.kpi .unit {{ color: {MUTED}; font-size: 0.85rem; font-weight: 600; margin-left: 6px; }}
.kpi .sub {{ color: {MUTED}; font-size: 0.8rem; margin-top: 6px; }}
.kpi.hero {{
    background: linear-gradient(135deg, {TURQUOISE} 0%, #1E9C93 100%);
    border: none;
}}
.kpi.hero .label, .kpi.hero .unit, .kpi.hero .sub {{ color: rgba(12,20,36,0.75); }}
.kpi.hero .value {{ color: {INK}; font-size: 1.9rem; }}
.kpi.gold .value {{ color: {SAFFRON}; }}

.chart-title {{ color:{TEXT}; font-weight:700; font-size:1.05rem; margin: 6px 0 -6px 4px; }}
.section-gap {{ height: 18px; }}
.note {{ color:{MUTED}; font-size:0.82rem; }}
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def fmt(x: float) -> str:
    """12 345 678 style number (Uzbek-friendly thousands separator)."""
    return f"{x:,.0f}".replace(",", " ")


def kpi(label: str, value: float, sub: str = "", style: str = "") -> str:
    return (
        f'<div class="kpi {style}">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{fmt(value)}<span class="unit">UZS</span></div>'
        f'<div class="sub">{sub}</div>'
        f"</div>"
    )


def kpi_text(label: str, value: str, sub: str = "", style: str = "") -> str:
    return (
        f'<div class="kpi {style}">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{value}</div>'
        f'<div class="sub">{sub}</div>'
        f"</div>"
    )


def style_fig(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(color=MUTED)),
        hoverlabel=dict(bgcolor=PANEL, font_color=TEXT),
    )
    fig.update_xaxes(showgrid=False, color=MUTED, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(143,160,192,0.12)", color=MUTED, zeroline=False)
    return fig


def donut(labels, values, colors, center_text):
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.64,
            marker=dict(colors=colors, line=dict(color=INK, width=3)),
            textinfo="percent",
            textfont=dict(color=INK, size=14),
            sort=False,
            hovertemplate="%{label}<br>%{value:,.0f} UZS<extra></extra>",
        )
    )
    fig.add_annotation(
        text=center_text, showarrow=False, font=dict(size=15, color=TEXT), align="center"
    )
    return style_fig(fig, 360)


def add_months(start: date, months: int) -> date:
    return (pd.Timestamp(start) + pd.DateOffset(months=months)).date()


# ----------------------------------------------------------------------------
# Calculations
# ----------------------------------------------------------------------------
def loan_schedule(principal: float, annual_rate: float, n: int, method: str, start: date) -> pd.DataFrame:
    r = annual_rate / 100 / 12
    balance = principal
    rows = []
    if method == "Annuity (equal payments)":
        pay = principal / n if r == 0 else principal * r / (1 - (1 + r) ** -n)
    for m in range(1, n + 1):
        interest = balance * r
        if method == "Annuity (equal payments)":
            princ = pay - interest
        else:  # differentiated
            princ = principal / n
        if m == n:
            princ = balance  # clear rounding dust
        payment = princ + interest
        balance = max(balance - princ, 0.0)
        rows.append(
            {
                "Month": m,
                "Date": add_months(start, m),
                "Payment": payment,
                "Principal": princ,
                "Interest": interest,
                "Balance": balance,
            }
        )
    return pd.DataFrame(rows)


COMPOUNDING = {
    "Monthly (compound)": 1,
    "Quarterly (compound)": 3,
    "Yearly (compound)": 12,
    "Simple (paid at the end)": None,
}


def deposit_schedule(initial: float, annual_rate: float, n: int, monthly_add: float, comp: str, start: date) -> pd.DataFrame:
    k = COMPOUNDING[comp]
    balance, accrued, deposited = initial, 0.0, initial
    rows = []
    for m in range(1, n + 1):
        if m > 1 and monthly_add > 0:  # top-up at the start of each month from month 2
            balance += monthly_add
            deposited += monthly_add
        accrued += balance * annual_rate / 100 / 12
        if (k and m % k == 0) or m == n:
            balance += accrued
            accrued = 0.0
        total = balance + accrued
        rows.append(
            {
                "Month": m,
                "Date": add_months(start, m),
                "Deposited": deposited,
                "Interest earned": total - deposited,
                "Balance": total,
            }
        )
    return pd.DataFrame(rows)


def duration_input(prefix: str, default_years: int = 1):
    c1, c2 = st.columns([2, 1])
    with c2:
        unit = st.radio("Unit", ["Years", "Months"], horizontal=True, key=f"{prefix}_unit")
    with c1:
        if unit == "Years":
            val = st.number_input("Duration", min_value=1, max_value=50, value=default_years, step=1, key=f"{prefix}_dur_y")
            return int(val) * 12, f"{val} year(s)"
        val = st.number_input("Duration", min_value=1, max_value=600, value=default_years * 12, step=1, key=f"{prefix}_dur_m")
        return int(val), f"{val} month(s)"


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="brand"><h1>Pul<span>Hisobchi</span></h1></div>'
    '<div class="tagline">Plan a loan or grow your savings. All amounts in Uzbek soum (UZS).</div>',
    unsafe_allow_html=True,
)

tab_loan, tab_dep = st.tabs(["Loan calculator", "Deposit calculator"])

# ----------------------------------------------------------------------------
# LOAN TAB
# ----------------------------------------------------------------------------
with tab_loan:
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        amount = st.number_input("Loan amount (UZS)", min_value=1_000_000, max_value=100_000_000_000,
                                 value=100_000_000, step=1_000_000, key="loan_amount")
    with b:
        rate = st.number_input("Interest rate (% per year)", min_value=0.0, max_value=200.0,
                               value=24.0, step=0.5, key="loan_rate")
    with c:
        n_months, dur_label = duration_input("loan", 3)

    d, e = st.columns([2, 1])
    with d:
        method = st.radio("Repayment type", ["Annuity (equal payments)", "Differentiated (decreasing payments)"],
                          horizontal=True, key="loan_method")
    with e:
        start = st.date_input("First month", value=date.today(), key="loan_start")

    df = loan_schedule(amount, rate, n_months, method, start)
    total_interest = df["Interest"].sum()
    total_paid = df["Payment"].sum()
    overpay_pct = total_interest / amount * 100

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    if method.startswith("Annuity"):
        k1.markdown(kpi("Monthly payment", df["Payment"].iloc[0], f"Same every month for {dur_label}", "hero"), unsafe_allow_html=True)
    else:
        k1.markdown(kpi("First monthly payment", df["Payment"].iloc[0],
                        f"Falls to {fmt(df['Payment'].iloc[-1])} UZS by the last month", "hero"), unsafe_allow_html=True)
    k2.markdown(kpi("Total interest", total_interest, f"{overpay_pct:.1f}% on top of the loan", "gold"), unsafe_allow_html=True)
    k3.markdown(kpi("Total you will pay", total_paid, "Loan + interest"), unsafe_allow_html=True)
    k4.markdown(kpi_text("Last payment", df["Date"].iloc[-1].strftime("%b %Y"), f"{n_months} payments in total"), unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    g1, g2 = st.columns([1, 1.4])
    with g1:
        st.markdown('<div class="chart-title">Where your money goes</div>', unsafe_allow_html=True)
        fig = donut(["Loan (principal)", "Interest"], [amount, total_interest], [TURQUOISE, SAFFRON],
                    f"{overpay_pct:.0f}%<br><span style='font-size:11px;color:{MUTED}'>extra cost</span>")
        st.plotly_chart(fig, width="stretch")
    with g2:
        st.markdown('<div class="chart-title">Principal vs interest in each payment</div>', unsafe_allow_html=True)
        if n_months <= 24:
            x = df["Month"].astype(str)
            p_vals, i_vals = df["Principal"], df["Interest"]
            xtitle = "Month"
        else:
            grp = df.assign(Year=(df["Month"] - 1) // 12 + 1).groupby("Year")[["Principal", "Interest"]].sum()
            x = grp.index.astype(str)
            p_vals, i_vals = grp["Principal"], grp["Interest"]
            xtitle = "Year"
        fig = go.Figure()
        fig.add_bar(x=x, y=p_vals, name="Principal", marker_color=TURQUOISE,
                    hovertemplate="%{y:,.0f} UZS<extra>Principal</extra>")
        fig.add_bar(x=x, y=i_vals, name="Interest", marker_color=SAFFRON,
                    hovertemplate="%{y:,.0f} UZS<extra>Interest</extra>")
        fig.update_layout(barmode="stack", bargap=0.25, xaxis_title=xtitle)
        st.plotly_chart(style_fig(fig), width="stretch")

    st.markdown('<div class="chart-title">Remaining debt over time</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_scatter(x=df["Date"], y=df["Balance"], mode="lines", name="Remaining debt",
                    line=dict(color=TURQUOISE, width=3), fill="tozeroy", fillcolor="rgba(46,196,182,0.15)",
                    hovertemplate="%{y:,.0f} UZS<extra></extra>")
    fig.add_scatter(x=df["Date"], y=df["Interest"].cumsum(), mode="lines", name="Interest paid so far",
                    line=dict(color=SAFFRON, width=3),
                    hovertemplate="%{y:,.0f} UZS<extra></extra>")
    st.plotly_chart(style_fig(fig, 340), width="stretch")

    with st.expander("Full payment schedule"):
        show = df.copy()
        for col in ["Payment", "Principal", "Interest", "Balance"]:
            show[col] = show[col].round(0).astype(int)
        st.dataframe(show, width="stretch", hide_index=True,
                     column_config={c: st.column_config.NumberColumn(c, format="%d")
                                    for c in ["Payment", "Principal", "Interest", "Balance"]})
        st.download_button("Download schedule (CSV)", show.to_csv(index=False).encode("utf-8"),
                           "loan_schedule.csv", "text/csv")
    st.markdown('<div class="note">This is an estimate. Banks may add fees or insurance and may count days slightly differently.</div>',
                unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# DEPOSIT TAB
# ----------------------------------------------------------------------------
with tab_dep:
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        initial = st.number_input("Deposit amount (UZS)", min_value=0, max_value=100_000_000_000,
                                  value=50_000_000, step=1_000_000, key="dep_amount")
    with b:
        d_rate = st.number_input("Interest rate (% per year)", min_value=0.0, max_value=200.0,
                                 value=20.0, step=0.5, key="dep_rate")
    with c:
        d_months, d_label = duration_input("dep", 1)

    d, e, f = st.columns(3)
    with d:
        monthly_add = st.number_input("Monthly top-up (UZS, optional)", min_value=0, max_value=10_000_000_000,
                                      value=0, step=500_000, key="dep_add")
    with e:
        comp = st.selectbox("Interest type", list(COMPOUNDING.keys()), key="dep_comp")
    with f:
        d_start = st.date_input("Start date", value=date.today(), key="dep_start")

    if initial == 0 and monthly_add == 0:
        st.info("Enter a deposit amount or a monthly top-up to see the results.")
    else:
        dd = deposit_schedule(initial, d_rate, d_months, monthly_add, comp, d_start)
        final = dd["Balance"].iloc[-1]
        put_in = dd["Deposited"].iloc[-1]
        earned = final - put_in
        yield_pct = earned / put_in * 100 if put_in else 0

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(kpi("You will have", final, f"After {d_label}", "hero"), unsafe_allow_html=True)
        k2.markdown(kpi("Interest earned", earned, f"{yield_pct:.1f}% total return", "gold"), unsafe_allow_html=True)
        k3.markdown(kpi("Money you put in", put_in, "Deposit + top-ups"), unsafe_allow_html=True)
        k4.markdown(kpi_text("Ends on", dd["Date"].iloc[-1].strftime("%d %b %Y"), f"{d_months} months in total"), unsafe_allow_html=True)

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        g1, g2 = st.columns([1, 1.4])
        with g1:
            st.markdown('<div class="chart-title">What you end up with</div>', unsafe_allow_html=True)
            fig = donut(["Your money", "Interest"], [put_in, max(earned, 0)], [TURQUOISE, SAFFRON],
                        f"{yield_pct:.0f}%<br><span style='font-size:11px;color:{MUTED}'>return</span>")
            st.plotly_chart(fig, width="stretch")
        with g2:
            st.markdown('<div class="chart-title">Growth over time</div>', unsafe_allow_html=True)
            if d_months <= 24:
                snap = dd.copy()
                snap["Label"] = "M" + snap["Month"].astype(str)
            else:
                snap = dd[(dd["Month"] % 12 == 0) | (dd["Month"] == d_months)].copy()
                snap["Label"] = snap["Month"].apply(lambda m: f"Year {m // 12}" if m % 12 == 0 else f"Month {m}")
            fig = go.Figure()
            fig.add_bar(x=snap["Label"], y=snap["Deposited"], name="Your money", marker_color=TURQUOISE,
                        hovertemplate="%{y:,.0f} UZS<extra>Your money</extra>")
            fig.add_bar(x=snap["Label"], y=snap["Interest earned"], name="Interest", marker_color=SAFFRON,
                        hovertemplate="%{y:,.0f} UZS<extra>Interest</extra>")
            fig.update_layout(barmode="stack", bargap=0.25)
            st.plotly_chart(style_fig(fig), width="stretch")

        st.markdown('<div class="chart-title">Balance month by month</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_scatter(x=dd["Date"], y=dd["Balance"], mode="lines", name="Total balance",
                        line=dict(color=TURQUOISE, width=3), fill="tozeroy", fillcolor="rgba(46,196,182,0.15)",
                        hovertemplate="%{y:,.0f} UZS<extra></extra>")
        fig.add_scatter(x=dd["Date"], y=dd["Deposited"], mode="lines", name="Money you put in",
                        line=dict(color=SAFFRON, width=2, dash="dot"),
                        hovertemplate="%{y:,.0f} UZS<extra></extra>")
        st.plotly_chart(style_fig(fig, 340), width="stretch")

        with st.expander("Full month-by-month table"):
            show = dd.copy()
            for col in ["Deposited", "Interest earned", "Balance"]:
                show[col] = show[col].round(0).astype(int)
            st.dataframe(show, width="stretch", hide_index=True,
                         column_config={c: st.column_config.NumberColumn(c, format="%d")
                                        for c in ["Deposited", "Interest earned", "Balance"]})
            st.download_button("Download table (CSV)", show.to_csv(index=False).encode("utf-8"),
                               "deposit_growth.csv", "text/csv")
        st.markdown('<div class="note">Top-ups are added at the start of each month from the second month. Taxes on interest are not included.</div>',
                    unsafe_allow_html=True)
