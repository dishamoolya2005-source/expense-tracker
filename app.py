import streamlit as st
import pandas as pd
import os
import re
from datetime import date, timedelta

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }

.stApp {
    background-color: #0A0C10;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(0, 191, 255, 0.04) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(99, 102, 241, 0.04) 0%, transparent 60%);
}

/* ── WELCOME PAGE ── */
.welcome-container {
    height: 88vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0;
}
.eyebrow {
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #00BFFF;
    margin-bottom: 20px;
}
.main-heading {
    font-family: 'Playfair Display', serif;
    font-size: 86px;
    font-weight: 700;
    color: #F0F4FF;
    text-align: center;
    line-height: 1.05;
    margin-bottom: 16px;
    letter-spacing: -2px;
}
.main-heading span { color: #00BFFF; }
.sub-text {
    color: #5A6478;
    font-size: 18px;
    font-weight: 300;
    margin-bottom: 36px;
    letter-spacing: 0.5px;
}
.divider-line {
    width: 60px;
    height: 1px;
    background: linear-gradient(to right, transparent, #00BFFF, transparent);
    margin: 0 auto 36px auto;
}
.credit-text {
    margin-top: 32px;
    font-size: 12px;
    color: #2E3A4E;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.credit-text span {
    color: #00BFFF;
    opacity: 0.7;
}

/* ── UNIFORM BUTTONS ──
   Every st.button renders the same fixed height/width so they all match.
*/
div.stButton > button {
    background: linear-gradient(135deg, rgba(0,191,255,0.12), rgba(0,191,255,0.04));
    color: #E8F4FF !important;
    border: 1px solid rgba(0, 191, 255, 0.4) !important;
    border-radius: 10px !important;
    padding: 0 !important;
    height: 42px !important;
    min-height: 42px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0.4px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 16px rgba(0,191,255,0.08), inset 0 1px 0 rgba(255,255,255,0.04) !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,191,255,0.22), rgba(0,191,255,0.10)) !important;
    border-color: rgba(0,191,255,0.8) !important;
    box-shadow: 0 0 28px rgba(0,191,255,0.22) !important;
    transform: translateY(-1px) !important;
}

/* Edit button — amber tint */
div.stButton > button[kind="secondary"],
div[data-testid*="edit"] div.stButton > button {
    border-color: rgba(255, 180, 50, 0.45) !important;
    background: linear-gradient(135deg, rgba(255,180,50,0.10), rgba(255,180,50,0.03)) !important;
    box-shadow: 0 0 14px rgba(255,180,50,0.07) !important;
}

/* Delete button — red tint */
div[data-testid*="delete"] div.stButton > button {
    border-color: rgba(255, 80, 80, 0.45) !important;
    background: linear-gradient(135deg, rgba(255,80,80,0.10), rgba(255,80,80,0.03)) !important;
    box-shadow: 0 0 14px rgba(255,80,80,0.07) !important;
}

/* ── SECTION HEADERS ── */
.section-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00BFFF;
    margin-bottom: 12px;
    margin-top: 32px;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: #E8F0FF;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
}

/* ── STAT CARDS ── */
.stat-card {
    background: linear-gradient(145deg, #13161E, #0F1218);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(0,191,255,0.5), transparent);
}
.stat-card:hover { border-color: rgba(0,191,255,0.3); }
.stat-icon { font-size: 22px; margin-bottom: 10px; }
.stat-label {
    font-size: 11px; font-weight: 500; letter-spacing: 2px;
    text-transform: uppercase; color: #4A566A; margin-bottom: 6px;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 28px; font-weight: 700; color: #E8F0FF; line-height: 1;
}
.stat-value.accent { color: #00BFFF; }
.stat-sub { font-size: 12px; color: #3A4456; margin-top: 4px; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background-color: #13161E !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #D0DCFF !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(0,191,255,0.5) !important;
    box-shadow: 0 0 0 2px rgba(0,191,255,0.1) !important;
}
.stTextInput > label, .stNumberInput > label,
.stDateInput > label, .stSelectbox > label {
    color: #4A566A !important; font-size: 12px !important; letter-spacing: 1px !important;
}
.stDateInput > div > div > input {
    background-color: #13161E !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #D0DCFF !important;
}
.stSelectbox > div > div {
    background-color: #13161E !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #D0DCFF !important;
}

/* ── EDIT FORM CARD ── */
.edit-card {
    background: linear-gradient(145deg, #151820, #111419);
    border: 1px solid rgba(255, 180, 50, 0.25);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
}
.edit-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,180,50,0.5), transparent);
    border-radius: 16px 16px 0 0;
}

