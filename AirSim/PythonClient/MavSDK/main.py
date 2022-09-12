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


    
    


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())