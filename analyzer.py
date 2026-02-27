from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FanpageMetrics:
    followers: int
    avg_post_reach: int
    engagement_rate: float
    posting_frequency_weekly: int
    video_share_percent: float
    response_time_minutes: int
    ad_spend_usd_monthly: float
    share_rate: float


@dataclass
class TrafficDriver:
    name: str
    score: float
    reason: str
    recommendation: str



def _clamp(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(max_value, value))



def analyze_traffic_drivers(metrics: FanpageMetrics) -> List[TrafficDriver]:
    organic_reach_score = _clamp((metrics.avg_post_reach / max(metrics.followers, 1)) * 120)
    engagement_score = _clamp(metrics.engagement_rate * 12)
    consistency_score = _clamp(metrics.posting_frequency_weekly * 12.5)
    video_score = _clamp(metrics.video_share_percent)
    community_score = _clamp(100 - (metrics.response_time_minutes / 10))
    paid_score = _clamp(metrics.ad_spend_usd_monthly / 20)
    virality_score = _clamp(metrics.share_rate * 14)

    drivers = [
        TrafficDriver(
            name="Organic distribution",
            score=organic_reach_score,
            reason="Your posts are reaching a healthy share of your follower base.",
            recommendation="Test more link posts and compare reach by topic clusters.",
        ),
        TrafficDriver(
            name="Engagement quality",
            score=engagement_score,
            reason="High reactions, comments, and clicks help Facebook push content further.",
            recommendation="Prioritize interactive posts (polls, comment prompts, social proof).",
        ),
        TrafficDriver(
            name="Posting consistency",
            score=consistency_score,
            reason="Regular cadence improves predictable audience touchpoints.",
            recommendation="Build a weekly calendar and keep posting at similar times.",
        ),
        TrafficDriver(
            name="Video content mix",
            score=video_score,
            reason="Video tends to get broader discovery and stronger watch signals.",
            recommendation="Repurpose top posts into short native videos with captions.",
        ),
        TrafficDriver(
            name="Community management",
            score=community_score,
            reason="Fast replies increase page trust and repeat visits.",
            recommendation="Set a response SLA and use saved replies for common questions.",
        ),
        TrafficDriver(
            name="Paid amplification",
            score=paid_score,
            reason="Ad spend can seed initial reach and retarget warm audiences.",
            recommendation="Boost top organic performers instead of random posts.",
        ),
        TrafficDriver(
            name="Shareability / virality",
            score=virality_score,
            reason="When users share posts, second-order network exposure drives visits.",
            recommendation="Use 'share-worthy' content formats like checklists and before/after stories.",
        ),
    ]

    return sorted(drivers, key=lambda d: d.score, reverse=True)



def summarize_analysis(drivers: List[TrafficDriver]) -> Dict[str, object]:
    top_3 = drivers[:3]
    weak_areas = [driver for driver in drivers if driver.score < 45][:2]

    return {
        "top_drivers": [
            {
                "name": d.name,
                "score": round(d.score, 1),
                "reason": d.reason,
                "recommendation": d.recommendation,
            }
            for d in top_3
        ],
        "weak_areas": [
            {
                "name": d.name,
                "score": round(d.score, 1),
                "recommendation": d.recommendation,
            }
            for d in weak_areas
        ],
        "overall_score": round(sum(d.score for d in drivers) / len(drivers), 1),
    }
