"""M-Pesa Daraja API wrapper.

Handles OAuth token management, STK Push, B2C, and transaction status queries.
Token is cached in Redis with a 55-minute TTL to avoid per-request auth.
"""

# TODO: Implement
# - get_access_token() with Redis caching
# - stk_push(phone, amount, reference, callback_url)
# - b2c_payment(phone, amount, remarks)
# - transaction_status(transaction_id)
