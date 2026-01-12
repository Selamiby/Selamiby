// NEXUS Game SDK - Unreal Engine (C++)
// Header file: NexusGameSDK.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Http.h"
#include "Json.h"
#include "NexusGameSDK.generated.h"

DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnLeaderboardReceived, bool, bSuccess, const FString&, Response);
DECLARE_DYNAMIC_DELEGATE_TwoParams(FOnVariantReceived, bool, bSuccess, const FString&, Variant);

UCLASS()
class GAME_API ANexusGameSDK : public AActor
{
    GENERATED_BODY()

public:
    ANexusGameSDK();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

    UFUNCTION(BlueprintCallable, Category = "Nexus")
    void Initialize(const FString& InPlayerId, const FString& BackendUrl = TEXT("http://127.0.0.1:7000"));

    UFUNCTION(BlueprintCallable, Category = "Nexus")
    void SubmitScore(int32 Score, const FString& MetadataJSON = TEXT("{}"));

    UFUNCTION(BlueprintCallable, Category = "Nexus")
    void SendTelemetry(const FString& EventName, const FString& PayloadJSON = TEXT("{}"));

    UFUNCTION(BlueprintCallable, Category = "Nexus")
    void ReportCrash(const FString& StackTrace, const FString& DeviceInfoJSON = TEXT("{}"));

    UFUNCTION(BlueprintCallable, Category = "Nexus")
    void GetLeaderboard(int32 Limit, FOnLeaderboardReceived OnComplete);

    UFUNCTION(BlueprintCallable, Category = "Nexus")
    void GetFeatureFlags(FOnLeaderboardReceived OnComplete);

    UFUNCTION(BlueprintCallable, Category = "Nexus")
    void GetABVariant(FOnVariantReceived OnComplete);

private:
    FString PlayerId;
    FString BackendUrl;
    bool bInitialized;
    float HeartbeatTimer;

    void PostRequest(const FString& Endpoint, const FString& JsonData);
    void GetRequest(const FString& Endpoint, FHttpRequestCompleteDelegate Callback);
    void OnHeartbeat();

    FHttpModule* HttpModule;
};
