// NEXUS Game SDK - Unreal Engine (C++)
// Implementation: NexusGameSDK.cpp
#include "NexusGameSDK.h"
#include "Http.h"
#include "HttpModule.h"
#include "Interfaces/IHttpResponse.h"
#include "GenericPlatform/GenericPlatformMisc.h"
#include "Misc/FileHelper.h"

ANexusGameSDK::ANexusGameSDK()
    : bInitialized(false), HeartbeatTimer(0.0f)
{
    PrimaryActorTick.TickInterval = 0.1f;
    PrimaryActorTick.bCanEverTick = true;
    HttpModule = &FHttpModule::Get();
}

void ANexusGameSDK::BeginPlay()
{
    Super::BeginPlay();
}

void ANexusGameSDK::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    if (bInitialized)
    {
        HeartbeatTimer += DeltaTime;
        if (HeartbeatTimer >= 30.0f)
        {
            OnHeartbeat();
            HeartbeatTimer = 0.0f;
        }
    }
}

void ANexusGameSDK::Initialize(const FString& InPlayerId, const FString& InBackendUrl)
{
    if (bInitialized) return;

    PlayerId = InPlayerId;
    BackendUrl = InBackendUrl;
    bInitialized = true;

    FString DeviceModel = FGenericPlatformMisc::GetDeviceId();
    FString OS = FPlatformMisc::GetOperatingSystemId();
    
    UE_LOG(LogTemp, Warning, TEXT("[NEXUS] Initialized for player %s"), *PlayerId);
}

void ANexusGameSDK::SubmitScore(int32 Score, const FString& MetadataJSON)
{
    if (!bInitialized) return;

    FString JsonData = FString::Printf(
        TEXT("{\"player_id\":\"%s\",\"score\":%d,\"meta\":%s}"),
        *PlayerId, Score, *MetadataJSON
    );
    PostRequest(TEXT("/leaderboard/submit"), JsonData);
}

void ANexusGameSDK::SendTelemetry(const FString& EventName, const FString& PayloadJSON)
{
    if (!bInitialized) return;

    FString JsonData = FString::Printf(
        TEXT("{\"player_id\":\"%s\",\"event\":\"%s\",\"payload\":%s}"),
        *PlayerId, *EventName, *PayloadJSON
    );
    PostRequest(TEXT("/telemetry"), JsonData);
}

void ANexusGameSDK::ReportCrash(const FString& StackTrace, const FString& DeviceInfoJSON)
{
    if (!bInitialized) return;

    FString JsonData = FString::Printf(
        TEXT("{\"player_id\":\"%s\",\"stacktrace\":\"%s\",\"device_info\":%s}"),
        *PlayerId, *StackTrace, *DeviceInfoJSON
    );
    PostRequest(TEXT("/crash"), JsonData);
}

void ANexusGameSDK::PostRequest(const FString& Endpoint, const FString& JsonData)
{
    if (!HttpModule) return;

    FHttpRequestRef Request = HttpModule->CreateRequest();
    Request->SetURL(BackendUrl + Endpoint);
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request->SetContentAsString(JsonData);
    Request->ProcessRequest();
}

void ANexusGameSDK::GetRequest(const FString& Endpoint, FHttpRequestCompleteDelegate Callback)
{
    if (!HttpModule) return;

    FHttpRequestRef Request = HttpModule->CreateRequest();
    Request->SetURL(BackendUrl + Endpoint);
    Request->SetVerb(TEXT("GET"));
    Request->OnProcessRequestComplete() = Callback;
    Request->ProcessRequest();
}

void ANexusGameSDK::GetLeaderboard(int32 Limit, FOnLeaderboardReceived OnComplete)
{
    FString Endpoint = FString::Printf(TEXT("/leaderboard/top?limit=%d"), Limit);
    GetRequest(Endpoint, FHttpRequestCompleteDelegate::CreateLambda(
        [OnComplete](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
        {
            if (bWasSuccessful && Response)
                OnComplete.ExecuteIfBound(true, Response->GetContentAsString());
            else
                OnComplete.ExecuteIfBound(false, TEXT(""));
        }
    ));
}

void ANexusGameSDK::GetFeatureFlags(FOnLeaderboardReceived OnComplete)
{
    GetRequest(TEXT("/feature-flags"), FHttpRequestCompleteDelegate::CreateLambda(
        [OnComplete](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
        {
            if (bWasSuccessful && Response)
                OnComplete.ExecuteIfBound(true, Response->GetContentAsString());
            else
                OnComplete.ExecuteIfBound(false, TEXT(""));
        }
    ));
}

void ANexusGameSDK::GetABVariant(FOnVariantReceived OnComplete)
{
    FString Endpoint = FString::Printf(TEXT("/ab-variant?player_id=%s"), *PlayerId);
    GetRequest(Endpoint, FHttpRequestCompleteDelegate::CreateLambda(
        [OnComplete](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
        {
            FString Variant = TEXT("");
            if (bWasSuccessful && Response)
                Variant = Response->GetContentAsString();
            OnComplete.ExecuteIfBound(bWasSuccessful, Variant);
        }
    ));
}

void ANexusGameSDK::OnHeartbeat()
{
    FString HeartbeatData = TEXT("{\"fps\":60,\"memory_mb\":512}");
    SendTelemetry(TEXT("heartbeat"), HeartbeatData);
}
