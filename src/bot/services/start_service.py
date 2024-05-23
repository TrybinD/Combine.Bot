from data.repositories import UserRepository


class StartService:
    user_repository: UserRepository = UserRepository()

    async def is_user_exists(self, user_id):
        user = await self.user_repository.find_by_options(unique=True, id=user_id)

        if user is None:
            return False
        return True
    
    async def create_new_user(self, user_id, chat_id, name, nickname):
        await self.user_repository.add({"id": user_id,
                                        "chat_id": chat_id,
                                        "nickname": nickname,
                                        "name": name})