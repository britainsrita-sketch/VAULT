import os
import logging
import random
import re
from collections import defaultdict
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# CONFIGURATION
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# --- NATIVE REPURPOSING ENGINE ---

def extract_hashtags(text, num=3):
    """Extracts prominent keywords to generate automated hashtags."""
    words = re.findall(r'\b[a-zA-Z]{5,12}\b', text.lower())
    stop_words = {'about', 'their', 'there', 'would', 'could', 'should', 'these', 'those'}
    keywords = [w for w in words if w not in stop_words]
    
    if not keywords:
        return "#content #repurposed"
        
    # Pick unique keywords
    unique_keys = list(set(keywords))[:num]
    return " ".join([f"#{k}" for k in unique_keys])

def build_markov_model(text):
    """Creates a probability map of word transitions from the text."""
    words = text.split()
    model = defaultdict(list)
    
    for i in range(len(words) - 1):
        model[words[i]].append(words[i+1])
        
    return model, words

def generate_markov_text(text, max_words=40):
    """Regenerates the text using a native Markov Chain distribution."""
    model, words = build_markov_model(text)
    if len(words) < 5:
        return text # Too short to modify algorithmically
        
    # Start with a random capitalized word if possible
    cap_words = [w for w in words if w[0].isupper()]
    current_word = random.choice(cap_words) if cap_words else random.choice(words)
    
    output = [current_word]
    
    for _ in range(max_words):
        next_words = model[current_word]
        if not next_words:
            # If a dead end is reached, sample a new starting point
            next_words = words
            
        current_word = random.choice(next_words)
        output.append(current_word)
        
        # Clean termination if it ends on a period
        if current_word.endswith(('.', '!', '?')) and len(output) > 15:
            break
            
    return " ".join(output)

def rewrite_structure(text):
    """Alternative structural framework shifter (Listicle format converter)."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) < 2:
        return text
        
    repurposed = "📝 **Key Takeaways & Shuffled Core Insights:**\n\n"
    for i, sentence in enumerate(sentences, 1):
        if len(sentence.strip()) > 5:
            repurposed += f"{i}️⃣ {sentence.strip()}\n"
            
    return repurposed

# --- TELEGRAM HANDLERS ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✍️ **Welcome to the Content Repurposer Bot!**\n\n"
        "Send me any blog post, caption, or long text paragraph. I will use native "
        "Markov linguistic shifting to scramble, spin, and convert it into completely "
        "new structural formats with automated hashtags."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    
    if len(user_text.split()) < 10:
        await update.message.reply_text("⚠️ Please send a longer paragraph (at least 10 words) so I can properly repurpose it.")
        return

    status_msg = await update.message.reply_text("🔄 Remixing sentence matrix structures...")
    
    # Run the native repurposing frameworks
    markov_variant = generate_markov_text(user_text)
    listicle_variant = rewrite_structure(user_text)
    tags = extract_hashtags(user_text)
    
    response_text = (
        f"🚀 **REPURPOSED CONTENT GENERATED** 🚀\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔄 **Variant A (Markov Fluid Mix):**\n"
        f"_\"{markov_variant}\"_\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{listicle_variant}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏷️ **Suggested Tags:** {tags}"
    )
    
    await status_msg.edit_text(response_text, parse_mode="Markdown")

def main():
    logger.info("🤖 Starting Content Repurposer Background Worker...")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Continuous background worker deployment safe polling
    application.run_polling()

if __name__ == "__main__":
    main()
