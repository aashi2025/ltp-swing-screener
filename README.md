# LTP Swing Trading Option Chain Screener

A dedicated, high-performance **Swing Trading Option Chain Screener** built using Python (Flask) and a clean, dark-themed responsive UI. Designed specifically for **Vercel Serverless Deployment** with **Zero Infinite Loops** and **Zero Timeouts**.

---

## 🚀 Key Features

1. **Vercel Serverless Ready Architecture:**
   - On-demand backend triggered **only** when the user clicks **`[⚡ Run Swing Scan]`**.
   - No `while True:` loops or background thread scheduling that cause Vercel 504 Gateway Timeouts.

2. **LTP Calculator Swing Filter Engine:**
   - **Support Strike:** Highest Put Open Interest (OI) & Volume -> Calculates **EOS** (Extension of Support).
   - **Resistance Strike:** Highest Call Open Interest (OI) & Volume -> Calculates **EOR** (Extension of Resistance).
   - **Bullish Swing Condition:** Spot price near EOS (within 0.5% - 1.2% range) with Strong Put Support (>55%). Generates signal: `BULLISH REVERSAL (BUY AT EOS)`.
   - **Bearish Swing Condition:** Spot price near EOR (within 0.5% - 1.2% range) with Strong Call Resistance (>55%). Generates signal: `BEARISH REVERSAL (SELL AT EOR)`.
   - **Target & Stop Loss:** Automatic target calculation (opposite strike/EOR/EOS) and 1.2% Stop Loss buffer calculation.

3. **Interactive & Clean Dashboard:**
   - Quick Filter Tabs: *All Stocks*, *Signals Only*, *🟢 Buy at EOS*, *🔴 Sell at EOR*.
   - Live Search & Multi-criteria Sorting (Signals First, Distance to Entry %, Symbol, Strength %).
   - **View Chain Modal:** Detailed option chain breakdown showing Call & Put OI, IV, LTP, Change in OI, and highlighted ATM/Support/Resistance strikes.
   - **CSV Export:** One-click CSV export of scanned results.

---

## 📂 Project Structure

```
swing-option-screener/
├── api/
│   ├── index.py              # Vercel Flask Serverless Handler
│   └── screener_engine.py    # LTP Calculator & Swing Filter Logic
├── public/
│   └── index.html            # Tailwind CSS Dark-themed Interactive Dashboard
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel V2 deployment configuration
└── README.md
```

---

## 🛠️ How to Run Locally

1. Clone or navigate to the project directory:
   ```bash
   cd swing-option-screener
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python api/index.py
   ```

4. Open your browser at `http://localhost:5000`.

---

## ☁️ How to Deploy to Vercel

1. Push this repository to GitHub / GitLab / Bitbucket.
2. Go to [Vercel Dashboard](https://vercel.com/dashboard) -> **Add New Project**.
3. Import the repository.
4. Keep standard settings (Vercel automatically detects `vercel.json` and `@vercel/python`).
5. Click **Deploy**.
