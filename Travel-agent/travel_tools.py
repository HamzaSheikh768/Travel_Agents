from agents import function_tool

@function_tool
def get_flights(destination: str) -> str:
    return f" Flights found to {destination}: PKR 50,000 - PKR 90,000."


@function_tool
def suggest_hotels(destination: str) -> str:
    return f" Hotels in {destination}: Pearl Continental, Marriot, Maldives, Rome, Local Guess House "