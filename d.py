import krpc

from krpctoolkit.launch import Ascend
from krpctoolkit.maneuver import circularize, ExecuteNode


def launch():
    target_altitude = 80000

    conn = krpc.connect(name='Kerbal-X')
    vessel = conn.space_center.active_vessel

    print('Launching')
    ascend = Ascend(conn, vessel, target_altitude, sas=True)
    staging = ascend.staging
    while not ascend():
        staging()

    print('Coasting out of atmosphere')
    altitude = ascend.altitude
    atmosphere_altitude = vessel.orbit.body.atmosphere_depth * 1.05
    while altitude() < atmosphere_altitude:
        staging()

    print('Circularizing')
    vessel.control.remove_nodes()
    node = circularize(conn, vessel)
    execute = ExecuteNode(conn, vessel, node)
    while not execute():
        staging()
    node.remove()

    print('Complete')