/* ── EXPENSE ROW ── */
.expense-row {
    background: linear-gradient(145deg, #13161E, #0F1218);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: border-color 0.2s;
}
.expense-row:hover { border-color: rgba(0,191,255,0.2); }
.exp-date { font-size: 12px; color: #3A4456; min-width: 80px; }
.exp-cat  { font-size: 12px; min-width: 120px; }
.exp-amt  {
    font-family: 'Playfair Display', serif;
    font-size: 18px; font-weight: 700; color: #E8F0FF; min-width: 90px;
}
.exp-note { font-size: 13px; color: #5A6478; flex: 1; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ── SUCCESS / ERROR ── */
.stSuccess { background-color: rgba(0,191,100,0.1) !important; border: 1px solid rgba(0,191,100,0.3) !important; border-radius: 10px !important; }
.stError   { background-color: rgba(255,80,80,0.1) !important; border: 1px solid rgba(255,80,80,0.3) !important; border-radius: 10px !important; }

/* ── TOTAL BANNER ── */
.total-banner {
    background: linear-gradient(135deg, rgba(0,191,255,0.12), rgba(99,102,241,0.08));
    border: 1px solid rgba(0,191,255,0.25);
    border-radius: 16px;
    padding: 24px 32px;
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 8px;
}
.total-label { font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: #5A6478; font-weight: 500; }
.total-value {
    font-family: 'Playfair Display', serif;
    font-size: 36px; font-weight: 700; color: #00BFFF;
    text-shadow: 0 0 30px rgba(0,191,255,0.4);
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(0,191,255,0.15), rgba(0,191,255,0.05)) !important;
    color: #00BFFF !important;
    border: 1px solid rgba(0,191,255,0.35) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    height: 42px !important;
}

/* ── TITLES ── */
h1 { font-family: 'Playfair Display', serif !important; color: #E8F0FF !important; letter-spacing: -1px !important; }
h2, h3 { color: #B0BCDC !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0A0C10; }
::-webkit-scrollbar-thumb { background: rgba(0,191,255,0.2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# CONSTANTS
# -----------------------------------
FILE_NAME = "expenses.xlsx"

CATEGORIES = {
    "🍕 Food":          ["pizza","burger","food","coffee","tea","lunch","dinner",
                         "breakfast","snack","restaurant","swiggy","zomato","eat",
                         "meal","chai","biryani","dosa","sandwich"],
    "🚗 Travel":        ["travel","uber","ola","auto","train","bus","metro",
                         "cab","flight","petrol","fuel","toll","rapido","taxi",
                         "rickshaw","commute"],
    "🛍️ Shopping":     ["shopping","clothes","shoes","amazon","flipkart","myntra",
                         "dress","shirt","jeans","jacket","bag","watch","accessory"],
    "⚡ Utilities":     ["electricity","water","bill","recharge","internet","wifi",
                         "gas","mobile","phone","subscription","netflix","spotify",
                         "rent","maintenance"],
    "🏥 Health":        ["medicine","doctor","hospital","pharmacy","gym","health",
                         "medical","clinic","dentist","chemist"],
    "🎮 Entertainment": ["movie","game","concert","show","ticket","entertainment",
                         "fun","outing","party","event"],
    "📚 Education":     ["book","course","class","tuition","fee","education",
                         "study","coaching","school","college"],
    "🗂️ Other":        [],
}

CATEGORY_COLORS = {
    "🍕 Food":          "#FF6B6B",
    "🚗 Travel":        "#4ECDC4",
    "🛍️ Shopping":     "#FFE66D",
    "⚡ Utilities":     "#A8E6CF",
    "🏥 Health":        "#FF8B94",
    "🎮 Entertainment": "#C9B1FF",
    "📚 Education":     "#FFA07A",
    "🗂️ Other":        "#778899",
}

# -----------------------------------
# HELPERS
# -----------------------------------
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            return df
        except Exception:
            pass
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

def save_data(df):
    df.to_excel(FILE_NAME, index=False)

def detect_category(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORIES.items():
        if any(kw in text_lower for kw in keywords):
            return category
    return "🗂️ Other"

def parse_amount(text: str) -> float:
    text = text.replace("₹", "").replace(",", "")
    match = re.search(r'\d+(?:\.\d+)?', text)
    return float(match.group()) if match else 0.0

def format_inr(amount) -> str:
    return f"₹{amount:,.2f}"

# -----------------------------------
# SESSION STATE
# -----------------------------------
for key, default in [
    ("started", False),
    ("selected_category", "All"),
    ("editing_index", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# -----------------------------------
# LOAD DATA
# -----------------------------------
df = load_data()

# ====================================
# WELCOME PAGE
# ====================================
if not st.session_state.started:

    st.markdown("""
    <div class="welcome-container">
        <div class="eyebrow">Personal Finance</div>
        <div class="main-heading">Expense<br><span>Tracker</span></div>
        <div class="divider-line"></div>
        <div class="sub-text">Track every rupee. Understand your spending.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        if st.button("Get Started →", use_container_width=True):
            st.session_state.started = True
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top: 8px;">
        <span class="credit-text">Created by <span>Disha Moolya</span></span>
    </div>
    """, unsafe_allow_html=True)

# ====================================
# MAIN DASHBOARD
# ====================================
else:

    st.markdown("<br>", unsafe_allow_html=True)
    st.title("💰 Expense Tracker")
    st.markdown(
        f"<p style='color:#3A4456;font-size:13px;margin-top:-12px;'>"
        f"Today is {date.today().strftime('%A, %d %B %Y')}</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ── ADD EXPENSE ──────────────────────────────────────────────
    st.markdown('<div class="section-label">New Entry</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Add an Expense</div>', unsafe_allow_html=True)

    col_input, col_cat, col_btn = st.columns([3, 2, 1])
    with col_input:
        user_input = st.text_input("DESCRIPTION", placeholder="e.g.  Spent 250 on lunch at Zomato")
    with col_cat:
        manual_category = st.selectbox(
            "CATEGORY",
            options=["Auto-Detect"] + list(CATEGORIES.keys())
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        add_clicked = st.button("➕ Add", use_container_width=True)

    if add_clicked:
        if not user_input.strip():
            st.error("⚠️  Please enter a description.")
        else:
            amount = parse_amount(user_input)
            if amount <= 0:
                st.error("⚠️  Couldn't find a valid amount. Include a number like '250'.")
            else:
                category = detect_category(user_input) if manual_category == "Auto-Detect" else manual_category
                new_row = {
                    "Date": pd.Timestamp(date.today()),
                    "Category": category,
                    "Amount": amount,
                    "Note": user_input.strip(),
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success(f"✅  Added {format_inr(amount)} under {category}")
                st.rerun()

    st.markdown("---")

    # ── DATE FILTER ──────────────────────────────────────────────
    st.markdown('<div class="section-label">Filter</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Date Range</div>', unsafe_allow_html=True)

    col_d1, col_d2, _ = st.columns([1, 1, 2])
    with col_d1:
        from_date = st.date_input("FROM", value=date.today() - timedelta(days=30))
    with col_d2:
        to_date = st.date_input("TO", value=date.today())

    if from_date > to_date:
        st.error("⚠️  'From' date cannot be after 'To' date.")
        filtered_df = df.iloc[0:0]
    elif not df.empty:
        filtered_df = df[
            (df["Date"] >= pd.Timestamp(from_date)) &
            (df["Date"] <= pd.Timestamp(to_date))
        ].copy()
    else:
        filtered_df = df.copy()

    st.markdown("---")

    # ── SUMMARY STATS ────────────────────────────────────────────
    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Summary</div>', unsafe_allow_html=True)

    total_expense = filtered_df["Amount"].sum() if not filtered_df.empty else 0
    num_entries   = len(filtered_df)
    avg_expense   = (total_expense / num_entries) if num_entries > 0 else 0
    top_category  = (
        filtered_df.groupby("Category")["Amount"].sum().idxmax()
        if num_entries > 0 else "—"
    )

    s1, s2, s3, s4 = st.columns(4)
    for col, icon, label, value, is_accent, sub in [
        (s1, "💸", "TOTAL SPENT",     format_inr(total_expense), True,  "in selected period"),
        (s2, "🔢", "TRANSACTIONS",    str(num_entries),           False, "entries recorded"),
        (s3, "📊", "AVG EXPENSE",     format_inr(avg_expense),    False, "per transaction"),
        (s4, "🏆", "TOP CATEGORY",    top_category,               False, "by total amount"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-label">{label}</div>
                <div class="stat-value {'accent' if is_accent else ''}">{value}</div>
                <div class="stat-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── CATEGORY BREAKDOWN ───────────────────────────────────────
    st.markdown('<div class="section-label">Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">By Category</div>', unsafe_allow_html=True)

    # Filter buttons — uniform via use_container_width
    all_cats = ["All"] + list(CATEGORIES.keys())
    btn_cols = st.columns(len(all_cats))
    for i, cat in enumerate(all_cats):
        with btn_cols[i]:
            short = cat if cat == "All" else " ".join(cat.split()[:2])
            if st.button(short, key=f"catbtn_{cat}", use_container_width=True):
                st.session_state.selected_category = cat

    st.markdown("<br>", unsafe_allow_html=True)

    # Category total cards
    cat_cols = st.columns(len(CATEGORIES))
    for i, (cat, _) in enumerate(CATEGORIES.items()):
        total = filtered_df[filtered_df["Category"] == cat]["Amount"].sum() if not filtered_df.empty else 0
        color = CATEGORY_COLORS.get(cat, "#778899")
        with cat_cols[i]:
            st.markdown(f"""
            <div class="stat-card" style="border-color:rgba(255,255,255,0.06);padding:16px 14px;text-align:center;">
                <div style="font-size:20px;margin-bottom:6px;">{cat.split()[0]}</div>
                <div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#3A4456;margin-bottom:4px;">{" ".join(cat.split()[1:])}</div>
                <div style="font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:{color};">{format_inr(total)}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── EXPENSE LOG WITH EDIT ─────────────────────────────────────
    st.markdown('<div class="section-label">History</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Expense Log</div>', unsafe_allow_html=True)

    selected = st.session_state.selected_category
    if selected == "All":
        display_df = filtered_df.copy()
    else:
        display_df = filtered_df[filtered_df["Category"] == selected].copy()

    if display_df.empty:
        st.markdown(
            "<p style='color:#3A4456;text-align:center;padding:40px 0;'>No expenses found for this period.</p>",
            unsafe_allow_html=True
        )
    else:
        display_df = display_df.sort_values("Date", ascending=False)

        # ── INLINE EDIT FORM ──
        edit_idx = st.session_state.editing_index
        if edit_idx is not None and edit_idx in df.index:
            row = df.loc[edit_idx]
            st.markdown('<div class="edit-card">', unsafe_allow_html=True)
            st.markdown(
                "<p style='color:#FFB432;font-size:12px;letter-spacing:2px;"
                "text-transform:uppercase;margin-bottom:16px;'>✏️ Editing Entry</p>",
                unsafe_allow_html=True
            )
            ec1, ec2, ec3, ec4 = st.columns([2, 2, 1.5, 1])
            with ec1:
                new_note = st.text_input("NOTE", value=str(row["Note"]), key="edit_note")
            with ec2:
                new_cat = st.selectbox(
                    "CATEGORY",
                    options=list(CATEGORIES.keys()),
                    index=list(CATEGORIES.keys()).index(row["Category"])
                          if row["Category"] in CATEGORIES else 0,
                    key="edit_cat"
                )
            with ec3:
                new_amount = st.number_input(
                    "AMOUNT (₹)",
                    value=float(row["Amount"]),
                    min_value=0.0,
                    step=1.0,
                    format="%.2f",
                    key="edit_amount"
                )
            with ec4:
                new_date = st.date_input(
                    "DATE",
                    value=row["Date"].date() if pd.notna(row["Date"]) else date.today(),
                    key="edit_date"
                )

            save_col, cancel_col, _ = st.columns([1, 1, 4])
            with save_col:
                if st.button("💾 Save", use_container_width=True):
                    df.at[edit_idx, "Note"]     = new_note
                    df.at[edit_idx, "Category"] = new_cat
                    df.at[edit_idx, "Amount"]   = new_amount
                    df.at[edit_idx, "Date"]     = pd.Timestamp(new_date)
                    save_data(df)
                    st.session_state.editing_index = None
                    st.success("✅ Expense updated!")
                    st.rerun()
            with cancel_col:
                if st.button("✖ Cancel", use_container_width=True):
                    st.session_state.editing_index = None
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ── ROW HEADERS ──
        hc = st.columns([1.2, 1.8, 1.2, 3, 0.7, 0.7])
        for h, label in zip(hc, ["DATE", "CATEGORY", "AMOUNT", "NOTE", "EDIT", "DEL"]):
            h.markdown(
                f"<p style='font-size:10px;letter-spacing:2px;color:#2E3A4E;"
                f"text-transform:uppercase;margin-bottom:4px;'>{label}</p>",
                unsafe_allow_html=True
            )

        # ── ROWS ──
        for idx, row in display_df.iterrows():
            c_date, c_cat, c_amt, c_note, c_edit, c_del = st.columns([1.2, 1.8, 1.2, 3, 0.7, 0.7])
            color = CATEGORY_COLORS.get(str(row["Category"]), "#778899")

            with c_date:
                d = row["Date"].strftime("%d %b %Y") if pd.notna(row["Date"]) else "—"
                st.markdown(f"<p style='font-size:12px;color:#3A4456;margin:0;padding:10px 0;'>{d}</p>", unsafe_allow_html=True)
            with c_cat:
                st.markdown(
                    f"<p style='font-size:12px;color:{color};margin:0;padding:10px 0;"
                    f"font-weight:600;'>{row['Category']}</p>",
                    unsafe_allow_html=True
                )
            with c_amt:
                st.markdown(
                    f"<p style='font-family:Playfair Display,serif;font-size:16px;"
                    f"color:#E8F0FF;font-weight:700;margin:0;padding:8px 0;'>"
                    f"{format_inr(row['Amount'])}</p>",
                    unsafe_allow_html=True
                )
            with c_note:
                note_text = str(row["Note"])[:60] + ("…" if len(str(row["Note"])) > 60 else "")
                st.markdown(f"<p style='font-size:13px;color:#5A6478;margin:0;padding:10px 0;'>{note_text}</p>", unsafe_allow_html=True)
            with c_edit:
                if st.button("✏️", key=f"edit_{idx}", use_container_width=True):
                    st.session_state.editing_index = idx
                    st.rerun()
            with c_del:
                if st.button("🗑️", key=f"del_{idx}", use_container_width=True):
                    df = df.drop(index=idx).reset_index(drop=True)
                    save_data(df)
                    if st.session_state.editing_index == idx:
                        st.session_state.editing_index = None
                    st.rerun()

            st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.04);margin:0;'>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TOTAL BANNER ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="total-banner">
        <div>
            <div class="total-label">Total Spent</div>
            <div style="color:#3A4456;font-size:12px;margin-top:2px;">
                {from_date.strftime('%d %b')} – {to_date.strftime('%d %b %Y')}
                {'  ·  ' + selected if selected != 'All' else '  ·  All Categories'}
            </div>
        </div>
        <div class="total-value">{format_inr(total_expense)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── DOWNLOAD ─────────────────────────────────────────────────
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as file:
            st.download_button(
                label="📥  Download Full Expense Report (.xlsx)",
                data=file,
                file_name="expenses.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=False
            )

    # ── FOOTER ───────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; margin-top:48px; padding-bottom:24px;">
        <span style="font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#1E2730;">
            Created by <span style="color:#00BFFF; opacity:0.6;">Disha Moolya</span>
        </span>
    </div>
    """, unsafe_allow_html=True)