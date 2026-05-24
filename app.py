import streamlit as st

st.set_page_config(page_title="407 Toll Route Optimizer", page_icon="⚡", layout="wide")

# --- Data ---

INTERCHANGES = [
    {"name": "Burlington (QEW)", "km": 0},
    {"name": "Appleby Line", "km": 5.2},
    {"name": "Walkers Line", "km": 8.1},
    {"name": "Guelph Line", "km": 11.4},
    {"name": "James Snow Pkwy", "km": 15.8},
    {"name": "Trafalgar Rd", "km": 19.3},
    {"name": "Hwy 403", "km": 23.7},
    {"name": "Winston Churchill", "km": 27.1},
    {"name": "Mississauga Rd", "km": 30.5},
    {"name": "Hurontario St", "km": 35.2},
    {"name": "Hwy 410", "km": 38.8},
    {"name": "Kennedy Rd", "km": 42.4},
    {"name": "Hwy 427", "km": 46.1},
    {"name": "Hwy 400", "km": 52.3},
    {"name": "Jane St", "km": 54.8},
    {"name": "Keele St", "km": 57.2},
    {"name": "Bathurst St", "km": 60.1},
    {"name": "Yonge St", "km": 64.5},
    {"name": "Leslie St", "km": 67.8},
    {"name": "Hwy 404", "km": 70.3},
    {"name": "Woodbine Ave", "km": 73.6},
    {"name": "Markham Rd", "km": 77.9},
    {"name": "Brock Rd (Pickering)", "km": 83.2},
    {"name": "Harmony Rd", "km": 89.5},
    {"name": "Hwy 35/115", "km": 96.0},
]

RATE_ZONES = {
    "light":   {"Peak": 0.5580, "Mid-Peak": 0.3490, "Off-Peak": 0.2710},
    "regular": {"Peak": 0.4460, "Mid-Peak": 0.2870, "Off-Peak": 0.2290},
    "heavy":   {"Peak": 0.3540, "Mid-Peak": 0.2250, "Off-Peak": 0.1870},
}

TRIP_TOLL = 1.00
CAMERA_CHARGE = 4.55

ALT_ROUTE_DISTANCE_MULT = 1.15
ALT_TIME_MULT = {"Peak": 2.5, "Mid-Peak": 1.8, "Off-Peak": 1.4}

INTERCHANGE_NAMES = [f"{ic['name']} — km {ic['km']}" for ic in INTERCHANGES]


def get_zone(km: float) -> str:
    if km <= 23.7:
        return "light"
    elif km <= 52.3:
        return "regular"
    return "heavy"


def calc_toll(start_km: float, end_km: float, time_period: str) -> float:
    dist = abs(end_km - start_km)
    mid_km = (start_km + end_km) / 2
    zone = get_zone(mid_km)
    rate = RATE_ZONES[zone][time_period]
    return rate * dist + TRIP_TOLL


def calc_fuel(dist_km: float, l_per_100km: float, price_per_l: float) -> float:
    return (dist_km / 100) * l_per_100km * price_per_l


# --- UI ---

