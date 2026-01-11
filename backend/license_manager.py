class LicenseManager:
    LEVELS = ["free", "pro", "enterprise"]
    FEATURES = {
        "free": [
            "local_backup",
            "basic_monitoring",
            "basic_self_healing",
            "community_support"
        ],
        "pro": [
            "cloud_backup",
            "advanced_monitoring",
            "ai_assistant",
            "priority_support"
        ],
        "enterprise": [
            "white_label",
            "custom_modules",
            "sla_guarantee",
            "24_7_support"
        ]
    }

    def __init__(self, level: str = "free"):
        self.level = level if level in self.LEVELS else "free"

    def has_feature(self, feature: str) -> bool:
        for lvl in self.LEVELS:
            if self.LEVELS.index(self.level) >= self.LEVELS.index(lvl):
                if feature in self.FEATURES.get(lvl, []):
                    return True
        return False

    def upgrade(self, new_level: str):
        if new_level in self.LEVELS:
            self.level = new_level

    def get_features(self):
        features = set()
        for lvl in self.LEVELS:
            if self.LEVELS.index(self.level) >= self.LEVELS.index(lvl):
                features.update(self.FEATURES.get(lvl, []))
        return list(features)
