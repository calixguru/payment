import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CalixGuru Payment", layout="centered")

st.markdown("## 🔐 CalixGuru Secure Payment Page")
st.markdown("Please choose an option below to proceed:")

# Use updated API for query params
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

# Your URLs
backend_url = "https://calixguru.pythonanywhere.com"
verify_url = f"{backend_url}/verify-payment/?ref={reference}&email={email}&amount={amount}&reason={reason}"
cancel_url = f"{backend_url}/payment-cancelled"

# --- BUTTONS ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💳 Start Payment"):
        # Inject Paystack popup
        payment_modal = f"""
        <html>
          <head><script src="https://js.paystack.co/v1/inline.js"></script></head>
          <body onload="payWithPaystack()">
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
            </script>
          </body>
        </html>
        """
        components.html(payment_modal, height=10)

with col2:
    st.markdown(
        f"""
        <a href="{verify_url}" style="text-decoration: none;">
            <button style="width: 100%; padding: 0.5rem; font-weight: bold; background-color: green; color: white; border: none; border-radius: 5px;">✅ Verify Payment</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <a href="{cancel_url}" style="text-decoration: none;">
            <button style="width: 100%; padding: 0.5rem; font-weight: bold; background-color: red; color: white; border: none; border-radius: 5px;">❌ Cancel Payment</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

# Optional debug info
if not all([email, amount, reason, reference]):
    st.warning("Some payment details are missing in the URL.")
else:
    st.info(f"🔎 **Email:** {email} | **Amount:** ₦{amount} | **Reason:** {reason}")
