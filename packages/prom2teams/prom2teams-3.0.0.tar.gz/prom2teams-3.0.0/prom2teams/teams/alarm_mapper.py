from prom2teams.teams.teams_alarm_schema import TeamsAlarm, TeamsAlarmSchema
from collections import defaultdict


def map_prom_alerts_to_teams_alarms(alerts):
    alerts = group_alerts(alerts, 'status')
    teams_alarms = []
    schema = TeamsAlarmSchema()
    for same_status_alerts in alerts:
        for alert in alerts[same_status_alerts]:
            alarm = TeamsAlarm(alert.name, alert.status.lower(), alert.severity,
                               alert.summary, alert.instance, alert.description,
                               alert.fingerprint, alert.extra_labels,
                               alert.extra_annotations)
            json_alarm = schema.dump(alarm)
            teams_alarms.append(json_alarm)
    return teams_alarms


def map_and_group(alerts, group_alerts_by):
    alerts = group_alerts(alerts, 'status')
    teams_alarms = []
    schema = TeamsAlarmSchema()
    for same_status_alerts in alerts:
        grouped_alerts = group_alerts(alerts[same_status_alerts], group_alerts_by)
        for alert in grouped_alerts:
            features = group_features(grouped_alerts[alert])
            name, description, instance, severity, status, summary = (teams_visualization(features["name"]),
                                                                      teams_visualization(features["description"]),
                                                                      teams_visualization(features["instance"]),
                                                                      teams_visualization(features["severity"]),
                                                                      teams_visualization(features["status"]),
                                                                      teams_visualization(features["summary"]))
            fingerprint = teams_visualization(features["fingerprint"])
            extra_labels = dict()
            extra_annotations = dict()
            for element in grouped_alerts[alert]:
                if hasattr(element, 'extra_labels'):
                    extra_labels = {**extra_labels, **element.extra_labels}
                if hasattr(element, 'extra_annotations'):
                    extra_annotations = {**extra_annotations, **element.extra_annotations}

            alarm = TeamsAlarm(name, status.lower(), severity, summary,
                               instance, description, fingerprint, extra_labels,
                               extra_annotations)
            json_alarm = schema.dump(alarm)
            teams_alarms.append(json_alarm)
    return teams_alarms


def teams_visualization(feature):
    feature.sort()
    # Teams won't print just one new line
    return ',\n\n\n'.join(feature) if feature else 'unknown'


def group_alerts(alerts, group_alerts_by):
    groups = defaultdict(list)
    for alert in alerts:
        groups[alert.__dict__[group_alerts_by]].append(alert)
    return dict(groups)


def group_features(alerts):
    grouped_features = {feature: list(set([individual_alert.__dict__[feature] for individual_alert in alerts]))
                        for feature in ["name", "description", "instance", "severity", "status", "summary", "fingerprint"]}
    return grouped_features
