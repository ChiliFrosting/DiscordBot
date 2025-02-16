
import asyncio
import aiohttp


async def twitch_status() -> None:
    status_url = "https://status.twitch.com/api/v2/components.json"

    while True: 
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url = status_url) as response: 
                    response_json = await response.json()
                    services = ""
                    for i in range(0, 7):

                        service = response_json["components"][i]["name"]
                        status = response_json["components"][i]["status"]
                        services += f"{service} -> {status}\n"

                    print(services)

                    break

        except Exception as e:
            print(f"Error occurred while checking status: {type(e).__name__} - {e}")


asyncio.run(twitch_status())