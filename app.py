import streamlit as st
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="CALIXGURU PAYMENT", layout="centered")

# --- Query Params ---
params = st.query_params
email = params.get("email", "")
amount = params.get("amount", "")
reason = params.get("reason", "")
reference = params.get("ref", "")

# --- Validation ---
if not all([email, amount, reason, reference]):
    st.error("🚫 Missing one or more required parameters in the URL.")
    st.stop()

# --- Convert Amount ---
try:
    kobo_amount = int(amount) * 100
except ValueError:
    st.error("🚫 Invalid amount.")
    st.stop()

# --- Config ---
paystack_pk = "pk_live_008159524c1237cf3094bc3db1ae0a5d8b4ce068"
backend_url = "https://calixguru.pythonanywhere.com"
verify_url = f"{backend_url}/verify-payment/?ref={reference}&email={email}&amount={amount}&reason={reason}"
cancel_url = f"{backend_url}/payment-cancelled/"
initiate_url = f"{backend_url}/initiate-payment/"

# --- Page Header ---
st.markdown(
    """
    <div style="text-align:center;">
        <h2 style="color:#4CAF50;">💳 Calixguru Payment Gateway</h2>
        <p style="font-size:16px;">Use the options below to initiate, verify, or cancel your payment.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Display Transaction Info ---
with st.expander("🔍 Payment Details", expanded=True):
    st.write(f"**Email:** {email}")
    st.write(f"**Amount:** ₦{amount}")
    st.write(f"**Reason:** {reason}")
    st.write(f"**Reference:** {reference}")

st.markdown("---")

# --- Buttons Section ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Start Payment"):
        payment_modal = f"""
        <html>
          <head>
            <script src="https://js.paystack.co/v1/inline.js"></script>
            <style>
              .exit-btn {{
                position: fixed;
                top: 15px;
                right: 15px;
                background-color: #f44336;
                color: white;
                padding: 10px 16px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                z-index: 9999;
                cursor: pointer;
                font-weight: bold;
              }}
              .exit-btn:hover {{
                background-color: #d32f2f;
              }}
            </style>
          </head>
          <body onload="payWithPaystack()">
            <button class="exit-btn" onclick="window.location.href='{cancel_url}'">❌ Cancel Payment</button>
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
        components.html(payment_modal, height=700)

with col2:
    if st.button("🔍 Verify Payment"):
        st.success("Redirecting to verify your payment...")
        st.markdown(f"""<meta http-equiv="refresh" content="0; URL={verify_url}">""", unsafe_allow_html=True)

with col3:
    if st.button("❌ Cancel Payment"):
        st.warning("Cancelling your payment...")
        st.markdown(f"""<meta http-equiv="refresh" content="0; URL={cancel_url}">""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; font-size: 13px; color: grey;">
        Powered by <strong>Calixguru</strong> | Secure Paystack Integration ✅
    </div>
    """,
    unsafe_allow_html=True
)
