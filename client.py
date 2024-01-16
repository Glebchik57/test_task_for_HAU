import asyncio


async def read_input(writer):
    while True:
        message = input("Введите сообщение: ")
        writer.write(message.encode())
        await writer.drain()
        if message.strip() == 'exit':
            writer.close()
            break


async def read_messages(reader):
    while True:
        data = await reader.read(100)
        message = data.decode()
        print(f"Получено от: {message}")


async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    await asyncio.gather(
        read_input(writer),
        read_messages(reader)
    )

if __name__ == "__main__":
    asyncio.run(main())
