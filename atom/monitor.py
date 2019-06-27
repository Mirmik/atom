print("Loading monitor module")

import threading
import pycrow
import time
import atom

crowthr = threading.Thread(target=pycrow.spin, args=())
crowthr.start()

#pycrow.diagnostic_enable()

pycrow.set_crowker(".12.127.0.0.1:10017")
pycrow.create_udpgate(12, 10019)

def base_started_notify(pack):
	atom.send_notify("Получено уведомление о запуске главной машины.")

def think_started_notify(pack):
	atom.send_notify("Получено уведомление о запуске think.")

def subscribe_thread():
	while 1:
		pycrow.subscribe("base-status",  base_started_notify)
		pycrow.subscribe("think-status",  think_started_notify)
		time.sleep(2)

substhr = threading.Thread(target=subscribe_thread, args=())
substhr.start()