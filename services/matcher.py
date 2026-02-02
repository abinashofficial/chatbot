from rapidfuzz import process, fuzz, utils
import json

KEYWORD_INTENTS = {
    "hi": "Hello 👋 Welcome to {company}. How can I help?",
    "hello": "Hi 👋 Welcome to {company}.",
    "support": "Contact support at {phone}.",
    "bye": "Goodbye 👋"
}

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
