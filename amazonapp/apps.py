from django.apps import AppConfig


class AmazonappConfig(AppConfig):
    name = 'amazonapp'

    def ready(self):
    	import amazonapp.signals