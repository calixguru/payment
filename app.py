import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CalixGuru Payment", layout="centered")

st.markdown("## 🔐 CalixGuru Secure Payment Page")
st.markdown("Please choose an option below to proceed:")

# Get query parameters
params = st.query_params
email = params.get("email", "")
amount = params.get("amount", "")
reason = params.get("reason", "")
reference = params.get("ref", "")

# Convert amount to Kobo
try:
    kobo_amount = int(amount) * 100
except (ValueError, TypeError):
    kobo_amount = 0

# Paystack public key
paystack_pk = "pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068"

# Django backend URLs
backend_url = "https://calixguru.pythonanywhere.com"
verify_url = f"{backend_url}/verify-payment/?ref={reference}&email={email}&amount={amount}&reason={reason}"
cancel_url = f"{backend_url}/payment-cancelled"

# Show payment info
if all([email, amount, reason, reference]):
    st.success(f"**Email:** {email} | **Amount:** ₦{amount} | **Reason:** {reason}")
else:
    st.error("Missing some payment parameters in the URL.")

# State to control display of Paystack
start_payment = st.button("💳 Start Payment")

# Manual links
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <a href="{verify_url}" style="text-decoration: none;">
            <button style="width: 100%; padding: 0.5rem; font-weight: bold; background-color: green; color: white; border: none; border-radius: 5px;">✅ Verify Payment</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <a href="{cancel_url}" style="text-decoration: none;">
            <button style="width: 100%; padding: 0.5rem; font-weight: bold; background-color: red; color: white; border: none; border-radius: 5px;">❌ Cancel Payment</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

# If "Start Payment" clicked, show Paystack popup trigger below
if start_payment:
    st.markdown("---")
    st.markdown("### 📤 Launching Paystack Payment...")
    components.html(f"""
        <html>
          <head>
            <script src="https://js.paystack.co/v1/inline.js"></script>
          </head>
          <body>
            <script>
              function payWithPaystack() {{
                var handler = PaystackPop.setup({{
                  key: '{paystack_pk}',
                  email: '{email}',
                  amount: {kobo_amount},
                  currency: 'NGN',
                  ref: '{reference}',
                  metadata: {{
                    custom_fields: [
                      {{
                        display_name: "Payment Reason",
                        variable_name: "reason",
                        value: "{reason}"
                      }}
                    ]
                  }},
                  callback: function(response) {{
                    window.location.href = "{verify_url}";
                  }},
                  onClose: function() {{
                    alert("Payment cancelled.");
                  }}
                }});
                handler.openIframe();
              }}
              payWithPaystack();
            </script>
          </body>
        </html>
        """, height=20)
