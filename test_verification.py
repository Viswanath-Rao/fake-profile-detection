import os
import sys

def verify_all():
    print("[1/4] Verifying imports and module loading...")
    from core.presets import PRESET_PROFILES
    print(f"  Loaded {len(PRESET_PROFILES)} presets successfully.")

    print("[2/4] Initializing ProfileForensicEngine...")
    from core.detector import ProfileForensicEngine
    engine = ProfileForensicEngine()
    print("  ProfileForensicEngine initialized successfully.")

    print("[3/4] Testing profile analysis...")
    test_data = {
        "username": "crypto_scam_bot_9982",
        "followers": 12,
        "following": 3200,
        "posts": 0,
        "bio": "Invest now! WhatsApp giveaway +123456789",
        "is_private": False
    }
    res = engine.analyze_profile(test_data, None)
    assert "fake_probability" in res
    assert "classification" in res
    assert "radar_scores" in res
    print(f"  Test profile result: {res['classification']} (Fake: {res['fake_probability']}%, Threat: {res['threat_level']})")

    print("[4/4] Verifying server routes...")
    import server
    print(f"  Server app loaded with {len(server.routes)} routes.")

    print("\n==============================================")
    print(" ALL FORENSIC ENGINE VERIFICATIONS PASSED 100%")
    print("==============================================")

if __name__ == "__main__":
    verify_all()
