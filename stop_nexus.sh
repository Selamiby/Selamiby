# Nexus'u durdurmak için:
pkill -f nexus_orchestrator.py

# Veya
docker stop nexus_auto

# Veya acil kill switch
echo "STOP" > /tmp/nexus_stop.signal
