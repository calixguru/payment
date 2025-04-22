import streamlit as st
import streamlit.components.v1 as components

# Get URL query parameters
params = st.query_params
email = params.get("email", "")
amount = params.get("amount", "")
reason = params.get("reason", "")
reference = params.get("ref", "")

# Validate required parameters
if not all([email, amount, reason, reference]):
    st.error("Missing payment information in URL.")
    st.stop()

# Convert amount to kobo
try:
    kobo_amount = int(amount) * 100
except ValueError:
    st.error("Invalid amount value.")
    st.stop()

# Paystack public key (safe to expose)
paystack_pk = "pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068"

# URLs
backend_url = "calixguru.pythonanywhere.com"
verify_url = f"https://{backend_url}/verify-payment?ref={reference}&email={email}&amount={amount}&reason={reason}"
cancel_url = f"https://{backend_url}/payment-cancelled"
manual_cancel_url = f"https://{backend_url}"  # Home page or wherever you want

# Paystack payment modal
payment_modal = f"""
<html>
  <head>
    <script src="https://js.paystack.co/v1/inline.js"></script>
    <style>
      body {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }}
      .cancel-btn {{
        margin-top: 20px;
        padding: 10px 20px;
        background-color: #ff4d4f;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
      }}
    </style>
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
            window.location.href = "{cancel_url}";
          }}
        }});
        handler.openIframe();
      }}
    </script>

    <button class="cancel-btn" onclick="window.location.href='{manual_cancel_url}'">
      Cancel and Return to Website
    </button>
  </body>
</html>
"""

# Display modal with custom cancel button
components.html(payment_modal, height=650)
