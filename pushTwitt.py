from service.send_slack_service import SlackPushService

if __name__ == '__main__':
    service = SlackPushService()
    service.pushSlack()