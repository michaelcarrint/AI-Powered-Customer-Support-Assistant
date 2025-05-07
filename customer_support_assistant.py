import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv('.env', override=True)

# Initialize the OpenAI client with your API key
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful and empathetic customer support assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def detect_intent(message):
    message = message.lower()
    if "return" in  message:
        return "return"
    elif "broken" in message or "damaged" in message or "late" in message:
        return "complaint"
    elif "satisfied" in message or "thanks" in message or "love" in message:
        return "positive"
    else:
        return "general"

def get_prompt(intent, customer_message):
    if intent == "return":
        return f"""A customer wants to return a product, \
```{customer_message}```
Return Policy – NovaNest™

At NovaNest, your satisfaction is our priority. If you're not completely happy with your purchase, we're here to help.

Returns:
- Timeframe: Return most items within 30 days of delivery for a full refund.
- Condition: Items must be in original condition and packaging.
- Exceptions: Personalized, clearance, or final-sale items are non-returnable unless defective.

Exchanges:
- Free exchanges available within 30 days.

Refunds:
- Issued to original payment method within 3–5 business days after inspection.
- Original shipping costs are non-refundable unless it's our error.

Start a Return:
1. Visit [returns.novanest.com](#)
2. Enter order number and email.
3. Follow the instructions to generate a return label.

Support:
Email: support@novanest.com  
Phone: 1-800-NOVA-123

---

Keep the tone warm and solution-focused.
Explain the return process in a friendly and helpful tone.
"""
    elif intent == "positive":
        return f"""A customer left a positive feedback, \
```{customer_message}```
Thank the customer warmly and let them know their feedback id deeply appreciated. \
"""
    elif intent == "complaint":
        return f"""A customer dropped a complaint: \
```{customer_message}```
Generate a response with an apology, use a kind and professional tone.
"""
    else:
        return f"""A customer dropped a complaint:
```{customer_message}```
respond helpfully and in a polite manner based on the intent of the message \
"""

# Sample customer complaint

def main():
    customer_message = input("Enter the customer's message: \n")
    intent = detect_intent(customer_message)
    prompt = get_prompt(intent, customer_message)

    response = call_gpt(prompt)
    print("\n📝 Here's what you can say to the customer:\n")
    print(response)

if __name__ == "__main__":
    main()
