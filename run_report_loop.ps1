# This script runs the language learning report every 2 minutes in an infinite loop.

while ($true) {
    try {
        Write-Host "Running language learning report..."
        # Execute the report script
        & "C:\Users\selam\NEXUS-ONE\report_learned_languages.ps1"
    }
    catch {
        Write-Host "Error running report script: $_"
    }
    
    Write-Host "Waiting for 2 minutes before next report..."
    Start-Sleep -Seconds 120
}
