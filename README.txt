RAKSHANET - IMPROVED CONNECTED PROTOTYPE
Project lead: Vijaysimha

FEATURES
- SOS button sends a Telegram message to one configured trusted test chat.
- Current device location with a Google Maps link.
- Optional live location updates every 30 seconds while this page stays open and tracking is ON.
- Alert history, local contact labels, and guardian check-in demo.
- The server never embeds your bot token in browser JavaScript.

IMPORTANT LIMITS
- This is a hackathon prototype, NOT a police/emergency-services integration.
- Telegram messages work only after you configure a bot token and chat ID.
- Use only a consenting test recipient. Tell them before testing.
- Live tracking stops when you press Stop, close/reload the tab, or the browser/device stops location updates.
- A browser cannot guarantee background tracking when closed or the phone is locked.
- Do not use this prototype as your only safety method. For a real emergency in India, call 112.
- Do not enter real children's sensitive data. Get informed consent for location sharing.

START ON WINDOWS
1. Install Python 3 if it is not installed.
2. Copy .env.example to a file named .env.
3. Follow the Telegram setup below and fill TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env.
4. Double-click run_windows.bat. Keep the black terminal window open.
5. Open Chrome and visit http://localhost:8080 (do not open index.html directly).
6. Click Get my location and choose Allow.
7. Click ACTIVATE SOS ALERT to send a test message to the configured Telegram chat.
8. For location updates, click Start live tracking. Click Stop live tracking when finished.

TELEGRAM SETUP (TEST RECIPIENT)
1. Open Telegram and message @BotFather. Use /newbot and follow the prompts.
2. BotFather gives you a bot token. Keep it secret; do not send it in this chat or commit it to GitHub.
3. Open your new bot and press Start. The trusted test recipient must also start the bot if they are the recipient.
4. To find a chat ID, message your bot once, then open this URL in your browser after replacing TOKEN with the token: https://api.telegram.org/botTOKEN/getUpdates
5. Find the message object and its chat.id value. For a private test chat, use that number as TELEGRAM_CHAT_ID. Do not share the getUpdates page or token.
6. Put both values into .env, save, and restart run_windows.bat.

CHROME LOCATION PERMISSION
1. Open http://localhost:8080.
2. Click the tune/lock icon to the left of the address bar.
3. Open Site settings.
4. Set Location to Allow.
5. Reload the page and click Get my location.
If blocked: Chrome Settings > Privacy and security > Site settings > Location; remove localhost from Blocked or change it to Allow. Also enable Windows Settings > Privacy & security > Location.

TROUBLESHOOTING
- 'Telegram is not configured': check .env file name and values, then restart server.
- 'chat not found': open the bot and press Start; verify chat ID.
- 'Unauthorized': bot token is incorrect. Revoke/regenerate it with BotFather if exposed.
- Port busy: change PORT=8081 in .env and visit http://localhost:8081.
- Location still denied: use localhost URL, set Location=Allow in Chrome Site settings, reload.
- If Python is not recognized, install Python and select 'Add Python to PATH'.

TECH STACK
HTML, CSS, JavaScript, Python standard library, Telegram Bot API.
