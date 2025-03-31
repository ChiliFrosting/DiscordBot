
import asyncio
import aiohttp


async def twitch_status() -> None:
    status_url = "https://status.twitch.com/api/v2/components.json"

    while True: 
        try:
            async with aiohttp.ClientSession() as session:
                #async with session.get(url = status_url) as response:

                    mock_services = {
                        "components" : [
                            {'id': 'yz28x40y5mq2', 'name': 'Login', 'status': 'operational', 'created_at': '2021-02-10T22:16:01.066Z', 'updated_at': '2023-04-12T19:49:29.486Z', 'position': 1, 'description': None, 'showcase': False, 'start_date': '2021-02-10', 'group_id': None, 'page_id': 'yfj40zdsk34s', 'group': False, 'only_show_if_degraded': False},
                            {'id': 'j6dkmwm0h3k2', 'name': 'Web', 'status': 'operational', 'created_at': '2020-04-21T15:23:49.804Z', 'updated_at': '2024-09-25T21:23:56.763Z', 'position': 2, 'description': None, 'showcase': False, 'start_date': None, 'group_id': None, 'page_id': 'yfj40zdsk34s', 'group': False, 'only_show_if_degraded': False},
                            {'id': '4qrh4gj6bgt2', 'name': 'Chat', 'status': 'operational', 'created_at': '2020-04-21T15:23:57.321Z', 'updated_at': '2024-09-26T13:30:23.595Z', 'position': 3, 'description': None, 'showcase': False, 'start_date': None, 'group_id': None, 'page_id': 'yfj40zdsk34s', 'group': False, 'only_show_if_degraded': False},
                            {'id': 'wkdq12ctv52c', 'name': 'Video (Watching)', 'status': 'operational', 'created_at': '2020-04-21T15:24:38.211Z', 'updated_at': '2023-11-07T21:34:23.558Z', 'position': 4, 'description': None, 'showcase': False, 'start_date': None, 'group_id': None, 'page_id': 'yfj40zdsk34s', 'group': False, 'only_show_if_degraded': False},
                            {'id': '6pr6psm3s003', 'name': 'Video (Broadcasting)', 'status': 'degraded_performance', 'created_at': '2020-04-21T15:24:51.094Z', 'updated_at': '2023-06-27T17:00:55.116Z', 'position': 5, 'description': None, 'showcase': False, 'start_date': None, 'group_id': None, 'page_id': 'yfj40zdsk34s', 'group': False, 'only_show_if_degraded': False},
                            {'id': 'ys9m23jjzpg0', 'name': 'Purchases', 'status': 'operational', 'created_at': '2020-04-21T15:25:00.535Z', 'updated_at': '2024-09-26T13:30:35.033Z', 'position': 6, 'description': None, 'showcase': False, 'start_date': None, 'group_id': None, 'page_id': 'yfj40zdsk34s', 'group': False, 'only_show_if_degraded': False}
                        ]
                    }

                    #response_json = await response.json()
                    services = mock_services.get("components", [])

                    critical = {"Login", "Web", "Video (Broadcasting)", "API"}

                    operational = {
                        service["name"] : service["status"]
                        for service in services
                        if service.get("name") in critical and service.get("status") == "operational"
                    }

                    degraded_performance = {
                        service["name"] : service["status"]
                        for service in services
                        if service.get("name") in critical and service.get("status") == "degraded_performance"
                    }
                    non_operational = {
                        service["name"] : service["status"]
                        for service in services
                        if service.get("name") in critical and service.get("status") not in {"operational", "degraded_performance"}
                    }

                    if non_operational:
                        message = "Could not connect to Twitch services.\n"
                        message += message.join(f"{name} -> {status}\n" for name, status in non_operational.items())
                        message += "Notifications are disabled until services stabalize."

                    elif degraded_performance:
                        message = "".join(f"{name} -> {status}\n" for name, status in operational.items())
                        message += "The following services are experiencing degraded performance:\n"
                        message += "".join(f"{name} -> {service}\n" for name, service in degraded_performance.items())
                        message += "Some notifications may be missed or delayed.\n"

                    elif operational: 
                        message = "".join(f"{name} -> {status}\n" for name, status in operational.items())

                    print(message)
                    await asyncio.sleep(10)

                    
                    

        except Exception as e:
            print(f"Error occurred while checking status: {type(e).__name__} - {e}")
            print("Retrying in 30 minutes....")
            await asyncio.sleep(1800)


asyncio.run(twitch_status())