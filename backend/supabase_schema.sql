-- =========================================================
-- TrendLoom Supabase PostgreSQL Schema
-- Real-Time Fashion Trend Intelligence Platform
-- =========================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Trends Table
CREATE TABLE IF NOT EXISTS trends (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    gender TEXT NOT NULL,
    region TEXT NOT NULL,
    trend_score INTEGER NOT NULL CHECK (trend_score >= 0 AND trend_score <= 100),
    growth_rate NUMERIC(6, 2) NOT NULL,
    velocity NUMERIC(6, 2) NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL CHECK (status IN ('EXPLODING', 'RISING', 'STABLE', 'DECLINING', 'FADING')),
    forecast TEXT NOT NULL,
    confidence INTEGER NOT NULL CHECK (confidence >= 0 AND confidence <= 100),
    description TEXT NOT NULL,
    image_url TEXT,
    source_count INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Trend Attributes Table
CREATE TABLE IF NOT EXISTS trend_attributes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_id TEXT REFERENCES trends(id) ON DELETE CASCADE,
    attribute_type TEXT NOT NULL, -- e.g. Silhouette, Fabric, Color Palette, Occasion, Cultural Context
    attribute_value TEXT NOT NULL,
    confidence INTEGER NOT NULL DEFAULT 85,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Trend Signals Table
CREATE TABLE IF NOT EXISTS trend_signals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_id TEXT REFERENCES trends(id) ON DELETE CASCADE,
    signal_type TEXT NOT NULL, -- e.g. Search Velocity, Editorial Coverage, Regional Cluster
    signal_strength INTEGER NOT NULL CHECK (signal_strength >= 0 AND signal_strength <= 100),
    signal_value TEXT NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Trend Sources Table
CREATE TABLE IF NOT EXISTS trend_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_id TEXT REFERENCES trends(id) ON DELETE CASCADE,
    source_name TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_type TEXT NOT NULL, -- News, Search, Product, Regional Archive
    published_at TIMESTAMPTZ,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Trend History Observations Table (for real chart generation)
CREATE TABLE IF NOT EXISTS trend_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_id TEXT REFERENCES trends(id) ON DELETE CASCADE,
    observation_date TIMESTAMPTZ NOT NULL,
    recorded_score INTEGER NOT NULL,
    growth_rate NUMERIC(6, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Trend AI Insights Table
CREATE TABLE IF NOT EXISTS trend_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_id TEXT REFERENCES trends(id) ON DELETE CASCADE,
    insight_type TEXT NOT NULL, -- why_trending, forecast_analysis, regional_synthesis
    content TEXT NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Retail Recommendations Table
CREATE TABLE IF NOT EXISTS retail_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_id TEXT REFERENCES trends(id) ON DELETE CASCADE,
    action TEXT NOT NULL, -- Scale Inventory, Test / Stock, Monitor
    timing TEXT NOT NULL,
    notes TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. Pipeline Audit Logs Table
CREATE TABLE IF NOT EXISTS pipeline_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type TEXT NOT NULL,
    source TEXT NOT NULL,
    message TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_trends_region ON trends(region);
CREATE INDEX IF NOT EXISTS idx_trends_category ON trends(category);
CREATE INDEX IF NOT EXISTS idx_trends_status ON trends(status);
CREATE INDEX IF NOT EXISTS idx_trends_score ON trends(trend_score DESC);
CREATE INDEX IF NOT EXISTS idx_history_trend_date ON trend_history(trend_id, observation_date ASC);
CREATE INDEX IF NOT EXISTS idx_sources_trend ON trend_sources(trend_id);
