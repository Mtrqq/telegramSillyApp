import asyncio
import time
from typing import BinaryIO
from typing import Optional

from telethon import TelegramClient
from telethon.tl.types import Message

from tlprog.cli import cmdline_arguments
from tlprog.letme import prepare_google_url
from tlprog.progress import Style
from tlprog.progress import bar_for
from tlprog.settings import settings


async def update_progress(
    client: TelegramClient, target: str, bar: str, message: Optional[Message] = None
) -> Message:
    if message is None:
        return await client.send_message(target, bar)
    else:
        return await client.edit_message(message, bar)


async def send_progress(
    client: TelegramClient,
    target: str,
    style: Style,
    interval: float,
    label: str,
    timeout: float,
) -> Message:
    start, now = time.time(), time.time()
    message: Optional[Message] = None
    last: Optional[str] = None
    while now - start < timeout:
        bar = bar_for(style, now - start, timeout, label)
        if bar != last:
            message = await update_progress(client, target, bar, message)

        await asyncio.sleep(interval)
        now, last = time.time(), bar

    finished = bar_for(style, timeout, timeout, label)
    return await client.edit_message(message, finished)


async def attach_message(
    client: TelegramClient,
    target: str,
    reply_to: Message,
    message: Optional[str],
    file: Optional[BinaryIO],
) -> Message:
    await client.send_message(target, message, reply_to=reply_to, file=file)


def main() -> None:
    arguments = cmdline_arguments()
    with TelegramClient(
        settings.SESSION_NAME, settings.API_ID, settings.API_HASH
    ) as client:
        message = client.loop.run_until_complete(
            send_progress(
                client=client,
                target=arguments.target,
                style=arguments.style,
                interval=arguments.interval,
                label=arguments.label,
                timeout=arguments.timeout,
            )
        )

        atext, afile = arguments.text, arguments.file
        if arguments.let_me is not None:
            atext = prepare_google_url(arguments.let_me)
        if atext is not None or afile is not None:
            client.loop.run_until_complete(
                attach_message(
                    client=client,
                    target=arguments.target,
                    reply_to=message,
                    message=atext,
                    file=afile,
                )
            )
