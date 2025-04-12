import openai as OpenAI
from time import sleep
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)
print("API key: " + api_key)   #DON'T DELETE (very important)

#different prompts
k = str(input("Do you want to buy stocks or call options? (stocks/options): ")).lower()
if k == "stocks":
    l = str(input("Enter if you want a short term, long term, or general stock recommendation: ")).lower()
    if l == "short term":
short_term = "find good stocks for the short term to invest in with the following factors in mind:, moving averages, RSI, current world news."
    
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": short_term
        }
    ]
)
print(completion.choices[0].message.content)
elif l == "long term":
long_term = "find good stocks in the long term to invest in with the following factors in mind:, moving averages, RSI, current world news."
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": long_term
        }
    ]
)
    print(completion.choices[0].message.content)
elif l == "general":
    general = "find good stocks in general with the following factors in mind:, moving averages, RSI, current world news."
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": general
        }
    ]
)
    print(completion.choices[0].message.content)
else:
    print("Please enter a valid input.")
    exit()
elif k == "options":
    u = str(input("Enter if you want a short term, long term, or general call option recommendation: ")).lower()
elif k == "cyrpto":
    v = str(input("Enter if you want a short term, long term, or general crypto recommendation: ")).lower()
