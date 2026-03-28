from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/c2b")
async def mpesa_c2b_callback(request: Request):
    """Receive M-Pesa C2B payment confirmation callback."""
    body = await request.json()
    # TODO: Validate callback, match CheckoutRequestID, update invoice status
    return {"ResultCode": 0, "ResultDesc": "Accepted"}


@router.post("/b2c-result")
async def mpesa_b2c_result(request: Request):
    """Receive M-Pesa B2C disbursement result callback."""
    body = await request.json()
    # TODO: Process B2C result
    return {"ResultCode": 0, "ResultDesc": "Accepted"}


@router.post("/ratiba")
async def ratiba_callback(request: Request):
    """Receive Ratiba scheduled job callback."""
    body = await request.json()
    # TODO: Trigger reminder action (send SMS, etc.)
    return {"status": "received"}
