from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import wave
import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import tempfile

api_key = st.secrets["API"]
client = genai.Client(
    api_key=api_key
)

SYSTEM_INSTRUCTION = """
You are Musafir Cafe AI.

Help users with:
- Coffee recommendations
- Menu suggestions
- Dessert pairings
- Brewing techniques
- General questions

Be friendly and helpful.
"""
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Musafir Cafe",
    page_icon="☕",
    layout="wide"
)
# Initialize Session State

if "cart" not in st.session_state:
    st.session_state.cart = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background-color:#FAF6F1;
}

.title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#5C4033;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:#666666;
    margin-bottom:20px;
}

.hero{
    background:linear-gradient(
    135deg,
    #6F4E37,
    #A67B5B
    );
    border-radius:20px;
    padding:40px;
    color:white;
    text-align:center;
    margin-bottom:25px;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.08);
}

.stButton>button{
    background:#6F4E37;
    color:white;
    border-radius:12px;
    border:none;
}

.stButton>button:hover{
    background:#4B2E2B;
    color:white;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
}

</style>
""",
unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
        use_container_width=True
    )

    st.title("☕ Musafir Cafe")

    st.caption("Where Every Sip Tells A Story")
    st.markdown(f"🛒 Cart Items:{len(st.session_state.cart)}")
    st.markdown("---")

    st.success("Today's Special: Hazelnut Latte ☕")

    st.info("Loyalty Offer: 20% OFF")

    st.markdown("---")

    st.subheader("💡 Coffee Tip")

    st.success(
        "Freshly ground coffee beans always provide richer flavor."
    )

# =====================================================
# BANNER
# =====================================================

st.image(
    "https://images.unsplash.com/photo-1509042239860-f550ce710b93",
    use_container_width=True
)

# =====================================================
# TITLE
# =====================================================

st.markdown(
"""
<div class="title">
☕ Musafir Cafe
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">
Your Smart AI Barista & Coffee Companion
</div>
""",
unsafe_allow_html=True
)

# =====================================================
# HERO SECTION
# =====================================================

st.markdown(
"""
<div class="hero">

<h1>Welcome To Musafir Cafe</h1>

<h3>Discover Coffee, Conversations & Comfort</h3>

<p>
Explore personalized coffee recommendations,
brewing techniques, dessert pairings,
and AI powered coffee guidance.
</p>

</div>
""",
unsafe_allow_html=True
)

# =====================================================
# DASHBOARD
# =====================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric("☕ Coffees Served","25K+")
c2.metric("😊 Happy Customers","10K+")
c3.metric("🍰 Desserts","50+")
c4.metric("⭐ Rating","4.9/5")

st.markdown("---")

# =====================================================
# =====================================================
# FEATURED MENU
# =====================================================

st.subheader("⭐ Featured Menu")

menu_items = [
    {
        "name": "Cappuccino",
        "price": 199,
        "image": "https://images.unsplash.com/photo-1511920170033-f8396924c348"
    },
    {
        "name": "Caramel Latte",
        "price": 249,
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"
    },
    {
        "name": "Cold Brew",
        "price": 229,
        "image": "https://images.unsplash.com/photo-1447933601403-0c6688de566e"
    }
]

cols = st.columns(3)

for i, item in enumerate(menu_items):

    with cols[i]:
        st.image(item["image"])

        st.success(item["name"])

        st.write(f"₹{item['price']}")

        if st.button(
            f"🛒 Add {item['name']}",
            key=f"add{i}"
        ):
            st.session_state.cart.append(item)
            st.success("Added to Cart")

        if st.button(
            f"⚡ Buy Now {item['name']}",
            key=f"buy{i}"
        ):
            st.success(
                f"Order placed for {item['name']} ✅"
            )
# =====================================================
# DAILY SPECIALS
# =====================================================

st.subheader("🔥 Daily Specials")

s1,s2,s3,s4 = st.columns(4)

with s1:
    st.info("☕ Mocha Delight\n\n₹249")

with s2:
    st.info("☕ Hazelnut Latte\n\n₹279")

with s3:
    st.info("☕ Irish Cappuccino\n\n₹299")

with s4:
    st.info("☕ Vanilla Cold Brew\n\n₹239")

st.markdown("---")



# =====================================================
# SHOPPING CART
# =====================================================

st.markdown("---")

st.subheader("🛒 Your Cart")

if len(st.session_state.cart) == 0:

    st.info("Cart is Empty")

else:

    total = 0

    for item in st.session_state.cart:

        st.write(
            f"{item['name']} - ₹{item['price']}"
        )

        total += item["price"]

    st.markdown(
        f"### Total: ₹{total}"
    )

    customer_name = st.text_input(
        "Customer Name"
    )

    address = st.text_area(
        "Delivery Address"
    )

    if st.button("✅ Place Order"):

        st.success(
            f"""
            Order Successfully Placed!

            Name: {customer_name}

            Total Amount: ₹{total}

            Thank you for choosing Musafir Cafe ☕
            """
        )

        st.session_state.cart = []

# =====================================================
# COFFEE GALLERY
# =====================================================

st.subheader("📸 Cafe Gallery")

g1,g2,g3,g4 = st.columns(4)

with g1:
    st.image(
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"
    )

with g2:
    st.image(
        "https://images.unsplash.com/photo-1511920170033-f8396924c348"
    )

with g3:
    st.image(
        "https://images.unsplash.com/photo-1509042239860-f550ce710b93"
    )

with g4:
    st.image(
        "https://images.unsplash.com/photo-1447933601403-0c6688de566e"
    )

st.markdown("---")

# =====================================================
# VOICE TO TEXT
# =====================================================

def speech_to_text(audio_bytes):

    try:

        recognizer = sr.Recognizer()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_audio:

            temp_audio.write(audio_bytes)
            temp_audio.close()

            with sr.AudioFile(temp_audio.name) as source:

                audio = recognizer.record(source)

            text = recognizer.recognize_google(audio)

            return text

    except Exception:

        return ""


# =====================================================
# CHATBOT SECTION
# =====================================================


st.subheader("🤖 Chat With Musafir Cafe")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input(
    "Ask anything..."
)

if user_prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:

        with st.spinner("☕ Thinking..."):

            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=user_prompt,
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                    max_output_tokens=1024
                )
            )

            ai_response = response.text

    except Exception as e:

        ai_response = f"""

Details:
{str(e)}
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    with st.chat_message("assistant"):
        st.markdown(ai_response)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
"""
<div class="footer">

☕ Musafir Cafe AI

<br><br>

Where Every Sip Tells A Story

<br><br>

Explore premium coffee, desserts,
coffee brewing techniques,
and AI-powered recommendations.

</div>
""",
unsafe_allow_html=True
)
