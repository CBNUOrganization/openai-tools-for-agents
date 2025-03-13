from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search_preview",
            "user_location": {       # AI will refine the results based on provided approximate geographical context
                "type": "approximate",
                "country": "KR",
                "city": "Chungcheongbuk-do",
                "region": "Chungcheongbuk-do",
                "timezone": "Asia/Seoul"
            }
        }],
    input="What is today weather?"
)

print(response.output_text)
