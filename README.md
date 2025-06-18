# Discord Bot for Minecraft servers status

This bot updates a Discord message with the status of a Minecraft Java Edition server.

## Installation

1. Install Python 3 and `pip3`.
2. Install dependencies:
   ```sh
   pip3 install -r requirements.txt
   ```
3. Set up the required variable inside `bot.py`:
   - `TOKEN`: Your Discord bot token.
4. Run the bot:
   ```sh
   python3 bot.py
   ```

### Notes

- The bot updates the message every 60 seconds.
- You have to change the time zone in all `bot.py`.

