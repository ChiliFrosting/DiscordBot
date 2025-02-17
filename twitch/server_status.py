
import asyncio
import aiohttp


async def twitch_status() -> None:
    status_url = "https://status.twitch.com/api/v2/components.json"

    while True: 
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url = status_url) as response:

                    response_json = await response.json()
                    services = response_json.get("components", [])
                    non_operational = {}
                    critical_services = ["Login", "Video (Broadcasting)", "API"]

                    for service in services:
                        if service.get("status") != "operational":
                            non_operational[service.get("name", "Unavailable")] = service.get("status", "Unavailable")

                    if any(service in non_operational for service in critical_services):
                        print("Unable to reach Twitch servers")

                        await asyncio.sleep(1800)

                    else:
                        print(
                            f"Twitch services operational.\n"
                            "Login -> OK\nAPI -> OK\nVideo (Broadcasting) -> OK"
                        )
                        break
                            

        except Exception as e:
            print(f"Error occurred while checking status: {type(e).__name__} - {e}")
            print("Retrying in 30 minutes....")
            await asyncio.sleep(1800)


asyncio.run(twitch_status())