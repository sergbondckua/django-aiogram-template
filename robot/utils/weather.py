import asyncio

from aiopygismeteo import Gismeteo
from core.settings import GISMETEO_TOKEN


async def main():
    d = [
        {"q": "Черкаси, Львівська, Україна", "l": "ua", "cid": 541696726},
        {"q": "Черкаси, Черкаська", "l": "en", "cid": 541696726}
    ]
    for i in d:
        gm = Gismeteo(token=None, lang=i.get("l"))
        search_results = await gm.search.by_query(query=i.get("q"))
        city_id = search_results[0].id
        forecast = await gm.step3.by_id(city_id, 1)
        lst = [(i.name, i.id) for i in search_results]
        print(search_results)


asyncio.run(main())
