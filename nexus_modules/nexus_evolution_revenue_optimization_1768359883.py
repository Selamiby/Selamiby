"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

class FreelanceProjectHunting:
    def __init__(self, project_data):
        self.project_data = project_data

    def data_preprocessing(self):
        # Veri ön işleme
        self.project_data['project_duration'] = pd.to_datetime(self.project_data['project_end_date']) - pd.to_datetime(self.project_data['project_start_date'])
        self.project_data['project_duration'] = self.project_data['project_duration'].dt.days
        self.project_data['project_price'] = self.project_data['project_price'].astype(float)
        self.project_data['freelancer_experience'] = self.project_data['freelancer_experience'].astype(float)

    def feature_engineering(self):
        # Özellik mühendisliği
        self.project_data['project_price_per_day'] = self.project_data['project_price'] / self.project_data['project_duration']
        self.project_data['freelancer_experience_per_year'] = self.project_data['freelancer_experience'] / self.project_data['project_duration']

    def train_model(self):
        # Model eğitimi
        X = self.project_data[['project_duration', 'freelancer_experience', 'project_price_per_day', 'freelancer_experience_per_year']]
        y = self.project_data['project_price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        print('Model Performansı (MSE):', mean_squared_error(y_test, y_pred))
        return model

    def predict_project_price(self, model, project_data):
        # Proje fiyatı tahmini
        project_data = pd.DataFrame(project_data)
        project_data['project_duration'] = pd.to_datetime(project_data['project_end_date']) - pd.to_datetime(project_data['project_start_date'])
        project_data['project_duration'] = project_data['project_duration'].dt.days
        project_data['project_price_per_day'] = project_data['project_price'] / project_data['project_duration']
        project_data['freelancer_experience_per_year'] = project_data['freelancer_experience'] / project_data['project_duration']
        X = project_data[['project_duration', 'freelancer_experience', 'project_price_per_day', 'freelancer_experience_per_year']]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        predicted_price = model.predict(X_scaled)
        return predicted_price

# Örnek kullanım
project_data = pd.DataFrame({
    'project_name': ['Proje 1', 'Proje 2', 'Proje 3'],
    'project_start_date': ['2022-01-01', '2022-02-01', '2022-03-01'],
    'project_end_date': ['2022-01-31', '2022-02-28', '2022-03-31'],
    'project_price': [1000, 2000, 3000],
    'freelancer_experience': [5, 10, 15]
})

freelance_project_hunting = FreelanceProjectHunting(project_data)
freelance_project_hunting.data_preprocessing()
freelance_project_hunting.feature_engineering()
model = freelance_project_hunting.train_model()

new_project_data = {
    'project_name': 'Yeni Proje',
    'project_start_date': '2022-04-01',
    'project_end_date': '2022-04-30',
    'project_price': 4000,
    'freelancer_experience': 20
}

predicted_price = freelance_project_hunting.predict_project_price(model, new_project_data)
print('Tahmin Edilen Proje Fiyatı:', predicted_price)