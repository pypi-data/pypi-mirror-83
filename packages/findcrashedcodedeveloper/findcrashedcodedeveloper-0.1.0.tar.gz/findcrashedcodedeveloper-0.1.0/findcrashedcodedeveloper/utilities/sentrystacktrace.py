def get_sentry_stack_trace_for_issue(sentry_api, issue_id):
    """Get stack trace of latest event of Sentry issue

    Parameters
    ----------
    sentry_api : SentryAPI
    issue_id : str
        id of Sentry issue. you can get it from url
        of issue or api response of issue info api.

    Returns
    -------
    SentryStackTrace
        stack trace of lastest event of this issue
    """
    latest_event = sentry_api.events.get_latest_event(issue_id)
    return latest_event.get_stack_trace()