st.markdown("""
<style>
    .metric-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #334155;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        margin: 4px 0;
    }
    .metric-label {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .verdict-box {
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin: 16px 0;
    }
    .verdict-yes {
        background: rgba(34, 197, 94, 0.1);
        border: 2px solid rgba(34, 197, 94, 0.4);
    }
    .verdict-no {
        background: rgba(239, 68, 68, 0.1);
        border: 2px solid rgba(239, 68, 68, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ 407 Toll Route Optimizer")
st.caption("Calculate if short 407 ETR hops save you money after toll + fuel + time")

st.divider()

# --- Sidebar inputs ---
with st.sidebar:
    st.header("🚗 Route")

    origin_idx = st.selectbox("Entry Point", range(len(INTERCHANGES)),
                              format_func=lambda i: INTERCHANGE_NAMES[i], index=9)

    dest_options = [i for i in range(len(INTERCHANGES)) if i != origin_idx]
    default_dest = dest_options.index(17) if 17 in dest_options else 0
    dest_idx = st.selectbox("Exit Point", dest_options,
                            format_func=lambda i: INTERCHANGE_NAMES[i], index=default_dest)

    time_period = st.radio("Time of Day", ["Peak", "Mid-Peak", "Off-Peak"],
                           captions=[
                               "6-7am, 3:30-6:30pm weekdays",
                               "7-9am, 11am-2pm, 6:30-7pm weekdays",
                               "All other times + weekends"
                           ])

    has_transponder = st.checkbox("I have a transponder", value=True,
                                 help=f"Saves ${CAMERA_CHARGE:.2f} camera fee per trip")

    st.divider()
    st.header("⛽ Vehicle & Cost")

    fuel_consumption = st.slider("Fuel consumption (L/100km)", 4.0, 18.0, 9.5, 0.5)
    fuel_price = st.slider("Gas price ($/L)", 1.00, 2.50, 1.65, 0.05)
    time_value = st.slider("Your time value ($/hr)", 0, 80, 25, 5,
                           help="Set to $0 to ignore time and compare hard costs only")


# --- Calculations ---

start_km = INTERCHANGES[origin_idx]["km"]
end_km = INTERCHANGES[dest_idx]["km"]
toll_dist = abs(end_km - start_km)
alt_dist = toll_dist * ALT_ROUTE_DISTANCE_MULT

toll_speed = 110  # km/h
toll_time_min = (toll_dist / toll_speed) * 60
alt_time_min = toll_time_min * ALT_TIME_MULT[time_period]
time_saved_min = alt_time_min - toll_time_min

toll_cost = calc_toll(start_km, end_km, time_period)
if not has_transponder:
    toll_cost += CAMERA_CHARGE

toll_fuel = calc_fuel(toll_dist, fuel_consumption, fuel_price)
alt_fuel = calc_fuel(alt_dist, fuel_consumption * 1.15, fuel_price)
fuel_saved = alt_fuel - toll_fuel

time_value_saved = (time_saved_min / 60) * time_value
net_cost = toll_cost - fuel_saved
net_benefit = time_value_saved - net_cost

break_even = (net_cost / time_saved_min) * 60 if time_saved_min > 0 else float("inf")
worth_it = net_benefit > 0
stops = abs(dest_idx - origin_idx)


# --- Verdict ---

verdict_class = "verdict-yes" if worth_it else "verdict-no"
verdict_icon = "✅" if worth_it else "❌"
verdict_text = "TAKE THE 407" if worth_it else "SKIP THE 407"
verdict_color = "#22c55e" if worth_it else "#ef4444"

if worth_it:
    explanation = (
        f"You save **{time_saved_min:.0f} min** and come out **${net_benefit:.2f} ahead** "
        f"when factoring time at ${time_value}/hr. "
        f"Toll costs ${toll_cost:.2f} but you save ${fuel_saved:.2f} in fuel."
    )
else:
    if time_value == 0:
        explanation = (
            f"Pure cost comparison: the toll (${toll_cost:.2f}) exceeds "
            f"fuel savings (${fuel_saved:.2f}) by ${abs(net_benefit):.2f}."
        )
    else:
        explanation = (
            f"Even valuing time at ${time_value}/hr (${time_value_saved:.2f} saved), "
            f"the toll costs ${net_cost:.2f} more than fuel savings. "
            f"Break-even time value: **${break_even:.0f}/hr**."
        )

st.markdown(f"""
<div class="verdict-box {verdict_class}">
    <div style="font-size: 28px; font-weight: 700; color: {verdict_color};">
        {verdict_icon} {verdict_text}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(explanation)

st.divider()

# --- Metrics row ---

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Interchanges", stops)
col2.metric("407 Toll", f"${toll_cost:.2f}")
col3.metric("Time Saved", f"{time_saved_min:.0f} min")
col4.metric("Fuel Saved", f"${fuel_saved:.2f}")
col5.metric("Net Benefit", f"${net_benefit:+.2f}",
            delta=f"{'saves' if worth_it else 'costs'} you money",
            delta_color="normal" if worth_it else "inverse")

st.divider()

# --- Route comparison ---

st.subheader("Route Comparison")

left, right = st.columns(2)

with left:
    st.markdown("#### 🛣️ 407 ETR")
    st.markdown(f"""
    | | |
    |---|---|
    | **Distance** | {toll_dist:.1f} km |
    | **Time** | {toll_time_min:.0f} min |
    | **Fuel cost** | ${toll_fuel:.2f} |
    | **Toll** | ${toll_cost:.2f} |
    | **Total** | **${toll_fuel + toll_cost:.2f}** |
    """)

with right:
    st.markdown("#### 🏙️ Alternative Route")
    st.markdown(f"""
    | | |
    |---|---|
    | **Distance** | {alt_dist:.1f} km |
    | **Time** | {alt_time_min:.0f} min |
    | **Fuel cost** | ${alt_fuel:.2f} |
    | **Toll** | $0.00 |
    | **Total** | **${alt_fuel:.2f}** |
    """)

st.caption(
    f"Alt route assumes ~15% longer distance and worse fuel economy (city driving). "
    f"Time multiplier: {ALT_TIME_MULT[time_period]}x during {time_period}."
)

st.divider()

# --- Cheapest short hops ---

st.subheader("Cheapest Short Hops (2-3 stops)")
st.caption(f"Sorted by toll cost at {time_period} rates")

hops = []
for i in range(len(INTERCHANGES) - 2):
    for j in range(i + 2, min(i + 4, len(INTERCHANGES))):
        cost = calc_toll(INTERCHANGES[i]["km"], INTERCHANGES[j]["km"], time_period)
        if not has_transponder:
            cost += CAMERA_CHARGE
        dist = abs(INTERCHANGES[j]["km"] - INTERCHANGES[i]["km"])
        hops.append({
            "From": INTERCHANGES[i]["name"],
            "To": INTERCHANGES[j]["name"],
            "Distance (km)": f"{dist:.1f}",
            "Stops": j - i,
            "Toll ($)": f"{cost:.2f}",
        })

hops.sort(key=lambda h: float(h["Toll ($)"]))
st.dataframe(hops[:10], use_container_width=True, hide_index=True)

st.divider()

# --- Rate table ---

with st.expander("📊 407 ETR Rate Zones ($/km)"):
    import pandas as pd

    rate_data = []
    for zone, rates in RATE_ZONES.items():
        rate_data.append({
            "Zone": zone.capitalize(),
            "Peak ($/km)": f"${rates['Peak']:.4f}",
            "Mid-Peak ($/km)": f"${rates['Mid-Peak']:.4f}",
            "Off-Peak ($/km)": f"${rates['Off-Peak']:.4f}",
        })
    st.dataframe(rate_data, use_container_width=True, hide_index=True)
    st.caption(f"Plus ${TRIP_TOLL:.2f} trip toll per use. "
               f"Camera charge: ${CAMERA_CHARGE:.2f} (waived with transponder).")

st.divider()
st.caption("Rates modeled on 2024 407 ETR published rates. Actual bills may vary. Not affiliated with 407 ETR.")
st.caption("Made by Rachel with the help of AI 🤖")
