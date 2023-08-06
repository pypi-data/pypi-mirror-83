""" Slack Message Creator """
import requests
import json


class MessageCreator:
    """ Message Creator Class """

    def __init__(self, webhook_url: str, title: str = ""):
        self.message_url = webhook_url
        self.__title = title
        self.message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": self.__title,
                        "emoji": True
                    }
                },
            ]
        }
        self.is_added_message = False

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        """
        This Function Set New Title of Message
        :param value: New Title str
        :return:
        """
        if self.__title != value:
            self.__title = value
            self.message["blocks"][0]["text"]["text"] = self.__title

    def bold(self, text: str) -> str:
        """
        Message Returns Bold Formatter
        :param text:
        :return: Bold Format Text
        """
        return "*{}*".format(text)

    def italic(self, text: str) -> str:
        """
        Message Returns Italic Formatter
        :param text:
        :return: Bold Format Text
        """
        return "_{}_".format(text)

    def strikethrough(self, text: str) -> str:
        """
        Message Returns Strikethrough Formatter
        :param text:
        :return: Bold Format Text
        """
        return "~{}~".format(text)

    def add_divider(self):
        """
        This Function Adds Divider Among Device Status Messages
        :return:
        """
        self.message["blocks"].append({"type": "divider"})

    def add_simple_message(self, text: str):
        """
        This Function Add Simple Message On Blocks
        :param text:
        :return:
        """
        self.message["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": text
                }
            }
        )
        self.is_added_message = True

    def add_rich_message(self, *args, separator: str = " ", indent: bool = False):
        """
        This Function Add Rich Message On Blocks
        :param indent: Is indented
        :param args: Message Texts
        :param separator: Message Seperator
        :return:
        """
        self.message["blocks"].append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "{indent}{text}".format(
                            indent=">" if indent else "",
                            text=separator.join(args)
                        )
                    }
                ]
            },
        )
        self.is_added_message = True

    def add_key_value_messages(self, messages: dict):
        """
        This Function Add Stack Key Value Messages
        Message Item Ex: {key:string,value:string}
        :param messages: Messages Dict Array
        :return:
        """
        fields = []

        for message in messages:
            fields.append({
                "type": "mrkdwn",
                "text": "*{key}:*\n{value}\n\n".format(
                    key=message["key"],
                    value=message["value"]
                )
            })

        if len(fields):
            self.message["blocks"].append(
                {
                    "type": "section",
                    "fields": fields
                },
            )
            self.is_added_message = True

    def send_message(self):
        """
        This Function Sends Message The Slack Application
        :return:
        """
        if self.is_added_message:
            requests.post(
                self.message_url,
                data=json.dumps(self.message),
                headers={"Content-Type": "application/json"}
            )
