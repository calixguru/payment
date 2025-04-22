
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# Get query parameters
params = st.experimental_get_query_params()
email = params.get("email", [""])[0]
amount = params.get("amount", [""])[0]
reason = params.get("reason", [""])[0]
reference = params.get("ref", [""])[0]

url = '127.0.0.1:8000'
# Convert amount to kobo (Paystack expects lowest currency unit)
try:
    kobo_amount = int(amount) * 100
except ValueError:
    st.error("Invalid amount provided.")
    st.stop()

# Construct redirect URLs
verify_url = f"https://{url}/verify-payment?ref={reference}&email={email}&amount={amount}&reason={reason}"
cancel_url = f"https://{url}/payment-cancelled"

# Your public Paystack key (safe to expose)
paystack_pk = "pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068"

# Trigger Paystack popup using HTML + JS
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
                display_name: "{email}",
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

# Display modal inside Streamlit iframe
components.html(payment_modal, height=10)
