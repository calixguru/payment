import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# Use updated query param handling
params = st.query_params
email = params.get("email", "")
amount = params.get("amount", "")
reason = params.get("reason", "")
reference = params.get("ref", "")
return_url = params.get("return", f"https://calixguru.pythonanywhere.com")  # fallback URL

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

# Paystack public key (safe to expose)
paystack_pk = "pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068"

# Backend endpoints
backend_url = "calixguru.pythonanywhere.com"
verify_url = f"https://{backend_url}/verify-payment?ref={urllib.parse.quote(reference)}&email={urllib.parse.quote(email)}&amount={amount}&reason={urllib.parse.quote(reason)}"
cancel_url = urllib.parse.quote(return_url)  # redirect to previous page or default

# Paystack modal
payment_modal = f"""
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
            window.location.href = "{verify_url}";
          }},
          onClose: function() {{
            window.location.href = decodeURIComponent("{cancel_url}");
          }}
        }});
        handler.openIframe();
      }}
    </script>
  </body>
</html>
"""

# Show modal inside Streamlit
components.html(payment_modal, height=600)
