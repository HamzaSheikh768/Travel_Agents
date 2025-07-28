import os
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI # type: ignore
)
from agents.run import RunConfig
from dotenv import load_dotenv
from travel_tools import get_flights, suggest_hotels

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model = model,
    model_provider = external_client, # pyright: ignore[reportArgumentType]
    tracing_disabled = True
)

# Destination Agent
destination_agent = Agent(
    name="DestinationAgent",
    instructions="You Travel destination based on users mood..",
    model=model
)

# Booking Agent
booking_agent = Agent(
    name="BookingAgent",
    instructions="You give flight and hotel info using tools.. ",
    model=model
)

# Explore Agent
explore_agent = Agent(
    name="ExploreAgent",
    instructions="You suggest adventure & places to explore in the destination.",
    model=model
)

def main():
    print("U0001F30D AI Travel Agent Designer\n")
    adventure = input("What's your travel adventure (relaxing/adventure places/etc)? ->")

    result1 = Runner.run_sync(destination_agent, adventure, run_config=config)
    travel = result1.final_output.strip()
    print("\n Destination Suggested:", travel)

    result2 = Runner.run_sync(booking_agent, travel, run_config=config)
    print("\n Booking Info:", result2.final_output)

    result3 = Runner.run_sync(explore_agent, travel, run_config=config)
    print("\n Explore Tips:", result3.final_output)

if __name__ == "__main__":
    main()
