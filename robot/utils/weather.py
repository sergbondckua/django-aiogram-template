import asyncio

from aiopygismeteo import Gismeteo
from core.settings import GISMETEO_TOKEN


async def main():
    d = [
        {"q": "е", "l": "ua", "cid": 541696726},
        {"q": "Черкаси, Черкаська", "l": "en", "cid": 541696726}
    ]
    for i in d:

        gm = Gismeteo(token="eeffefe", lang=i.get("l"))
        search_results = await gm.search.by_query(i.get("q"))
        # city_id = search_results[0].id
        # forecast = await gm.current.by_id(id=4956)
        print(gm)



asyncio.run(main())
