import datetime
import os
import re

import backoff
import boto3
import telegram
from telegram.ext import Application



QUEUE_URL = os.environ['QUEUE_URL']
TG_TOKEN = os.environ['TG_TOKEN']
ME = os.environ['TG_ME_ID']

import functools

expo = functools.partial(backoff.expo, max_value=3_600)


@backoff.on_exception(expo, KeyError)
def poll_for_messages():
    print("Polling....")
    print(datetime.datetime.now())
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=20,
    )
    return response['Messages']


def remove_from_queue(receipt_handle):
    response = sqs.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=receipt_handle
    )
    print(f'Deleted: {response}')


def format_message(message):
    from datetime import datetime

    time = datetime.fromtimestamp(int(message['time'])).strftime('%Y/%m/%d %H:%M:%S')
    description = re.escape(message['description'])
    amount = re.escape(str(int(message['amount']) / 100))
    # comment = message['comment']
    import textwrap
    return textwrap.dedent(f"""\
        Time: `{time}`
        Amount: *{amount}*
        Description: _{description}_
        Comment: _abobus_""")


async def send_message(context, message):
    bot = telegram.Bot(TG_TOKEN)
    async with bot:
        await bot.send_message(chat_id=ME, text=format_message(message),
                               parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)


async def main(context):
    while True:
        messages = poll_for_messages()
        for message in messages:
            import json
            message_body = json.loads(message['Body'])
            receipt_handle = message['ReceiptHandle']

            await send_message(context, message_body)
            remove_from_queue(receipt_handle)


if __name__ == '__main__':
    application = Application.builder().token(TG_TOKEN).build()
    job_queue = application.job_queue
    job_queue.run_once(main, when=0)
    application.run_polling()
