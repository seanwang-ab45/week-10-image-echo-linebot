from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, ImageSendMessage

app = Flask(__name__)

# Line Bot API and Webhook Handler
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # Get the image message ID
    message_id = event.message.id

    # Get the image content
    message_content = line_bot_api.get_message_content(message_id)

    # Save the image
    with open(f"{message_id}.jpg", 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # Reply with the same image
    image_url=f"https://your-server.com/static/{message_id}.jpg"
    line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
if __name__ == "__main__":
    app.run()