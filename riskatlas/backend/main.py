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
            {"title": "US announces new semiconductor export controls", "source": "Trade Weekly", "date": "2024-01-15", "category": "Policy", "impact": "high"},
            {"title": "Bilateral trade agreement negotiations progress with EU", "source": "Global Trade News", "date": "2024-01-12", "category": "Diplomacy", "impact": "medium"},
            {"title": "Tariff review scheduled for Q2 2024", "source": "Commerce Daily", "date": "2024-01-10", "category": "Tariff", "impact": "medium"},
            {"title": "CHIPS Act funding boosts domestic chip production", "source": "Tech Policy", "date": "2024-01-08", "category": "Policy", "impact": "high"}
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
            {"title": "New regulations on foreign investment in tech sector", "source": "Asia Business Review", "date": "2024-01-16", "category": "Regulation", "impact": "high"},
            {"title": "Trade tensions rise over rare earth export quotas", "source": "Commodities Today", "date": "2024-01-14", "category": "Geopolitics", "impact": "high"},
            {"title": "Tariff retaliation measures announced", "source": "Trade Monitor", "date": "2024-01-11", "category": "Tariff", "impact": "high"},
            {"title": "Semiconductor self-sufficiency program accelerates", "source": "China Tech", "date": "2024-01-09", "category": "Policy", "impact": "medium"}
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
            {"title": "Brazil strengthens Mercosur trade bloc position", "source": "LatAm Trade", "date": "2024-01-16", "category": "Trade Bloc", "impact": "medium"},
            {"title": "New environmental regulations impact agricultural exports", "source": "AgriBusiness News", "date": "2024-01-14", "category": "Regulation", "impact": "high"},
            {"title": "Currency fluctuations affect import costs", "source": "Financial Times BR", "date": "2024-01-12", "category": "Currency", "impact": "medium"}
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
            {"title": "India reduces tariffs on electronics imports", "source": "Tech Trade India", "date": "2024-01-15", "category": "Tariff", "impact": "medium"},
            {"title": "New FDI rules in retail sector announced", "source": "Business Standard", "date": "2024-01-13", "category": "Investment", "impact": "medium"},
            {"title": "Production-linked incentive scheme attracts manufacturers", "source": "Economic Times", "date": "2024-01-11", "category": "Policy", "impact": "high"}
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
            {"title": "Japan-US trade agreement enters new phase", "source": "Nikkei Asia", "date": "2024-01-15", "category": "Agreement", "impact": "medium"},
            {"title": "Tech sector sees increased foreign investment", "source": "Japan Times", "date": "2024-01-13", "category": "Investment", "impact": "low"},
            {"title": "Semiconductor material exports to expand", "source": "Tech Japan", "date": "2024-01-10", "category": "Industry", "impact": "medium"}
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
            {"title": "Nearshoring boom continues with new factory announcements", "source": "Mexico Today", "date": "2024-01-16", "category": "Investment", "impact": "high"},
            {"title": "Automotive production reaches record levels", "source": "Auto Mexico", "date": "2024-01-14", "category": "Industry", "impact": "medium"},
            {"title": "USMCA compliance review scheduled", "source": "Trade North America", "date": "2024-01-12", "category": "Policy", "impact": "medium"}
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
            {"title": "New trade deals signed with Indo-Pacific partners", "source": "FT", "date": "2024-01-16", "category": "Diplomacy", "impact": "medium"},
            {"title": "Services sector growth exceeds expectations", "source": "BBC Business", "date": "2024-01-14", "category": "Economy", "impact": "low"},
            {"title": "UK AI Safety Summit drives new regulations", "source": "TechUK", "date": "2024-01-12", "category": "Policy", "impact": "medium"}
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
            {"title": "New industrial decarbonization fund launched", "source": "Le Monde Business", "date": "2024-01-15", "category": "Energy", "impact": "medium"},
            {"title": "Agricultural exports remain strong amidst EU reforms", "source": "Eurostat", "date": "2024-01-13", "category": "Agriculture", "impact": "low"},
            {"title": "Tech startup funding reaches new record", "source": "France Tech", "date": "2024-01-10", "category": "Investment", "impact": "medium"}
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
            {"title": "Critical minerals partnership expanded with US", "source": "Globe and Mail", "date": "2024-01-16", "category": "Raw Materials", "impact": "high"},
            {"title": "Energy exports via TMX pipeline project update", "source": "Calgary Herald", "date": "2024-01-14", "category": "Energy", "impact": "medium"},
            {"title": "New tech talent visa attracts global specialists", "source": "Financial Post", "date": "2024-01-11", "category": "Policy", "impact": "low"}
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
            {"title": "Iron ore exports reach new highs in Q4", "source": "AFR", "date": "2024-01-15", "category": "Economy", "impact": "medium"},
            {"title": "New critical minerals strategy launched", "source": "Government News", "date": "2024-01-13", "category": "Policy", "impact": "high"},
            {"title": "Wine exports to China normalize", "source": "ABC News", "date": "2024-01-10", "category": "Agriculture", "impact": "medium"}
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
    }
}

# Policy Alerts Data
POLICY_ALERTS = [
    {
        "id": 1,
        "title": "New US Export Controls on AI Chips",
        "country": "US",
        "category": "Export Control",
        "impact": "High",
        "date": "2024-01-16",
        "description": "Expanded restrictions on AI chip exports to certain countries affecting semiconductor supply chains.",
        "affected_industries": ["Semiconductors", "Electronics", "AI"]
    },
    {
        "id": 2,
        "title": "China Rare Earth Export Quotas Reduced",
        "country": "CN",
        "category": "Export Restriction",
        "impact": "High",
        "date": "2024-01-15",
        "description": "New quotas on rare earth exports may affect electronics and EV manufacturing globally.",
        "affected_industries": ["Electronics", "Automotive", "Energy"]
    },
    {
        "id": 3,
        "title": "EU Carbon Border Tax Implementation",
        "country": "EU",
        "category": "Tariff",
        "impact": "Medium",
        "date": "2024-01-14",
        "description": "New carbon border adjustment mechanism affects imports from high-emission countries.",
        "affected_industries": ["Raw Materials", "Energy", "Manufacturing"]
    },
    {
        "id": 4,
        "title": "India PLI Scheme Expansion",
        "country": "IN",
        "category": "Subsidy",
        "impact": "Medium",
        "date": "2024-01-13",
        "description": "Production-linked incentive scheme expanded to include more electronics categories.",
        "affected_industries": ["Electronics", "Semiconductors"]
    },
    {
        "id": 5,
        "title": "Mexico Nearshoring Tax Incentives",
        "country": "MX",
        "category": "Incentive",
        "impact": "Medium",
        "date": "2024-01-12",
        "description": "New tax benefits for companies relocating manufacturing from Asia to Mexico.",
        "affected_industries": ["Automotive", "Electronics", "Textiles"]
    },
    {
        "id": 6,
        "title": "Japan Semiconductor Equipment Export Rules",
        "country": "JP",
        "category": "Export Control",
        "impact": "High",
        "date": "2024-01-11",
        "description": "Updated export controls on advanced semiconductor manufacturing equipment.",
        "affected_industries": ["Semiconductors"]
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
