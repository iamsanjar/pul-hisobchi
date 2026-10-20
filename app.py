"""
Pul Hisobchi - Loan & Deposit calculator (UZS)
Languages: O'zbekcha / English / Русский
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

# ----------------------------------------------------------------------------
# Translations
# ----------------------------------------------------------------------------
LANGS = {"O'zbekcha": "uz", "English": "en", "Русский": "ru"}

TR = {
    "en": {
        "tagline": "Plan a loan or grow your savings. All amounts in Uzbek soum (UZS).",
        "tab_loan": "Loan calculator",
        "tab_dep": "Deposit calculator",
        "loan_amount": "Loan amount (UZS)",
        "rate": "Interest rate (% per year)",
        "duration": "Duration",
        "unit": "Unit",
        "u_years": "Years",
        "u_months": "Months",
        "repay_type": "Repayment type",
        "annuity": "Annuity (equal payments)",
        "diff": "Differentiated (decreasing payments)",
        "first_month": "First month",
        "monthly_payment": "Monthly payment",
        "first_payment": "First monthly payment",
        "same_every": "Same every month for {dur}",
        "falls_to": "Falls to {x} UZS by the last month",
        "total_interest": "Total interest",
        "on_top": "{p}% on top of the loan",
        "total_pay": "Total you will pay",
        "loan_plus_int": "Loan + interest",
        "last_payment": "Last payment",
        "n_payments": "{n} payments in total",
        "chart_where": "Where your money goes",
        "loan_principal": "Loan (principal)",
        "interest": "Interest",
        "extra_cost": "extra cost",
        "chart_each": "Principal vs interest in each payment",
        "principal": "Principal",
        "month": "Month",
        "year": "Year",
        "chart_remaining": "Remaining debt over time",
        "remaining_debt": "Remaining debt",
        "interest_so_far": "Interest paid so far",
        "full_schedule": "Full payment schedule",
        "dl_schedule": "Download schedule (CSV)",
        "note_loan": "This is an estimate. Banks may add fees or insurance and may count days slightly differently.",
        "payment": "Payment",
        "balance": "Balance",
        "date": "Date",
        "deposited": "Deposited",
        "interest_earned": "Interest earned",
        "dep_amount": "Deposit amount (UZS)",
        "monthly_topup": "Monthly top-up (UZS, optional)",
        "interest_type": "Interest type",
        "comp_monthly": "Monthly (compound)",
        "comp_quarterly": "Quarterly (compound)",
        "comp_yearly": "Yearly (compound)",
        "comp_simple": "Simple (paid at the end)",
        "start_date": "Start date",
        "enter_hint": "Enter a deposit amount or a monthly top-up to see the results.",
        "you_will_have": "You will have",
        "after_dur": "After {dur}",
        "interest_earned_kpi": "Interest earned",
        "total_return": "{p}% total return",
        "money_in": "Money you put in",
        "dep_plus_topups": "Deposit + top-ups",
        "ends_on": "Ends on",
        "months_total": "{n} months in total",
        "chart_end": "What you end up with",
        "your_money": "Your money",
        "return_word": "return",
        "chart_growth": "Growth over time",
        "year_label": "Year {n}",
        "month_label": "Month {n}",
        "chart_balance": "Balance month by month",
        "total_balance": "Total balance",
        "put_in_line": "Money you put in",
        "full_table": "Full month-by-month table",
        "dl_table": "Download table (CSV)",
        "note_dep": "Top-ups are added at the start of each month from the second month. Taxes on interest are not included.",
    },
    "uz": {
        "tagline": "Kreditni rejalashtiring yoki jamg'armangizni o'stiring. Barcha summalar so'mda (UZS).",
        "tab_loan": "Kredit kalkulyatori",
        "tab_dep": "Omonat kalkulyatori",
        "loan_amount": "Kredit summasi (UZS)",
        "rate": "Foiz stavkasi (yillik, %)",
        "duration": "Muddat",
        "unit": "Birlik",
        "u_years": "Yillar",
        "u_months": "Oylar",
        "repay_type": "To'lov turi",
        "annuity": "Annuitet (teng to'lovlar)",
        "diff": "Differensial (kamayib boruvchi to'lovlar)",
        "first_month": "Birinchi oy",
        "monthly_payment": "Oylik to'lov",
        "first_payment": "Birinchi oylik to'lov",
        "same_every": "Har oy bir xil, muddat: {dur}",
        "falls_to": "Oxirgi oyga kelib {x} UZS gacha kamayadi",
        "total_interest": "Jami foiz",
        "on_top": "Kreditdan {p}% ortiq",
        "total_pay": "Jami to'laysiz",
        "loan_plus_int": "Kredit + foiz",
        "last_payment": "Oxirgi to'lov",
        "n_payments": "Jami {n} ta to'lov",
        "chart_where": "Pulingiz qayerga ketadi",
        "loan_principal": "Kredit (asosiy qarz)",
        "interest": "Foiz",
        "extra_cost": "qo'shimcha xarajat",
        "chart_each": "Har bir to'lovda asosiy qarz va foiz",
        "principal": "Asosiy qarz",
        "month": "Oy",
        "year": "Yil",
        "chart_remaining": "Qolgan qarz vaqt bo'yicha",
        "remaining_debt": "Qolgan qarz",
        "interest_so_far": "Hozirgacha to'langan foiz",
        "full_schedule": "To'liq to'lov jadvali",
        "dl_schedule": "Jadvalni yuklab olish (CSV)",
        "note_loan": "Bu taxminiy hisob. Banklar komissiya yoki sug'urta qo'shishi va kunlarni biroz boshqacha hisoblashi mumkin.",
        "payment": "To'lov",
        "balance": "Qoldiq",
        "date": "Sana",
        "deposited": "Kiritilgan",
        "interest_earned": "Topilgan foiz",
        "dep_amount": "Omonat summasi (UZS)",
        "monthly_topup": "Oylik to'ldirish (UZS, ixtiyoriy)",
        "interest_type": "Foiz turi",
        "comp_monthly": "Oylik (murakkab)",
        "comp_quarterly": "Choraklik (murakkab)",
        "comp_yearly": "Yillik (murakkab)",
        "comp_simple": "Oddiy (oxirida to'lanadi)",
        "start_date": "Boshlanish sanasi",
        "enter_hint": "Natijani ko'rish uchun omonat summasi yoki oylik to'ldirish miqdorini kiriting.",
        "you_will_have": "Sizda bo'ladi",
        "after_dur": "{dur} dan keyin",
        "interest_earned_kpi": "Topilgan foiz",
        "total_return": "Jami daromad {p}%",
        "money_in": "Siz kiritgan pul",
        "dep_plus_topups": "Omonat + to'ldirishlar",
        "ends_on": "Tugash sanasi",
        "months_total": "Jami {n} oy",
        "chart_end": "Oxirida nima olasiz",
        "your_money": "Sizning pulingiz",
        "return_word": "daromad",
        "chart_growth": "Vaqt bo'yicha o'sish",
        "year_label": "{n}-yil",
        "month_label": "{n}-oy",
        "chart_balance": "Oyma-oy balans",
        "total_balance": "Umumiy balans",
        "put_in_line": "Siz kiritgan pul",
        "full_table": "To'liq oyma-oy jadval",
        "dl_table": "Jadvalni yuklab olish (CSV)",
        "note_dep": "To'ldirishlar ikkinchi oydan boshlab har oy boshida qo'shiladi. Foizdan olinadigan soliqlar hisobga olinmagan.",
    },
    "ru": {
        "tagline": "Спланируйте кредит или приумножьте накопления. Все суммы в узбекских сумах (UZS).",
        "tab_loan": "Кредитный калькулятор",
        "tab_dep": "Калькулятор вклада",
        "loan_amount": "Сумма кредита (UZS)",
        "rate": "Процентная ставка (годовая, %)",
        "duration": "Срок",
        "unit": "Единица",
        "u_years": "Годы",
        "u_months": "Месяцы",
        "repay_type": "Тип платежей",
        "annuity": "Аннуитетный (равные платежи)",
        "diff": "Дифференцированный (уменьшающиеся платежи)",
        "first_month": "Первый месяц",
        "monthly_payment": "Ежемесячный платёж",
        "first_payment": "Первый ежемесячный платёж",
        "same_every": "Одинаковый каждый месяц, срок: {dur}",
        "falls_to": "К последнему месяцу снижается до {x} UZS",
        "total_interest": "Всего процентов",
        "on_top": "{p}% сверх суммы кредита",
        "total_pay": "Всего к выплате",
        "loan_plus_int": "Кредит + проценты",
        "last_payment": "Последний платёж",
        "n_payments": "Всего платежей: {n}",
        "chart_where": "Куда уходят ваши деньги",
        "loan_principal": "Кредит (основной долг)",
        "interest": "Проценты",
        "extra_cost": "переплата",
        "chart_each": "Основной долг и проценты в каждом платеже",
        "principal": "Основной долг",
        "month": "Месяц",
        "year": "Год",
        "chart_remaining": "Остаток долга со временем",
        "remaining_debt": "Остаток долга",
        "interest_so_far": "Выплачено процентов на сегодня",
        "full_schedule": "Полный график платежей",
        "dl_schedule": "Скачать график (CSV)",
        "note_loan": "Это приблизительный расчёт. Банки могут добавлять комиссии или страховку и считать дни немного иначе.",
        "payment": "Платёж",
        "balance": "Остаток",
        "date": "Дата",
        "deposited": "Внесено",
        "interest_earned": "Начислено процентов",
        "dep_amount": "Сумма вклада (UZS)",
        "monthly_topup": "Ежемесячное пополнение (UZS, необязательно)",
        "interest_type": "Тип процентов",
        "comp_monthly": "Ежемесячная капитализация",
        "comp_quarterly": "Ежеквартальная капитализация",
        "comp_yearly": "Ежегодная капитализация",
        "comp_simple": "Простые проценты (в конце срока)",
        "start_date": "Дата начала",
        "enter_hint": "Введите сумму вклада или ежемесячное пополнение, чтобы увидеть результат.",
        "you_will_have": "У вас будет",
        "after_dur": "Через {dur}",
        "interest_earned_kpi": "Начислено процентов",
        "total_return": "Общая доходность {p}%",
        "money_in": "Ваши вложения",
        "dep_plus_topups": "Вклад + пополнения",
        "ends_on": "Дата окончания",
        "months_total": "Всего месяцев: {n}",
        "chart_end": "Что вы получите в итоге",
        "your_money": "Ваши деньги",
        "return_word": "доходность",
        "chart_growth": "Рост со временем",
        "year_label": "Год {n}",
        "month_label": "Месяц {n}",
        "chart_balance": "Баланс по месяцам",
        "total_balance": "Общий баланс",
        "put_in_line": "Ваши вложения",
        "full_table": "Полная таблица по месяцам",
        "dl_table": "Скачать таблицу (CSV)",
        "note_dep": "Пополнения добавляются в начале каждого месяца, начиная со второго. Налоги на проценты не учтены.",
    },
}

MONTH_NAMES = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "uz": ["yan", "fev", "mar", "apr", "may", "iyun", "iyul", "avg", "sen", "okt", "noy", "dek"],
    "ru": ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"],
}

# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
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
# Language switch (top right) + header
# ----------------------------------------------------------------------------
head_left, head_right = st.columns([3, 1.6])
with head_right:
    choice = st.segmented_control(
        "Language",
        options=list(LANGS.keys()),
        selection_mode="single",
        default="English",
        key="lang",
        label_visibility="collapsed",
    )
LANG = LANGS.get(choice or "English", "en")


def t(key: str, **kw) -> str:
    text = TR[LANG][key]
    return text.format(**kw) if kw else text


with head_left:
    st.markdown(
        '<div class="brand"><h1>Pul<span>Hisobchi</span></h1></div>'
        f'<div class="tagline">{t("tagline")}</div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def fmt(x: float) -> str:
    """12 345 678 style number (Uzbek-friendly thousands separator)."""
    return f"{x:,.0f}".replace(",", " ")


def fmt_month_year(d: date) -> str:
    return f"{MONTH_NAMES[LANG][d.month - 1]} {d.year}"


def fmt_full_date(d: date) -> str:
    return f"{d.day} {MONTH_NAMES[LANG][d.month - 1]} {d.year}"


def ru_plural(n: int, forms: tuple) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return forms[0]
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return forms[1]
    return forms[2]


def dur_text(n: int, kind: str) -> str:
    """'3 years', '3 yil', '3 года' ... kind is 'y' or 'm'."""
    if LANG == "uz":
        return f"{n} {'yil' if kind == 'y' else 'oy'}"
    if LANG == "ru":
        forms = ("год", "года", "лет") if kind == "y" else ("месяц", "месяца", "месяцев")
        return f"{n} {ru_plural(n, forms)}"
    word = "year" if kind == "y" else "month"
    return f"{n} {word}{'' if n == 1 else 's'}"


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
# Calculations (language independent)
# ----------------------------------------------------------------------------
def loan_schedule(principal: float, annual_rate: float, n: int, method: str, start: date) -> pd.DataFrame:
    r = annual_rate / 100 / 12
    balance = principal
    rows = []
    if method == "annuity":
        pay = principal / n if r == 0 else principal * r / (1 - (1 + r) ** -n)
    for m in range(1, n + 1):
        interest = balance * r
        if method == "annuity":
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


COMPOUNDING = {"comp_monthly": 1, "comp_quarterly": 3, "comp_yearly": 12, "comp_simple": None}


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
        unit = st.radio(
            t("unit"), ["years", "months"], horizontal=True,
            format_func=lambda k: t("u_" + k), key=f"{prefix}_unit",
        )
    with c1:
        if unit == "years":
            val = st.number_input(t("duration"), min_value=1, max_value=50, value=default_years,
                                  step=1, key=f"{prefix}_dur_y")
            return int(val) * 12, dur_text(int(val), "y")
        val = st.number_input(t("duration"), min_value=1, max_value=600, value=default_years * 12,
                              step=1, key=f"{prefix}_dur_m")
        return int(val), dur_text(int(val), "m")


tab_loan, tab_dep = st.tabs([t("tab_loan"), t("tab_dep")])

# ----------------------------------------------------------------------------
# LOAN TAB
# ----------------------------------------------------------------------------
with tab_loan:
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        amount = st.number_input(t("loan_amount"), min_value=1_000_000, max_value=100_000_000_000,
                                 value=100_000_000, step=1_000_000, key="loan_amount")
    with b:
        rate = st.number_input(t("rate"), min_value=0.0, max_value=200.0,
                               value=24.0, step=0.5, key="loan_rate")
    with c:
        n_months, dur_label = duration_input("loan", 3)

    d, e = st.columns([2, 1])
    with d:
        method = st.radio(t("repay_type"), ["annuity", "diff"], horizontal=True,
                          format_func=lambda k: t(k), key="loan_method")
    with e:
        start = st.date_input(t("first_month"), value=date.today(), key="loan_start")

    df = loan_schedule(amount, rate, n_months, method, start)
    total_interest = df["Interest"].sum()
    total_paid = df["Payment"].sum()
    overpay_pct = total_interest / amount * 100

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    if method == "annuity":
        k1.markdown(kpi(t("monthly_payment"), df["Payment"].iloc[0], t("same_every", dur=dur_label), "hero"),
                    unsafe_allow_html=True)
    else:
        k1.markdown(kpi(t("first_payment"), df["Payment"].iloc[0],
                        t("falls_to", x=fmt(df["Payment"].iloc[-1])), "hero"), unsafe_allow_html=True)
    k2.markdown(kpi(t("total_interest"), total_interest, t("on_top", p=f"{overpay_pct:.1f}"), "gold"),
                unsafe_allow_html=True)
    k3.markdown(kpi(t("total_pay"), total_paid, t("loan_plus_int")), unsafe_allow_html=True)
    k4.markdown(kpi_text(t("last_payment"), fmt_month_year(df["Date"].iloc[-1]), t("n_payments", n=n_months)),
                unsafe_allow_html=True)

    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    g1, g2 = st.columns([1, 1.4])
    with g1:
        st.markdown(f'<div class="chart-title">{t("chart_where")}</div>', unsafe_allow_html=True)
        fig = donut([t("loan_principal"), t("interest")], [amount, total_interest], [TURQUOISE, SAFFRON],
                    f"{overpay_pct:.0f}%<br><span style='font-size:11px;color:{MUTED}'>{t('extra_cost')}</span>")
        st.plotly_chart(fig, width="stretch")
    with g2:
        st.markdown(f'<div class="chart-title">{t("chart_each")}</div>', unsafe_allow_html=True)
        if n_months <= 24:
            x = df["Month"].astype(str)
            p_vals, i_vals = df["Principal"], df["Interest"]
            xtitle = t("month")
        else:
            grp = df.assign(Year=(df["Month"] - 1) // 12 + 1).groupby("Year")[["Principal", "Interest"]].sum()
            x = grp.index.astype(str)
            p_vals, i_vals = grp["Principal"], grp["Interest"]
            xtitle = t("year")
        fig = go.Figure()
        fig.add_bar(x=x, y=p_vals, name=t("principal"), marker_color=TURQUOISE,
                    hovertemplate=f"%{{y:,.0f}} UZS<extra>{t('principal')}</extra>")
        fig.add_bar(x=x, y=i_vals, name=t("interest"), marker_color=SAFFRON,
                    hovertemplate=f"%{{y:,.0f}} UZS<extra>{t('interest')}</extra>")
        fig.update_layout(barmode="stack", bargap=0.25, xaxis_title=xtitle)
        st.plotly_chart(style_fig(fig), width="stretch")

    st.markdown(f'<div class="chart-title">{t("chart_remaining")}</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_scatter(x=df["Date"], y=df["Balance"], mode="lines", name=t("remaining_debt"),
                    line=dict(color=TURQUOISE, width=3), fill="tozeroy", fillcolor="rgba(46,196,182,0.15)",
                    hovertemplate="%{y:,.0f} UZS<extra></extra>")
    fig.add_scatter(x=df["Date"], y=df["Interest"].cumsum(), mode="lines", name=t("interest_so_far"),
                    line=dict(color=SAFFRON, width=3),
                    hovertemplate="%{y:,.0f} UZS<extra></extra>")
    st.plotly_chart(style_fig(fig, 340), width="stretch")

    with st.expander(t("full_schedule")):
        show = df.copy()
        for col in ["Payment", "Principal", "Interest", "Balance"]:
            show[col] = show[col].round(0).astype(int)
        show = show.rename(columns={
            "Month": t("month"), "Date": t("date"), "Payment": t("payment"),
            "Principal": t("principal"), "Interest": t("interest"), "Balance": t("balance"),
        })
        money_cols = [t("payment"), t("principal"), t("interest"), t("balance")]
        st.dataframe(show, width="stretch", hide_index=True,
                     column_config={c: st.column_config.NumberColumn(c, format="%d") for c in money_cols})
        st.download_button(t("dl_schedule"), show.to_csv(index=False).encode("utf-8-sig"),
                           "loan_schedule.csv", "text/csv")
    st.markdown(f'<div class="note">{t("note_loan")}</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# DEPOSIT TAB
# ----------------------------------------------------------------------------
with tab_dep:
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        initial = st.number_input(t("dep_amount"), min_value=0, max_value=100_000_000_000,
                                  value=50_000_000, step=1_000_000, key="dep_amount")
    with b:
        d_rate = st.number_input(t("rate"), min_value=0.0, max_value=200.0,
                                 value=20.0, step=0.5, key="dep_rate")
    with c:
        d_months, d_label = duration_input("dep", 1)

    d, e, f = st.columns(3)
    with d:
        monthly_add = st.number_input(t("monthly_topup"), min_value=0, max_value=10_000_000_000,
                                      value=0, step=500_000, key="dep_add")
    with e:
        comp = st.selectbox(t("interest_type"), list(COMPOUNDING.keys()),
                            format_func=lambda k: t(k), key="dep_comp")
    with f:
        d_start = st.date_input(t("start_date"), value=date.today(), key="dep_start")

    if initial == 0 and monthly_add == 0:
        st.info(t("enter_hint"))
    else:
        dd = deposit_schedule(initial, d_rate, d_months, monthly_add, comp, d_start)
        final = dd["Balance"].iloc[-1]
        put_in = dd["Deposited"].iloc[-1]
        earned = final - put_in
        yield_pct = earned / put_in * 100 if put_in else 0

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(kpi(t("you_will_have"), final, t("after_dur", dur=d_label), "hero"), unsafe_allow_html=True)
        k2.markdown(kpi(t("interest_earned_kpi"), earned, t("total_return", p=f"{yield_pct:.1f}"), "gold"),
                    unsafe_allow_html=True)
        k3.markdown(kpi(t("money_in"), put_in, t("dep_plus_topups")), unsafe_allow_html=True)
        k4.markdown(kpi_text(t("ends_on"), fmt_full_date(dd["Date"].iloc[-1]), t("months_total", n=d_months)),
                    unsafe_allow_html=True)

        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        g1, g2 = st.columns([1, 1.4])
        with g1:
            st.markdown(f'<div class="chart-title">{t("chart_end")}</div>', unsafe_allow_html=True)
            fig = donut([t("your_money"), t("interest")], [put_in, max(earned, 0)], [TURQUOISE, SAFFRON],
                        f"{yield_pct:.0f}%<br><span style='font-size:11px;color:{MUTED}'>{t('return_word')}</span>")
            st.plotly_chart(fig, width="stretch")
        with g2:
            st.markdown(f'<div class="chart-title">{t("chart_growth")}</div>', unsafe_allow_html=True)
            if d_months <= 24:
                snap = dd.copy()
                snap["Label"] = snap["Month"].apply(lambda m: t("month_label", n=m))
            else:
                snap = dd[(dd["Month"] % 12 == 0) | (dd["Month"] == d_months)].copy()
                snap["Label"] = snap["Month"].apply(
                    lambda m: t("year_label", n=m // 12) if m % 12 == 0 else t("month_label", n=m))
            fig = go.Figure()
            fig.add_bar(x=snap["Label"], y=snap["Deposited"], name=t("your_money"), marker_color=TURQUOISE,
                        hovertemplate=f"%{{y:,.0f}} UZS<extra>{t('your_money')}</extra>")
            fig.add_bar(x=snap["Label"], y=snap["Interest earned"], name=t("interest"), marker_color=SAFFRON,
                        hovertemplate=f"%{{y:,.0f}} UZS<extra>{t('interest')}</extra>")
            fig.update_layout(barmode="stack", bargap=0.25)
            st.plotly_chart(style_fig(fig), width="stretch")

        st.markdown(f'<div class="chart-title">{t("chart_balance")}</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_scatter(x=dd["Date"], y=dd["Balance"], mode="lines", name=t("total_balance"),
                        line=dict(color=TURQUOISE, width=3), fill="tozeroy", fillcolor="rgba(46,196,182,0.15)",
                        hovertemplate="%{y:,.0f} UZS<extra></extra>")
        fig.add_scatter(x=dd["Date"], y=dd["Deposited"], mode="lines", name=t("put_in_line"),
                        line=dict(color=SAFFRON, width=2, dash="dot"),
                        hovertemplate="%{y:,.0f} UZS<extra></extra>")
        st.plotly_chart(style_fig(fig, 340), width="stretch")

        with st.expander(t("full_table")):
            show = dd.copy()
            for col in ["Deposited", "Interest earned", "Balance"]:
                show[col] = show[col].round(0).astype(int)
            show = show.rename(columns={
                "Month": t("month"), "Date": t("date"), "Deposited": t("deposited"),
                "Interest earned": t("interest_earned"), "Balance": t("balance"),
            })
            money_cols = [t("deposited"), t("interest_earned"), t("balance")]
            st.dataframe(show, width="stretch", hide_index=True,
                         column_config={c: st.column_config.NumberColumn(c, format="%d") for c in money_cols})
            st.download_button(t("dl_table"), show.to_csv(index=False).encode("utf-8-sig"),
                               "deposit_growth.csv", "text/csv")
        st.markdown(f'<div class="note">{t("note_dep")}</div>', unsafe_allow_html=True)
