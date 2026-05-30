from datetime import datetime

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
)


class EchoBot(ActivityHandler):

    async def on_message_activity(
        self,
        turn_context: TurnContext
    ):

        user_message = (
            turn_context.activity.text
            .lower()
            .strip()
        )

        # Greeting
        if user_message in [
            "hello",
            "hi",
            "hey"
        ]:

            response = (
                "Hello! Welcome to the chatbot.\n\n"
                "Type 'help' to see available commands."
            )

        # Help
        elif user_message == "help":

            response = (
                "Available Commands:\n\n"
                "1. hello\n"
                "2. about\n"
                "3. time\n"
                "4. course\n"
                "5. help\n"
                "6. bye"
            )

        # About
        elif user_message == "about":

            response = (
                "I am a rule-based chatbot built "
                "using Python and Microsoft "
                "Bot Framework."
            )

        # Course
        elif user_message == "course":

            response = (
                "This chatbot was developed for "
                "the University of the Cumberlands "
                "chatbot assignment."
            )

        # Time
        elif user_message == "time":

            current_time = (
                datetime.now()
                .strftime("%Y-%m-%d %H:%M:%S")
            )

            response = (
                f"Current Time: {current_time}"
            )

        # Goodbye
        elif user_message == "bye":

            response = (
                "Goodbye! Have a great day."
            )

        # Unknown command
        else:

            response = (
                "Sorry, I don't understand "
                "that command.\n\n"
                "Type 'help' to see "
                "available commands."
            )

        await turn_context.send_activity(
            response
        )