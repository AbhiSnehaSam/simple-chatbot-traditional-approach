import sys

from aiohttp import web
from aiohttp.web import (
    Request,
    Response,
    json_response,
)

from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
)

from botbuilder.core.integration import (
    aiohttp_error_middleware,
)

from botbuilder.schema import Activity

from config import DefaultConfig
from bots import EchoBot


CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings(
    CONFIG.APP_ID,
    CONFIG.APP_PASSWORD
)

ADAPTER = BotFrameworkAdapter(
    SETTINGS
)


# Error Handler
async def on_error(
    context: TurnContext,
    error: Exception
):

    print(
        f"\n[on_turn_error] {error}",
        file=sys.stderr
    )

    await context.send_activity(
        "The bot encountered an error."
    )


ADAPTER.on_turn_error = on_error

BOT = EchoBot()


# Main Message Endpoint
async def messages(
    req: Request
) -> Response:

    if (
        "application/json"
        in req.headers["Content-Type"]
    ):

        body = await req.json()

    else:

        return Response(
            status=415
        )

    activity = Activity().deserialize(
        body
    )

    auth_header = (
        req.headers["Authorization"]
        if "Authorization"
        in req.headers
        else ""
    )

    response = (
        await ADAPTER.process_activity(
            activity,
            auth_header,
            BOT.on_turn
        )
    )

    if response:

        return json_response(
            data=response.body,
            status=response.status
        )

    return Response(status=201)


APP = web.Application(
    middlewares=[
        aiohttp_error_middleware
    ]
)

APP.router.add_post(
    "/api/messages",
    messages
)

if __name__ == "__main__":

    try:

        web.run_app(
            APP,
            host="localhost",
            port=CONFIG.PORT
        )

    except Exception as error:

        raise error