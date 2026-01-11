class ServiceCatalog:
    SERVICES = [
        {
            "name": "Community Edition",
            "description": "Ücretsiz, açık kaynak, topluluk desteğiyle (GitHub)",
            "price": 0,
            "unit": "ay"
        },
        {
            "name": "Enterprise Edition",
            "description": "Kaynak kodu ve kurumsal destek ile tam sürüm",
            "price": 199,
            "unit": "ay"
        },
        {
            "name": "Managed Service",
            "description": "Tüm altyapı ve yönetim hizmeti, anahtar teslim",
            "price": 499,
            "unit": "ay"
        },
        {
            "name": "Small Business Backup",
            "description": "Yerel ve bulut tabanlı küçük işletme yedekleme hizmeti",
            "price": 29,
            "unit": "ay"
        },
        {
            "name": "SME System Monitoring",
            "description": "Küçük ve orta ölçekli işletmeler için sistem izleme",
            "price": 49,
            "unit": "ay"
        },
        {
            "name": "IT Automation Consulting",
            "description": "BT otomasyon danışmanlığı ve entegrasyon hizmeti",
            "price": 99,
            "unit": "saat"
        },
        {
            "name": "Custom Module Development",
            "description": "İhtiyaca özel modül geliştirme ve entegrasyon",
            "price": "500-5000",
            "unit": "proje"
        }
    ]

    @classmethod
    def list_services(cls):
        return cls.SERVICES

    @classmethod
    def get_service(cls, name: str):
        for s in cls.SERVICES:
            if s["name"].lower() == name.lower():
                return s
        return None
