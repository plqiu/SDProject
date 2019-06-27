import pandas as pd
import numpy as np
import time
start_time=time.time()
try:
    _modbus_release_table = pd.read_csv('conf/ModbusServer.csv',
                                        usecols={'var_name': np.string_,
                                                 'init_value': np.float32,
                                                 'publish_regisrer': np.uint8,
                                                 'data_publish_type': np.string_,
                                                 'scaling': np.float32})

except:
    print ('load ModbusServer.csv failed')

for i in _modbus_release_table.itertuples():
    print i[1]
# for j, i in _modbus_release_table.iterrows():
#     print i[0]
print time.time()
print start_time