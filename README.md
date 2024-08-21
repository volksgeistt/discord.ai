# Discord.Ai
This is a Discord bot source that integrates with Google's Generative AI API to provide an AI-powered chat functionality in your Discord server.
# Features
- **Ai Chat:** The bot can be configured to respond to messages in a specific channel with AI-generated responses using the Generative AI API.
- **Setup Commands:** The bot provides commands for administrators to set up the AI chat functionality, enable/disable it, and view the current configuration.
# Installation and Setup
- Install the required dependencies.
- Obtain a Google Generative AI API key and replace "API_KEY" in the setup_gemini() method with your own API key.
- Run the bot using `python ai.py`
# Usage
1. Invite the bot to your Discord server.
2. Use the `ai` command to open the setup view, which allows you to configure the AI chat functionality.
  - **Ai Setup:** Set the channel where the AI chat will be enabled.
  - **Ai Delete:** Disable the AI chat functionality for the current server.
  - **Ai Config:** Display the current configuration for the AI chat.
3. Once the AI chat is set up, the bot will automatically respond to messages in the configured channel with AI-generated responses.
# Customization
You can customize the bot's behavior by modifying the GeminiCog class in the main.py file. For example, you can change the AI model used, add additional commands, or modify the responses.
Making any changes to this code or anything requires the original credit of the creator, make sure to mention it ( @volksgeistt )
# Credits 
- [@volksgeistt](https://instagram.com/volksgeistt)





