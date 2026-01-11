class TargetAudienceAndMarketing:
    TARGET_AUDIENCE = [
        "Developers & DevOps engineers",
        "Small business owners",
        "IT consultants",
        "Educational institutions"
    ]

    MARKETING_CHANNELS = [
        "GitHub (open source visibility)",
        "Product Hunt launch",
        "Reddit communities",
        "LinkedIn B2B marketing",
        "YouTube tutorials"
    ]

    @classmethod
    def get_target_audience(cls):
        return cls.TARGET_AUDIENCE

    @classmethod
    def get_marketing_channels(cls):
        return cls.MARKETING_CHANNELS
