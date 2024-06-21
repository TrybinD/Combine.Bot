from data.repositories import UserTeamRecommendationsRepository

import logging


class RecomendationService:
    user_team_recommendations_repository: UserTeamRecommendationsRepository = UserTeamRecommendationsRepository()

    async def get_recomendations_to_team(self, team_id):
        
        res = await self.user_team_recommendations_repository.get_users_with_info(team_id=team_id)

        recos = [{"name": user.name, 
                  "discription": user_in_search.description,
                  "contact": "@" + user.nickname} for user, user_in_search, _ in res]
        
        return recos

    async def get_recomendations_to_user(self, user_in_search_id):
        
        res = await self.user_team_recommendations_repository.get_teams_with_info(user_in_search_id=user_in_search_id)

        logging.info(res)

        recos = [{"team_name": team.name, 
                  "discription": team.description,
                  "contact": "@" + creator.nickname} for team, creator, _ in res]
        
        return recos

