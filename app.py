import streamlit as st
import streamlit.components.v1 as components

# Use updated API
params = st.query_params
email = params.get("email", "")
amount = params.get("amount", "")
reason = params.get("reason", "")
reference = params.get("ref", "")

# Validate input
if not all([email, amount, reason, reference]):
    st.error("Missing payment information in URL.")
    st.stop()

# Convert amount to Kobo
try:
    kobo_amount = int(amount) * 100
except ValueError:
    st.error("Invalid amount value.")
    st.stop()

# Your public Paystack key (safe to expose)
paystack_pk = "pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068"

# Your Django URLs (replace 127.0.0.1 with actual deployed domain when live)
backend_url = "127.0.0.1:8000"
verify_url = f"http://{backend_url}/verify-payment?ref={reference}&email={email}&amount={amount}&reason={reason}"
cancel_url = f"http://{backend_url}/payment-cancelled"

# Paystack modal HTML
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
            window.location.href = "{cancel_url}";
          }}
        }});
        handler.openIframe();
      }}
    </script>
  </body>
</html>
"""

# Display in Streamlit iframe (adjust height to show full modal)
components.html(payment_modal, height=600)
