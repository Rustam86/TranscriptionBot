import telegram
from telegram.ext import Updater, MessageHandler, Filters
import requests
import openai
from pytube import YouTube
import re

# Set up Telegram API credentials
TOKEN = 'YOUR_TELEGRAM_TOKEN'

# Set up Telegraph API credentials
telegraph_access_token = 'YOUR_TELEGRAPH_TOKEN'

# Set up OpenAI API credentials
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Create an instance of the Bot
bot = telegram.Bot(token=TOKEN)

def join_sentences(sentences, max_length):
    """
    Joins a list of sentences into chunks of text, where each chunk has a maximum length.

    Args:
        sentences (list): List of sentences to be joined.
        max_length (int): Maximum length of each chunk of text.

    Returns:
        list: List of chunks of text.
    """
    result = []
    current_string = ''
    current_length = 0

    for sentence in sentences:
        if current_length + len(sentence) <= max_length:
            current_string += sentence + '. '
            current_length += len(sentence) + 2  # Add 2 for the period and space
        else:
            result.append(current_string)
            current_string = sentence + '. '
            current_length = len(sentence) + 2  # Add 2 for the period and space

    if current_string:
        result.append(current_string)

    return result


def is_youtube_link(text):
    """
    Checks if the given text is a valid YouTube link.

    Args:
        text (str): Text to be checked.

    Returns:
        bool: True if the text is a valid YouTube link, False otherwise.
    """
    youtube_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?(?=.*v=\w+)(?:\S+)?|embed\/\w+|\w+)|youtu\.be\/\w+)(?:\S+)?'
    match = re.match(youtube_regex, text)
    return match is not None


def create_telegraph_page(title, content):
    """
    Creates a page on Telegraph with the given title and content.

    Args:
        title (str): Title of the page.
        content (str): Content of the page.

    Returns:
        str: URL of the created page on Telegraph.
    """
    api_endpoint = "https://api.telegra.ph/createPage"

    # Prepare the request payload
    payload = {
        "access_token": telegraph_access_token,
        "title": title,
        "content": content,
        "return_content": True  # Set to False if you don't want the content to be returned in the response
    }

    # Make the API request
    response = requests.post(api_endpoint, json=payload)
    data = response.json()

    # Check the response status
    if data["ok"]:
        page_url = data["result"]["url"]
        return page_url
    else:
        error_message = data["error"]
        return error_message


def process_text(text):
    """
    Processes the given text, which is expected to be a YouTube link.
    Downloads the audio from the YouTube video, transcribes it using OpenAI API,
    splits the transcribed text into sentences, joins them into chunks, and creates
    Telegraph pages for each chunk.

    Args:
        text (str): YouTube link to be processed.

    Returns:
        list: List of URLs of the created Telegraph pages.
    """
    youtube_link = text
    video = YouTube(youtube_link)
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_file = f"{video.video_id}.wav"
    audio_stream.download(filename=audio_file)

    audio_file = open(f"{video.video_id}.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    transcript_text = dict(transcript)['text']

    text_title = video.title

    sentences = transcript_text.split('. ')
    parts = join_sentences(sentences, 12000)
    pages = []
    
    for index, part in enumerate(parts):
        text_title = f"Part {index+1}: {video.title}"
        processed_text = create_telegraph_page(text_title, [part])
        pages.append(processed_text)

    return pages


def handle_message(update, context):
    """
    Handles incoming messages in the Telegram chat.
    Checks if the message is a YouTube link and processes it if true.
    Sends the processed text back to the user in the form of Telegraph page URLs.

    Args:
        update: Update object from Telegram.
        context: Context object from Telegram.
    """
    user = update.message.from_user
    message_text = update.message.text

    if is_youtube_link(message_text):
        please_wait_message = "Hold on tight! 🎧 Our transcription gnomes are diligently working to decode the audio magic of your video." \
                      "⏳ It might take a moment, but we promise it'll be worth the wait! 😊"
        pages = process_text(message_text)
        for page in pages:
            bot.send_message(chat_id=update.effective_chat.id, text=page)

    elif message_text == '/start':
        welcome_text = "Welcome to the YouTube Transcription Bot! 🎵🤖\n\n" \
                       "This bot can help you transcribe audio from YouTube videos. " \
                       "Simply send a YouTube link, and the bot will download the audio, " \
                       "transcribe it using OpenAI, and provide you with the transcribed text in the form of Telegraph page URLs. " \
                       "Give it a try! 🎶\n\nPlease provide a valid YouTube link to get started."
        
        bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)

    else:
        processed_text = "Welcome, give me your YouTube link"
        bot.send_message(chat_id=update.effective_chat.id, text=processed_text)


def main():
    """
    Main entry point of the program.
    Initializes the Telegram bot and starts the message handler.
    """


    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Start the bot
    updater.start_polling()
    print("Bot started.")

    # Set up a message handler to handle incoming messages
    message_handler = MessageHandler(Filters.text, handle_message)
    dispatcher.add_handler(message_handler)

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
