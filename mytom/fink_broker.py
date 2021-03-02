from django import forms
import requests

from tom_alerts.alerts import GenericQueryForm, GenericAlert
from tom_alerts.models import BrokerQuery
from tom_targets.models import Target

broker_url = 'https://gist.githubusercontent.com/mgdaily/f5dfb4047aaeb393bf1996f0823e1064/raw/6fe1680f22b86467c50a21a138177838378eb143/example_broker_data.json'

class FinkBrokerForm(GenericQueryForm):
    name = forms.CharField(required=True)

class FinkBroker:
    name = 'Fink'
    form = FinkBrokerForm

    @classmethod
    def fetch_alerts(clazz, parameters):
        response = requests.get(broker_url)
        response.raise_for_status()
        test_alerts = response.json()
        return iter([alert for alert in test_alerts if alert['name'] == parameters['name']])

    @classmethod
    def fetch_alert(clazz, alert_id):
        response = requests.get(broker_url)
        test_alerts = response.json()
        response.raise_for_status()
        for alert in test_alerts:
            if (alert['id'] == int(alert_id)):
                return alert
        return None


    @classmethod
    def to_generic_alert(clazz, alert):
        return GenericAlert(
            timestamp=alert['timestamp'],
            url= broker_url,
            id=alert['id'],
            name=alert['name'],
            ra=alert['ra'],
            dec=alert['dec'],
            mag=alert['mag'],
            score=alert['score']
        )

    @classmethod
    def to_target(clazz, alert):
        return Target(
            identifier=alert['id'],
            name=alert['name'],
            type='SIDEREAL',
            designation='MY ALERT',
            ra=alert['ra'],
            dec=alert['dec'],
        )
