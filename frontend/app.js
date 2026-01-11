// AETHEROS Dashboard JavaScript

const API_BASE_URL = 'http://localhost:8000/api';
let logsPaused = false;

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    console.log('AETHEROS Dashboard initialized');
    refreshMetrics();
    updateSystemInfo();
    startLiveLogs();

    // Auto-refresh every 30 seconds
    setInterval(refreshMetrics, 30000);
    setInterval(updateSystemInfo, 60000);
});

// API Helper
async function callAPI(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'API Error');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        addLog(`API Error: ${error.message}`, 'error');
        throw error;
    }
}

// Metrics
async function refreshMetrics() {
    try {
        const health = await callAPI('/health');
        const metrics = await callAPI('/system/metrics');

        // Update CPU
        const cpuPercent = metrics.data?.metrics?.cpu_percent || 0;
        document.getElementById('cpu-usage').textContent = `${cpuPercent.toFixed(1)}%`;
        document.getElementById('cpu-progress').style.width = `${cpuPercent}%`;

        // Update Memory
        const memoryPercent = metrics.data?.metrics?.memory_percent || 0;
        document.getElementById('memory-usage').textContent = `${memoryPercent.toFixed(1)}%`;
        document.getElementById('memory-progress').style.width = `${memoryPercent}%`;

        // Update Disk
        const diskPercent = metrics.data?.metrics?.disk_percent || 0;
        document.getElementById('disk-usage').textContent = `${diskPercent.toFixed(1)}%`;
        document.getElementById('disk-progress').style.width = `${diskPercent}%`;

        addLog('Metrics refreshed', 'info');

    } catch (error) {
        addLog('Failed to refresh metrics', 'error');
    }
}

// System Info
async function updateSystemInfo() {
    try {
        const status = await callAPI('/system/status');

        document.getElementById('module-count').textContent =
            status.data?.nexus_core?.modules_loaded || 0;

        document.getElementById('system-version').textContent =
            status.data?.config?.version || '2.0.0';

        // Update uptime
        const uptime = status.data?.nexus_core?.uptime || 0;
        document.getElementById('system-uptime').textContent =
            formatUptime(uptime);

    } catch (error) {
        console.error('Failed to update system info:', error);
    }
}

// Backup Functions
async function createBackup() {
    try {
        const result = await callAPI('/backup/create', 'POST', {
            name: `manual_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}`
        });

        if (result.success) {
            addLog(`Backup started: ${result.backup_id}`, 'success');
            showNotification('Backup started successfully!', 'success');

            // Update backup info after 5 seconds
            setTimeout(updateBackupInfo, 5000);
        }
    } catch (error) {
        addLog(`Backup failed: ${error.message}`, 'error');
        showNotification('Backup failed!', 'error');
    }
}

async function listBackups() {
    try {
        const result = await callAPI('/backup/list?limit=10');

        if (result.success && result.data.length > 0) {
            const backupList = result.data.map(b =>
                `${b.name} (${new Date(b.start_time).toLocaleString()})`
            ).join('\n');

            showNotification(`Recent backups:\n${backupList}`, 'info');
        } else {
            showNotification('No backups found', 'info');
        }
    } catch (error) {
        showNotification('Failed to list backups', 'error');
    }
}

async function updateBackupInfo() {
    try {
        const result = await callAPI('/backup/list?limit=1');

        if (result.success && result.data.length > 0) {
            const latest = result.data[0];
            document.getElementById('last-backup').textContent =
                new Date(latest.start_time).toLocaleString();
            document.getElementById('backup-count').textContent =
                result.count || 0;
        }
    } catch (error) {
        console.error('Failed to update backup info:', error);
    }
}

// System Actions
function optimizeSystem() {
    addLog('System optimization started...', 'info');
    showNotification('Optimizing system...', 'info');

    // Simulate optimization
    setTimeout(() => {
        addLog('System optimization completed', 'success');
        showNotification('System optimized successfully!', 'success');
        refreshMetrics();
    }, 2000);
}

function emergencyStop() {
    if (confirm('⚠️ Are you sure you want to emergency stop? This will stop all modules.')) {
        addLog('Emergency stop initiated', 'warning');
        showNotification('Emergency stop initiated', 'warning');

        // Call emergency stop API
        callAPI('/command', 'POST', {
            command: 'emergency_stop'
        }).then(() => {
            addLog('System stopped', 'error');
            showNotification('System stopped', 'error');
        }).catch(error => {
            addLog(`Stop failed: ${error.message}`, 'error');
        });
    }
}

// Log Functions
function addLog(message, level = 'info') {
    if (logsPaused) return;

    const logContainer = document.getElementById('log-container');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';

    const time = new Date().toLocaleTimeString();
    const levelClass = `log-${level}`;

    logEntry.innerHTML = `
        <span class="log-time">[${time}]</span>
        <span class="${levelClass}">${message}</span>
    `;

    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

function clearLogs() {
    document.getElementById('log-container').innerHTML = '';
    addLog('Logs cleared', 'info');
}

function toggleLogs() {
    logsPaused = !logsPaused;
    const button = document.querySelector('button[onclick="toggleLogs()"]');
    button.innerHTML = logsPaused ?
        '<i class="fas fa-play"></i> Resume' :
        '<i class="fas fa-pause"></i> Pause';

    addLog(logsPaused ? 'Logs paused' : 'Logs resumed', 'info');
}

function startLiveLogs() {
    // Simulate live logs (in real app, use WebSocket)
    setInterval(() => {
        if (!logsPaused && Math.random() > 0.7) {
            const messages = [
                'System check completed',
                'Monitoring disk usage',
                'Checking network connectivity',
                'Updating cache',
                'Verifying backups'
            ];
            const levels = ['info', 'success', 'info', 'info', 'success'];
            const idx = Math.floor(Math.random() * messages.length);
            addLog(messages[idx], levels[idx]);
        }
    }, 5000);
}

// Utility Functions
function formatUptime(seconds) {
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h`;
    return `${Math.floor(seconds / 86400)}d`;
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Style
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;

    // Add to page
    document.body.appendChild(notification);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Menu Functions
function openAPIDocs() {
    window.open('/api/docs', '_blank');
}

function showLogs() {
    document.getElementById('log-container').scrollIntoView({ behavior: 'smooth' });
}

function showMetrics() {
    refreshMetrics();
    showNotification('Metrics refreshed', 'info');
}

function openBackupConfig() {
    showNotification('Backup configuration opened in new tab', 'info');
    // In real app, open config page
}

// Error handling
window.addEventListener('error', function (event) {
    addLog(`JavaScript Error: ${event.message}`, 'error');
    console.error('Global error:', event.error);
});

// Online/Offline detection
window.addEventListener('online', () => {
    addLog('Network connection restored', 'success');
    refreshMetrics();
});

window.addEventListener('offline', () => {
    addLog('Network connection lost', 'error');
});
