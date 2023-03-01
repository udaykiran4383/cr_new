from import_export import resources
from .models import Team, D2c

class TeamResource(resources.ModelResource):
    class Meta:
        model = Team

class D2cResource(resources.ModelResource):
    class Meta:
        model = D2c

