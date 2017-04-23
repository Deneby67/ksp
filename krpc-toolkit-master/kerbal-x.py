import krpc
import time
from krpctoolkit.launch import Ascend
from krpctoolkit.staging import AutoStage
from krpctoolkit.maneuver import circularize, ExecuteNode

target_altitude = 19500000

conn = krpc.connect(name='Kerbal-X')
vessel = conn.space_center.active_vessel

print('Launching')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
ascend = Ascend(conn, vessel, target_altitude)
staging = AutoStage(conn, vessel)
while not ascend():
    staging()
    print(altitude())
    time.sleep(0.5)

print('Coasting out of atmosphere')
# time.sleep(5)
# raise Exception()
# altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
atmosphere_altitude = vessel.orbit.body.atmosphere_depth * 1.01


while altitude() < atmosphere_altitude:
    pass

print('Circularizing')
vessel.control.remove_nodes()
node = circularize(conn, vessel)
execute = ExecuteNode(conn, vessel, node)
while not execute():
    time.sleep(0.1)
node.remove()

print('Complete')
