# TranscriptionBot

Try it at [Video-to-text bot](https://t.me/TranscriptiobBot)

This script processes YouTube links by downloading the audio from the video, transcribing it using OpenAI API,  splitting the transcribed text into sentences, joining them into chunks, and creating Telegraph pages for each chunk.

Requirements:
- Python 3.x
- python-telegram-bot library (https://python-telegram-bot.org/)
- requests library (https://pypi.org/project/requests/)
- pytube library (https://pypi.org/project/pytube/)
- openai library (https://pypi.org/project/openai/)

Instructions:
1. Install the required libraries by running: pip install python-telegram-bot requests pytube openai.
2. Obtain the required API credentials:
   - Telegram API token: 
      1. Open the Telegram app or visit the Telegram website (https://telegram.org/).
      2. Search for the BotFather bot. You can either search for "@BotFather" in the search bar or click on the following link: [BotFather](https://t.me/BotFather).
      3. Start a chat with BotFather by clicking on the "Start" button or sending the "/start" command.
      4. Send the "/newbot" command to BotFather to create a new bot.
      5. BotFather will guide you through the process of creating the bot. You will be asked to provide a name for your bot (e.g., "MyAwesomeBot") and a username (e.g., "my_awesome_bot"). The username must end with "bot"            (no spaces or special characters).
      6. Once you have provided the necessary information, BotFather will create your bot and provide you with an API token. The API token is a long string of characters (e.g., "1234567890:ABCdefGHIjklMnoPqrStuvwXYz").
      7. Copy the API token provided by BotFather. This token is unique to your bot and will be used to authenticate your bot's requests to the Telegram API

   - Telegraph access token: Register an account on Telegraph and obtain the access token (https://telegra.ph/):
      1. Make a POST request to the createAccount endpoint with the necessary parameters:
         Endpoint: https://api.telegra.ph/createAccount
         HTTP Method: POST
         Parameters:
         short_name (required): Your desired short name for the account (unique identifier used in the account's URL).
         author_name (optional): The author name associated with the account.
         ```
         endpoint = "https://api.telegra.ph/createAccount"
         data = {
         "short_name": "YourShortName",
         "author_name": "YourAuthorName"
         }
         response = requests.post(endpoint, data=data)
         ```
      2. Handle the response to obtain the access token:
         ```
         if response.status_code == 200:
             access_token = response.json().get("access_token")
             print("Access token:", access_token)
         else:
             print("Account creation failed. Status code:", response.status_code)
         ```
   - OpenAI API key: Sign up for OpenAI and obtain the API key (https://openai.com/).
      1. Go to the OpenAI website (https://openai.com/) and sign up for an account. Provide the necessary information and complete the registration process.
      2. Once you have successfully signed up and logged in to your OpenAI account, navigate to the API section. You can typically find it in the account dashboard or in the developer settings.
      3. In the API section, you should find an option to generate an API key. Click on that option to create a new API key.
      4. After generating the API key, it will be displayed on your screen. Copy the API key and securely store it in a safe location.

3. Replace the placeholder API credentials in the code with your own.
4. Run the script: python bot.py.
5. Start a conversation with your bot on Telegram.
