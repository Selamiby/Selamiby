
using UnityEngine;
using System.Collections.Generic;

public class Street_TraderAI : MonoBehaviour
{
    // NEXUS-ONE: Dinamik Ticaret ve NPC Ekonomi Zekası (V1.0)

    [System.Serializable]
    public class InventoryItem
    {
        public string itemName;
        public float basePrice;
        public int quantity;
    }

    public string merchantName = "Kurnaz Alim";
    public List<InventoryItem> inventory = new List<InventoryItem>();
    public float greedFactor = 1.2f; // Fiyatları artırma çarpanı

    void Start()
    {
        // Rastgele stok oluştur
        InitializeStock();
    }

    void InitializeStock()
    {
        inventory.Add(new InventoryItem { itemName = "Yolcu Ekmeği", basePrice = 5, quantity = 20 });
        inventory.Add(new InventoryItem { itemName = "Paslı Kılıç", basePrice = 50, quantity = 2 });
        inventory.Add(new InventoryItem { itemName = "İpek Kumaş", basePrice = 120, quantity = 5 });
    }

    public float GetCurrentPrice(string itemName)
    {
        InventoryItem item = inventory.Find(i => i.itemName == itemName);
        if (item != null)
        {
            // Arz-talep dengesi simülasyonu: Stok azaldıkça fiyat artar
            float supplyShortage = 1f + (1f / (item.quantity + 0.1f));
            return item.basePrice * greedFactor * supplyShortage;
        }
        return 0;
    }

    public void TradeItem(string itemName, int amount, bool isBuyingFromPlayer)
    {
        InventoryItem item = inventory.Find(i => i.itemName == itemName);
        if (item != null)
        {
            if (isBuyingFromPlayer)
            {
                item.quantity += amount;
                Debug.Log($"[NEXUS-TRADE] {merchantName} oyuncudan {itemName} aldı. Yeni stok: {item.quantity}");
            }
            else if (item.quantity >= amount)
            {
                item.quantity -= amount;
                float finalPrice = GetCurrentPrice(itemName) * amount;
                Debug.Log($"[NEXUS-TRADE] {merchantName} oyuncuya {itemName} sattı. Tutar: {finalPrice} Altın.");
            }
        }
    }
}
