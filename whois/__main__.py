from . import get_whois_info, get_whois_info_async
import asyncio


async def main(domain_name: str):
    print(await get_whois_info_async(domain_name))


if __name__ == "__main__":
    domain_name = input("Enter a domain name: ")
    whois_info = get_whois_info(domain_name)

    print(whois_info)

    asyncio.run(main(domain_name))