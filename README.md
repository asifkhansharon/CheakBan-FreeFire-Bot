# CheckBan-FreeFire-Bot

This is a Discord bot that checks whether a Free Fire account is banned using a provided user ID. The bot also includes a Flask web server to monitor its status.

## Features

- Check if a Free Fire account is banned using the `!ID <user_id>` command.
- Displays ban status and ban duration (if available) in a Discord embed message.
- Flask web server to indicate that the bot is running.
- Uses `.env` file for secure storage of credentials.

## Requirements

- Python 3.8+
- A Discord bot token
- A `.env` file containing:
  ```ini
  APPLICATION_ID=your_application_id
  TOKEN=your_bot_token
  ```

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/paulafredo/check-ban-and-info-discord
   cd your-repo
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your credentials:
   ```ini
   APPLICATION_ID=your_application_id
   TOKEN=your_bot_token
   ```

4. Run the bot:
   ```sh
   python main.py
   ```

## Usage

- Use `!ID <user_id>` in a Discord server where the bot is present.
- The bot will fetch ban information from [api-check-ban-freefire](https://github.com/paulafredo/api-check-ban-freefire) and respond with an embedded message.
- The bot's status can be checked via the Flask server running at `http://localhost:10000`.

## Technologies Used

- Python
- Discord.py
- Flask
- dotenv

## License

This project is licensed under the MIT License. Feel free to use and modify it.

## Author

[Paul Alfredo](https://github.com/paulafredo)

