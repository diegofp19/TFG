import asyncio

from mavsdk import System

import airsim

from droneMovement import move

from droneCamera import camera

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

    await move(drone)

    await camera()

    print("-----------------", end='')

    # client = airsim.VehicleClient()

    # client.confirmConnection()

    # print(client.isApiControlEnabled())

    # position = client.simGetObjectPose("car")

    # print(client.ping())
    
    # print(position)

    # position.position = position.position + airsim.Vector3r(100, 0,0)

    # try:
    #     client.simSetObjectPose("car", position)
    # except:
    #     print("ERROR: Car movement went wrong!")
    
    


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())