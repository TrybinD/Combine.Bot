from data.repositories import UserRepository


class StartService:
    user_repository: UserRepository = UserRepository()

    async def is_user_exists(self, user_id):
        user = await self.user_repository.get(id=user_id)

        if user:
            return True
        return False
    
    async def create_new_user(self, user_id, chat_id, name, nickname):
        await self.user_repository.add({"id": user_id,
                                        "chat_id": chat_id,
                                        "nickname": nickname,
                                        "name": name})