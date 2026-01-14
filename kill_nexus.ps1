$procs = Get-CimInstance Win32_Process -Filter "name = 'python.exe' or name = 'pythonw.exe'"
foreach ($p in $procs) {
    if ($p.CommandLine -like "*nexus*") {
        Write-Host "Killing process: $($p.ProcessId) - $($p.CommandLine)"
        Stop-Process -Id $p.ProcessId -Force
    }
}
