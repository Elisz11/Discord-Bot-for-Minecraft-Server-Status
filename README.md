# Discord Bot for Minecraft Servers

This bot updates a Discord message with the status of a Minecraft Java Edition server. It is available in two versions:

- **Without Docker**: Requires manual installation of dependencies via `pip`.
- **With Docker**: Uses a containerized environment for easier deployment.

## Installation (Without Docker)

1. Install Python 3 and `pip`.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the required variables inside `bot_nodocker.py`:
   - `TOKEN`: Your Discord bot token.
   - `CHANNEL_ID`: The Discord channel ID where the bot will post updates.
   - `server_ip`: The IP address of the Minecraft server.
4. Run the bot:
   ```sh
   python bot_nodocker.py
   ```

## Installation (With Docker)

1. Build the Docker image:
   ```sh
   docker build -t discord-mc-bot .
   ```
2. Run the container:
   ```sh
   docker run -d --name mc-bot \
      -e DISCORD_TOKEN="your_token_here" \
      -e CHANNEL_ID="your_channel_id" \
      -e SERVER_IP="your_server_ip" \
      discord-mc-bot
   ```

### Dockerfile

The `Dockerfile` ensures the bot runs inside a lightweight Python environment with all dependencies pre-installed.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY bot.py .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -u 1000 -U botuser && chown -R botuser:botuser /app
USER botuser

CMD ["python", "bot.py"]
```

### Notes

- The Docker version reads environment variables for configuration instead of hardcoded values.
- The bot updates the message every 30 seconds.
- You have to change the time zone in all `bot.py`.

