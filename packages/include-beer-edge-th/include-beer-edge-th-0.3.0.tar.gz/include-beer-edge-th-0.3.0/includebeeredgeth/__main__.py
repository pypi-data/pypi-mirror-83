# main script for Temperature Humidity package
__version__ = "0.3.0"

from datetime import datetime
import os
import importlib
import core.config.manager as cfg_mgr
import core.utils.logging as logger
import core.utils.csv as csv
import core.utils.ftp as ftp

# Set config object
config = cfg_mgr.ConfigManager()

# Set stats objects
stats_buffer = {}
stats_field_names = ['timestamp', 'temperature', 'humidity']
stats_dir = os.path.expanduser(config.stats_dir)
if not os.path.exists(stats_dir):
    os.makedirs(stats_dir)
stats_file = stats_dir + '/' + __package__ + '.csv'
stats_date = datetime.now()
stats_buffer['timestamp'] = stats_date.isoformat()

# Set logging objects
log_buffer = []
log_dir = os.path.expanduser(config.log_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, __package__ + '.log')
log_this = logger.load_logger(
    __package__, log_file, config.debugging)

# build ftp connection
ftps = ftp.connect_tls(config.azure_app.ftp_host,
        config.azure_app.ftp_user, config.azure_app.ftp_passwd)
try:
    ftps.cwd(config.azure_app.ftp_data_dir)
    print(config.azure_app)
except Exception:
    ftps.mkd(config.azure_app.ftp_data_dir)

# Load ambient sensor module
ambient_sensor = config.ambient_sensor.type
log_this.debug('Set ambient sensor to: ' + ambient_sensor)
try:
    a_sensor = importlib.import_module(ambient_sensor)
except Exception as e:
    log_this.error('Error loading ambient sensor: ' +
                    ambient_sensor + ' exception: ' + str(e))

# Get ambient temperature and humidity
ambient_temp, ambient_humidity = a_sensor.read(config.ambient_sensor.pin)
if isinstance(ambient_temp, (float, int)) and isinstance(ambient_humidity, (float, int)):
    stats_buffer['humidity'] = ambient_humidity
    stats_buffer['temperature'] = ambient_temp
    csv.dict_writer(stats_file, stats_field_names, stats_buffer)
    log_buffer.append('A/T: ' + str(ambient_temp))
    log_buffer.append('A/H: ' + str(ambient_humidity))
    log_this.info(' | '.join(map(str, log_buffer)))
else:
    log_this.error('Error reading ' + config.ambient_sensor.type + 
        ' : ' + str(ambient_temp) + ' ' + str(ambient_humidity))

# send stats file to ftp site if it exists
if os.path.exists(stats_file):
    ftps.storbinary("STOR " + stats_file.split('/')
                    [-1], open(stats_file, 'rb'))

ftps.close()
