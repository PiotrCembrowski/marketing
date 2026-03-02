from analyzer import FanpageMetrics, analyze_traffic_drivers, summarize_analysis


def test_analysis_returns_sorted_drivers():
    metrics = FanpageMetrics(
        followers=20000,
        avg_post_reach=10000,
        engagement_rate=8.0,
        posting_frequency_weekly=7,
        video_share_percent=70,
        response_time_minutes=80,
        ad_spend_usd_monthly=3000,
        share_rate=5.0,
    )

    drivers = analyze_traffic_drivers(metrics)

    assert len(drivers) == 7
    assert drivers[0].score >= drivers[1].score


def test_summary_includes_top_and_overall():
    metrics = FanpageMetrics(
        followers=10000,
        avg_post_reach=2000,
        engagement_rate=2.4,
        posting_frequency_weekly=2,
        video_share_percent=20,
        response_time_minutes=900,
        ad_spend_usd_monthly=100,
        share_rate=0.8,
    )

    summary = summarize_analysis(analyze_traffic_drivers(metrics))

    assert "top_drivers" in summary
    assert "weak_areas" in summary
    assert "overall_score" in summary
    assert len(summary["top_drivers"]) == 3
