"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

"""
Bu modül, küresel finans alanında son gelişmeleri analiz etmek için tasarlanmıştır.
NEXUS'un yeteneklerini bir üst seviyeye taşımak amacıyla geliştirilmiştir.
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class FinanceAnalyzer:
    def __init__(self, ticker):
        """
        Initialize the FinanceAnalyzer class.
        
        Parameters:
        ticker (str): Finansal Enstrümanın ticker kodu (örneğin: GOOG, AAPL)
        """
        self.ticker = ticker
        self.data = yf.Ticker(ticker)

    def get_historical_data(self):
        """
        Finansal enstrümanın historical veriğini alıntılar.
        
        Returns:
        pandas.DataFrame: Historical veriler
        """
        return self.data.history(period="max")

    def plot_stock_price(self):
        """
        Finansal enstrümanın hisse senedi fiyatını grafik olarak gösterir.
        """
        data = self.get_historical_data()
        plt.figure(figsize=(12,6))
        plt.plot(data['Close'], label='Kapanış Fiyatı')
        plt.title(f'{self.ticker} Hisse Senedi Fiyatı')
        plt.xlabel('Tarih')
        plt.ylabel('Fiyat (USD)')
        plt.legend()
        plt.show()

    def calculate_moving_averages(self, window):
        """
        Hareketli ortalamaları hesaplar.
        
        Parameters:
        window (int): Hesaplama pencere genişliği
        
        Returns:
        pandas.Series: Hareketli ortalamalar
        """
        data = self.get_historical_data()
        return data['Close'].rolling(window).mean()

def main():
    analyzer = FinanceAnalyzer('AAPL')
    print(analyzer.get_historical_data().head())
    analyzer.plot_stock_price()
    print(analyzer.calculate_moving_averages(50))

if __name__ == "__main__":
    main()