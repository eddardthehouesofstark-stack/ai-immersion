# TrendLoom — AI-Powered Fashion Trend Intelligence Platform

TrendLoom is a real-time fashion and textile trend intelligence platform designed for fashion designers, retail buyers, merchandisers, and apparel manufacturers. It monitors search momentum, editorial coverage, social discourse, and verified regional signals to identify emerging textile trends across India and regional artisanal clusters (with dedicated focus on Tamil Nadu handlooms).

![TrendLoom Dashboard Preview](https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=1200&q=80)

---

## 🌟 Key Features

- **Live Trend Momentum & Scoring**: Continuously calculates trend velocity, acceleration, and composite Trend Scores (0–100) categorized into `EXPLODING`, `RISING`, `STABLE`, and `PEAKED`.
- **Regional Textile Intelligence**: Deep focus on regional hubs, especially Tamil Nadu GI-tagged weaves (Kanchipuram Mulberry Silk, Madurai Sungudi, Chettinad Cotton, Kovai Kora, Coimbatore handlooms), highlighting fabric compositions, motif patterns, and authentic color palettes.
- **Retail & Merchandising Forecasting**: Translates raw consumer search signals into actionable business intelligence—actionable inventory triggers (`SCALE INVENTORY`, `TEST / STOCK`, `HOLD`), recommended price points, and target channels.
- **AI Fashion Intelligence Analyst**: Integrated AI assistant powered by Google Gemini (`@google/genai`), delivering synthesis, demand forecasts, and trend validation with live citations.
- **Multi-Source Signal Ingestion**: Cross-references verified fashion journalism (*The Hindu Life & Style*, *Hindustan Times*, *Vogue India*), search indices, trade reports, and state handloom guilds (*Co-optex*).
- **Dual-Engine Architecture**: Runs as a full-stack Express & TypeScript service with SSE real-time streaming, and compiles into a static single-page bundle for automated **GitHub Pages** deployment with zero 404 errors.

---

## 🏗️ Project Architecture

```
├── .github/
│   └── workflows/
│       └── deploy.yml          # Automated CI/CD GitHub Pages deployment
├── backend/                    # Python ingestion & signal processing pipeline
│   ├── api/                    # FastAPI routes
│   ├── database/               # Supabase / relational schemas
│   ├── jobs/                   # Periodic scrapers and collectors
│   └── services/               # Signal analysis and normalization
├── data/
│   └── trendloom.json          # Seed & verified trend intelligence database
├── frontend/                   # Client-side web application
│   ├── css/                    # Modular stylesheets (style, dashboard, trends, responsive)
│   ├── js/                     # Client application logic & state managers
│   │   ├── api.js              # Centralized API client with offline/static fallback
│   │   ├── app.js              # Entry controller & route dispatcher
│   │   ├── charts.js           # Chart.js trend trajectories & sparklines
│   │   ├── dashboard.js        # KPI cards & live trend board
│   │   ├── forecast.js         # Commercial retail demand forecast views
│   │   ├── realtime.js         # SSE stream listener & static pulse manager
│   │   └── trend-detail.js     # Comprehensive single-trend intelligence dossier
│   ├── index.html              # Live Trend Command Center
│   ├── trends.html             # Trend Explorer & Multi-filter directory
│   ├── trend-detail.html       # Individual Trend Dossier
│   ├── regional.html           # Regional & Tamil Nadu Textile Intelligence
│   └── forecast.html           # Commercial Buying & Inventory Forecast
├── build.js                    # Production compilation script for GitHub Pages
├── server.ts                   # Production Node.js / Express server & Gemini API proxy
├── REPORT.md                   # Detailed technical & market intelligence report
└── package.json                # Project configuration and dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18.0.0 or higher (v20+ or v22 recommended)
- **npm** or **bun**

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eddardthehouesofstark-stack/ai-immersion.git
   cd ai-immersion
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure Environment Variables *(Optional for AI Features)*:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=3000
   ```
   *(Note: TrendLoom runs with comprehensive built-in market intelligence fallbacks even if an API key is not supplied).*

### Running Locally

```bash
# Start the full-stack development server
npm run dev

# Or using the start command
npm start
```
The application will be accessible at `http://localhost:3000`.

---

## 📦 Building for Production & GitHub Pages

To compile the application into a static distribution for deployment:

```bash
npm run build
```

This generates a ready-to-deploy `./dist` directory featuring:
- Normalized relative asset paths for custom subpaths.
- Clean route folders (`/trends/index.html`, `/regional/index.html`, etc.).
- SPA fallback handler `404.html` and `.nojekyll`.
- Pre-compiled static JSON endpoints in `dist/api/`.

---

## 🤖 CI/CD GitHub Actions Deployment

The repository includes an automated workflow at `.github/workflows/deploy.yml`:
1. Whenever code is pushed to the `main` or `master` branch, GitHub Actions builds the project with Node.js 22.
2. The static distribution (`./dist`) is uploaded as a Pages artifact and deployed directly to GitHub Pages.
3. Zero configuration required—ensure **Settings → Pages → Build and deployment → Source** is set to **GitHub Actions**.

---

## 📡 API Endpoints

When running in full-stack mode, the following endpoints are exposed:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status and subsystem checks |
| `GET` | `/api/dashboard/stats` | High-level metrics (active trends, velocity, source counts) |
| `GET` | `/api/trends/live` | Combined live board stats and prioritized trends |
| `GET` | `/api/trends` | Filterable trend catalog (`category`, `region`, `status`, `search`) |
| `GET` | `/api/trends/:id` | Full intelligence dossier for an individual trend |
| `GET` | `/api/regional/:region` | Regional breakdown with fabric, color, and guild insights |
| `GET` | `/api/forecast` | Retail assortment recommendations and demand forecasting |
| `POST` | `/api/intelligence/ask` | Grounded Gemini AI fashion intelligence query |
| `GET` | `/api/realtime/stream` | Server-Sent Events (SSE) live updates stream |

---

## 📄 Documentation

For an in-depth breakdown of the scoring algorithms, data taxonomy, handloom case studies, and engineering architecture, refer to:
👉 **[Technical & Intelligence Report (REPORT.md)](./REPORT.md)**

---

## ⚖️ License

MIT License. Designed and engineered for the AI Immersion Fashion Intelligence Initiative.
