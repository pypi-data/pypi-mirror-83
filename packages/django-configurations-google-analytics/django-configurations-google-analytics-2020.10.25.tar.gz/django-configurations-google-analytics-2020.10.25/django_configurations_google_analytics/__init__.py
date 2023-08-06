from configurations import Configuration, values

APP = 'django_configurations_google_analytics'


class GoogleAnalyticsMixin:
    GA_ID = values.Value(None)

    @classmethod
    def setup(cls):
        super(GoogleAnalyticsMixin, cls).setup()
        if APP not in cls.INSTALLED_APPS:
            cls.INSTALLED_APPS.append(APP)


class GoogleAnalyticsConfiguration(GoogleAnalyticsMixin, Configuration):
    pass
