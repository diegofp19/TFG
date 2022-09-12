
import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def move(drone):
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 15m Up to avoid trees")
    await drone.offboard.set_position_ned(PositionNedYaw(0, 0, -15, 0))
    await asyncio.sleep(10)
    # Camera down mode
    print("-- Go 90m South, 100m East, -15m Down within local coordinate system")
    await drone.offboard.set_position_ned(PositionNedYaw(70, 100, -15, 0))
    # print("-- Go 15m Up to avoid trees")
    # await drone.offboard.set_position_ned(PositionNedYaw(0, 0, -15, 180))
    # await asyncio.sleep(10)
    # print("-- Go 90m South, 100m East, -15m Down within local coordinate system")
    # await drone.offboard.set_position_ned(PositionNedYaw(90, 100, -15, 180))
    # await asyncio.sleep(10)
    # print("-- Go -2m Down")
    # await drone.offboard.set_position_ned(PositionNedYaw(90, 100, 5, 180))












#     print_mission_progress_task = asyncio.ensure_future(
#         print_mission_progress(drone))

#     running_tasks = [print_mission_progress_task]
#     # termination_task = asyncio.ensure_future(
#     #      observe_is_in_air(drone, running_tasks))

#     mission_items = []
#     mission_items.append(MissionItem(40.542477, -4.011132,
#                                      35,
#                                      30,
#                                      True,
#                                      float('nan'),
#                                      float('nan'),
#                                      MissionItem.CameraAction.NONE,
#                                      float('nan'),
#                                      float('nan'),
#                                      float('nan'),
#                                      float('nan'),
#                                      ))

#     mission_items.append(MissionItem(40.542614, -4.011158,
#                                      35,
#                                      30,
#                                      False,
#                                      float('nan'),
#                                      float('nan'),
#                                      MissionItem.CameraAction.NONE,
#                                      float('nan'),
#                                      float('nan'),
#                                      float('nan'),
#                                      float('nan'),
#                                      ))
   

#     mission_plan = MissionPlan(mission_items)



#     print("-- Uploading mission")
#     drone.mission.upload_mission(mission_plan)

#     print("-- Arming")
#     drone.action.arm()

#     print("-- Starting mission")
#     drone.mission.start_mission()

#     # termination_task


# async def print_mission_progress(drone):
#     async for mission_progress in drone.mission.mission_progress():
#         print(f"Mission progress: "
#               f"{mission_progress.current}/"
#               f"{mission_progress.total}")


# async def observe_is_in_air(drone, running_tasks):
#     """ Monitors whether the drone is flying or not and
#     returns after landing """

#     was_in_air = False

#     async for is_in_air in drone.telemetry.in_air():
#         if is_in_air:
#             was_in_air = is_in_air

#         if was_in_air and not is_in_air:
#             for task in running_tasks:
#                 task.cancel()
#                 try:
#                     await task
#                 except asyncio.CancelledError:
#                     pass
#             await asyncio.get_event_loop().shutdown_asyncgens()

#             return


# async def completed_mission(drone):
#     """ Monitors whether the drone is flying or not and
#     returns after landing """
#     async for mission_progress in drone.mission.mission_progress():
#         if(mission_progress.current == mission_progress.total):
#             await asyncio.get_event_loop().shutdown_asyncgens()