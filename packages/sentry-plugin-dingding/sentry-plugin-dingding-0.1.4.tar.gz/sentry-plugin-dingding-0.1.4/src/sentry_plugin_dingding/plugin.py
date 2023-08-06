# coding: utf-8

from valueDict import defaultMarkdown, formatTemplate
import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin
import sentry_plugin_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"

print('version ===========> 0.1.4')

class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'wangjinjie'
    author_url = 'http://gogs.visionacademy.cn/tools/sentry-plugin-dingding'
    version = sentry_plugin_dingding.VERSION
    description = 'Send error counts to DingDing.'
    resource_links = [
        ('Source', 'http://gogs.visionacademy.cn/tools/sentry-plugin-dingding'),
        ('Bug Tracker', 'http://gogs.visionacademy.cn/tools/sentry-plugin-dingding'),
        ('README', 'http://gogs.visionacademy.cn/tools/sentry-plugin-dingding'),
    ]

    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        detail = event._data.data
        print(" event =================>>", event.__dict__)
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)

        customer_markdown = self.get_option('customer_markdown', group.project)
        try:
            if customer_markdown is None or len(customer_markdown.strip()) <= 0:
                customer_markdown = defaultMarkdown
            linkUrl = u"{}events/{}/".format(group.get_absolute_url(), event.event_id)
            detail.PROJECT_NAME = event.project.slug
            detail.URL = linkUrl
            text = formatTemplate(detail, customer_markdown)
        except Exception as e:
            text = ''' unknow error :  ''' + str(e)
        # print('TEMPLATE =======================>', text)
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": detail.PROJECT_NAME,
                "text": text
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
