# heliosBot

**HeliosBot** is an advanced Discord bot with adjustable features and effective automation that improves user experience. By utilizing [Pycord](https://pycord.dev/) and including sophisticated features, this bot offers administrators and users a seamless and user-friendly interface.


## Features

- **Complete Slash Commands Support**: heliosBot is built with Slash Commands in mind. They are much more user-friendly and have bigger flexibility.
- **Customizable**: Adaptable options to customize the bot to meet particular server requirements.
- **Efficient Database Integration**: Allows for easy data storing with support for SQLite3.
- **Basic Logging**: See the basic database logging.


## Demo

![image](https://github.com/user-attachments/assets/3cc8e96c-9557-4505-9222-6f52e3bf8501)

![image](https://github.com/user-attachments/assets/3df19f92-5b69-4316-b4b6-c7365beede39)

![image](https://github.com/user-attachments/assets/abfd2536-70ff-4bb8-9a08-62ab9d4f13b4)

![image](https://github.com/user-attachments/assets/c9e10906-bfb9-4d08-bcbc-b78c92e12a0d)

![image](https://github.com/user-attachments/assets/aab20b5c-92b9-4937-ba49-d0c57b9a6a23)

![image](https://github.com/user-attachments/assets/ce8d2d12-cd94-4e68-a89a-333550ed7b56)


## Installation

### Prerequisites

- Python 3.9+
- SQLite3 (optional: PostgreSQL or MySQL for production environments)
- Discord API Token

## Setup

#### 1. Clone the repository:

   ```bash
   git clone https://github.com/fontsz/heliosBot.git
   cd heliosBot
   ```

#### 2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

#### 3. Set up environment variables:

Create a **.env** file in the root directory with the following content:
   ```env
   BOT_TOKEN=your_discord_bot_token
   OWNER_ID=your_discord_account_id
   ```
##### How to Get Your Discord Bot Token

1. **Create a Discord Application**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click **"New Application"** and give your bot a name.

2. **Create the Bot**:
   - In your application's settings, navigate to the **"Bot"** tab.
   - Click **"Add Bot"**, then confirm by clicking **"Yes, do it!"**.

3. **Get Your Token**:
   - After creating the bot, under the **"Bot"** tab, you’ll see a **"Token"** section.
   - Click **"Copy"** to get your bot token. **Keep it safe** and **never share** this token publicly!

4. **Invite the Bot to Your Server**:
   - In the **"OAuth2"** tab, go to **"URL Generator"**.
   - Under **"SCOPES"**, select **"bot"**.
   - Under **"BOT PERMISSIONS"**, choose the necessary permissions.
   - Copy the generated URL, paste it into your browser, and invite your bot to your server.
  
##### How to Get Your Discord ID

1. **Enable Developer Mode on Discord**
   - Go to Discord Settings and find the Advanced Tab
   - Enable the Developer Mode
2. **Get your ID**
   - Right click on any of your messages and copy your ID

#### 4. Run the bot:

   ```bash
   python main.py
   ```


## Usage
Once the bot is running, invite it to your server and start using the built-in commands:

- `/profile`: See your profile. (Will be created if it does not exist)
- `/badge`: Give or remove badges from users. (You have to create the badge in the database)
- `/gambling`: Gamble your points. (Points can be acquired using the `/daily` command)


## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch ```(git checkout -b feature-branch).```
3. Make your changes and test thoroughly.
4. Submit a pull request with a detailed description of the changes.


## Roadmap
Here's what's planned for future releases:

- **Badge Creation System**: Implement a user-friendly interface where server administrators can create custom badges directly within Discord. This feature will allow admins to define badge types, assign them based on activity, and set criteria for earning badges.
  
- **Advanced Logging**: Introduce a more comprehensive logging system that tracks bot activities such as command usage, errors, and user interactions. This feature will include log export functionality and integration with external logging services for better monitoring and analytics.

- **Profile Customization**: Expand profile customization options, allowing users to personalize their profiles with images for example.
  
- **Multi-language Support**: Add support for multiple languages, making the bot accessible to a broader audience.
