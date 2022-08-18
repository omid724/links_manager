# in the name of God

import re
import requests
import urllib.parse


def titleBug5(link):
    """pass the function a link to find its title for you"""

    headers = {}
    data = {}

    # headers = {

    #    "Host": "www.dideo.ir",
    #    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #    "Accept-Language": "en-US,en;q=0.5",
    #    "Accept-Encoding": "gzip, deflate, br",
    #    "Referer": "https://www.dideo.ir/ch/yt/UC_Oao2FYkLAUlUVkBfze4jg/mining-massive-datasets",
    #    "Upgrade-Insecure-Requests": "1",
    #    "Connection": "keep-alive",
    #    "Cookie": "ch=eyJpdiI6Ikt4TWhFWGFSQ3RtUEFpTHp4UUZPRFE9PSIsInZhbHVlIjoiRlRtUWYwQmQ3emtIbzA3WXQ4eVVJUT09IiwibWFjIjoiMGI0ZWY4MjdkZDFjZWZlMDA0MmUyNTAyOWNiYWM2MGQyMGJkYTM0NjU1NmE2OWRjNDZjYWU4ZTc3NjIxNDI1ZSJ9; hm=eyJpdiI6Ilo4aGpcLzNYYWg1c2ZvbFVJQjZXbnh3PT0iLCJ2YWx1ZSI6IjU2a1VQNzA4Y0hCRHYzWHNpcEM4dWc9PSIsIm1hYyI6IjRkZTMzNmMzZTMyODQ4NGI2MDhjYmU2NjYyMmQ5NDZiMWQwM2U5YzdmMzNkNzNlNDY0ZjQ5NmVmZTE3YWI5YzEifQ%3D%3D; _hjid=01ceff05-ab8e-471a-b556-8b10cd74caa9; _ga=GA1.2.1301730268.1622740778; can-ide=1; _ga_WNXH6FY3JQ=GS1.1.1622740885.1.0.1622740889.0; re-au=0; XSRF-TOKEN=eyJpdiI6IjNvckc5XC9BaHZmTXBxV3hOaWljazJ3PT0iLCJ2YWx1ZSI6Imc5R0NXN1NEb2NIY0xvSkhDNTdxblV4SjRuTWhDZ01NYnlPc0dzZHZJa25HeWdFeFIyTjNCMUFTYko3bXVqSkIiLCJtYWMiOiI4MzJhZjgwYTRhNDc5MzA3YThkMjBhZGU5NzNhNjkxNTZlZWI2NzlhMzYyNDkyZmQ5ODdjMDk2MGQ0N2YyNGU2In0%3D; kraken_session=eyJpdiI6Ijl0S1RXTUlTdG84d3J2UHEyOWFwZnc9PSIsInZhbHVlIjoiN3hEZ3VVNlJMNDZTY0xlK2dYNm9CSHU5RkFpNmRLR3BZXC8rTzVTQmIrWUsrY20zcUF0amhQelNrWXNOYkJnajUiLCJtYWMiOiI0MzFjNmU5Zjk1OWJiYzJkYmJiYmRmNzRiZDVhYTRkNGYzODhjMjJlMmY3M2Q5NWY2NTA2MTI1ZjJhZGVlMmVkIn0%3D; vQnnFCkmZZHEodWa0yAOIu6jaf9fwfTMNLeSEFQ4=eyJpdiI6ImxZTUxPYklBU3ZJWHNLcVFsSFZjd1E9PSIsInZhbHVlIjoiaStzeWZ4K1BBKytZT3Arb1ZEam51V0VTVGs5S1wvN1ZzZkxySUZ3OVV2N09Eb2NsRDVtRUZ6b2FlSTU1RFF6RzBkMkNqOXFzNlFSR3BUMzhKRTRrYzE2QmV6QmwzUmpvREMyWkpSQ2NLbEJwWktuQ3hheCtlaXAzWGw1NDBBUDFtZUg1SlNjRVwveGFlbzBhVXRTTEFycXJ6eGNrVktiblJ0eDI1c1hYNG1YdVVmTlJvbWoxWktRMDY5U3pRVjhyenNIbk1HWlFPZXkrTHJtR2lKZE5hZHcyc1pLU214dUxlampnaUdpUm9cL1Nxem1xTUs2VmI2RW9qSk05czVPdXpvdFppSUkyc0RJa2ZRQnljXC9YdmhldEhzaHlwMEltUlc3UEZ6ZlBzM1ZDbzVNQm9XRFQ2dXBaNXNRdGlGQ3hFZEtcL0hVUTk4WGl2b3hDb3RUTlQyZG1adW03d1Q5WHZiTlNkNmN2bUtKUER2Ylh1cExYYjZLa2tSVHZ1Q2JNTllsYStOZG54OGc2ME1Ub1dOQmxhTnpDWjdNVU5RWURNanZyNHpvNU5mbHdUbkhmRXEwaGFUM1JLTDFVcnpST0NPNncrQ2xUR1pDSDFuQXBuaXVBaGVhUit0VTRiMmU0eXg0V1BJOUNQeWVTNHNWVWg2c2p0QTF0OFdDT0k5MWNOV283ZG9JY3c4a1h6T2xoaVY3ajlMQ1VyQXR0U3RwVFwvMUoxd051SHJwbXJYS2RrPSIsIm1hYyI6IjFkOTc2MzFkMDc0NGUyYzkzODliMmQ1YTlhMzkzN2QzZjljYTk4NTY0NTE0YjZkMTkxOWIzMDAxNmFjNzA0MDAifQ%3D%3D; _hjTLDTest=1; _hjAbsoluteSessionInProgress=1; _gid=GA1.2.752561178.1624001582; XSRF-TOKEN=eyJpdiI6Imk0NndVTEhVSUk4N2M1VjVnNW5BdlE9PSIsInZhbHVlIjoiMDBGNXk3d0JxWnpVNElBYVBNcDlyeU12dFBxK2c0bjh2Zk5RRjVhUitIY1ZMR2psQThEcnVvUTZiTGJJT1NUc1VvWElEQVFZT2M5S3YwckFZQytiNWc9PSIsIm1hYyI6ImU4NGMyNWE5YjQyNmJhYjZlZDQ2NTMyZmQxMGRlN2Q0NTdmODE4YTdhODJhMmEzYzZkNGU0ZGQ2Yjk3ZjdhMjgifQ%3D%3D; client-id=eyJpdiI6ImVZdzVtZ1hrRmhQeGRQRUFSZUE1dUE9PSIsInZhbHVlIjoiaG9EMXhaS3VNYU9Pc1dHdVlHSTBnQT09IiwibWFjIjoiNjEzZWU1MmQ1YzAyZDdiMDE0YWMzNzY5YzllNTE5NzJkNTNlZDRiZDQ1MzUwZWE0NjJmNDhiZGYyNWM3NDZhNCJ9; _gat_UA-82218710-1=1"
    #    }
    try:
        total_page = requests.get(link, headers=headers, timeout=7)
        total_text = total_page.text
    except requests.exceptions.MissingSchema:
        print("Couldn't find title")
        total_text = ''
    except requests.exceptions.ConnectionError:
        print("Couldn't find title")
        total_text = ''

    total_page = re.sub(r'\n', '', total_text)

    title = re.findall(r'title>(.+?)</title', total_page)
    try:
        title = title[0].strip()
    except IndexError:
        print("Title didn't find.")
        title = '---'
        # answer = input('Do you want try find title from url if it has unicode? [Y/N]? ')
        answer = "y"
        if answer == "y" or answer == "Y":
            title = urllib.parse.unquote(link, encoding='utf-8', errors='replace')

    return title
