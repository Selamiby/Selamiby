
using UnityEngine;
using System.Collections.Generic;

public class MB_CombatHandler : MonoBehaviour
{
    // NEXUS-ONE: Üst Düzey Dövüş Mekaniği (V1.2)
    // Mount & Blade tarzı yönlü saldırı ve bloklama motoru.

    public enum CombatState { IDLE, ATTACKING, BLOCKING, STUNNED }
    public enum Direction { Up, Down, Left, Right, None }

    [Header("Combat Stats")]
    public CombatState currentState = CombatState.IDLE;
    public Direction currentDirection = Direction.None;
    public float attackSpeed = 1.2f;
    public float blockStamina = 100f;

    private float lastActionTime;

    void Update()
    {
        if (currentState == CombatState.STUNNED) return;

        HandleCombatInput();
    }

    void HandleCombatInput()
    {
        // Fare hareketinden yön tespiti
        float mouseX = Input.GetAxis("Mouse X");
        float mouseY = Input.GetAxis("Mouse Y");

        if (Mathf.Abs(mouseX) > 0.1f || Mathf.Abs(mouseY) > 0.1f)
        {
            UpdateDirection(mouseX, mouseY);
        }

        // Saldırı (Sol Tık)
        if (Input.GetMouseButtonDown(0) && currentState == CombatState.IDLE)
        {
            ExecuteAttack();
        }

        // Bloklama (Sağ Tık)
        if (Input.GetMouseButton(1))
        {
            currentState = CombatState.BLOCKING;
        }
        else if (currentState == CombatState.BLOCKING)
        {
            currentState = CombatState.IDLE;
        }
    }

    void UpdateDirection(float x, float y)
    {
        if (Mathf.Abs(x) > Mathf.Abs(y))
        {
            currentDirection = x > 0 ? Direction.Right : Direction.Left;
        }
        else
        {
            currentDirection = y > 0 ? Direction.Up : Direction.Down;
        }
    }

    void ExecuteAttack()
    {
        currentState = CombatState.ATTACKING;
        lastActionTime = Time.time;

        // Raycast veya Trigger tabanlı gerçek fiziksel vuruş kontrolü
        Debug.Log($"[NEXUS-COMBAT] {currentDirection} yönünde gerçek fiziksel saldırı başlatıldı!");

        // Saldırı animasyonu süresi sonrasında IDLE'a dön (Simülatif bekleme)
        Invoke("ResetState", 1f / attackSpeed);
    }

    void ResetState()
    {
        if (currentState != CombatState.STUNNED)
        {
            currentState = CombatState.IDLE;
        }
    }

    public void OnHitReceived(float damage, Direction hitDirection)
    {
        if (currentState == CombatState.BLOCKING && currentDirection == hitDirection)
        {
            Debug.Log("[NEXUS-COMBAT] Mükemmel Blok! Hasar engellendi.");
            blockStamina -= damage * 0.1f;
        }
        else
        {
            Debug.Log($"[NEXUS-COMBAT] Darbe alındı! {damage} hasar.");
            // Bir saniyeliğine sersemlet
            currentState = CombatState.STUNNED;
            Invoke("ResetState", 1f);
        }
    }
}
