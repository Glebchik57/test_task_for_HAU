import asyncio


async def handle_client(reader, writer, clients):
    clients.add(writer)
    address = writer.get_extra_info('peername')
    print(f"соединение {address}")

    while True:
        data = await reader.read(100)
        message = data.decode()
        if message.strip() == 'exit':
            writer.close()
            break
        print(f"Получено от {address}: {message}")
        await send_msg(message, clients, writer)


async def send_msg(message, clients, sender):
    for client in clients:
        if client != sender:
            client.write(message.encode())
            print(f'отправляю сообщение{client}')
            await client.drain()


async def main():
    clients = set()
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, clients),
        '127.0.0.1',
        8888
    )
    addr = server.sockets[0].getsockname()
    print(f"Сервер {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
