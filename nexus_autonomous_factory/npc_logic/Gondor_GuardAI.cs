
using UnityEngine;
using System.Collections.Generic;

public class Gondor_GuardAI : MonoBehaviour
{
    // NEXUS-ONE: Üst Düzey Otonom Muhafız Zekası (V1.0)
    public enum GuardState { IDLE, PATROL, ALERT, COMBAT }
    public GuardState currentState = GuardState.IDLE;

    public string personality = "Ciddi ve Koruyucu";
    public float detectionRange = 15f;
    public List<Transform> patrolPoints;

    private int currentPoint = 0;

    void Update()
    {
        switch (currentState)
        {
            case GuardState.IDLE: HandleIdle(); break;
            case GuardState.PATROL: HandlePatrol(); break;
            case GuardState.ALERT: HandleAlert(); break;
            case GuardState.COMBAT: HandleCombat(); break;
        }

        CheckForThreats();
    }

    void CheckForThreats()
    {
        if (PlayerDetected())
        {
            currentState = GuardState.COMBAT;
        }
    }

    void HandleCombat()
    {
        // NEXUS: Gerçek saldırı ve savunma algoritmaları burada başlar
        Debug.Log($"[NEXUS-AI] {personality} muhafız saldırıya geçti! Tehdit bertaraf ediliyor.");
    }

    bool PlayerDetected()
    {
        // Yerel sensör verisi simülasyonu
        return false;
    }

    void HandlePatrol()
    {
        // Devriye mantığı
    }

    void HandleIdle()
    {
        if (Random.value > 0.98f) currentState = GuardState.PATROL;
    }
}
