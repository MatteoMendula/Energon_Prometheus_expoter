import time
import energon
from prometheus_client import start_http_server, Gauge, Info

class EnergonPrometheusExporter:

    def __init__(self, app_port=9877, polling_interval_seconds=5):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        # Start up the server to expose the metrics.
        self.energon = energon.Energon()

        # ----------------- Prometheus metrics to collect -----------------
        # static metrics
        self.jetson_model = Info("energon_jetson_model", "Jetson model")
        self.n_cores = Info("energon_n_cores", "Number of cores")
        self.network_interfaces = Info("energon_available_network_interfaces", "Available network interfaces")
        
        # power metrics
        self.current_total_power_consumption = Gauge("energon_total_power_consumption_mW", "Current total power consumption in milliwatts")
        self.current_cpu_power_consumption = Gauge("energon_cpu_power_consumption_mW", "Current cpu power consumption in milliwatts")
        self.current_gpu_power_consumption = Gauge("energon_gpu_power_consumption_mW", "Current gpu power consumption in milliwatts")
        
        # network metrics
        self.network_metrics_eth0_rx_packets = Gauge("energon_network_metrics_eth0_rx_packets_per_seconds", "Network metrics eth0 rx_packets_per_seconds")
        self.network_metrics_eth0_rx_bytes = Gauge("energon_network_metrics_eth0_rx_bytes_per_seconds", "Network metrics eth0 rx_bytes_per_seconds")
        self.network_metrics_eth0_rx_errors = Gauge("energon_network_metrics_eth0_rx_errors_per_seconds", "Network metrics eth0 rx_errors_per_seconds")
        self.network_metrics_eth0_rx_dropped = Gauge("energon_network_metrics_eth0_rx_dropped_per_seconds", "Network metrics eth0 rx_dropped_per_seconds")
        self.network_metrics_eth0_tx_packets = Gauge("energon_network_metrics_eth0_tx_packets_per_seconds", "Network metrics eth0 tx_packets_per_seconds")
        self.network_metrics_eth0_tx_bytes = Gauge("energon_network_metrics_eth0_tx_bytes_per_seconds", "Network metrics eth0 tx_bytes_per_seconds")
        self.network_metrics_eth0_tx_errors = Gauge("energon_network_metrics_eth0_tx_errors_per_seconds", "Network metrics eth0 tx_errors_per_seconds")
        self.network_metrics_eth0_tx_dropped = Gauge("energon_network_metrics_eth0_tx_dropped_per_seconds", "Network metrics eth0 tx_dropped_per_seconds")

        # cpu frequency metrics
        self.cpu_core_0_frequency = Gauge("energon_cpu_core_0_MHz", "CPU core_0 frequency in MHz")
        self.cpu_core_1_frequency = Gauge("energon_cpu_core_1_MHz", "CPU core_1 frequency in MHz")
        self.cpu_core_2_frequency = Gauge("energon_cpu_core_2_MHz", "CPU core_2 frequency in MHz")
        self.cpu_core_3_frequency = Gauge("energon_cpu_core_3_MHz", "CPU core_3 frequency in MHz")

        # cpu load metrics
        self.cpu_total_load = Gauge("energon_cpu_total_load_percentage", "CPU total load in %")
        self.cpu_core_0_load = Gauge("energon_cpu_core_0_load_percentage", "CPU core_0 load in %")
        self.cpu_core_1_load = Gauge("energon_cpu_core_1_load_percentage", "CPU core_1 load in %")
        self.cpu_core_2_load = Gauge("energon_cpu_core_2_load_percentage", "CPU core_2 load in %")
        self.cpu_core_3_load = Gauge("energon_cpu_core_3_load_percentage", "CPU core_3 load in %")

        # storage metrics
        self.storage_total = Gauge("energon_storage_total_bytes", "Storage total in bytes")
        self.storage_used = Gauge("energon_storage_used_bytes", "Storage used in bytes")
        self.storage_available = Gauge("energon_storage_available_bytes", "Storage available in bytes")
        self.storage_percent_used = Gauge("energon_storage_percent_used_percentage", "Storage percent used in %")

        # ram metrics 
        self.ram_total = Gauge("energon_ram_total_bytes", "RAM total in bytes")
        self.ram_free = Gauge("energon_ram_free_bytes", "RAM free in bytes")
        self.ram_available = Gauge("energon_ram_available_bytes", "RAM available in bytes")
        self.ram_percent_used = Gauge("energon_ram_percent_used_percentage", "RAM percent used in %")

        # gpu metrics
        self.gpu_total_percent_used = Gauge("energon_gpu_total_percent_used_percentage", "GPU total percent used in %")

        # temperature metrics
        self.temperature_ao = Gauge("energon_temperature_ao_mC", "Temperature ao in mC")
        self.temperature_cpu = Gauge("energon_temperature_cpu_mC", "Temperature cpu in mC")
        self.temperature_gpu = Gauge("energon_temperature_gpu_mC", "Temperature gpu in mC")
        self.temperature_pll = Gauge("energon_temperature_pll_mC", "Temperature pll in mC")
        self.temperature_pmic = Gauge("energon_temperature_pmic_mC", "Temperature pmic in mC")
        self.temperature_fan = Gauge("energon_temperature_fan_mC", "Temperature fan in mC")
    
    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        self.jetson_model = self.energon.detected_model
        self.n_cores = self.energon.n_cores
        self.network_interfaces = self.energon.network_interfaces

        # power metrics
        current_total_power_consumption = self.energon.get_energy_metrics()
        self.current_total_power_consumption = current_total_power_consumption["total"]
        self.current_cpu_power_consumption = current_total_power_consumption["cpu"]
        self.current_gpu_power_consumption = current_total_power_consumption["gpu"]

        # network metrics
        self.network_metrics_eth0_rx_packets = self.energon.get_network_metrics()["eth0"]["rx_packets"]
        self.network_metrics_eth0_rx_bytes = self.energon.get_network_metrics()["eth0"]["rx_bytes"]
        self.network_metrics_eth0_rx_errors = self.energon.get_network_metrics()["eth0"]["rx_errors"]
        self.network_metrics_eth0_rx_dropped = self.energon.get_network_metrics()["eth0"]["rx_dropped"]
        self.network_metrics_eth0_tx_packets = self.energon.get_network_metrics()["eth0"]["tx_packets"]
        self.network_metrics_eth0_tx_bytes = self.energon.get_network_metrics()["eth0"]["tx_bytes"]
        self.network_metrics_eth0_tx_errors = self.energon.get_network_metrics()["eth0"]["tx_errors"]
        self.network_metrics_eth0_tx_dropped = self.energon.get_network_metrics()["eth0"]["tx_dropped"]

        # cpu frequency metrics
        current_cpu_frequency_metrics = self.energon.get_cpu_frequency_metrics()
        self.cpu_core_0_frequency = current_cpu_frequency_metrics["core_0"]
        self.cpu_core_1_frequency = current_cpu_frequency_metrics["core_1"]
        self.cpu_core_2_frequency = current_cpu_frequency_metrics["core_2"]
        self.cpu_core_3_frequency = current_cpu_frequency_metrics["core_3"]

        # cpu load metrics
        current_cpu_load_metrics = self.energon.get_cpu_load_metrics()
        self.cpu_total_load = current_cpu_load_metrics["total"]
        self.cpu_core_0_load = current_cpu_load_metrics["core_0"]
        self.cpu_core_1_load = current_cpu_load_metrics["core_1"]
        self.cpu_core_2_load = current_cpu_load_metrics["core_2"]
        self.cpu_core_3_load = current_cpu_load_metrics["core_3"]

        # storage metrics
        current_storage_metrics = self.energon.get_storage_metrics()
        self.storage_total = current_storage_metrics["total"]
        self.storage_used = current_storage_metrics["used"]
        self.storage_available = current_storage_metrics["available"]
        self.storage_percent_used = current_storage_metrics["percent_used"]

        # ram metrics
        current_ram_metrics = self.energon.get_ram_metrics()
        self.ram_total = current_ram_metrics["total"]
        self.ram_free = current_ram_metrics["free"]
        self.ram_available = current_ram_metrics["available"]
        self.ram_percent_used = current_ram_metrics["percent_used"]

        # gpu metrics
        self.gpu_total_percent_used = self.energon.get_gpu_metrics()["total_percent_used"]

        # temperature metrics
        current_temperature_metrics = self.energon.get_temperature_metrics()
        self.temperature_ao = current_temperature_metrics["ao"]
        self.temperature_cpu = current_temperature_metrics["cpu"]
        self.temperature_gpu = current_temperature_metrics["gpu"]
        self.temperature_pll = current_temperature_metrics["pll"]
        self.temperature_pmic = current_temperature_metrics["pmic"]
        self.temperature_fan = current_temperature_metrics["fan"]

    
    def run(self):
        """Run the metrics server"""
        start_http_server(self.app_port)
        self.run_metrics_loop()

if __name__ == "__main__":
    server = EnergonPrometheusExporter()
    server.run()