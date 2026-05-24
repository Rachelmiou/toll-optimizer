# ⚡ 407 Toll Route Optimizer

> Should you hop on the 407 ETR or take the free route? This tool does the math for you.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚗 What Is This?

An interactive calculator for Ontario drivers that compares **407 ETR toll routes** against free alternatives. It factors in toll cost, fuel savings, and time saved to give you a clear **TAKE IT** or **SKIP IT** answer.

---

## 📸 Features

✅ 25 major 407 interchanges (Burlington → Hwy 35/115)  
✅ Real rate zones — light, regular, heavy  
✅ Peak / mid-peak / off-peak pricing  
✅ Fuel savings from highway vs city driving  
✅ Configurable time value ($/hr)  
✅ Transponder vs camera toll comparison  
✅ Cheapest short hop finder (2-3 stops)  

---

## 🧮 How The Math Works

| Factor | What It Measures |
|--------|-----------------|
| **Toll Cost** | Per-km rate × distance + trip fee + camera charge |
| **Fuel Savings** | Alt routes burn ~15% more fuel (city driving) |
| **Time Value** | Your hourly rate × minutes saved |

**Verdict:** `(time saved × hourly rate) − (toll − fuel savings) = net benefit`

---

## 🚀 Getting Started

```bash
git clone https://github.com/Rachelmiou/toll-optimizer-python.git
cd toll-optimizer-python
pip3 install -r requirements.txt
python3 -m streamlit run app.py
```

Opens at `http://localhost:8501`

> Requires [Python 3.9+](https://python.org)

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Interactive web UI |
| Pandas | Data handling |

---

## ⚠️ Disclaimer

Rates are modeled on 2024 407 ETR published schedules. Actual bills may vary. No live traffic data. Not affiliated with 407 ETR.

---

Made by Rachel Miou with the help of AI 🤖
