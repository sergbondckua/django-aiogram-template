import asyncio

from aiopygismeteo import Gismeteo


async def main():
    d = [
        {"q": "Київ", "l": "ua", "cid": 541696726},
        {"q": "Черкаси, Черкаська", "l": "en", "cid": 541696726}
    ]
    for i in d:
        gm = Gismeteo(lang=i.get("l"))
        search_results = await gm.search.by_query(i.get("q"))
        city_id = search_results[0].id
        forecast = await gm.step3.by_id(id=city_id, days=1)
        print(forecast[6].temperature.air.c)
        print(search_results[0], i.get("cid"))


asyncio.run(main())
