from example.consumers import Consumer


class ChatConsumer(Consumer):
    public = ['post']

    group = 'chat'

    async def before_accept(self):
        await self.group_add(self.group)

    async def after_accept(self):
        await self.send_group(self.group, 'signal', 'connected')

    async def disconnect(self, code):
        await self.group_discard(self.group)
        await self.send_group(self.group, 'signal', 'disconnected')

    async def client_post(self, content):
        await self.send_group(self.group, 'post', content)

    async def group_signal(self, name):
        await self.send_client('signal', name)

    async def group_post(self, content):
        await self.send_client('post', content)
