import os
import time
import json
import requests
from paho.mqtt.client import Client, CallbackAPIVersion
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_TLS_CA = os.getenv("MQTT_TLS_CA")
TOPIC_PREFIX = os.getenv("TOPIC_PREFIX", "dessmonitor")
INTERVAL = int(os.getenv("INTERVAL", 10))


client = Client(callback_api_version=CallbackAPIVersion.VERSION2)
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()
client.tls_insecure_set(False)  # Standard: Nur vertrauenswürdige Server erlauben


def publish(topic, value, unit=""):
    payload = json.dumps(
        {
            "value": float(value),
            "unit": unit,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    )
    client.publish(f"{TOPIC_PREFIX}/{topic}", payload, retain=True)


def publish_raw(topic, value):
    payload = json.dumps(float(value))
    client.publish(f"{TOPIC_PREFIX}/{topic}", payload, retain=True)


def publish_timestamp(topic, value):
    payload = json.dumps(value)
    client.publish(f"{TOPIC_PREFIX}/{topic}", payload, retain=True)


def name_correction(name: str) -> str:
    """
    Function to make it easier readable what is what.
    Therefore a more easy understandable naming will be used here.
    It will do it in a loop manner.
    """
    corrections = {
        "bt_battery_": "battery_",
        "bc_output_": "output_",
        "pv_": "solar_pv_",
        "bt_": "battery_",
        "bc_": "output_",
        "gd_grid_": "grid_",
        "gd_": "grid_",
    }
    for correction in corrections:
        name = name.replace(correction, corrections[correction])
    return name


def extract_and_publish(data, add_json=False):
    formatted = data.get("formattedData", {})

    # Publishing it raw without json struct
    publish_raw("live/battery_voltage_V", formatted.get("battery_voltage"))
    publish_raw("live/battery_level_%", formatted.get("battery_real_level"))
    publish_raw("live/load_active_power_kW", formatted.get("load_active_power"))
    publish_raw("live/solar_pv_power_W", formatted.get("solar_pv_power"))
    publish_raw("live/solar_pv_power_kW", float(formatted.get("solar_pv_power")) / 1000)


    if add_json:
        publish("live/battery_voltage", formatted.get("battery_voltage"), "V")
        publish("live/battery_level", formatted.get("battery_real_level"), "%")
        publish("live/load_active_power", formatted.get("load_active_power"), "kW")
        publish("live/solar_pv_power", formatted.get("solar_pv_power"), "kW")

    live = data.get("queryDeviceParsEs", {}).get("parameter", {})
    for item in live:
        publish_raw(f"live/{name_correction(item['par'])}_{item['unit']}", item["val"])
        if add_json:
            # If needed a json will be published
            publish(f"live/{item['par']}", item["val"], item["unit"])

    time_stamp = data.get("querySPDeviceLastData", {}).get("gts", {})
    last_data = data.get("querySPDeviceLastData", {}).get("pars", {})
    publish_timestamp("datapoint/timestamp", time_stamp)

    for part in last_data:
        for val in last_data.get(part):
            publish_raw(
                f"datapoint/{name_correction(part)}/{name_correction(val['id'])}_{val['unit']}",
                val["val"],
            )
            if add_json:
                # If needed a json will be published
                publish(
                    f"datapoint/{name_correction(part)}/{name_correction(val['id'])}",
                    val["val"],
                    val["unit"],
                )

    energy_flow = data.get("webQueryDeviceEnergyFlowEs", {})
    for part in energy_flow:
        if "_status" in part:
            for val in energy_flow.get(part):
                publish_raw(
                    f"energyflow/{name_correction(part)}/{name_correction(val['par'])}_{val.get('unit', '')}",
                    val["val"],
                )
                if add_json:
                    # If needed a json will be published
                    publish(
                        f"energyflow/{name_correction(part)}/{name_correction(val['par'])}",
                        val["val"],
                        val.get("unit", ""),
                    )
        else:
            publish_timestamp(f"energyflow/{part}", energy_flow.get(part, {}))


def main():
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
    while True:
        try:
            res = requests.get(API_URL, timeout=20)
            if res.status_code == 200:
                extract_and_publish(res.json())
            else:
                print(f"Fehler beim Abruf: Status {res.status_code}")
        except Exception as e:
            print("Fehler:", e)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
