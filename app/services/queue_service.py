import json
import aio_pika


# todo: lord forgive me for the code that is next...
# todo: (fix) this is such a fucking hack, but works to remove stale data from queue
async def remove_jobs_with_campaign_id(queue_name: str, campaign_id: int):
    try:
        connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5672//")
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)

            async for message in queue.iterator(no_ack=False):
                if message is None:
                    break

                message_body = json.loads(message.body.decode('utf-8'))
                extracted_campaign_id = message_body[0][0]['campaign_id']

                if extracted_campaign_id is not None and extracted_campaign_id == campaign_id:
                    await message.ack()
                else:
                    await message.reject(requeue=True)
    except Exception as e:
        print(f"Error in clean_up_call_queue: {str(e)}")

