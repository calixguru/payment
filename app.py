import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# Get query params
params = st.query_params
email = params.get("email", "")
amount = params.get("amount", "")
reason = params.get("reason", "")
reference = params.get("ref", "")

# App title
st.title("Calixguru Payment Page")

# Validate inputs
if not all([email, amount, reason, reference]):
    st.error("Missing payment info in URL. Please ensure email, amount, reason, and reference are passed.")
    st.stop()

# Convert to kobo
try:
    kobo_amount = int(amount) * 100
except ValueError:
    st.error("Invalid amount.")
    st.stop()

# Base URLs
backend_url = "https://calixguru.pythonanywhere.com"
streamlit_url = "https://calixguru.streamlit.app"
verify_url = f"{backend_url}/verify-payment?ref={reference}&email={email}&amount={amount}&reason={reason}"
cancel_url = f"{backend_url}"  # Home page or landing page
return_to_self_url = f"{streamlit_url}?ref={reference}&email={email}&amount={amount}&reason={reason}"

# Your Paystack public key (safe to expose)
paystack_pk = "pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068"

# 3 Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💳 Start Payment"):
        # Inject Paystack modal inside iframe
        payment_html = f"""
        <html>
          <head>
            <script src="https://js.paystack.co/v1/inline.js"></script>
          </head>
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
                    window.location.href = "{return_to_self_url}";
                  }},
                  onClose: function() {{
                    alert("Payment modal closed.");
                  }}
                }});
                handler.openIframe();
              }}
            </script>
          </body>
        </html>
        """
        components.html(payment_html, height=600)

with col2:
    verify_link = f"{verify_url}"
    st.markdown(f"[🔍 Verify Payment]({verify_link})", unsafe_allow_html=True)

with col3:
    cancel_link = f"{cancel_url}"
    st.markdown(f"[❌ Cancel Payment]({cancel_link})", unsafe_allow_html=True)
