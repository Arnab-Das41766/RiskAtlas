"""
RiskAtlas - Trade Risk Intelligence Dashboard
FastAPI Backend - Enhanced Version with AI Features
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import random

app = FastAPI(
    title="RiskAtlas API",
    description="Trade Risk Intelligence Dashboard API with AI-powered forecasting",
    version="2.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Industry Sectors
INDUSTRIES = [
    "Semiconductors", "Automotive", "Agriculture", "Textiles", 
    "Pharmaceuticals", "Energy", "Electronics", "Raw Materials"
]

# Enhanced Country Data with Industries and Supply Chain Info
COUNTRIES_DATA = {
    "US": {
        "id": "US",
        "name": "United States",
        "risk_score": 45,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 15.5,
        "trade_policy_summary": "Stable trade environment with recent tariff adjustments on tech imports. Strong IP protection laws. CHIPS Act driving domestic semiconductor manufacturing.",
        "headlines": [
            {"title": "US announces 25% tariff on Mexico and Canada via executive order", "source": "Reuters", "date": "2025-02-10", "category": "Tariff", "impact": "high"},
            {"title": "New 10% tariff on Chinese imports takes effect", "source": "Bloomberg", "date": "2025-02-15", "category": "Tariff", "impact": "high"},
            {"title": "Reciprocal Tariff framework (10% global minimum) established", "source": "Trade Monitor", "date": "2025-04-12", "category": "Policy", "impact": "high"},
            {"title": "US imposes 50% tariff on India and Brazil imports", "source": "Commerce Daily", "date": "2025-07-14", "category": "Policy", "impact": "high"}
        ],
        "coordinates": {"lat": 37.0902, "lng": -95.7129},
        "key_industries": ["Semiconductors", "Automotive", "Pharmaceuticals", "Electronics"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 95,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 48, "trend": "increasing", "confidence": 78},
            "6_month": {"score": 52, "trend": "increasing", "confidence": 65},
            "12_month": {"score": 55, "trend": "stable", "confidence": 52}
        }
    },
    "CN": {
        "id": "CN",
        "name": "China",
        "risk_score": 78,
        "risk_level": "High",
        "risk_trend": "increasing",
        "tariff_percentage": 25.0,
        "trade_policy_summary": "Elevated geopolitical tensions affecting trade relations. Increased scrutiny on tech transfers. Currency volatility concerns. Rare earth export controls tightened.",
        "headlines": [
            {"title": "China introduces new export control regulations for dual-use items", "source": "MOFCOM", "date": "2024-10-22", "category": "Regulation", "impact": "high"},
            {"title": "New Dual-Use Items Export Control List published", "source": "China Briefing", "date": "2024-11-15", "category": "Policy", "impact": "high"},
            {"title": "Export controls on advanced semiconductor manufacturing equipment expanded", "source": "Asia Tech", "date": "2024-12-05", "category": "Regulation", "impact": "high"},
            {"title": "US-China agree to extend select tariff reductions through 2026", "source": "Bloomberg Asia", "date": "2025-11-20", "category": "Agreement", "impact": "medium"}
        ],
        "coordinates": {"lat": 35.8617, "lng": 104.1954},
        "key_industries": ["Electronics", "Raw Materials", "Textiles", "Semiconductors"],
        "supply_chain_risk": "High",
        "friend_shore_score": 25,
        "alternative_to": [],
        "alternatives": ["VN", "IN", "MX", "TH"],
        "ai_forecast": {
            "3_month": {"score": 82, "trend": "increasing", "confidence": 85},
            "6_month": {"score": 85, "trend": "increasing", "confidence": 72},
            "12_month": {"score": 80, "trend": "stable", "confidence": 58}
        }
    },
    "DE": {
        "id": "DE",
        "name": "Germany",
        "risk_score": 32,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.5,
        "trade_policy_summary": "Stable EU trade framework. Strong manufacturing sector with predictable regulations. Low corruption risk. Leading automotive and industrial equipment exporter.",
        "headlines": [
            {"title": "Germany pushes for EU-wide supply chain resilience", "source": "EU Trade Journal", "date": "2024-01-15", "category": "Policy", "impact": "medium"},
            {"title": "Automotive industry welcomes new trade pact", "source": "Industry Today", "date": "2024-01-13", "category": "Industry", "impact": "low"},
            {"title": "Green energy transition creates new export opportunities", "source": "Energy Daily", "date": "2024-01-10", "category": "Energy", "impact": "medium"}
        ],
        "coordinates": {"lat": 51.1657, "lng": 10.4515},
        "key_industries": ["Automotive", "Pharmaceuticals", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 90,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 33, "trend": "stable", "confidence": 88},
            "6_month": {"score": 34, "trend": "stable", "confidence": 80},
            "12_month": {"score": 35, "trend": "stable", "confidence": 72}
        }
    },
    "BR": {
        "id": "BR",
        "name": "Brazil",
        "risk_score": 58,
        "risk_level": "Medium",
        "risk_trend": "decreasing",
        "tariff_percentage": 18.0,
        "trade_policy_summary": "Emerging market with currency volatility. Agricultural exports stable but regulatory changes frequent. Moderate political risk. Strengthening Mercosur position.",
        "headlines": [
            {"title": "Brazil pushes for Mercosur-EU agreement finalization", "source": "LatAm Trade", "date": "2024-03-10", "category": "Trade Bloc", "impact": "medium"},
            {"title": "US imposes 50% tariff on Brazilian imports in new trade schedule", "source": "Bloomberg", "date": "2025-07-14", "category": "Tariff", "impact": "high"},
            {"title": "Renewable energy sector attracts record FDI in 2024", "source": "Finance BR", "date": "2024-08-22", "category": "Investment", "impact": "medium"}
        ],
        "coordinates": {"lat": -14.2350, "lng": -51.9253},
        "key_industries": ["Agriculture", "Raw Materials", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 70,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 56, "trend": "decreasing", "confidence": 68},
            "6_month": {"score": 54, "trend": "decreasing", "confidence": 58},
            "12_month": {"score": 52, "trend": "stable", "confidence": 48}
        }
    },
    "IN": {
        "id": "IN",
        "name": "India",
        "risk_score": 52,
        "risk_level": "Medium",
        "risk_trend": "decreasing",
        "tariff_percentage": 22.5,
        "trade_policy_summary": "Growing market with protectionist tendencies. Complex tariff structure but improving ease of doing business. Major beneficiary of China+1 strategy.",
        "headlines": [
            {"title": "India joins US-led initiative for secure technology supply chains", "source": "Business Standard", "date": "2024-01-18", "category": "Policy", "impact": "medium"},
            {"title": "UK-India Free Trade Agreement negotiations enter final round", "source": "BBC News", "date": "2024-02-15", "category": "Agreement", "impact": "high"},
            {"title": "US imposes 50% tariff on Indian imports under secondary trade reviews", "source": "Global Trade Daily", "date": "2025-07-20", "category": "Tariff", "impact": "high"}
        ],
        "coordinates": {"lat": 20.5937, "lng": 78.9629},
        "key_industries": ["Textiles", "Pharmaceuticals", "Electronics", "Automotive"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 85,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 50, "trend": "decreasing", "confidence": 72},
            "6_month": {"score": 48, "trend": "decreasing", "confidence": 62},
            "12_month": {"score": 45, "trend": "stable", "confidence": 52}
        }
    },
    "RU": {
        "id": "RU",
        "name": "Russia",
        "risk_score": 92,
        "risk_level": "Critical",
        "risk_trend": "increasing",
        "tariff_percentage": 35.0,
        "trade_policy_summary": "Severe sanctions regime in place. Extremely high risk for international trade. Limited payment channels. Energy exports diverted to Asia.",
        "headlines": [
            {"title": "New sanctions package affects energy exports", "source": "Geopolitical Risk", "date": "2024-01-16", "category": "Sanctions", "impact": "high"},
            {"title": "Trade diverted to Asian markets increases", "source": "Eurasia Review", "date": "2024-01-14", "category": "Trade Flow", "impact": "medium"},
            {"title": "Currency controls tightened further", "source": "Moscow Finance", "date": "2024-01-12", "category": "Currency", "impact": "high"}
        ],
        "coordinates": {"lat": 61.5240, "lng": 105.3188},
        "key_industries": ["Energy", "Raw Materials"],
        "supply_chain_risk": "Critical",
        "friend_shore_score": 15,
        "alternative_to": [],
        "alternatives": ["SA", "US", "NO", "QA"],
        "ai_forecast": {
            "3_month": {"score": 94, "trend": "increasing", "confidence": 90},
            "6_month": {"score": 95, "trend": "stable", "confidence": 82},
            "12_month": {"score": 90, "trend": "decreasing", "confidence": 65}
        }
    },
    "JP": {
        "id": "JP",
        "name": "Japan",
        "risk_score": 28,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.2,
        "trade_policy_summary": "Highly stable trade environment. Strong rule of law. Low tariff barriers for most goods. Reliable partner. Advanced manufacturing and technology hub.",
        "headlines": [
            {"title": "Japan updates export controls on advanced chip manufacturing equipment", "source": "Nikkei News", "date": "2024-11-11", "category": "Export Control", "impact": "high"},
            {"title": "Investment in domestic semiconductor fabs surges", "source": "Japan Times", "date": "2024-09-13", "category": "Investment", "impact": "low"},
            {"title": "New trade framework discussed with ASEAN partners", "source": "Tech Japan", "date": "2024-12-10", "category": "Diplomacy", "impact": "medium"}
        ],
        "coordinates": {"lat": 36.2048, "lng": 138.2529},
        "key_industries": ["Semiconductors", "Automotive", "Electronics"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 92,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 29, "trend": "stable", "confidence": 90},
            "6_month": {"score": 30, "trend": "stable", "confidence": 85},
            "12_month": {"score": 31, "trend": "stable", "confidence": 78}
        }
    },
    "SA": {
        "id": "SA",
        "name": "Saudi Arabia",
        "risk_score": 48,
        "risk_level": "Medium",
        "risk_trend": "decreasing",
        "tariff_percentage": 12.0,
        "trade_policy_summary": "Vision 2030 driving economic diversification. Oil exports remain dominant. Regional geopolitical considerations. Improving business environment.",
        "headlines": [
            {"title": "Saudi Arabia announces new free trade zone", "source": "Gulf Business", "date": "2024-01-16", "category": "Policy", "impact": "medium"},
            {"title": "Energy exports stable despite regional tensions", "source": "Energy Trade", "date": "2024-01-14", "category": "Energy", "impact": "low"},
            {"title": "Manufacturing sector incentives launched", "source": "Saudi Gazette", "date": "2024-01-12", "category": "Investment", "impact": "medium"}
        ],
        "coordinates": {"lat": 23.8859, "lng": 45.0792},
        "key_industries": ["Energy", "Raw Materials"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 75,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 46, "trend": "decreasing", "confidence": 72},
            "6_month": {"score": 44, "trend": "decreasing", "confidence": 62},
            "12_month": {"score": 42, "trend": "stable", "confidence": 52}
        }
    },
    "VN": {
        "id": "VN",
        "name": "Vietnam",
        "risk_score": 42,
        "risk_level": "Low",
        "risk_trend": "decreasing",
        "tariff_percentage": 14.0,
        "trade_policy_summary": "Major beneficiary of supply chain shift from China. Growing electronics and textile manufacturing hub. Stable political environment.",
        "headlines": [
            {"title": "Electronics exports surge as manufacturers relocate", "source": "Vietnam Business", "date": "2024-01-15", "category": "Industry", "impact": "high"},
            {"title": "New trade agreement with EU takes effect", "source": "Trade Vietnam", "date": "2024-01-13", "category": "Agreement", "impact": "medium"},
            {"title": "Infrastructure investments boost logistics capacity", "source": "Logistics Asia", "date": "2024-01-11", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": 14.0583, "lng": 108.2772},
        "key_industries": ["Electronics", "Textiles"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 88,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 40, "trend": "decreasing", "confidence": 78},
            "6_month": {"score": 38, "trend": "decreasing", "confidence": 68},
            "12_month": {"score": 36, "trend": "stable", "confidence": 58}
        }
    },
    "MX": {
        "id": "MX",
        "name": "Mexico",
        "risk_score": 55,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 12.5,
        "trade_policy_summary": "Nearshoring destination for US companies. USMCA trade agreement provides stability. Automotive and electronics manufacturing growing rapidly.",
        "headlines": [
            {"title": "US imposes 25% tariff on Mexican imports via executive order", "source": "El Universal", "date": "2025-02-10", "category": "Tariff", "impact": "high"},
            {"title": "Nearshoring boom continues as US companies shift manufacturing from Asia", "source": "Mexico News Daily", "date": "2024-11-16", "category": "Investment", "impact": "high"},
            {"title": "EU-Mexico trade agreement update finalized", "source": "Trade Monitor", "date": "2024-05-12", "category": "Agreement", "impact": "medium"}
        ],
        "coordinates": {"lat": 23.6345, "lng": -102.5528},
        "key_industries": ["Automotive", "Electronics", "Agriculture"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 82,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 54, "trend": "stable", "confidence": 75},
            "6_month": {"score": 53, "trend": "stable", "confidence": 68},
            "12_month": {"score": 52, "trend": "stable", "confidence": 58}
        }
    },
    "TH": {
        "id": "TH",
        "name": "Thailand",
        "risk_score": 48,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 13.0,
        "trade_policy_summary": "Established manufacturing hub for electronics and automotive. Stable political environment. Strong logistics infrastructure in Southeast Asia.",
        "headlines": [
            {"title": "EV manufacturing investments accelerate", "source": "Thai Business", "date": "2024-01-15", "category": "Investment", "impact": "high"},
            {"title": "Digital economy promotion scheme launched", "source": "Tech Thailand", "date": "2024-01-13", "category": "Policy", "impact": "medium"},
            {"title": "Regional logistics hub status strengthened", "source": "ASEAN Trade", "date": "2024-01-11", "category": "Industry", "impact": "low"}
        ],
        "coordinates": {"lat": 15.8700, "lng": 100.9925},
        "key_industries": ["Automotive", "Electronics", "Agriculture"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 80,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 47, "trend": "stable", "confidence": 76},
            "6_month": {"score": 46, "trend": "stable", "confidence": 68},
            "12_month": {"score": 45, "trend": "stable", "confidence": 58}
        }
    },
    "TW": {
        "id": "TW",
        "name": "Taiwan",
        "risk_score": 65,
        "risk_level": "Medium",
        "risk_trend": "increasing",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Critical semiconductor manufacturing hub. Geopolitical tensions create uncertainty. World-leading chip foundry operations.",
        "headlines": [
            {"title": "TSMC announces new overseas fab locations", "source": "Semiconductor Daily", "date": "2024-01-16", "category": "Industry", "impact": "high"},
            {"title": "Geopolitical tensions raise supply concerns", "source": "Asia Risk", "date": "2024-01-14", "category": "Geopolitics", "impact": "high"},
            {"title": "Chip export controls discussion continues", "source": "Tech Policy", "date": "2024-01-12", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": 23.6978, "lng": 120.9605},
        "key_industries": ["Semiconductors", "Electronics"],
        "supply_chain_risk": "High",
        "friend_shore_score": 70,
        "alternative_to": [],
        "alternatives": ["KR", "US", "JP"],
        "ai_forecast": {
            "3_month": {"score": 68, "trend": "increasing", "confidence": 72},
            "6_month": {"score": 70, "trend": "increasing", "confidence": 62},
            "12_month": {"score": 72, "trend": "stable", "confidence": 52}
        }
    },
    "KR": {
        "id": "KR",
        "name": "South Korea",
        "risk_score": 38,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 9.5,
        "trade_policy_summary": "Advanced technology and semiconductor manufacturing. Stable democracy. Strong IP protection. Major chip and display producer.",
        "headlines": [
            {"title": "Chip Act support boosts domestic production", "source": "Korea Herald", "date": "2024-01-15", "category": "Policy", "impact": "medium"},
            {"title": "Battery manufacturing capacity expands", "source": "Energy Korea", "date": "2024-01-13", "category": "Industry", "impact": "medium"},
            {"title": "New trade agreements with Southeast Asia", "source": "Trade Korea", "date": "2024-01-11", "category": "Agreement", "impact": "low"}
        ],
        "coordinates": {"lat": 35.9078, "lng": 127.7669},
        "key_industries": ["Semiconductors", "Electronics", "Automotive"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 88,
        "alternative_to": ["TW", "CN"],
        "ai_forecast": {
            "3_month": {"score": 37, "trend": "stable", "confidence": 85},
            "6_month": {"score": 36, "trend": "stable", "confidence": 78},
            "12_month": {"score": 35, "trend": "stable", "confidence": 70}
        }
    },
    "GB": {
        "id": "GB",
        "name": "United Kingdom",
        "risk_score": 35,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 7.0,
        "trade_policy_summary": "Post-Brexit trade framework stabilizing. Strong services sector and growing tech ecosystem. Predictable regulatory environment.",
        "headlines": [
            {"title": "UK-India Free Trade Agreement negotiations finalize", "source": "Financial Times", "date": "2024-02-15", "category": "Agreement", "impact": "high"},
            {"title": "UK joins CPTPP trade bloc to boost Indo-Pacific trade", "source": "BBC News", "date": "2024-01-20", "category": "Diplomacy", "impact": "medium"},
            {"title": "New regulatory framework for AI and tech startups launched", "source": "London Biz", "date": "2024-03-12", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": 55.3781, "lng": -3.4360},
        "key_industries": ["Pharmaceuticals", "Energy", "Electronics"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 90,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 36, "trend": "stable", "confidence": 88},
            "6_month": {"score": 37, "trend": "stable", "confidence": 80},
            "12_month": {"score": 38, "trend": "stable", "confidence": 72}
        }
    },
    "FR": {
        "id": "FR",
        "name": "France",
        "risk_score": 30,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Stable EU member with strong industrial base. Focus on strategic autonomy in energy and pharmaceuticals.",
        "headlines": [
            {"title": "France expands strategic autonomy initiatives in pharmaceuticals", "source": "Le Monde", "date": "2024-03-15", "category": "Policy", "impact": "medium"},
            {"title": "New EU-wide dual-use export control regime supported by France", "source": "Paris Trade", "date": "2025-09-13", "category": "Regulation", "impact": "medium"},
            {"title": "Green hydrogen infrastructure project hits massive milestone", "source": "Energy Daily", "date": "2024-11-10", "category": "Investment", "impact": "medium"}
        ],
        "coordinates": {"lat": 46.2276, "lng": 2.2137},
        "key_industries": ["Pharmaceuticals", "Automotive", "Energy", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 95,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 31, "trend": "stable", "confidence": 92},
            "6_month": {"score": 32, "trend": "stable", "confidence": 85},
            "12_month": {"score": 33, "trend": "stable", "confidence": 75}
        }
    },
    "CA": {
        "id": "CA",
        "name": "Canada",
        "risk_score": 25,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 6.5,
        "trade_policy_summary": "Stable USMCA partner. Strong natural resource exporter. Reliable regulatory framework and high supply chain resilience.",
        "headlines": [
            {"title": "US 25% tariff on Canadian imports takes effect via executive order", "source": "Global News", "date": "2025-02-10", "category": "Tariff", "impact": "high"},
            {"title": "Canada implements 25% surtax on steel derivative goods", "source": "Canada Trade Bureau", "date": "2025-12-05", "category": "Tariff", "impact": "high"},
            {"title": "Critical minerals partnership expanded with US and Australia", "source": "Globe and Mail", "date": "2024-03-16", "category": "Agreement", "impact": "medium"}
        ],
        "coordinates": {"lat": 56.1304, "lng": -106.3468},
        "key_industries": ["Raw Materials", "Energy", "Automotive"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 98,
        "alternative_to": ["RU", "CN"],
        "ai_forecast": {
            "3_month": {"score": 26, "trend": "stable", "confidence": 95},
            "6_month": {"score": 27, "trend": "stable", "confidence": 88},
            "12_month": {"score": 28, "trend": "stable", "confidence": 78}
        }
    },
    "AU": {
        "id": "AU",
        "name": "Australia",
        "risk_score": 28,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Major commodity exporter. Stable legal system. Pivoting trade relations toward SE Asia and strengthening links with US/UK.",
        "headlines": [
            {"title": "Australia expands critical minerals partnership with US and UK", "source": "ABC News", "date": "2024-03-12", "category": "Agreement", "impact": "high"},
            {"title": "Trade barriers on Australian wine and barley removed by China", "source": "Sydney Morning Herald", "date": "2024-04-15", "category": "Diplomacy", "impact": "high"},
            {"title": "New green hydrogen export strategy launched", "source": "The Age", "date": "2024-11-20", "category": "Energy", "impact": "medium"}
        ],
        "coordinates": {"lat": -25.2744, "lng": 133.7751},
        "key_industries": ["Raw Materials", "Energy", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 94,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 29, "trend": "stable", "confidence": 92},
            "6_month": {"score": 30, "trend": "stable", "confidence": 85},
            "12_month": {"score": 31, "trend": "stable", "confidence": 75}
        }
    },
    "SG": {
        "id": "SG",
        "name": "Singapore",
        "risk_score": 20,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 0.0,
        "trade_policy_summary": "Global trade and finance hub. Highly efficient logistics and low regulatory risk. Strategic location for SE Asian trade.",
        "headlines": [
            {"title": "Port of Singapore breaks container throughput record", "source": "Straits Times", "date": "2024-01-16", "category": "Logistics", "impact": "medium"},
            {"title": "FinTech investments surge in early 2024", "source": "Business Times", "date": "2024-01-14", "category": "Investment", "impact": "low"},
            {"title": "Digital economy agreement signed with ASEAN", "source": "CNA", "date": "2024-01-12", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": 1.3521, "lng": 103.8198},
        "key_industries": ["Electronics", "Pharmaceuticals", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 96,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 21, "trend": "stable", "confidence": 98},
            "6_month": {"score": 22, "trend": "stable", "confidence": 92},
            "12_month": {"score": 23, "trend": "stable", "confidence": 85}
        }
    },
    "AE": {
        "id": "AE",
        "name": "UAE",
        "risk_score": 35,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Diversifying economy away from oil. Strategic trade gateway between East and West. Stable business environment.",
        "headlines": [
            {"title": "Non-oil trade reaches historic high", "source": "WAM", "date": "2024-01-15", "category": "Economy", "impact": "medium"},
            {"title": "New trade corridor agreement with India progressed", "source": "Gulf News", "date": "2024-01-13", "category": "Diplomacy", "impact": "medium"},
            {"title": "AI research hub expanded in Abu Dhabi", "source": "Khaleej Times", "date": "2024-01-11", "category": "Policy", "impact": "low"}
        ],
        "coordinates": {"lat": 23.4241, "lng": 53.8478},
        "key_industries": ["Energy", "Electronics", "Pharmaceuticals"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 85,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 36, "trend": "stable", "confidence": 90},
            "6_month": {"score": 37, "trend": "stable", "confidence": 85},
            "12_month": {"score": 38, "trend": "stable", "confidence": 75}
        }
    },
    "ID": {
        "id": "ID",
        "name": "Indonesia",
        "risk_score": 55,
        "risk_level": "Medium",
        "risk_trend": "decreasing",
        "tariff_percentage": 15.0,
        "trade_policy_summary": "Rich in natural resources, especially nickel for EV batteries. Improving infrastructure but regulatory complexity remains high.",
        "headlines": [
            {"title": "Nickel export ban drives downstream investment", "source": "Jakarta Post", "date": "2024-01-15", "category": "Raw Materials", "impact": "high"},
            {"title": "New capital city project attracts foreign interest", "source": "Tempo", "date": "2024-01-13", "category": "Investment", "impact": "medium"},
            {"title": "Tech sector growth continues despite global slowdown", "source": "DealStreetAsia", "date": "2024-01-11", "category": "Industry", "impact": "low"}
        ],
        "coordinates": {"lat": -0.7893, "lng": 113.9213},
        "key_industries": ["Raw Materials", "Energy", "Agriculture", "Textiles"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 75,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 53, "trend": "decreasing", "confidence": 80},
            "6_month": {"score": 51, "trend": "decreasing", "confidence": 70},
            "12_month": {"score": 48, "trend": "stable", "confidence": 60}
        }
    },
    "ZA": {
        "id": "ZA",
        "name": "South Africa",
        "risk_score": 62,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 12.0,
        "trade_policy_summary": "Key entry point to African markets. Infrastructure challenges (energy, logistics) affect export efficiency. Strong legal framework.",
        "headlines": [
            {"title": "Energy grid stability efforts show progress", "source": "Fin24", "date": "2024-01-15", "category": "Energy", "impact": "medium"},
            {"title": "Logistics bottlenecks at ports affect mining exports", "source": "Reuters SA", "date": "2024-01-13", "category": "Logistics", "impact": "high"},
            {"title": "Automotive manufacturing incentives extended", "source": "Business Day", "date": "2024-01-11", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": -30.5595, "lng": 22.9375},
        "key_industries": ["Raw Materials", "Automotive", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 65,
        "alternative_to": ["CN", "RU"],
        "ai_forecast": {
            "3_month": {"score": 63, "trend": "stable", "confidence": 75},
            "6_month": {"score": 64, "trend": "increasing", "confidence": 65},
            "12_month": {"score": 60, "trend": "decreasing", "confidence": 50}
        }
    },
    "IT": {
        "id": "IT",
        "name": "Italy",
        "risk_score": 40,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Strong manufacturing tradition, particularly in luxury goods, automotive, and pharmaceuticals. Reliable EU partner.",
        "headlines": [
            {"title": "Luxury exports reach pre-pandemic levels", "source": "Il Sole 24 Ore", "date": "2024-01-15", "category": "Industry", "impact": "low"},
            {"title": "Pharmaceutical exports surge in Q4", "source": "ANSA", "date": "2024-01-13", "category": "Pharmaceuticals", "impact": "medium"},
            {"title": "New solar energy park announced in Sicily", "source": "Corriere della Sera", "date": "2024-01-11", "category": "Energy", "impact": "low"}
        ],
        "coordinates": {"lat": 41.8719, "lng": 12.5674},
        "key_industries": ["Pharmaceuticals", "Automotive", "Textiles", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 90,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 41, "trend": "stable", "confidence": 88},
            "6_month": {"score": 42, "trend": "stable", "confidence": 80},
            "12_month": {"score": 43, "trend": "stable", "confidence": 70}
        }
    },
    "ES": {
        "id": "ES",
        "name": "Spain",
        "risk_score": 35,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Growing hub for renewable energy and digital services. Major agricultural exporter within the EU.",
        "headlines": [
            {"title": "Green hydrogen project receives EU funding", "source": "El Pais", "date": "2024-01-16", "category": "Energy", "impact": "medium"},
            {"title": "Tech talent migration boosts Barcelona tech hub", "source": "The Local", "date": "2024-01-14", "category": "Investment", "impact": "low"},
            {"title": "Drought affects olive oil export forecasts", "source": "AgriNews", "date": "2024-01-12", "category": "Agriculture", "impact": "high"}
        ],
        "coordinates": {"lat": 40.4637, "lng": -3.7492},
        "key_industries": ["Energy", "Agriculture", "Automotive", "Textiles"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 92,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 36, "trend": "stable", "confidence": 90},
            "6_month": {"score": 37, "trend": "stable", "confidence": 82},
            "12_month": {"score": 38, "trend": "stable", "confidence": 72}
        }
    },
    "NL": {
        "id": "NL",
        "name": "Netherlands",
        "risk_score": 18,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Critical global logistics hub via Port of Rotterdam. Extremely stable with world-class infrastructure.",
        "headlines": [
            {"title": "Rotterdam Port expands smart terminal capacity", "source": "Port Insider", "date": "2024-01-15", "category": "Logistics", "impact": "medium"},
            {"title": "ASML reports strong demand for chip equipment", "source": "NL Times", "date": "2024-01-13", "category": "Semiconductors", "impact": "high"},
            {"title": "New sustainable agriculture tech exported globally", "source": "Wageningen News", "date": "2024-01-11", "category": "Agriculture", "impact": "low"}
        ],
        "coordinates": {"lat": 52.1326, "lng": 5.2913},
        "key_industries": ["Semiconductors", "Agriculture", "Energy", "Pharmaceuticals"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 97,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 19, "trend": "stable", "confidence": 99},
            "6_month": {"score": 20, "trend": "stable", "confidence": 95},
            "12_month": {"score": 21, "trend": "stable", "confidence": 88}
        }
    },
    "AR": {
        "id": "AR",
        "name": "Argentina",
        "risk_score": 75,
        "risk_level": "High",
        "risk_trend": "decreasing",
        "tariff_percentage": 20.0,
        "trade_policy_summary": "Economic reforms underway to stabilize currency and reduce debt. Rich in lithium and agricultural commodities.",
        "headlines": [
            {"title": "Lithium production capacity expands for EV market", "source": "LatAm Mining", "date": "2024-01-16", "category": "Raw Materials", "impact": "high"},
            {"title": "New economic measures aim to reduce inflation", "source": "BA Times", "date": "2024-01-14", "category": "Economy", "impact": "medium"},
            {"title": "Soybean harvest outlook improves following rains", "source": "AgroArgentina", "date": "2024-01-12", "category": "Agriculture", "impact": "medium"}
        ],
        "coordinates": {"lat": -38.4161, "lng": -63.6167},
        "key_industries": ["Agriculture", "Raw Materials", "Energy"],
        "supply_chain_risk": "High",
        "friend_shore_score": 60,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 72, "trend": "decreasing", "confidence": 70},
            "6_month": {"score": 68, "trend": "decreasing", "confidence": 60},
            "12_month": {"score": 60, "trend": "stable", "confidence": 45}
        }
    },
    "TR": {
        "id": "TR",
        "name": "Turkey",
        "risk_score": 60,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 13.5,
        "trade_policy_summary": "Strategic bridge between Europe and Asia. Strong automotive and textile exporter. Complex economic environment.",
        "headlines": [
            {"title": "Automotive exports reach new peaks in Q4", "source": "Daily Sabah", "date": "2024-01-15", "category": "Industry", "impact": "medium"},
            {"title": "New logistics hub opened on Mediterranean coast", "source": "Trade News TR", "date": "2024-01-13", "category": "Logistics", "impact": "low"},
            {"title": "Economic policy shift aims for stability", "source": "Hurriyet Daily", "date": "2024-01-11", "category": "Economy", "impact": "medium"}
        ],
        "coordinates": {"lat": 38.9637, "lng": 35.2433},
        "key_industries": ["Automotive", "Textiles", "Raw Materials"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 70,
        "alternative_to": ["CN", "RU"],
        "ai_forecast": {
            "3_month": {"score": 61, "trend": "stable", "confidence": 82},
            "6_month": {"score": 62, "trend": "stable", "confidence": 75},
            "12_month": {"score": 58, "trend": "decreasing", "confidence": 60}
        }
    },
    "MY": {
        "id": "MY",
        "name": "Malaysia",
        "risk_score": 45,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 10.0,
        "trade_policy_summary": "Core hub for semiconductor backend operations. Stable democracy with business-friendly policies.",
        "headlines": [
            {"title": "Semiconductor testing facilities expand in Penang", "source": "The Star", "date": "2024-01-16", "category": "Semiconductors", "impact": "high"},
            {"title": "New digital hub initiatives launched", "source": "Malaysian Business", "date": "2024-01-14", "category": "Investment", "impact": "medium"},
            {"title": "Renewable energy exports to Singapore progress", "source": "Edge Markets", "date": "2024-01-12", "category": "Energy", "impact": "low"}
        ],
        "coordinates": {"lat": 4.2105, "lng": 101.9758},
        "key_industries": ["Semiconductors", "Electronics", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 85,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 46, "trend": "stable", "confidence": 85},
            "6_month": {"score": 47, "trend": "stable", "confidence": 78},
            "12_month": {"score": 45, "trend": "stable", "confidence": 65}
        }
    },
    "CH": {
        "id": "CH",
        "name": "Switzerland",
        "risk_score": 15,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 4.0,
        "trade_policy_summary": "Highly stable neutral state with premium export focus. Global leader in pharmaceuticals and precision engineering.",
        "headlines": [
            {"title": "Swiss precision exports reach record levels", "source": "Swissinfo", "date": "2024-01-16", "category": "Economy", "impact": "low"},
            {"title": "Pharma giants announce new R&D investments", "source": "NZZ", "date": "2024-01-14", "category": "Pharmaceuticals", "impact": "medium"},
            {"title": "Digital banking regulations updated", "source": "Finews", "date": "2024-01-11", "category": "Finance", "impact": "low"}
        ],
        "coordinates": {"lat": 46.8182, "lng": 8.2275},
        "key_industries": ["Pharmaceuticals", "Electronics", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 99,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 15, "trend": "stable", "confidence": 98},
            "6_month": {"score": 16, "trend": "stable", "confidence": 92},
            "12_month": {"score": 16, "trend": "stable", "confidence": 85}
        }
    },
    "NO": {
        "id": "NO",
        "name": "Norway",
        "risk_score": 18,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Major energy exporter. High supply chain stability and low political risk. Strong focus on green transition and EV adoption.",
        "headlines": [
            {"title": "Offshore wind capacity reaches new milestone", "source": "Energy Norway", "date": "2024-01-16", "category": "Energy", "impact": "medium"},
            {"title": "Energy exports to EU increase following winter demand", "source": "Aftenposten", "date": "2024-01-14", "category": "Economy", "impact": "low"},
            {"title": "Sovereign wealth fund hits record value", "source": "Reuters", "date": "2024-01-12", "category": "Finance", "impact": "low"}
        ],
        "coordinates": {"lat": 60.4720, "lng": 8.4689},
        "key_industries": ["Energy", "Raw Materials", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 97,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 18, "trend": "stable", "confidence": 98},
            "6_month": {"score": 19, "trend": "stable", "confidence": 92},
            "12_month": {"score": 20, "trend": "stable", "confidence": 85}
        }
    },
    "SE": {
        "id": "SE",
        "name": "Sweden",
        "risk_score": 20,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 6.0,
        "trade_policy_summary": "Innovative economy with strong industrial and tech sectors. High digital integration and trade openness.",
        "headlines": [
            {"title": "Green steel production ramps up with new fab", "source": "Nordic Business", "date": "2024-01-15", "category": "Industry", "impact": "high"},
            {"title": "Tech unicorns see valuation stability in 2024", "source": "Tech Stockholm", "date": "2024-01-13", "category": "Investment", "impact": "low"},
            {"title": "Defense exports surge amid regional security focus", "source": "Defense News", "date": "2024-01-11", "category": "Industry", "impact": "medium"}
        ],
        "coordinates": {"lat": 60.1282, "lng": 18.6435},
        "key_industries": ["Automotive", "Electronics", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 96,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 21, "trend": "stable", "confidence": 95},
            "6_month": {"score": 22, "trend": "stable", "confidence": 88},
            "12_month": {"score": 23, "trend": "stable", "confidence": 80}
        }
    },
    "PL": {
        "id": "PL",
        "name": "Poland",
        "risk_score": 42,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Major manufacturing hub in Central Europe. Diversifying energy sources and investing heavily in defense and automotive sectors.",
        "headlines": [
            {"title": "EV battery production capacity hits record highs", "source": "PTE", "date": "2024-01-16", "category": "Automotive", "impact": "high"},
            {"title": "Defense manufacturing contracts expanded", "source": "Defense Poland", "date": "2024-01-14", "category": "Industry", "impact": "medium"},
            {"title": "Agri-exports to EU remain key economic driver", "source": "AgroNews", "date": "2024-01-11", "category": "Agriculture", "impact": "low"}
        ],
        "coordinates": {"lat": 51.9194, "lng": 19.1451},
        "key_industries": ["Automotive", "Agriculture", "Electronics"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 92,
        "alternative_to": ["RU", "CN"],
        "ai_forecast": {
            "3_month": {"score": 43, "trend": "stable", "confidence": 85},
            "6_month": {"score": 44, "trend": "stable", "confidence": 78},
            "12_month": {"score": 40, "trend": "decreasing", "confidence": 65}
        }
    },
    "UA": {
        "id": "UA",
        "name": "Ukraine",
        "risk_score": 85,
        "risk_level": "High",
        "risk_trend": "stable",
        "tariff_percentage": 10.0,
        "trade_policy_summary": "Wartime economy with focused corridors for grain and iron exports. Heavy Reliance on international support.",
        "headlines": [
            {"title": "Black Sea grain corridor throughput remains stable", "source": "UA Trade", "date": "2024-01-16", "category": "Agriculture", "impact": "medium"},
            {"title": "Tech sector demonstrates strong resilience", "source": "Kyiv Tech", "date": "2024-01-14", "category": "Economy", "impact": "low"},
            {"title": "Reconstruction contracts attract early investment", "source": "Intl Finance", "date": "2024-01-12", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": 48.3794, "lng": 31.1656},
        "key_industries": ["Agriculture", "Raw Materials", "Energy"],
        "supply_chain_risk": "High",
        "friend_shore_score": 80,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 86, "trend": "increasing", "confidence": 65},
            "6_month": {"score": 82, "trend": "decreasing", "confidence": 55},
            "12_month": {"score": 75, "trend": "decreasing", "confidence": 42}
        }
    },
    "BE": {
        "id": "BE",
        "name": "Belgium",
        "risk_score": 22,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Logistics and chemical hub for Europe. Open trade environment with world-class ports.",
        "headlines": [
            {"title": "Port of Antwerp-Bruges merges digital systems", "source": "Logistics BE", "date": "2024-01-15", "category": "Logistics", "impact": "medium"},
            {"title": "Chemical sector R&D boosted by new incentives", "source": "Biz Brussels", "date": "2024-01-13", "category": "Pharmaceuticals", "impact": "low"},
            {"title": "Energy transition strategy updated for 2024", "source": "Belga", "date": "2024-01-10", "category": "Energy", "impact": "medium"}
        ],
        "coordinates": {"lat": 50.5039, "lng": 4.4699},
        "key_industries": ["Pharmaceuticals", "Energy", "Automotive"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 96,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 23, "trend": "stable", "confidence": 95},
            "6_month": {"score": 24, "trend": "stable", "confidence": 88},
            "12_month": {"score": 25, "trend": "stable", "confidence": 80}
        }
    },
    "PT": {
        "id": "PT",
        "name": "Portugal",
        "risk_score": 32,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Expanding tech hub and renewable energy leader. Strategic gateway to Atlantic trade corridors.",
        "headlines": [
            {"title": "Renewable energy production hits 70% of grid", "source": "Público", "date": "2024-01-16", "category": "Energy", "impact": "high"},
            {"title": "Digital nomad visa scheme boosts services economy", "source": "Lisbon Journal", "date": "2024-01-14", "category": "Investment", "impact": "low"},
            {"title": "New deep-water port terminal project update", "source": "Trade PT", "date": "2024-01-11", "category": "Logistics", "impact": "medium"}
        ],
        "coordinates": {"lat": 39.3999, "lng": -8.2245},
        "key_industries": ["Energy", "Textiles", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 93,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 33, "trend": "stable", "confidence": 90},
            "6_month": {"score": 34, "trend": "stable", "confidence": 82},
            "12_month": {"score": 35, "trend": "stable", "confidence": 75}
        }
    },
    "PH": {
        "id": "PH",
        "name": "Philippines",
        "risk_score": 58,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 18.5,
        "trade_policy_summary": "Rising electronics manufacturing as part of China+1. Large services sector and strategic Pacific location.",
        "headlines": [
            {"title": "Semiconductor assembly exports increase by 12%", "source": "Manila Times", "date": "2024-01-16", "category": "Industry", "impact": "high"},
            {"title": "Infrastructure spending focused on ports and rail", "source": "PhilStar", "date": "2024-01-14", "category": "Logistics", "impact": "medium"},
            {"title": "New trade pact proposed with EU", "source": "BusinessWorld", "date": "2024-01-12", "category": "Agreement", "impact": "medium"}
        ],
        "coordinates": {"lat": 12.8797, "lng": 121.7740},
        "key_industries": ["Electronics", "Agriculture", "Semiconductors"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 82,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 57, "trend": "stable", "confidence": 78},
            "6_month": {"score": 55, "trend": "decreasing", "confidence": 68},
            "12_month": {"score": 52, "trend": "stable", "confidence": 58}
        }
    },
    "DE": {
        "id": "DE",
        "name": "Germany",
        "risk_score": 25,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Europe's largest economy, strong manufacturing and export base. High regulatory stability and advanced infrastructure.",
        "headlines": [
            {"title": "Germany updates export control list for high-end manufacturing technology", "source": "Handelsblatt", "date": "2024-12-05", "category": "Export Control", "impact": "medium"},
            {"title": "Industrial production sees recovery as energy prices stabilize", "source": "DW Business", "date": "2024-03-22", "category": "Energy", "impact": "medium"},
            {"title": "New EU-wide trade restrictions supported by German cabinet", "source": "Spiegel", "date": "2024-11-15", "category": "Policy", "impact": "high"}
        ],
        "coordinates": {"lat": 51.1657, "lng": 10.4515},
        "key_industries": ["Automotive", "Electronics", "Pharmaceuticals"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 95,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 26, "trend": "stable", "confidence": 95},
            "6_month": {"score": 27, "trend": "stable", "confidence": 88},
            "12_month": {"score": 28, "trend": "stable", "confidence": 80}
        }
    },
    "PK": {
        "id": "PK",
        "name": "Pakistan",
        "risk_score": 82,
        "risk_level": "High",
        "risk_trend": "increasing",
        "tariff_percentage": 25.0,
        "trade_policy_summary": "Economic instability and high inflation affects trade flows. Large textile sector remains the primary export engine.",
        "headlines": [
            {"title": "Textile exports target new high-end markets", "source": "Dawn Business", "date": "2024-01-15", "category": "Textiles", "impact": "medium"},
            {"title": "IMF review mission arrives for talks", "source": "Express Tribune", "date": "2024-01-13", "category": "Economy", "impact": "high"},
            {"title": "New tech policy aims to boost software exports", "source": "Profit", "date": "2024-01-11", "category": "Policy", "impact": "low"}
        ],
        "coordinates": {"lat": 30.3753, "lng": 69.3451},
        "key_industries": ["Textiles", "Agriculture"],
        "supply_chain_risk": "High",
        "friend_shore_score": 45,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 84, "trend": "increasing", "confidence": 72},
            "6_month": {"score": 86, "trend": "increasing", "confidence": 62},
            "12_month": {"score": 80, "trend": "stable", "confidence": 52}
        }
    },
    "BD": {
        "id": "BD",
        "name": "Bangladesh",
        "risk_score": 68,
        "risk_level": "High",
        "risk_trend": "stable",
        "tariff_percentage": 14.0,
        "trade_policy_summary": "Second largest global garment exporter. Improving infrastructure but challenges in energy supply persist.",
        "headlines": [
            {"title": "RMG exports show growth despite global headwinds", "source": "Daily Star", "date": "2024-01-16", "category": "Textiles", "impact": "medium"},
            {"title": "New economic zones attract Japanese investment", "source": "Financial Express", "date": "2024-01-14", "category": "Investment", "impact": "medium"},
            {"title": "Port capacity expansion at Chittagong updated", "source": "Maritime BD", "date": "2024-01-11", "category": "Logistics", "impact": "low"}
        ],
        "coordinates": {"lat": 23.6850, "lng": 90.3563},
        "key_industries": ["Textiles", "Pharmaceuticals", "Agriculture"],
        "supply_chain_risk": "High",
        "friend_shore_score": 65,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 69, "trend": "stable", "confidence": 75},
            "6_month": {"score": 70, "trend": "stable", "confidence": 65},
            "12_month": {"score": 65, "trend": "decreasing", "confidence": 55}
        }
    },
    "IL": {
        "id": "IL",
        "name": "Israel",
        "risk_score": 52,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 6.0,
        "trade_policy_summary": "High-tech economy with strong focus on cybersecurity and medical tech. Geopolitical situation remains a key risk factor.",
        "headlines": [
            {"title": "Cybersecurity exports reach new annual peak", "source": "Globes", "date": "2024-01-15", "category": "Electronics", "impact": "medium"},
            {"title": "Tech funding remains resilient in Q1", "source": "Calcalist", "date": "2024-01-13", "category": "Investment", "impact": "low"},
            {"title": "New gas export pipelines discussed with Cyprus", "source": "Times of Israel", "date": "2024-01-10", "category": "Energy", "impact": "medium"}
        ],
        "coordinates": {"lat": 31.0461, "lng": 34.8516},
        "key_industries": ["Electronics", "Pharmaceuticals", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 90,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 54, "trend": "increasing", "confidence": 78},
            "6_month": {"score": 50, "trend": "decreasing", "confidence": 68},
            "12_month": {"score": 45, "trend": "stable", "confidence": 55}
        }
    },
    "NZ": {
        "id": "NZ",
        "name": "New Zealand",
        "risk_score": 15,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 4.5,
        "trade_policy_summary": "Stable agricultural exporter with world-leading food safety standards. Reliable and open trade partner.",
        "headlines": [
            {"title": "Dairy exports reach record values in Asian markets", "source": "NZ Herald", "date": "2024-01-16", "category": "Agriculture", "impact": "medium"},
            {"title": "New FTA with UK enters second year with growth", "source": "Radio NZ", "date": "2024-01-14", "category": "Agreement", "impact": "low"},
            {"title": "Agri-tech innovation sector receives state funding", "source": "Otago Times", "date": "2024-01-11", "category": "Policy", "impact": "low"}
        ],
        "coordinates": {"lat": -40.9006, "lng": 174.8860},
        "key_industries": ["Agriculture", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 98,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 15, "trend": "stable", "confidence": 99},
            "6_month": {"score": 16, "trend": "stable", "confidence": 95},
            "12_month": {"score": 16, "trend": "stable", "confidence": 88}
        }
    },
    "CL": {
        "id": "CL",
        "name": "Chile",
        "risk_score": 38,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 10.0,
        "trade_policy_summary": "World's largest copper producer. Stable legal framework in Latin America and committed to free trade.",
        "headlines": [
            {"title": "Lithium state policy review progresses with industry", "source": "La Tercera", "date": "2024-01-16", "category": "Raw Materials", "impact": "high"},
            {"title": "Copper exports target high demand from green energy", "source": "Mining Chile", "date": "2024-01-14", "category": "Economy", "impact": "medium"},
            {"title": "New trade agreements with SE Asia explored", "source": "EMOL", "date": "2024-01-12", "category": "Agreement", "impact": "low"}
        ],
        "coordinates": {"lat": -35.6751, "lng": -71.5430},
        "key_industries": ["Raw Materials", "Agriculture", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 88,
        "alternative_to": ["RU", "CN"],
        "ai_forecast": {
            "3_month": {"score": 39, "trend": "stable", "confidence": 90},
            "6_month": {"score": 37, "trend": "stable", "confidence": 82},
            "12_month": {"score": 35, "trend": "stable", "confidence": 72}
        }
    },
    "CO": {
        "id": "CO",
        "name": "Colombia",
        "risk_score": 60,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 15.0,
        "trade_policy_summary": "Major exporter of oil, coal, and coffee. Infrastructure challenges and political transitions affect trade predictability.",
        "headlines": [
            {"title": "Coffee exports stabilize despite climate challenges", "source": "El Tiempo", "date": "2024-01-15", "category": "Agriculture", "impact": "medium"},
            {"title": "New renewable energy projects announced", "source": "Portafolio", "date": "2024-01-13", "category": "Energy", "impact": "low"},
            {"title": "Infrastructure upgrades boost Pacific port capacity", "source": "Trade CO", "date": "2024-01-10", "category": "Logistics", "impact": "medium"}
        ],
        "coordinates": {"lat": 4.5709, "lng": -74.2973},
        "key_industries": ["Energy", "Raw Materials", "Agriculture"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 75,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 61, "trend": "stable", "confidence": 80},
            "6_month": {"score": 62, "trend": "stable", "confidence": 70},
            "12_month": {"score": 58, "trend": "decreasing", "confidence": 60}
        }
    },
    "PE": {
        "id": "PE",
        "name": "Peru",
        "risk_score": 55,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 12.0,
        "trade_policy_summary": "Major global supplier of copper and silver. Political instability is the primary bottleneck for trade potential.",
        "headlines": [
            {"title": "Mining production grows as project strikes resolve", "source": "Gestion", "date": "2024-01-16", "category": "Raw Materials", "impact": "high"},
            {"title": "Agricultural exports hit record value in 2023", "source": "El Comercio", "date": "2024-01-14", "category": "Agriculture", "impact": "medium"},
            {"title": "New port mega-project in Chancay update", "source": "Andina", "date": "2024-01-11", "category": "Logistics", "impact": "high"}
        ],
        "coordinates": {"lat": -9.1900, "lng": -75.0152},
        "key_industries": ["Raw Materials", "Agriculture"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 70,
        "alternative_to": ["RU", "CN"],
        "ai_forecast": {
            "3_month": {"score": 56, "trend": "stable", "confidence": 78},
            "6_month": {"score": 57, "trend": "stable", "confidence": 68},
            "12_month": {"score": 52, "trend": "stable", "confidence": 55}
        }
    },
    "NG": {
        "id": "NG",
        "name": "Nigeria",
        "risk_score": 78,
        "risk_level": "High",
        "risk_trend": "stable",
        "tariff_percentage": 25.0,
        "trade_policy_summary": "Africa's largest economy. Heavily reliant on oil exports. Diversification efforts ongoing but challenged by currency volatility.",
        "headlines": [
            {"title": "New refinery startup aims to boost local supply", "source": "BusinessDay", "date": "2024-01-16", "category": "Energy", "impact": "high"},
            {"title": "Currency reforms aim to attract foreign investment", "source": "Channels TV", "date": "2024-01-14", "category": "Economy", "impact": "medium"},
            {"title": "Tech ecosystem grows as digital exports climb", "source": "TechCity", "date": "2024-01-11", "category": "Economy", "impact": "low"}
        ],
        "coordinates": {"lat": 9.0820, "lng": 8.6753},
        "key_industries": ["Energy", "Agriculture"],
        "supply_chain_risk": "High",
        "friend_shore_score": 55,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 80, "trend": "increasing", "confidence": 75},
            "6_month": {"score": 75, "trend": "decreasing", "confidence": 65},
            "12_month": {"score": 70, "trend": "stable", "confidence": 52}
        }
    },
    "EG": {
        "id": "EG",
        "name": "Egypt",
        "risk_score": 65,
        "risk_level": "High",
        "risk_trend": "stable",
        "tariff_percentage": 22.0,
        "trade_policy_summary": "Strategic control of Suez Canal. Economic reforms focusing on attracting manufacturing and logistics investment.",
        "headlines": [
            {"title": "Suez Canal revenue records reported for 2023", "source": "Al-Ahram", "date": "2024-01-15", "category": "Logistics", "impact": "medium"},
            {"title": "New green hydrogen hub in Suez Zone update", "source": "Daily News Egypt", "date": "2024-01-13", "category": "Energy", "impact": "low"},
            {"title": "Structural reforms discussed with international lenders", "source": "Egypt Today", "date": "2024-01-11", "category": "Economy", "impact": "medium"}
        ],
        "coordinates": {"lat": 26.8206, "lng": 30.8025},
        "key_industries": ["Energy", "Textiles", "Agriculture"],
        "supply_chain_risk": "High",
        "friend_shore_score": 60,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 67, "trend": "stable", "confidence": 80},
            "6_month": {"score": 63, "trend": "decreasing", "confidence": 70},
            "12_month": {"score": 60, "trend": "stable", "confidence": 60}
        }
    },
    "KE": {
        "id": "KE",
        "name": "Kenya",
        "risk_score": 55,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 20.0,
        "trade_policy_summary": "East Africa's economic hub. World leader in tech innovation (M-Pesa) and major tea and flower exporter.",
        "headlines": [
            {"title": "Tea exports to emerging markets show growth", "source": "The Star", "date": "2024-01-16", "category": "Agriculture", "impact": "low"},
            {"title": "Mombasa port expansion boosts regional trade", "source": "Standard", "date": "2024-01-14", "category": "Logistics", "impact": "medium"},
            {"title": "New energy transition strategy focused on geothermal", "source": "BBC Africa", "date": "2024-01-11", "category": "Energy", "impact": "medium"}
        ],
        "coordinates": {"lat": -1.2864, "lng": 36.8219},
        "key_industries": ["Agriculture", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 80,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 56, "trend": "stable", "confidence": 85},
            "6_month": {"score": 54, "trend": "stable", "confidence": 78},
            "12_month": {"score": 52, "trend": "stable", "confidence": 70}
        }
    },
    "MA": {
        "id": "MA",
        "name": "Morocco",
        "risk_score": 45,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 15.0,
        "trade_policy_summary": "Strategic link between Africa and Europe. Strong automotive and energy base, particularly in phosphate and solar.",
        "headlines": [
            {"title": "Automotive exports become primary trade driver", "source": "Morocco World News", "date": "2024-01-16", "category": "Automotive", "impact": "high"},
            {"title": "World's largest solar plant capacity expanded", "source": "Hespress", "date": "2024-01-14", "category": "Energy", "impact": "medium"},
            {"title": "New trade agreements with EU finalized", "source": "Daily Morocco", "date": "2024-01-12", "category": "Agreement", "impact": "medium"}
        ],
        "coordinates": {"lat": 31.7917, "lng": -7.0926},
        "key_industries": ["Automotive", "Energy", "Raw Materials", "Agriculture"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 85,
        "alternative_to": ["RU", "CN"],
        "ai_forecast": {
            "3_month": {"score": 46, "trend": "stable", "confidence": 88},
            "6_month": {"score": 44, "trend": "stable", "confidence": 80},
            "12_month": {"score": 42, "trend": "stable", "confidence": 72}
        }
    },
    "FI": {
        "id": "FI",
        "name": "Finland",
        "risk_score": 15,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Highly stable Nordic economy with emphasis on technology, forestry, and high-tech manufacturing. NATO membership stabilizing regional risk.",
        "headlines": [
            {"title": "Finland joins NATO-led secure supply chain initiatives", "source": "Helsinki Times", "date": "2024-03-15", "category": "Policy", "impact": "medium"},
            {"title": "Technology sector sees surge in FDI following security upgrades", "source": "Finnish Biz", "date": "2024-11-20", "category": "Investment", "impact": "low"}
        ],
        "coordinates": {"lat": 61.9241, "lng": 25.7482},
        "key_industries": ["Electronics", "Raw Materials", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 98,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 16, "trend": "stable", "confidence": 99},
            "6_month": {"score": 16, "trend": "stable", "confidence": 95},
            "12_month": {"score": 16, "trend": "stable", "confidence": 88}
        }
    },
    "DK": {
        "id": "DK",
        "name": "Denmark",
        "risk_score": 14,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Leading green energy hub with exceptional political stability and highly skilled workforce. Strong logistics through Oresund Bridge.",
        "headlines": [
            {"title": "Denmark implements new maritime trade security protocols", "source": "Copenhagen Post", "date": "2024-04-12", "category": "Regulation", "impact": "medium"},
            {"title": "Green energy partnerships expanded with EU and North Sea neighbors", "source": "Danish Trade Daily", "date": "2024-12-05", "category": "Agreement", "impact": "medium"}
        ],
        "coordinates": {"lat": 56.2639, "lng": 9.5018},
        "key_industries": ["Pharmaceuticals", "Energy", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 99,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 14, "trend": "stable", "confidence": 99},
            "6_month": {"score": 15, "trend": "stable", "confidence": 95},
            "12_month": {"score": 15, "trend": "stable", "confidence": 90}
        }
    },
    "AT": {
        "id": "AT",
        "name": "Austria",
        "risk_score": 18,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 6.5,
        "trade_policy_summary": "Diverse manufacturing and services economy. Central European hub with high logistics performance and legal stability.",
        "headlines": [
            {"title": "Austria aligns with EU modernized dual-use export control regime", "source": "Die Presse", "date": "2025-09-22", "category": "Regulation", "impact": "medium"},
            {"title": "Industrial machinery exports to Central Europe grow 12%", "source": "Austrian Biz", "date": "2024-11-15", "category": "Industry", "impact": "low"}
        ],
        "coordinates": {"lat": 47.5162, "lng": 14.5501},
        "key_industries": ["Electronics", "Automotive", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 97,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 19, "trend": "stable", "confidence": 98},
            "6_month": {"score": 19, "trend": "stable", "confidence": 92},
            "12_month": {"score": 20, "trend": "stable", "confidence": 85}
        }
    },
    "GR": {
        "id": "GR",
        "name": "Greece",
        "risk_score": 48,
        "risk_level": "Medium",
        "risk_trend": "decreasing",
        "tariff_percentage": 9.0,
        "trade_policy_summary": "Major logistics and shipping hub. Improving fiscal position and high strategic importance in Eastern Mediterranean.",
        "headlines": [
            {"title": "Port of Piraeus throughput reaches record high", "source": "Kathimerini", "date": "2024-01-15", "category": "Logistics", "impact": "medium"},
            {"title": "Tourism and energy sector investments surge", "source": "Greece News", "date": "2024-01-13", "category": "Investment", "impact": "medium"},
            {"title": "Digital state reform project shows early result", "source": "ERT", "date": "2024-01-10", "category": "Policy", "impact": "low"}
        ],
        "coordinates": {"lat": 39.0742, "lng": 21.8243},
        "key_industries": ["Energy", "Agriculture", "Raw Materials"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 88,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 46, "trend": "decreasing", "confidence": 85},
            "6_month": {"score": 44, "trend": "decreasing", "confidence": 75},
            "12_month": {"score": 40, "trend": "stable", "confidence": 65}
        }
    },
    "CZ": {
        "id": "CZ",
        "name": "Czechia",
        "risk_score": 28,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 7.0,
        "trade_policy_summary": "Highly industrialized economy, key player in European automotive and electronics supply chains. Very stable regulatory environment.",
        "headlines": [
            {"title": "Automotive exports drive trade surplus", "source": "Prague Post", "date": "2024-01-16", "category": "Automotive", "impact": "medium"},
            {"title": "Tech and AI startup scene expands in Brno", "source": "CZ Radio", "date": "2024-01-14", "category": "Industry", "impact": "low"},
            {"title": "New solar energy projects announced for industry", "source": "Energy CZ", "date": "2024-01-11", "category": "Energy", "impact": "medium"}
        ],
        "coordinates": {"lat": 49.8175, "lng": 15.4730},
        "key_industries": ["Automotive", "Electronics", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 95,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 28, "trend": "stable", "confidence": 95},
            "6_month": {"score": 27, "trend": "stable", "confidence": 88},
            "12_month": {"score": 26, "trend": "decreasing", "confidence": 80}
        }
    },
    "RO": {
        "id": "RO",
        "name": "Romania",
        "risk_score": 52,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 8.5,
        "trade_policy_summary": "Strong growth hub for software and automotive parts in SE Europe. Strategic location for Near-shoring within the EU.",
        "headlines": [
            {"title": "IT sector records highest growth in five years", "source": "Digi24", "date": "2024-01-16", "category": "Technology", "impact": "medium"},
            {"title": "Automotive manufacturing exports to EU surge", "source": "Economica", "date": "2024-01-14", "category": "Automotive", "impact": "medium"},
            {"title": "Offshore gas projects in Black Sea progress", "source": "Adevarul", "date": "2024-01-12", "category": "Energy", "impact": "high"}
        ],
        "coordinates": {"lat": 45.9432, "lng": 24.9668},
        "key_industries": ["Automotive", "Electronics", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 85,
        "alternative_to": ["CN", "RU"],
        "ai_forecast": {
            "3_month": {"score": 53, "trend": "stable", "confidence": 82},
            "6_month": {"score": 50, "trend": "decreasing", "confidence": 72},
            "12_month": {"score": 45, "trend": "decreasing", "confidence": 60}
        }
    },
    "KZ": {
        "id": "KZ",
        "name": "Kazakhstan",
        "risk_score": 65,
        "risk_level": "High",
        "risk_trend": "stable",
        "tariff_percentage": 11.0,
        "trade_policy_summary": "Central Asia's energy giant. Pivoting trade links while balancing regional powers. Major exporter of oil and uranium.",
        "headlines": [
            {"title": "Oil exports via Trans-Caspian route reaching new high", "source": "Astana Times", "date": "2024-01-16", "category": "Energy", "impact": "high"},
            {"title": "Uranium production hits record levels for global supply", "source": "Kazinform", "date": "2024-01-14", "category": "Raw Materials", "impact": "medium"},
            {"title": "New logistics hub development announced", "source": "Trade KZ", "date": "2024-01-11", "category": "Logistics", "impact": "low"}
        ],
        "coordinates": {"lat": 48.0196, "lng": 66.9237},
        "key_industries": ["Energy", "Raw Materials", "Agriculture"],
        "supply_chain_risk": "High",
        "friend_shore_score": 60,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 66, "trend": "stable", "confidence": 78},
            "6_month": {"score": 67, "trend": "increasing", "confidence": 68},
            "12_month": {"score": 60, "trend": "decreasing", "confidence": 55}
        }
    },
    "LK": {
        "id": "LK",
        "name": "Sri Lanka",
        "risk_score": 72,
        "risk_level": "High",
        "risk_trend": "decreasing",
        "tariff_percentage": 22.0,
        "trade_policy_summary": "Recovering economy with strong focus on textile exports and agricultural commodities. Debt restructuring remains critical.",
        "headlines": [
            {"title": "Tea exports show recovery in early 2024", "source": "Ceylon Today", "date": "2024-01-16", "category": "Agriculture", "impact": "medium"},
            {"title": "Garment industries pivot to high-end fashion markets", "source": "Daily FT", "date": "2024-01-14", "category": "Textiles", "impact": "low"},
            {"title": "IMF review shows positive progress on reforms", "source": "Reuters SL", "date": "2024-01-12", "category": "Economy", "impact": "high"}
        ],
        "coordinates": {"lat": 7.8731, "lng": 80.7718},
        "key_industries": ["Textiles", "Agriculture"],
        "supply_chain_risk": "High",
        "friend_shore_score": 65,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 70, "trend": "decreasing", "confidence": 75},
            "6_month": {"score": 65, "trend": "decreasing", "confidence": 65},
            "12_month": {"score": 58, "trend": "stable", "confidence": 50}
        }
    },
    "KH": {
        "id": "KH",
        "name": "Cambodia",
        "risk_score": 64,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 14.5,
        "trade_policy_summary": "Key garment and footwear exporter. Deepening integration into regional SE Asian supply chains.",
        "headlines": [
            {"title": "Cambodia-US Reciprocal Trade Pact signed to eliminate tariffs", "source": "Phnom Penh Post", "date": "2025-10-15", "category": "Agreement", "impact": "high"},
            {"title": "Cambodia agrees to align with US dual-use export controls", "source": "Trade News Asia", "date": "2025-10-20", "category": "Policy", "impact": "medium"},
            {"title": "Textile exports surge as manufacturing diversifies across SE Asia", "source": "Khmer Times", "date": "2024-11-12", "category": "Industry", "impact": "medium"}
        ],
        "coordinates": {"lat": 12.5657, "lng": 104.9910},
        "key_industries": ["Textiles", "Agriculture"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 75,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 65, "trend": "stable", "confidence": 78},
            "6_month": {"score": 63, "trend": "decreasing", "confidence": 68},
            "12_month": {"score": 58, "trend": "stable", "confidence": 55}
        }
    },
    "MN": {
        "id": "MN",
        "name": "Mongolia",
        "risk_score": 58,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 12.0,
        "trade_policy_summary": "Resource-rich economy dependent on mining exports to China. High strategic significance for copper and coal.",
        "headlines": [
            {"title": "Copper exports reach record volumes", "source": "Montsame", "date": "2024-01-16", "category": "Raw Materials", "impact": "high"},
            {"title": "New dry port logistics hub project update", "source": "Mongolia Biz", "date": "2024-01-14", "category": "Logistics", "impact": "low"},
            {"title": "Mining law updates reviewed for better investment", "source": "News MN", "date": "2024-01-12", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": 46.8625, "lng": 103.8467},
        "key_industries": ["Raw Materials", "Agriculture"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 72,
        "alternative_to": ["RU", "CN"],
        "ai_forecast": {
            "3_month": {"score": 59, "trend": "stable", "confidence": 80},
            "6_month": {"score": 57, "trend": "stable", "confidence": 70},
            "12_month": {"score": 52, "trend": "stable", "confidence": 58}
        }
    },
    "PA": {
        "id": "PA",
        "name": "Panama",
        "risk_score": 35,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 9.5,
        "trade_policy_summary": "Critical global trade artery via the Panama Canal. Stable banking and dollarized economy.",
        "headlines": [
            {"title": "Canal water management projects show initial success", "source": "La Prensa", "date": "2024-01-16", "category": "Logistics", "impact": "high"},
            {"title": "Banking sector stability confirmed in early 2024", "source": "Panama Biz", "date": "2024-01-14", "category": "Finance", "impact": "low"},
            {"title": "New free trade zone incentives for tech hub", "source": "News PA", "date": "2024-01-11", "category": "Investment", "impact": "medium"}
        ],
        "coordinates": {"lat": 8.5380, "lng": -80.7821},
        "key_industries": ["Logistics", "Finance", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 90,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 36, "trend": "stable", "confidence": 92},
            "6_month": {"score": 37, "trend": "stable", "confidence": 85},
            "12_month": {"score": 35, "trend": "decreasing", "confidence": 75}
        }
    },
    "CR": {
        "id": "CR",
        "name": "Costa Rica",
        "risk_score": 28,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 8.0,
        "trade_policy_summary": "Highly stable Central American democracy. Hub for high-tech medical device manufacturing and sustainable trade.",
        "headlines": [
            {"title": "Medical device exports become primary trade driver", "source": "La Nacion", "date": "2024-01-15", "category": "Pharmaceuticals", "impact": "high"},
            {"title": "Renewable energy grid stability attracts tech hubs", "source": "Biz Costa Rica", "date": "2024-01-13", "category": "Energy", "impact": "medium"},
            {"title": "Agricultural exports pivot to high-end EU markets", "source": "Trade CR", "date": "2024-01-10", "category": "Agriculture", "impact": "low"}
        ],
        "coordinates": {"lat": 9.7489, "lng": -83.7534},
        "key_industries": ["Pharmaceuticals", "Electronics", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 95,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 29, "trend": "stable", "confidence": 98},
            "6_month": {"score": 28, "trend": "stable", "confidence": 92},
            "12_month": {"score": 26, "trend": "stable", "confidence": 85}
        }
    },
    "EC": {
        "id": "EC",
        "name": "Ecuador",
        "risk_score": 68,
        "risk_level": "High",
        "risk_trend": "stable",
        "tariff_percentage": 18.0,
        "trade_policy_summary": "Oil and agricultural exporter. Security challenges in early 2024 are the primary factor affecting trade confidence.",
        "headlines": [
            {"title": "Shrimp exports maintain global market lead", "source": "El Universo", "date": "2024-01-16", "category": "Agriculture", "impact": "medium"},
            {"title": "New energy project financing secured", "source": "Quito Biz", "date": "2024-01-14", "category": "Energy", "impact": "low"},
            {"title": "Trade corridor security enhanced for exports", "source": "Defense EC", "date": "2024-01-12", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": -1.8312, "lng": -78.1834},
        "key_industries": ["Energy", "Agriculture"],
        "supply_chain_risk": "High",
        "friend_shore_score": 70,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 70, "trend": "increasing", "confidence": 75},
            "6_month": {"score": 65, "trend": "decreasing", "confidence": 65},
            "12_month": {"score": 60, "trend": "stable", "confidence": 50}
        }
    },
    "UY": {
        "id": "UY",
        "name": "Uruguay",
        "risk_score": 22,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 9.0,
        "trade_policy_summary": "Consistently stable and high-income Latin American economy. Leading exporter of agricultural goods and software services.",
        "headlines": [
            {"title": "Software exports hit new record in 2023", "source": "El Pais UY", "date": "2024-01-16", "category": "Technology", "impact": "low"},
            {"title": "New paper mill project ramps up production", "source": "Nordic UY", "date": "2024-01-14", "category": "Industry", "impact": "medium"},
            {"title": "Renewable energy production exceeds targets", "source": "Trade UY", "date": "2024-01-11", "category": "Energy", "impact": "low"}
        ],
        "coordinates": {"lat": -32.5228, "lng": -55.7658},
        "key_industries": ["Agriculture", "Electronics", "Energy"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 96,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 22, "trend": "stable", "confidence": 98},
            "6_month": {"score": 23, "trend": "stable", "confidence": 92},
            "12_month": {"score": 24, "trend": "stable", "confidence": 85}
        }
    },
    "GH": {
        "id": "GH",
        "name": "Ghana",
        "risk_score": 62,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 15.0,
        "trade_policy_summary": "One of West Africa's most stable democracies. Major gold and cocoa exporter undergoing fiscal adjustment.",
        "headlines": [
            {"title": "Ghana signs major trade facilitation agreement with EU", "source": "Ghana News Agency", "date": "2024-03-20", "category": "Agreement", "impact": "medium"},
            {"title": "Gold and cocoa exports hit record revenues in 2024", "source": "Business Ghana", "date": "2024-12-11", "category": "Agriculture", "impact": "medium"},
            {"title": "New digital trade platform launched to streamline customs", "source": "Policy GH", "date": "2024-11-05", "category": "Regulation", "impact": "low"}
        ],
        "coordinates": {"lat": 7.9465, "lng": -1.0232},
        "key_industries": ["Raw Materials", "Agriculture", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 80,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 63, "trend": "stable", "confidence": 82},
            "6_month": {"score": 60, "trend": "decreasing", "confidence": 72},
            "12_month": {"score": 55, "trend": "decreasing", "confidence": 60}
        }
    },
    "ET": {
        "id": "ET",
        "name": "Ethiopia",
        "risk_score": 75,
        "risk_level": "High",
        "risk_trend": "stable",
        "tariff_percentage": 18.0,
        "trade_policy_summary": "Rising manufacturing hub in East Africa. Balancing rapid development with geopolitical stability and currency challenges.",
        "headlines": [
            {"title": "Industrial parks report consistent textile output", "source": "Addis Fortune", "date": "2024-01-15", "category": "Textiles", "impact": "medium"},
            {"title": "New trade corridors planned with Djibouti", "source": "Biz Ethiopia", "date": "2024-01-13", "category": "Logistics", "impact": "high"},
            {"title": "Telecom sector liberalisation enters new phase", "source": "BBC Africa", "date": "2024-01-11", "category": "Policy", "impact": "low"}
        ],
        "coordinates": {"lat": 9.1450, "lng": 40.4897},
        "key_industries": ["Textiles", "Agriculture", "Energy"],
        "supply_chain_risk": "High",
        "friend_shore_score": 65,
        "alternative_to": ["CN"],
        "ai_forecast": {
            "3_month": {"score": 76, "trend": "stable", "confidence": 75},
            "6_month": {"score": 78, "trend": "increasing", "confidence": 65},
            "12_month": {"score": 70, "trend": "decreasing", "confidence": 50}
        }
    },
    "QA": {
        "id": "QA",
        "name": "Qatar",
        "risk_score": 30,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Global leader in LNG exports. Highly stable and high-income state with extremely low business risk.",
        "headlines": [
            {"title": "North Field expansion projects hit massive production milestone", "source": "Qatar Tribune", "date": "2024-01-15", "category": "Energy", "impact": "high"},
            {"title": "Qatar signs new long-term LNG supply deal with Germany and UK", "source": "Reuters", "date": "2024-05-12", "category": "Energy", "impact": "high"},
            {"title": "Non-energy sector grows as Qatar positioning as logistics hub", "source": "Gulf Times", "date": "2024-11-20", "category": "Investment", "impact": "medium"}
        ],
        "coordinates": {"lat": 25.3548, "lng": 51.1839},
        "key_industries": ["Energy", "Pharmaceuticals", "Electronics"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 92,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 31, "trend": "stable", "confidence": 98},
            "6_month": {"score": 32, "trend": "stable", "confidence": 92},
            "12_month": {"score": 33, "trend": "stable", "confidence": 85}
        }
    },
    "KW": {
        "id": "KW",
        "name": "Kuwait",
        "risk_score": 38,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Extremely oil-dependent but wealthy and stable. Significant investment in domestic infrastructure and petrochemical sectors.",
        "headlines": [
            {"title": "New Al Zour refinery ramp-up boosts global export capacity", "source": "KUNA", "date": "2024-01-16", "category": "Energy", "impact": "medium"},
            {"title": "Kuwait updates economic diversification roadmap focusing on logistics", "source": "Kuwait Times", "date": "2024-11-14", "category": "Policy", "impact": "medium"}
        ],
        "coordinates": {"lat": 29.3117, "lng": 47.4818},
        "key_industries": ["Energy", "Pharmaceuticals"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 88,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 39, "trend": "stable", "confidence": 95},
            "6_month": {"score": 40, "trend": "stable", "confidence": 88},
            "12_month": {"score": 38, "trend": "stable", "confidence": 80}
        }
    },
    "OM": {
        "id": "OM",
        "name": "Oman",
        "risk_score": 40,
        "risk_level": "Low",
        "risk_trend": "stable",
        "tariff_percentage": 5.0,
        "trade_policy_summary": "Strategically located at the mouth of the Persian Gulf. Focus on becoming a global logistics and green hydrogen hub.",
        "headlines": [
            {"title": "Duqm special economic zone attracts new global firms", "source": "Oman Observer", "date": "2024-01-15", "category": "Investment", "impact": "medium"},
            {"title": "Green hydrogen projects enter second phase of development", "source": "Muscat Daily", "date": "2024-01-13", "category": "Energy", "impact": "high"},
            {"title": "Non-oil exports show 8% increase in Q4", "source": "Trade OM", "date": "2024-01-11", "category": "Economy", "impact": "low"}
        ],
        "coordinates": {"lat": 21.4735, "lng": 55.9754},
        "key_industries": ["Energy", "Logistics", "Agriculture"],
        "supply_chain_risk": "Low",
        "friend_shore_score": 90,
        "alternative_to": ["RU"],
        "ai_forecast": {
            "3_month": {"score": 41, "trend": "stable", "confidence": 95},
            "6_month": {"score": 42, "trend": "stable", "confidence": 88},
            "12_month": {"score": 40, "trend": "stable", "confidence": 80}
        }
    },
    "JO": {
        "id": "JO",
        "name": "Jordan",
        "risk_score": 52,
        "risk_level": "Medium",
        "risk_trend": "stable",
        "tariff_percentage": 10.0,
        "trade_policy_summary": "Highly stable regional partner with strong focus on pharmaceutical and tech services. Key player in regional energy and water security.",
        "headlines": [
            {"title": "Pharma exports reach new MENA markets", "source": "Jordan Times", "date": "2024-01-16", "category": "Pharmaceuticals", "impact": "medium"},
            {"title": "Tech startup ecosystem sees record early-stage funding", "source": "Amman Biz", "date": "2024-01-14", "category": "Investment", "impact": "low"},
            {"title": "Strategic trade agreements with US and EU expanded", "source": "Policy JO", "date": "2024-01-12", "category": "Agreement", "impact": "medium"}
        ],
        "coordinates": {"lat": 30.5852, "lng": 36.2384},
        "key_industries": ["Pharmaceuticals", "Electronics", "Energy"],
        "supply_chain_risk": "Medium",
        "friend_shore_score": 85,
        "alternative_to": [],
        "ai_forecast": {
            "3_month": {"score": 53, "trend": "stable", "confidence": 88},
            "6_month": {"score": 54, "trend": "stable", "confidence": 80},
            "12_month": {"score": 52, "trend": "stable", "confidence": 72}
        }
    }
}

# Policy Alerts Data
POLICY_ALERTS = [
    {
        "id": 1,
        "title": "US 25% Tariff on Canada and Mexico",
        "country": "US",
        "category": "Tariff",
        "impact": "High",
        "date": "2025-02-10",
        "description": "Executive order imposes 25% tariffs on most products from Canada and Mexico, with 10% on energy products.",
        "affected_industries": ["Energy", "Automotive", "Agriculture", "Manufacturing"]
    },
    {
        "id": 2,
        "title": "China Dual-Use Export Control List",
        "country": "CN",
        "category": "Policy",
        "impact": "High",
        "date": "2024-11-15",
        "description": "Consolidated list of dual-use items subject to strict export licensing, affecting global high-tech supply chains.",
        "affected_industries": ["Electronics", "Semiconductors", "Defense"]
    },
    {
        "id": 3,
        "title": "US 10% Tariff on Chinese Imports",
        "country": "US",
        "category": "Tariff",
        "impact": "High",
        "date": "2025-02-15",
        "description": "Initial 10% tariff on all Chinese imports, with plans to increase to 20% by March 2025.",
        "affected_industries": ["Electronics", "Consumer Goods", "Manufacturing"]
    },
    {
        "id": 4,
        "title": "EU Modernized Export Control Regime",
        "country": "EU",
        "category": "Regulation",
        "impact": "Medium",
        "date": "2025-09-20",
        "description": "EU updates dual-use export control list to enhance coordination and address emerging security technologies.",
        "affected_industries": ["Technology", "Semiconductors", "AI"]
    },
    {
        "id": 5,
        "title": "US 50% Tariff on India and Brazil",
        "country": "US",
        "category": "Tariff",
        "impact": "High",
        "date": "2025-07-14",
        "description": "New tariff schedule imposes 50% rates on major imports from India and Brazil due to trade disputes.",
        "affected_industries": ["Agriculture", "Pharmaceuticals", "Raw Materials"]
    },
    {
        "id": 6,
        "title": "Canada 25% Steel Surtax",
        "country": "CA",
        "category": "Tariff",
        "impact": "High",
        "date": "2025-12-05",
        "description": "Canada implements a 25% surtax on steel derivative goods in response to global trade volatility.",
        "affected_industries": ["Construction", "Automotive", "Infrastructure"]
    },
    {
        "id": 7,
        "title": "Cambodia-US Reciprocal Trade Pact",
        "country": "KH",
        "category": "Agreement",
        "impact": "Medium",
        "date": "2025-10-15",
        "description": "Cambodia eliminates tariffs on US goods and aligns with US export controls under new agreement.",
        "affected_industries": ["Agriculture", "Electronics", "Policy"]
    },
    {
        "id": 8,
        "title": "India Joins US Secure Tech Initiative",
        "country": "IN",
        "category": "Policy",
        "impact": "Medium",
        "date": "2024-01-18",
        "description": "India joins US-led initiative to secure technology supply chains and enhance regional stability.",
        "affected_industries": ["Semiconductors", "Communications", "Electronics"]
    }
]

# Supply Chain Vulnerability Data
SUPPLY_CHAIN_DATA = {
    "Semiconductors": {
        "risk_level": "High",
        "concentration_risk": "Critical",
        "top_suppliers": ["TW", "KR", "CN", "JP"],
        "vulnerabilities": ["Geopolitical tensions", "Natural disasters", "Single points of failure"],
        "alternatives_available": True
    },
    "Automotive": {
        "risk_level": "Medium",
        "concentration_risk": "Medium",
        "top_suppliers": ["DE", "JP", "CN", "US", "MX"],
        "vulnerabilities": ["Chip shortages", "Raw material costs"],
        "alternatives_available": True
    },
    "Electronics": {
        "risk_level": "High",
        "concentration_risk": "High",
        "top_suppliers": ["CN", "VN", "TW", "KR"],
        "vulnerabilities": ["China concentration", "Shipping disruptions"],
        "alternatives_available": True
    },
    "Agriculture": {
        "risk_level": "Medium",
        "concentration_risk": "Low",
        "top_suppliers": ["BR", "US", "IN", "AR"],
        "vulnerabilities": ["Climate change", "Trade disputes"],
        "alternatives_available": True
    },
    "Pharmaceuticals": {
        "risk_level": "Medium",
        "concentration_risk": "High",
        "top_suppliers": ["IN", "CN", "DE", "US"],
        "vulnerabilities": ["API concentration in India/China", "Regulatory changes"],
        "alternatives_available": False
    },
    "Textiles": {
        "risk_level": "Low",
        "concentration_risk": "Medium",
        "top_suppliers": ["CN", "VN", "BD", "IN"],
        "vulnerabilities": ["Labor costs rising", "Sustainability concerns"],
        "alternatives_available": True
    },
    "Energy": {
        "risk_level": "High",
        "concentration_risk": "High",
        "top_suppliers": ["SA", "RU", "US", "QA"],
        "vulnerabilities": ["Geopolitical instability", "Transition to renewables"],
        "alternatives_available": True
    },
    "Raw Materials": {
        "risk_level": "High",
        "concentration_risk": "Critical",
        "top_suppliers": ["CN", "RU", "AU", "BR"],
        "vulnerabilities": ["China dominance in rare earths", "Price volatility"],
        "alternatives_available": False
    }
}

# Pydantic Models
class Headline(BaseModel):
    title: str
    source: str
    date: str
    category: str
    impact: Optional[str] = "medium"

class AIForecast(BaseModel):
    score: int
    trend: str
    confidence: int

class Country(BaseModel):
    id: str
    name: str
    risk_score: int
    risk_level: str
    risk_trend: Optional[str] = "stable"
    tariff_percentage: float
    coordinates: dict
    key_industries: Optional[List[str]] = []
    supply_chain_risk: Optional[str] = "Medium"
    friend_shore_score: Optional[int] = 50

class CountryDetail(Country):
    trade_policy_summary: str
    headlines: List[Headline]
    ai_forecast: Optional[Dict[str, AIForecast]] = {}
    alternative_to: Optional[List[str]] = []
    alternatives: Optional[List[str]] = []

class PolicyAlert(BaseModel):
    id: int
    title: str
    country: str
    category: str
    impact: str
    date: str
    description: str
    affected_industries: List[str]

class SupplyChainInfo(BaseModel):
    industry: str
    risk_level: str
    concentration_risk: str
    top_suppliers: List[str]
    vulnerabilities: List[str]
    alternatives_available: bool

class AlternativeSupplier(BaseModel):
    country_id: str
    country_name: str
    risk_score: int
    friend_shore_score: int
    tariff_percentage: float
    key_industries: List[str]
    suitability_score: int
    reason: str

class CostSimulationRequest(BaseModel):
    base_cost: float
    tariff_percentage: float
    country_id: Optional[str] = None
    industry: Optional[str] = None

class CostSimulationResponse(BaseModel):
    base_cost: float
    tariff_percentage: float
    tariff_amount: float
    final_cost: float
    risk_adjustment: Optional[float] = None
    supply_chain_premium: Optional[float] = None
    ai_prediction: Optional[Dict] = None

class DashboardMetrics(BaseModel):
    total_countries_monitored: int
    high_risk_countries: int
    policy_alerts_this_week: int
    avg_global_risk: float
    top_risk_trend: str
    supply_chain_alerts: int

# API Endpoints

@app.get("/")
def root():
    return {
        "message": "RiskAtlas API - Trade Risk Intelligence Dashboard",
        "version": "2.0.0",
        "features": [
            "Real-time policy monitoring",
            "AI-based risk forecasting",
            "Supply chain vulnerability mapping",
            "Alternative supplier recommendations",
            "Predictive cost simulation"
        ],
        "endpoints": [
            "/countries",
            "/country/{id}",
            "/policy-alerts",
            "/supply-chain/{industry}",
            "/alternative-suppliers/{country_id}",
            "/simulate-cost",
            "/dashboard-metrics",
            "/industries"
        ]
    }

@app.get("/dashboard-metrics", response_model=DashboardMetrics)
def get_dashboard_metrics():
    """Get key dashboard metrics"""
    high_risk = sum(1 for c in COUNTRIES_DATA.values() if c["risk_score"] > 70)
    avg_risk = sum(c["risk_score"] for c in COUNTRIES_DATA.values()) / len(COUNTRIES_DATA)
    
    # Count increasing trends
    increasing = sum(1 for c in COUNTRIES_DATA.values() if c.get("risk_trend") == "increasing")
    decreasing = sum(1 for c in COUNTRIES_DATA.values() if c.get("risk_trend") == "decreasing")
    
    if increasing > decreasing:
        trend = "increasing"
    elif decreasing > increasing:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return DashboardMetrics(
        total_countries_monitored=len(COUNTRIES_DATA),
        high_risk_countries=high_risk,
        policy_alerts_this_week=len(POLICY_ALERTS),
        avg_global_risk=round(avg_risk, 1),
        top_risk_trend=trend,
        supply_chain_alerts=sum(1 for s in SUPPLY_CHAIN_DATA.values() if s["risk_level"] == "High")
    )

@app.get("/countries", response_model=List[Country])
def get_countries(
    industry: Optional[str] = Query(None, description="Filter by industry"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level")
):
    """Get all countries with optional filtering"""
    countries = []
    for country_id, data in COUNTRIES_DATA.items():
        # Apply industry filter
        if industry and industry not in data.get("key_industries", []):
            continue
        # Apply risk level filter
        if risk_level and data["risk_level"] != risk_level:
            continue
            
        countries.append(Country(
            id=data["id"],
            name=data["name"],
            risk_score=data["risk_score"],
            risk_level=data["risk_level"],
            risk_trend=data.get("risk_trend", "stable"),
            tariff_percentage=data["tariff_percentage"],
            coordinates=data["coordinates"],
            key_industries=data.get("key_industries", []),
            supply_chain_risk=data.get("supply_chain_risk", "Medium"),
            friend_shore_score=data.get("friend_shore_score", 50)
        ))
    return countries

@app.get("/country/{country_id}", response_model=CountryDetail)
def get_country(country_id: str):
    """Get detailed information for a specific country"""
    country_id = country_id.upper()
    if country_id not in COUNTRIES_DATA:
        raise HTTPException(status_code=404, detail=f"Country {country_id} not found")
    
    data = COUNTRIES_DATA[country_id]
    return CountryDetail(
        id=data["id"],
        name=data["name"],
        risk_score=data["risk_score"],
        risk_level=data["risk_level"],
        risk_trend=data.get("risk_trend", "stable"),
        tariff_percentage=data["tariff_percentage"],
        coordinates=data["coordinates"],
        key_industries=data.get("key_industries", []),
        supply_chain_risk=data.get("supply_chain_risk", "Medium"),
        friend_shore_score=data.get("friend_shore_score", 50),
        trade_policy_summary=data["trade_policy_summary"],
        headlines=[Headline(**h) for h in data["headlines"]],
        ai_forecast={k: AIForecast(**v) for k, v in data.get("ai_forecast", {}).items()},
        alternative_to=data.get("alternative_to", []),
        alternatives=data.get("alternatives", [])
    )

@app.get("/policy-alerts", response_model=List[PolicyAlert])
def get_policy_alerts(
    country: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    impact: Optional[str] = Query(None)
):
    """Get policy alerts with optional filtering"""
    alerts = POLICY_ALERTS
    
    if country:
        alerts = [a for a in alerts if a["country"] == country.upper()]
    if category:
        alerts = [a for a in alerts if a["category"].lower() == category.lower()]
    if impact:
        alerts = [a for a in alerts if a["impact"].lower() == impact.lower()]
    
    return [PolicyAlert(**a) for a in alerts]

@app.get("/supply-chain/{industry}", response_model=SupplyChainInfo)
def get_supply_chain_info(industry: str):
    """Get supply chain vulnerability information for an industry"""
    if industry not in SUPPLY_CHAIN_DATA:
        raise HTTPException(status_code=404, detail=f"Industry {industry} not found")
    
    data = SUPPLY_CHAIN_DATA[industry]
    return SupplyChainInfo(
        industry=industry,
        risk_level=data["risk_level"],
        concentration_risk=data["concentration_risk"],
        top_suppliers=data["top_suppliers"],
        vulnerabilities=data["vulnerabilities"],
        alternatives_available=data["alternatives_available"]
    )

@app.get("/industries")
def get_industries():
    """Get list of all industries"""
    return {
        "industries": INDUSTRIES,
        "supply_chain_data": list(SUPPLY_CHAIN_DATA.keys())
    }

@app.get("/alternative-suppliers/{country_id}", response_model=List[AlternativeSupplier])
def get_alternative_suppliers(
    country_id: str,
    industry: Optional[str] = Query(None, description="Filter by industry")
):
    """Get alternative supplier recommendations for a country"""
    country_id = country_id.upper()
    if country_id not in COUNTRIES_DATA:
        raise HTTPException(status_code=404, detail=f"Country {country_id} not found")
    
    country = COUNTRIES_DATA[country_id]
    alternatives = country.get("alternatives", [])
    
    if not alternatives:
        return []
    
    result = []
    for alt_id in alternatives:
        if alt_id not in COUNTRIES_DATA:
            continue
        alt = COUNTRIES_DATA[alt_id]
        
        # Filter by industry if specified
        if industry and industry not in alt.get("key_industries", []):
            continue
        
        # Calculate suitability score (0-100)
        suitability = min(100, alt.get("friend_shore_score", 50) + (50 - alt["risk_score"] // 2))
        
        reason = f"Lower risk score ({alt['risk_score']} vs {country['risk_score']})"
        if alt.get("friend_shore_score", 0) > 80:
            reason += " | Strong friend-shoring partner"
        
        result.append(AlternativeSupplier(
            country_id=alt_id,
            country_name=alt["name"],
            risk_score=alt["risk_score"],
            friend_shore_score=alt.get("friend_shore_score", 50),
            tariff_percentage=alt["tariff_percentage"],
            key_industries=alt.get("key_industries", []),
            suitability_score=suitability,
            reason=reason
        ))
    
    # Sort by suitability score
    result.sort(key=lambda x: x.suitability_score, reverse=True)
    return result

@app.post("/simulate-cost", response_model=CostSimulationResponse)
def simulate_cost(request: CostSimulationRequest):
    """Simulate final cost including tariffs and risk adjustments with AI prediction"""
    tariff_amount = request.base_cost * (request.tariff_percentage / 100)
    
    risk_adjustment = None
    supply_chain_premium = None
    ai_prediction = None
    
    if request.country_id and request.country_id.upper() in COUNTRIES_DATA:
        country = COUNTRIES_DATA[request.country_id.upper()]
        
        # Risk premium for high-risk countries
        if country["risk_score"] > 70:
            risk_adjustment = request.base_cost * 0.05
        elif country["risk_score"] > 50:
            risk_adjustment = request.base_cost * 0.02
        
        # Supply chain premium for critical industries
        if request.industry and request.industry in SUPPLY_CHAIN_DATA:
            supply_data = SUPPLY_CHAIN_DATA[request.industry]
            if supply_data["concentration_risk"] == "Critical":
                supply_chain_premium = request.base_cost * 0.03
            elif supply_data["concentration_risk"] == "High":
                supply_chain_premium = request.base_cost * 0.015
        
        # AI prediction for future costs
        forecast = country.get("ai_forecast", {})
        if forecast:
            ai_prediction = {
                "predicted_risk_3m": forecast.get("3_month", {}).get("score"),
                "predicted_risk_6m": forecast.get("6_month", {}).get("score"),
                "predicted_risk_12m": forecast.get("12_month", {}).get("score"),
                "confidence": forecast.get("3_month", {}).get("confidence"),
                "trend": forecast.get("3_month", {}).get("trend"),
                "estimated_future_tariff": request.tariff_percentage * (1 + (forecast.get("3_month", {}).get("score", country["risk_score"]) - country["risk_score"]) / 100)
            }
    
    final_cost = request.base_cost + tariff_amount + (risk_adjustment or 0) + (supply_chain_premium or 0)
    
    return CostSimulationResponse(
        base_cost=request.base_cost,
        tariff_percentage=request.tariff_percentage,
        tariff_amount=round(tariff_amount, 2),
        final_cost=round(final_cost, 2),
        risk_adjustment=round(risk_adjustment, 2) if risk_adjustment else None,
        supply_chain_premium=round(supply_chain_premium, 2) if supply_chain_premium else None,
        ai_prediction=ai_prediction
    )

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "features_active": [
            "policy_monitoring",
            "ai_forecasting",
            "supply_chain_mapping",
            "supplier_recommendations"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
