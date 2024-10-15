from django.conf import settings
from core.services.api_service import OddsAPIService
from core.services.sport_service import SportService
from core.task_registry import TaskRegistry
from .base_task import BaseTask

class GetSportsTask(BaseTask):
    @classmethod
    def execute(cls, *args, **kwargs):
        api_service = OddsAPIService(base_url=settings.THE_ODDS_API_BASE_URL, api_key=settings.THE_ODDS_API_KEY)
        sport_service = SportService()

        try:
            sports_data = api_service.fetch_sports()
            updated_count = sport_service.update_or_create_sports(sports_data)
            return f"Successfully updated {updated_count} sports."
        except Exception as e:
            return f"Error updating sports: {str(e)}"

