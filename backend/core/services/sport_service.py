from core.models import Sport

class SportService:
    def update_or_create_sports(self, sports_data):
        for sport_info in sports_data:
            Sport.objects.update_or_create(
                key=sport_info['key'],
                defaults={
                    'group': sport_info['group'],
                    'title': sport_info['title'],
                    'description': sport_info['description'],
                    'active': sport_info['active'],
                    'has_outrights': sport_info['has_outrights']
                }
            )