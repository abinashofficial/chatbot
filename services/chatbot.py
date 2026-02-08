from functools import lru_cache
from services.vendor import VENDORS
from services.matcher import keyword_match, fuzzy_match, word_match

@lru_cache(maxsize=200)
def chatbot_reply(message: str, vendor_id: str):
    vendor = VENDORS.get(vendor_id)

    if not vendor:
        return "❌ Invalid vendor ID", 0
    
    matched_msg, ok = word_match(message, vendor)
    if ok == False:
        # Keyword
        kw = keyword_match(matched_msg, vendor)
        if kw:
            return kw, 100

    # Fuzzy
    q, answer, score = fuzzy_match(matched_msg, vendor["json_file"])

    if score > 45:
        return answer, score
    elif score >= 35:
        return f"Did you mean: '{q}'?", score

    return "🤖 Sorry, I didn’t understand.", score
