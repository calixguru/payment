import streamlit as st
import streamlit.components.v1 as components

# Page config
st.set_page_config(page_title="Pay with Paystack", layout="centered")

# White background and no header/footer
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding-top: 3rem;}
        .paybox {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            max-width: 500px;
            margin: auto;
            box-shadow: 0px 0px 25px rgba(0,0,0,0.1);
        }
        .paybox input, .paybox button {
            font-size: 16px;
            margin-top: 1rem;
            padding: 0.8rem;
            width: 100%;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        .paybox button {
            background-color: #f57c00;
            color: white;
            border: none;
            cursor: pointer;
        }
        .paybox button:hover {
            background-color: #ef6c00;
        }
    </style>
""", unsafe_allow_html=True)

# Query param reset
params = st.query_params()
if "reset" in params:
    st.query_params()
    st.session_state.clear()

# Payment control flag
if "pay_clicked" not in st.session_state:
    st.session_state.pay_clicked = False

# Show form
if not st.session_state.pay_clicked:
    st.markdown("<div class='paybox'>", unsafe_allow_html=True)
    st.markdown("### 💳 Make a Payment")

    email = st.text_input("Enter your email")
    amount = st.number_input("Enter amount (₦)", min_value=100)

    if st.button("Click to pay"):
        if email and amount:
            st.session_state.pay_clicked = True
            st.session_state.email = email
            st.session_state.amount = amount
        else:
            st.error("⚠️ Please enter both email and amount.")

    st.markdown("</div>", unsafe_allow_html=True)

# Show Paystack full-screen with animation
else:
    email = st.session_state.email
    amount = st.session_state.amount
    ref_code = f"Ref{st.session_state.get('run_id', 0)}"
    st.session_state['run_id'] = st.session_state.get('run_id', 0) + 1

    components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://js.paystack.co/v1/inline.js"></script>
            <style>
                html, body {{
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    background: #ffffff;
                    font-family: 'Segoe UI', sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .loading {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    color: #f57c00;
                }}
                .spinner {{
                    border: 4px solid rgba(0, 0, 0, 0.1);
                    border-top: 4px solid #f57c00;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin-bottom: 10px;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
        </head>
        <body>
            <div class="loading">
                <div class="spinner"></div>
                <div>Initiating Payment...</div>
            </div>

            <script>
                setTimeout(function() {{
                    PaystackPop.setup({{
                        key: 'pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068',
                        email: '{email}',
                        amount: {int(amount) * 100},
                        currency: 'NGN',
                        ref: '{ref_code}',
                        callback: function(response) {{
                            alert('✅ Payment successful! Reference: ' + response.reference);
                            window.location.href = "https://your-django-app.com/verify-payment?ref=" + response.reference;
                        }},
                        onClose: function() {{
                            window.location.href = "?reset=1";
                        }}
                    }}).openIframe();
                }}, 1000);  // Delay to allow animation
            </script>
        </body>
        </html>
    """, height=900)
