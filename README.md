# 🌍 RiskAtlas — Trade Risk Intelligence Platform

A real-time trade risk intelligence dashboard that helps businesses monitor geopolitical risks, tariff changes, supply chain vulnerabilities, and policy alerts across the globe. Powered by AI-driven forecasting and interactive data visualization.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗺️ **Interactive World Map** | Color-coded global risk map with click-to-inspect country details |
| 📊 **Dashboard Metrics** | Key KPIs — countries monitored, average risk score, active tariffs, policy alerts |
| 🧠 **AI Risk Forecasting** | ML-powered 3/6/12-month geopolitical risk predictions with confidence scores |
| 💰 **Cost Simulator** | Calculate tariff and supply chain impact on product costs (with AI prediction tab) |
| 🔔 **Policy Alerts Feed** | Real-time trade policy updates, filterable by category (Export Control, Tariff, Subsidy, etc.) |
| 🔗 **Supply Chain Vulnerability** | Industry-level risk and concentration mapping with supplier analysis |
| 🔄 **Alternative Suppliers** | Friend-shoring recommendations for high-risk countries |

---

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** — blazing-fast build tool
- **Tailwind CSS** — utility-first styling
- **shadcn/ui** — modern, accessible component library
- **react-simple-maps** — interactive map
- **d3-scale** — color scale for risk visualization
- **Lucide React** — icons
- **Recharts** — charts

### Backend
- **FastAPI** (Python) — high-performance REST API
- **Uvicorn** — ASGI server
- **Pydantic** — data validation

---

## 📁 Project Structure

```
RiskAtlas/
├── app/                          # Frontend (React + Vite)
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ui/               # shadcn/ui base components
│   │   │   ├── WorldMap.tsx      # Interactive global risk map
│   │   │   ├── DashboardMetrics.tsx
│   │   │   ├── CostSimulator.tsx
│   │   │   ├── AIForecasting.tsx
│   │   │   ├── PolicyAlertsFeed.tsx
│   │   │   ├── SupplyChainVulnerability.tsx
│   │   │   ├── AlternativeSuppliers.tsx
│   │   │   └── CountryInfoPanel.tsx
│   │   ├── services/
│   │   │   └── api.ts            # API client (connects to backend)
│   │   ├── types/
│   │   │   └── index.ts          # TypeScript type definitions
│   │   ├── hooks/                # Custom React hooks
│   │   ├── lib/
│   │   │   └── utils.ts          # Utility functions
│   │   ├── App.tsx               # Main app layout
│   │   ├── App.css               # App-specific styles
│   │   ├── index.css             # Global styles + Tailwind
│   │   └── main.tsx              # Entry point
│   ├── index.html                # HTML template
│   ├── package.json              # JS dependencies
│   ├── vite.config.ts            # Vite configuration
│   ├── tailwind.config.js        # Tailwind CSS configuration
│   ├── tsconfig.json             # TypeScript configuration
│   └── postcss.config.js         # PostCSS configuration
│
├── riskatlas/
│   └── backend/                  # Backend (FastAPI)
│       ├── main.py               # API server with all endpoints
│       └── requirements.txt      # Python dependencies
│
└── README.md                     # This file
```

---

## 🚀 Getting Started (Beginner-Friendly Setup)

Follow these steps **in order** to run the project on your own computer. You need **two terminal windows** — one for the backend, one for the frontend.

### Prerequisites

Make sure you have these installed before starting:

