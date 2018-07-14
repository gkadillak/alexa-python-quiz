SESSION_ID = "123"
USER_ID = "amzn1.ask.account.someuserid"

guess_body = {
    "request": {
        "type": "IntentRequest",
        "intent": {
            "name": "QuizAnswerIntent",
            "confirmationStatus": "NONE",
            "slots": {
                "Answer": {"name": "Answer", "value": "1", "confirmationStatus": "NONE"}
            },
        },
    },
    "session": {
        "application": {"applicationId": "amzn1.ask.skill"},
        "new": False,
        "sessionId": SESSION_ID,
        "user": {"userId": "amzn1.ask.account"},
    },
    "version": "1.0",
}
start_game_body = {
    "version": "1.0",
    "session": {
        "new": False,
        "sessionId": SESSION_ID,
        "application": {
            "applicationId": "amzn1.ask.skill.c28e1765-5109-4837-a2aa-850c002d076a"
        },
        "user": {"userId": USER_ID},
    },
    "context": {
        "System": {
            "application": {
                "applicationId": "amzn1.ask.skill.c28e1765-5109-4837-a2aa-850c002d076a"
            },
            "user": {"userId": USER_ID},
            "device": {
                "deviceId": "amzn1.ask.device.AGT7O65JKJJOKHDOPJXK7OAQNX6NL4Q2UBPYCPSTASTTEGERMR3VFODXUSQSNFQIO3FM6KQDLSL3L4OFI6JIJIKYHDZA5CPXLB6WET66KLDZMD6XLI5XUDLWNWKRBMOTL6H25ZGAI4CORQWDT7MIFETAPDAQ",
                "supportedInterfaces": {},
            },
            "apiEndpoint": "https://api.amazonalexa.com",
            "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLmMyOGUxNzY1LTUxMDktNDgzNy1hMmFhLTg1MGMwMDJkMDc2YSIsImV4cCI6MTUzMDE2NTQxMCwiaWF0IjoxNTMwMTYxODEwLCJuYmYiOjE1MzAxNjE4MTAsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUdUN082NUpLSkpPS0hET1BKWEs3T0FRTlg2Tkw0UTJVQlBZQ1BTVEFTVFRFR0VSTVIzVkZPRFhVU1FTTkZRSU8zRk02S1FETFNMM0w0T0ZJNkpJSklLWUhEWkE1Q1BYTEI2V0VUNjZLTERaTUQ2WExJNVhVRExXTldLUkJNT1RMNkgyNVpHQUk0Q09SUVdEVDdNSUZFVEFQREFRIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUY2T0M1RUlBVVNJVkpEVTVZVkU2NEFTNzI3Rk1XNk9FTFZHV0UzUUFNM0ZGVEVOV0tVM01TMk9NMk1UR0dVWUNLWldFN0tCMjZWVlZXSFpVR0ZYSEFQU0M1VEdNQVNZT0VDUERDQUtIWE9BNk0yVEtTNDVMNzU2N0tJWVJZNkVHQVlIWE9GQUVETjNNWlNQNlJRVlBRTktMQUpYTlg1UVNDQ1o1WExXMldSQzdYSTJISE5KV0xITEJRRkhVRDdXQk1GWlU2WEtUTE5HTUhBIn19.dBdxH--ozDyTwcuBRddbNLd6CgewPj8rXUv8hLUpnwkOxQMzhabfH53J827aFCBlck89a8Pv9ei6HowKiuQxwL9b6gsneoGJGtaAZl4YopHFzkg0RILYnJPHm4xGPLtrfiHtsRSYPwc-DDOrb6i7qNYp2NQMi-lpU86yfAELbCtWaRJK2RwIY8xJheI4Z7z6DwbbQssbv16vUgPHpCsT_moE9tFoembAC6gEtWxO4vBE8VzDjMeBaZg5J6sbiEwKNTgHg3Tz2v6eQqgdxqQXdrOK07cmc7S-_-_HguKoPefriea0RugAoxHaNf6yTQRumgYdrsy2iyqTpx8NmpWLbQ",
        }
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "amzn1.echo-api.request.14b93f2d-06be-4946-a928-ec29128cac0d",
        "timestamp": "2018-06-28T04:56:50Z",
        "locale": "en-US",
        "intent": {"name": "AMAZON.YesIntent", "confirmationStatus": "NONE"},
        "dialogState": "STARTED",
    },
}
