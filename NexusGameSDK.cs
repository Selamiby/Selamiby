/**
 * NEXUS Game SDK - Unity (C#)
 * Production-grade client for leaderboard, telemetry, crashes, feature flags, A/B testing
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.Profiling;

public class NexusGameSDK : MonoBehaviour
{
    private static NexusGameSDK _instance;
    private string _backendUrl = "http://127.0.0.1:7000";
    private string _playerId;
    private bool _initialized = false;
    private Queue<Action> _eventQueue = new Queue<Action>();
    private Dictionary<string, object> _sessionMeta = new Dictionary<string, object>();
    private float _lastHeartbeat;
    private const float HeartbeatInterval = 30f;

    public static NexusGameSDK Instance => _instance ??= FindObjectOfType<NexusGameSDK>();

    public void Initialize(string playerId, string backendUrl = null)
    {
        if (_initialized) return;

        _playerId = playerId;
        if (backendUrl != null) _backendUrl = backendUrl;

        DontDestroyOnLoad(gameObject);
        _initialized = true;

        _sessionMeta["device_model"] = SystemInfo.deviceModel;
        _sessionMeta["gpu_name"] = SystemInfo.graphicsDeviceName;
        _sessionMeta["os"] = SystemInfo.operatingSystem;
        _sessionMeta["ram_mb"] = SystemInfo.systemMemorySize;
        _sessionMeta["gpu_memory_mb"] = SystemInfo.graphicsMemorySize;

        Debug.Log($"[NEXUS] Initialized for player {_playerId}");
        StartCoroutine(HeartbeatLoop());
    }

    private IEnumerator HeartbeatLoop()
    {
        while (_initialized)
        {
            yield return new WaitForSeconds(HeartbeatInterval);
            SendTelemetry("heartbeat", new Dictionary<string, object>
            {
                { "fps", (int)(1f / Time.deltaTime) },
                { "heap_mb", (int)(Profiler.GetTotalMemoryUsed() / 1024 / 1024) }
            });
        }
    }

    public void SubmitScore(int score, Dictionary<string, object> metadata = null)
    {
        var data = new Dictionary<string, object>
        {
            { "player_id", _playerId },
            { "score", score },
            { "meta", metadata ?? new Dictionary<string, object>() }
        };
        StartCoroutine(PostRequest("/leaderboard/submit", data));
    }

    public void SendTelemetry(string eventName, Dictionary<string, object> payload = null)
    {
        var data = new Dictionary<string, object>
        {
            { "player_id", _playerId },
            { "event", eventName },
            { "payload", payload ?? new Dictionary<string, object>() }
        };
        StartCoroutine(PostRequest("/telemetry", data));
    }

    public void ReportCrash(string stackTrace, Dictionary<string, object> deviceInfo = null)
    {
        var data = new Dictionary<string, object>
        {
            { "player_id", _playerId },
            { "stacktrace", stackTrace },
            { "device_info", deviceInfo ?? _sessionMeta }
        };
        StartCoroutine(PostRequest("/crash", data));
    }

    public void GetLeaderboard(int limit, System.Action<List<Dictionary<string, object>>> callback)
    {
        StartCoroutine(GetRequest($"/leaderboard/top?limit={limit}", callback));
    }

    public void GetFeatureFlags(System.Action<Dictionary<string, object>> callback)
    {
        StartCoroutine(GetRequest("/feature-flags", callback));
    }

    public void GetABVariant(System.Action<string> callback)
    {
        StartCoroutine(GetRequest($"/ab-variant?player_id={_playerId}", (obj) =>
        {
            if (obj is Dictionary<string, object> dict && dict.ContainsKey("variant"))
                callback((string)dict["variant"]);
        }));
    }

    private IEnumerator PostRequest(string endpoint, Dictionary<string, object> data)
    {
        string json = JsonUtility.ToJson(new Wrapper { data = data });
        using (UnityWebRequest req = new UnityWebRequest(_backendUrl + endpoint, "POST"))
        {
            req.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(json));
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");

            yield return req.SendWebRequest();

            if (req.result != UnityWebRequest.Result.Success)
                Debug.LogWarning($"[NEXUS] POST error: {req.error}");
        }
    }

    private IEnumerator GetRequest(string endpoint, System.Action<object> callback)
    {
        using (UnityWebRequest req = UnityWebRequest.Get(_backendUrl + endpoint))
        {
            yield return req.SendWebRequest();

            if (req.result == UnityWebRequest.Result.Success)
            {
                var json = req.downloadHandler.text;
                Debug.Log($"[NEXUS] GET {endpoint}: {json}");
                // Parse JSON and invoke callback
                callback(new Dictionary<string, object> { { "response", json } });
            }
            else
                Debug.LogWarning($"[NEXUS] GET error: {req.error}");
        }
    }

    [Serializable]
    private class Wrapper { public Dictionary<string, object> data; }
}
