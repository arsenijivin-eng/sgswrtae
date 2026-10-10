# CristyVPN migration bot

## What it does
- Sends the supplied CristyVPN welcome image on `/start`.
- Shows the channel subscription link and a “Я подписался” button.
- Checks channel membership and, when confirmed, shows the “НОВЫЙ ВПН” button.
- Automatically approves join requests in the configured channel.

## Setup
1. Create a bot with @BotFather and copy its token.
2. Add the bot as an **administrator** to your channel. Give it permission to invite users / manage join requests (and ensure it can read membership).
3. Find the channel's numeric ID (usually starts with `-100`). The invite link alone is not enough for Telegram's membership-check API.
4. Install Python 3.10+ and dependencies:
   `pip install -r requirements.txt`
5. Set environment variables:
   - `BOT_TOKEN` — token from @BotFather
   - `CHANNEL_ID` — numeric channel ID, e.g. `-1001234567890`
6. Run:
   `python bot.py`

The channel must have join requests enabled for requests to arrive. The bot only approves requests for the channel ID configured in `CHANNEL_ID`.

On Linux/macOS, for example:
`export BOT_TOKEN='123:abc'`
`export CHANNEL_ID='-1001234567890'`
`python bot.py`

Do not share your bot token publicly.
