import logging

from .binder import bind_api

log = logging.getLogger(__name__)


class SendyAPI:
    """ Class used to map to all Sendy API endpoints
    """

    def __init__(self, host, api_key, debug=False):
        self.host = host
        if self.host[-1] != "/":
            self.host = "{0}/".format(self.host)
        self.api_key = api_key
        self.debug = debug

    subscribe = bind_api(
        path="subscribe",
        allowed_param=["list", "email", "name",],
        extra_param={"boolean": "true"},
        success_message="1",
        method="POST",
    )

    unsubscribe = bind_api(
        path="unsubscribe",
        allowed_param=["list", "email"],
        extra_param={"boolean": "true"},
        success_message="1",
        method="POST",
    )

    delete = bind_api(
        path="api/subscribers/delete.php",
        allowed_param=["list_id", "email"],
        success_message="1",
        method="POST",
    )

    subscription_status = bind_api(
        path="api/subscribers/subscription-status.php",
        allowed_param=["list_id", "email"],
        success_message=[
            "Subscribed",
            "Unsubscribed",
            "Unconfirmed",
            "Bounced",
            "Soft bounced",
            "Complained",
        ],
        method="POST",
    )

    subscriber_count = bind_api(
        path="api/subscribers/active-subscriber-count.php",
        allowed_param=["list_id"],
        success_message=int,
        method="POST",
    )

    create_campaign = bind_api(
        path="api/campaigns/create.php",
        allowed_param=[
            "from_name",
            "from_email",
            "reply_to",
            "title",
            "subject",
            "plain_text",
            "html_text",
            "list_ids",
            "brand_id",
            "query_string",
            "send_campaign",
            "segment_ids",
            "exclude_list_ids",
            "exclude_segments_ids",
            "track_opens",
            "track_clicks",
        ],
        success_message=["Campaign created", "Campaign created and now sending"],
        method="POST",
    )