| Tool | Version | Check with | Download |
|---|---|---|---|
| **Node.js** | 18 or higher | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 9 or higher | `npm --version` | Comes with Node.js |
| **Python** | 3.9 or higher | `python --version` | [python.org](https://www.python.org/downloads/) |
| **pip** | Latest | `pip --version` | Comes with Python |

> **💡 Tip for Windows users:** When installing Python, make sure to check **"Add Python to PATH"** during installation.

---

### Step 1: Clone or Download the Project

If you downloaded a ZIP, extract it. Or clone with git:

```bash
git clone <repository-url>
cd "Kimi_Agent_RiskAtlas Feature Expansion (1)"
```

---

### Step 2: Set Up the Backend (Terminal 1)

Open your **first terminal** and run these commands one by one:

```bash
# Navigate to the backend folder
cd riskatlas/backend

# (Recommended) Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

✅ **You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

> **🔍 Verify:** Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser — you should see the Swagger API documentation.

**⚠️ Keep this terminal running!** Don't close it.

---

### Step 3: Set Up the Frontend (Terminal 2)

Open a **second terminal** and run these commands:

```bash
# Navigate to the frontend folder
cd app

# Install JavaScript dependencies
npm install --legacy-peer-deps

# Start the development server
npm run dev
```

✅ **You should see:**
```
  VITE v7.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://xxx.xxx.xxx.xxx:5173/
```

> **💡 Note:** If port 5173 is busy, Vite will automatically use 5174 or the next available port. Just use whatever URL Vite shows you.

---

### Step 4: Open the Dashboard

Open your browser and go to the URL shown by Vite (usually one of these):

- 👉 **http://localhost:5173/**
- 👉 **http://localhost:5174/** (if 5173 was busy)

You should see the full RiskAtlas dashboard with the world map, metrics, and all panels!

---

## 🔧 Troubleshooting

### ❌ "Cannot connect to backend" / "Connection Error" on the dashboard

**Cause:** The backend server is not running on port 8000.

**Fix:** Make sure Terminal 1 is running with `python -m uvicorn main:app --host 0.0.0.0 --port 8000`. Check for no error messages.

---

### ❌ `npm install` fails with `ERESOLVE` errors

**Cause:** Peer dependency version conflicts between React 18 and some packages.

**Fix:** Use the `--legacy-peer-deps` flag:
```bash
npm install --legacy-peer-deps
```

---

### ❌ Blank page with "504 Outdated Optimize Dep" in console

**Cause:** Stale Vite dependency cache.

**Fix:**
```bash
# Stop the dev server (Ctrl+C), then:
npx vite --force
```
Or manually delete the `node_modules/.vite` folder and restart.

---

### ❌ `pip install` fails with compilation errors

**Cause:** Some Python packages may not have pre-built wheels for your Python version.

**Fix:** Install packages individually without version pinning:
```bash
pip install fastapi uvicorn pydantic python-multipart
```

---

### ❌ "Module not found" or import errors in the terminal

**Cause:** Dependencies not installed.

**Fix:** Make sure you ran `npm install --legacy-peer-deps` in the `app/` folder and `pip install -r requirements.txt` in the `riskatlas/backend/` folder.

---

## 📡 API Endpoints

The backend runs at `http://localhost:8000`. Key endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/countries` | List all monitored countries |
| `GET` | `/api/countries/{id}` | Get detailed country info (risk, tariffs, policies) |
| `GET` | `/api/dashboard/metrics` | Dashboard summary metrics |
| `GET` | `/api/policy-alerts` | Policy alerts with optional filters |
| `POST` | `/api/cost-simulation` | Run a tariff cost simulation |
| `GET` | `/api/supply-chain/{industry}` | Supply chain vulnerability data |
| `GET` | `/api/alternative-suppliers/{country_id}` | Alternative supplier recommendations |
| `GET` | `/api/industries` | List of tracked industries |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger API documentation (interactive) |

---

## 🛑 Stopping the Servers

- Press **Ctrl + C** in each terminal to stop the frontend and backend servers.

---

## 📝 Notes

- The backend uses **mock data** for all endpoints — no database or external API keys needed.
- The frontend API URL is configured in `app/src/services/api.ts` — if your backend runs on a different port, update the `API_BASE_URL` constant there.
- The project uses **Tailwind CSS v3** with the `tailwindcss-animate` plugin for micro-animations.

---

## 📄 License

This project is for educational and hackathon purposes.
