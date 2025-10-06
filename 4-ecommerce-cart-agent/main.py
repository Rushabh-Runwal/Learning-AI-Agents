import asyncio

# Import the main ecommerce cart agent
from ecommerce_cart_agent.agent import ecommerce_cart_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

load_dotenv()

session_service = InMemorySessionService()


initial_state = {
    "user_name": "Rushabh Runwal",
    "cart_items": [],  
    "interaction_history": [],
    "total_amount": 0.0,
    "order_history": [],  
}


async def main_async():

    APP_NAME = "Ecommerce Cart"
    USER_ID = "customer_001"


    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent=ecommerce_cart_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    while True:
        user_input = input(f"{"\033[42m"}You:{"\033[0m"} ")

        if user_input.lower() in ["exit", "quit"]:
            break

        add_user_query_to_history(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_input
        )

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()