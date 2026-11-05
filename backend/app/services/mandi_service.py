"""
Mandi & Economics Service for DHARTI-X
Deterministic agricultural calculations with Low / Expected / High Scenarios.
Strictly disallows LLM arithmetic hallucinations.
"""

from typing import Dict, Any, List

class MandiService:
    # Benchmark agricultural economic parameters for Palghar District
    CROPS = {
        "rice": {
            "name": "Paddy (Rice / Dhan - Kharif)",
            "benchmark_cost_breakdown": {
                "seeds": 2400,
                "land_preparation": 4500,
                "fertilizers_manure": 5500,
                "transplanting_labor": 4000,
                "harvesting_threshing": 3500
            },
            "scenarios": {
                "low": {"yield_quintal": 14, "mandi_price": 2050},
                "expected": {"yield_quintal": 18, "mandi_price": 2300},
                "high": {"yield_quintal": 22, "mandi_price": 2550}
            },
            "market": "Palghar / Manor APMC",
            "source": "Agmarknet Palghar APMC Benchmark (Sample Reference)"
        },
        "nachani": {
            "name": "Finger Millet (Nachani / Ragi)",
            "benchmark_cost_breakdown": {
                "seeds": 1200,
                "land_preparation": 3800,
                "fertilizers_manure": 3500,
                "weeding_labor": 3200,
                "harvesting_threshing": 2800
            },
            "scenarios": {
                "low": {"yield_quintal": 7, "mandi_price": 2800},
                "expected": {"yield_quintal": 10, "mandi_price": 3200},
                "high": {"yield_quintal": 13, "mandi_price": 3600}
            },
            "market": "Jawhar / Vikramgad APMC",
            "source": "Agmarknet Jawhar APMC Benchmark (Sample Reference)"
        },
        "sapota": {
            "name": "Sapota (Gholvad Chikoo - GI)",
            "benchmark_cost_breakdown": {
                "sapling_care": 4000,
                "drip_irrigation_maintenance": 6000,
                "organic_manure": 8000,
                "plucking_labor": 7000,
                "packing_crates": 3000
            },
            "scenarios": {
                "low": {"yield_quintal": 25, "mandi_price": 2200},
                "expected": {"yield_quintal": 35, "mandi_price": 2800},
                "high": {"yield_quintal": 45, "mandi_price": 3400}
            },
            "market": "Dahanu / Gholvad APMC",
            "source": "Dahanu Chikoo Producers APMC (Sample Reference)"
        }
    }

    @classmethod
    def calculate_scenario_economics(cls, crop_key: str = "rice", acreage: float = 2.0) -> Dict[str, Any]:
        crop_data = cls.CROPS.get(crop_key.lower(), cls.CROPS["rice"])
        
        # Base per-acre cost
        breakdown = crop_data["benchmark_cost_breakdown"]
        cost_per_acre = sum(breakdown.values())
        total_cost = round(cost_per_acre * acreage, 2)

        results = {}
        for scenario_name, params in crop_data["scenarios"].items():
            per_acre_yield = params["yield_quintal"]
            price_per_q = params["mandi_price"]
            
            total_yield = round(per_acre_yield * acreage, 2)
            gross_revenue = round(total_yield * price_per_q, 2)
            net_profit = round(gross_revenue - total_cost, 2)
            roi = round((net_profit / total_cost) * 100, 1) if total_cost > 0 else 0.0
            break_even = round(total_cost / total_yield, 2) if total_yield > 0 else 0.0

            results[scenario_name] = {
                "per_acre_yield_quintals": per_acre_yield,
                "total_yield_quintals": total_yield,
                "mandi_price_rs_per_quintal": price_per_q,
                "gross_revenue_rs": gross_revenue,
                "net_profit_rs": net_profit,
                "roi_percentage": roi,
                "break_even_price_per_quintal_rs": break_even
            }

        return {
            "crop": crop_data["name"],
            "acreage": acreage,
            "cost_breakdown_per_acre": breakdown,
            "total_cost_per_acre_rs": cost_per_acre,
            "total_cultivation_cost_rs": total_cost,
            "scenarios": results,
            "source": crop_data["source"],
            "disclaimer": "Scenarios are indicative ranges based on seasonal weather and market volatility."
        }
