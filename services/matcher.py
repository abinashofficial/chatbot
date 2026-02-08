from rapidfuzz import process, fuzz, utils
import json

KEYWORD_INTENTS = {
    "hi": "Hello 👋. How can I help you today?",
    "hello": "Hi there 👋. How can I assist you today?",
    "hey": "Welcome to {company}. How can I help you today?",

    "good morning": "Good morning ☀️. How can I help?",
    "good afternoon": "Good afternoon 😊 How can {company} assist you?",
    "good evening": "Good evening 🌙 How can I help you today?",

    "how are you": "I'm doing great 😊 How can I help?",
    "are you there": "Yes — I'm here and ready to help 👍",

    "who are you": "I am {bot_name} 🤖, your virtual assistant for {company}.",
    "what are you": "I am an AI business assistant chatbot for {company}.",

    "talk to human": "Sure 👍 Please call {phone} to speak with our team.",
    "human support": "You can reach our support team at {phone}.",

    "help": "Sure 👍 I can help with services, pricing, demos, and support.",
    "thank": "You're welcome 😊 Happy to help!",
    "bye": "Goodbye 👋 Have a great day!",
    "price":"Our pricing plans are Free ($0), Business ($29/month), and Developer ($49/month).",
"cost":"Our pricing plans are Free ($0), Business ($29/month), and Developer ($49/month).",
}






def word_match(message, vendor):
    intents = vendor.get("quick_intents", "")
    for item in intents:
        if item in message:
            return item, True
        
    return message, False




def keyword_match(message: str, vendor: dict):
    msg = message.lower()
    for k, template in KEYWORD_INTENTS.items():
        if k in msg:
            return template.format(
                company=vendor["company"],
                phone=vendor["phone"],
                bot_name=vendor["bot_name"]
            )
    return None

def fuzzy_match(message: str, json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        faq = json.load(f)

    questions = list(faq.keys())
    processed = [utils.default_process(q) for q in questions]

    match = process.extractOne(
        utils.default_process(message),
        processed,
        scorer=fuzz.token_sort_ratio
    )

    if not match:
        return None, None, 0

    idx = match[2]
    return questions[idx], faq[questions[idx]], match[1]
