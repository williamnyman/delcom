import requests

url = "https://www.ubereats.com/_p/api/getSearchFeedV1"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Cookie": "dId=6e44940b-4671-4703-a78e-b28f7055b3ff; marketing_vistor_id=052e3e47-3c96-4860-9cfd-527a3656cb79; uev2.gg=true; _scid=B3Doay9XEw5kbKs1os8IjguFpOsxTXQA; _fbp=fb.1.1752442609419.590241800677165254; _gcl_au=1.1.460400741.1752442610; _yjsu_yjad=1752442609.872823be-75cf-40e2-b68b-6abc06072ccc; _tt_enable_cookie=1; _ttp=01K02VG82JCC2ZXAB39B9QB6RN_.tt.1; _ga=GA1.1.1440118121.1752442610; u-cookie-prefs=eyJ2ZXJzaW9uIjoxMDAsImRhdGUiOjE3NTMxMzIzODc0ODQsImNvb2tpZUNhdGVnb3JpZXMiOlsiYWxsIl0sImltcGxpY2l0IjpmYWxzZX0%3D; uev2.loc=%7B%22address%22%3A%7B%22address1%22%3A%221042%20Clay%20St%22%2C%22address2%22%3A%22San%20Francisco%2C%20CA%22%2C%22aptOrSuite%22%3A%22%22%2C%22eaterFormattedAddress%22%3A%221042%20Clay%20St%2C%20San%20Francisco%2C%20CA%2094108-1510%2C%20US%22%2C%22subtitle%22%3A%22San%20Francisco%2C%20CA%22%2C%22title%22%3A%221042%20Clay%20St%22%2C%22uuid%22%3A%22%22%7D%2C%22latitude%22%3A37.79391%2C%22longitude%22%3A-122.41029%2C%22reference%22%3A%22here%3Aaf%3Astreetsection%3AuXWZLwautBxsYgi3scVPAA%3ACgcIBCDTp9x0EAEaBDEwNDI%22%2C%22referenceType%22%3A%22here_places%22%2C%22type%22%3A%22here_places%22%2C%22addressComponents%22%3A%7B%22city%22%3A%22San%20Francisco%22%2C%22countryCode%22%3A%22US%22%2C%22firstLevelSubdivisionCode%22%3A%22CA%22%2C%22postalCode%22%3A%2294108-1510%22%7D%2C%22categories%22%3A%5B%22address_point%22%5D%2C%22originType%22%3A%22user_autocomplete%22%2C%22source%22%3A%22manual_auto_complete%22%2C%22userState%22%3A%22Unknown%22%7D; uev2.diningMode=DELIVERY; _sctr=1%7C1753772400000; _ScCbts=%5B%5D; uev2.embed_theme_preference=light; uev2.id.xp=717fb258-59b7-48ae-a6aa-2672c07ff2b7; uev2.id.session=806a414d-83db-4c53-a432-b9f2d90f74b3; uev2.ts.session=1753993208723; _ua={\"session_id\":\"3a0eeba8-44a7-4b5e-a2e7-2ff4748538d4\",\"session_time_ms\":1753993208955}; utag_main__sn=9; utag_main_ses_id=1753993209640%3Bexp-session; utm_medium=undefined; utm_source=undefined; utag_main__ss=0%3Bexp-session; _clck=m686h8%7C2%7Cfy2%7C0%7C2020; utag_main__pn=3%3Bexp-session; _scid_r=A_Doay9XEw5kbKs1os8IjguFpOsxTXQAbbcV3w; _userUuid=; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTM5OTMyMDgsImRhdGEiOnsic2xhdGUtZXhwaXJlcy1hdCI6MTc1Mzk5NzAzOTAyMH0sImV4cCI6MTc1NDA3OTYwOH0.UGg-OjKKlRMAZFE7dsli-_BJr_ewFAfsU6_F7ajvjU8; ttcsid=1753993210210::CFGsWo176LBi2Xhzivx4.9.1753995724083; utag_main__se=24%3Bexp-session; utag_main__st=1753998764159%3Bexp-session; _uetsid=c3a5ea906e4b11f0a120532162c5a37f; _uetvid=7bb83cb0603111f08b132ba7995def24; ttcsid_C69TD6PO8QD6LKH42DTG=1753993210210::V3eGrBlbu2AMplHlW3qw.9.1753996964799; _ga_P1RM71MPFP=GS2.1.s1753993210$o13$g1$t1753996971$j53$l0$h0",
    "x-csrf-token": "x",
}


payload = {
    "userQuery": "Cheeseburger",
    "date": "",
    "startTime": 0,
    "endTime": 0,
    "sortAndFilters": [
        {
            "uuid": "f844706c-2b1b-4db2-b40a-13d43cb338da",  # Sort/filter category
            "options": [
                {"uuid": "12ce1932-1878-4e2e-80d0-5760c095c641"}  # Filter option
            ]
        }
    ],
    "vertical": "ALL",  
    "displayType": "SEARCH_RESULTS",
    "searchSource": "SEARCH_BAR",
    "searchType": "GLOBAL_SEARCH",
    "cacheKey": "",
    "keyName": "",
    "recaptchaToken": ""
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text[:500])

print(response.status_code)
print(response.json())
