# ⚡ dess-to-mqtt  
[![Docker Pulls](https://img.shields.io/docker/pulls/9madmax5/dess-to-mqtt?style=flat-square)](https://hub.docker.com/r/9madmax5/dess-to-mqtt)  
[![GitHub Stars](https://img.shields.io/github/stars/9Mad-Max5/dess-to-mqtt?style=flat-square)](https://github.com/9Mad-Max5/dess-to-mqtt/stargazers)  
[![GitHub Forks](https://img.shields.io/github/forks/9Mad-Max5/dess-to-mqtt?style=flat-square)](https://github.com/9Mad-Max5/dess-to-mqtt/network/members)  
[![GitHub Issues](https://img.shields.io/github/issues/9Mad-Max5/dess-to-mqtt?style=flat-square)](https://github.com/9Mad-Max5/dess-to-mqtt/issues)  
[![GitHub License](https://img.shields.io/github/license/9Mad-Max5/dess-to-mqtt?style=flat-square)](https://github.com/9Mad-Max5/dess-to-mqtt/blob/main/LICENSE)  

> 🔗 [GitHub Repository](https://github.com/9Mad-Max5/dess-to-mqtt) • 🐳 [Docker Hub](https://hub.docker.com/r/9madmax5/dess-to-mqtt)

Periodically fetches live data from a DESS API endpoint and publishes structured MQTT messages – ideal for integration with Home Assistant, Node-RED, or Grafana.


## ✨ Features
- ✅ Periodically fetches live data from a DESS API endpoint  
- ✅ Publishes structured MQTT messages with timestamps  
- ✅ Supports raw values and JSON-formatted MQTT payloads  
- ✅ Simplified MQTT topic naming for easier integration  
- ✅ TLS-secured MQTT connection  
- ✅ Customizable fetch intervals  
- ✅ Docker-ready for easy deployment


## 🐳 Quick Start with Docker
Example `docker-compose.yaml`:

```yaml
version: '3.8'

services:
  dess-to-mqtt:
    image: 9madmax5/dess-to-mqtt:latest
    container_name: dess-to-mqtt
    restart: unless-stopped
    environment:
      API_URL: https://example.com/api/data
      MQTT_HOST: mqtt.example.com
      MQTT_PORT: 8883
      MQTT_USER: yourMqttUser
      MQTT_PASS: yourMqttPass
      MQTT_TLS_CA: /certs/ca.crt
      TOPIC_PREFIX: dessmonitor
      INTERVAL: 10
    volumes:
      - ./certs:/certs:ro
```


## ⚙️ Environment Variables
| Variable        | Required | Description                                                   |
|-----------------|----------|---------------------------------------------------------------|
| `API_URL`       | ✅        | The DESS API endpoint                                         |
| `MQTT_HOST`     | ✅        | Hostname or IP of the MQTT broker                            |
| `MQTT_PORT`     | ❌        | Port for the MQTT connection (default: `8883`)               |
| `MQTT_USER`     | ✅        | MQTT username                                                 |
| `MQTT_PASS`     | ✅        | MQTT password                                                 |
| `MQTT_TLS_CA`   | ❌        | Path to the CA certificate for the MQTT connection           |
| `TOPIC_PREFIX`  | ❌        | MQTT topic prefix (default: `dessmonitor`)                   |
| `INTERVAL`      | ❌        | Polling interval in seconds (default: `10`)                  |


## 🔁 How It Works
1. Establishes a secure connection to the MQTT broker  
2. Periodically sends a GET request to the configured API endpoint  
3. Parses and normalizes incoming JSON data  
4. Publishes values under structured topics like:
   - `dessmonitor/live/battery_voltage_V`
   - `dessmonitor/datapoint/battery/battery_soc_%`
   - `dessmonitor/energyflow/grid/grid_import_kW`
5. Optionally publishes extended JSON payloads with timestamps and units


## 🧪 Local Development
You’ll need **Python 3.10+** and a `.env` file with your configuration:

```bash
pip install -r requirements.txt
python main.py
```

Example `.env`:

```env
API_URL=https://example.com/api/data
MQTT_HOST=mqtt.example.com
MQTT_PORT=8883
MQTT_USER=youruser
MQTT_PASS=yourpass
TOPIC_PREFIX=dessmonitor
INTERVAL=10
```


## 📈 Example Topics & Payloads

**Topic:** `dessmonitor/live/battery_voltage_V`  
**Payload:** `13.2`

**Topic:** `dessmonitor/datapoint/battery/battery_soc_%`  
**Payload:** `75.4`

**Topic:** `dessmonitor/live/solar_pv_power_kW`  
**Payload:**  
```json
{
  "value": 2.31,
  "unit": "kW",
  "ts": "2025-07-17T10:15:00Z"
}
```


## 📌 Use Cases
- Monitor your PV/battery/grid setup in real time  
- Integrate with dashboards and home automation tools  
- Replace proprietary gateways with your own data pipeline


## ⚠️ Legal Notice
This project is **not affiliated with** or **endorsed by** any DESS hardware or API vendor. Use at your own risk.

All trademarks and brand names belong to their respective owners.


## ✉️ Feedback & Contributing
Missing a feature or found a bug?  
Feel free to open an [issue on GitHub](https://github.com/9Mad-Max5/dess-to-mqtt/issues) or contribute via pull request!