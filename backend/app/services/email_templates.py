from app.config import settings

BRAND_COLOR = "#10b981"
LOGO_MARK = "CF"

def _base(content: str, footer_link: str, footer_text: str, bottom_note: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, 'Segoe UI', sans-serif; background: #f5f5f0; }}
  .wrap {{ max-width: 600px; margin: 0 auto; padding: 32px 16px 48px; }}
  .logo-bar {{ text-align: center; padding: 24px 0 20px; }}
  .logo-inner {{ display: inline-flex; align-items: center; gap: 10px; text-decoration: none; }}
  .logo-img {{ width: 36px; height: 36px; border-radius: 8px; display: block; }}
  .logo-name {{ font-size: 16px; font-weight: 600; color: #141413; letter-spacing: -0.3px; }}
  .logo-name em {{ font-style: normal; color: {BRAND_COLOR}; }}
  .card {{ background: #fff; border: 1px solid #e2e0d8; border-radius: 6px; }}
  .body {{ padding: 44px 40px 36px; }}
  .rule {{ width: 32px; border-top: 3px solid {BRAND_COLOR}; margin-bottom: 20px; }}
  .h1 {{ font-size: 22px; line-height: 1.35; font-weight: 400; color: #141413; margin-bottom: 24px; }}
  .p {{ font-size: 14px; line-height: 1.65; color: #3a3a34; margin-bottom: 24px; }}
  .label {{ font-size: 12px; color: #87867f; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }}
  .value {{ font-size: 14px; color: #141413; margin-bottom: 20px; line-height: 1.5; }}
  .code-block {{ margin: 4px 0 24px; padding: 28px 0; text-align: center; border-top: 1px solid #e2e0d8; border-bottom: 1px solid #e2e0d8; }}
  .code {{ font-size: 42px; font-weight: 600; letter-spacing: 14px; color: #141413; }}
  .code-hint {{ font-size: 13px; color: #87867f; margin-bottom: 14px; }}
  .code-exp {{ font-size: 13px; color: #87867f; margin-top: 12px; }}
  .big {{ font-size: 30px; font-weight: 600; color: {BRAND_COLOR}; letter-spacing: -0.5px; margin-bottom: 4px; }}
  .big-sub {{ font-size: 13px; color: #87867f; margin-bottom: 24px; }}
  .row {{ display: flex; padding: 10px 0; border-bottom: 1px solid #f0ede4; font-size: 14px; }}
  .row:last-child {{ border-bottom: none; }}
  .row-label {{ width: 150px; flex-shrink: 0; color: #87867f; }}
  .row-val {{ color: #141413; flex: 1; }}
  .rows {{ margin-bottom: 24px; }}
  .feat {{ display: flex; align-items: flex-start; gap: 9px; padding: 5px 0; font-size: 14px; color: #3a3a34; line-height: 1.5; }}
  .dot {{ width: 7px; height: 7px; border-radius: 50%; background: {BRAND_COLOR}; flex-shrink: 0; margin-top: 5px; }}
  .feats {{ margin-bottom: 24px; }}
  .footer-bar {{ border-top: 1px solid #e2e0d8; padding: 20px 40px; }}
  .footer-link {{ font-size: 14px; color: #141413; text-decoration: underline; }}
  .bottom {{ text-align: center; padding: 16px 20px; }}
  .bottom p {{ font-size: 12px; color: #87867f; line-height: 1.6; }}
  .bottom a {{ font-size: 12px; color: #87867f; text-decoration: underline; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="logo-bar">
    <a class="logo-inner" href="{settings.APP_URL}">
      <img src="{settings.APP_URL}/logo-gold.png" alt="CashFlow AI" class="logo-img" />
      <span class="logo-name">Cash<em>Flow</em> AI</span>
    </a>
  </div>
  <div class="card">
    <div class="body">
      {content}
    </div>
    <div class="footer-bar">
      <a href="{footer_link}" class="footer-link">{footer_text}</a>
    </div>
  </div>
  <div class="bottom">
    <p>{bottom_note}</p>
  </div>
</div>
</body>
</html>"""


def welcome_email(business_name: str) -> tuple[str, str]:
    """Returns (subject, html)"""
    subject = f"Welcome to CashFlow AI, {business_name}"
    content = f"""<div class="rule"></div>
<h2 class="h1">Welcome to CashFlow AI, {business_name}</h2>
<p class="p">Your account is set up and ready. Start managing invoices, tracking payments, and using AI-powered cash flow insights.</p>
<div class="label">What you can do</div>
<div class="feats">
  <div class="feat"><div class="dot"></div>Create and send professional invoices</div>
  <div class="feat"><div class="dot"></div>Collect payments via M-Pesa STK push</div>
  <div class="feat"><div class="dot"></div>Get AI-powered cash flow insights</div>
  <div class="feat"><div class="dot"></div>Set automated payment reminders</div>
  <div class="feat"><div class="dot"></div>Manage your team and track activity</div>
</div>"""
    html = _base(
        content=content,
        footer_link=f"{settings.APP_URL}/dashboard",
        footer_text="Go to your dashboard →",
        bottom_note="You received this because you created a CashFlow AI account.",
    )
    return subject, html


def password_reset_email(business_name: str, reset_token: str, requested_at: str) -> tuple[str, str]:
    """Returns (subject, html)"""
    reset_link = f"{settings.APP_URL}/reset-password?token={reset_token}"
    subject = "Reset your CashFlow AI password"
    content = f"""<div class="rule"></div>
<h2 class="h1">Reset your password</h2>
<p class="p">We received a request to reset the password for your CashFlow AI account. Click the link below to choose a new password. This link expires in 30 minutes.</p>
<div class="label">Requested at</div>
<div class="value">{requested_at}</div>
<p class="p" style="margin-bottom:0">If you didn't request a reset, no action is needed. Your password remains unchanged.</p>"""
    html = _base(
        content=content,
        footer_link=reset_link,
        footer_text="Reset my password",
        bottom_note="You received this because a password reset was requested for your account.",
    )
    return subject, html


def login_notification_email(
    business_name: str,
    ip_address: str,
    device: str,
    location: str,
    login_time: str,
) -> tuple[str, str]:
    """Returns (subject, html)"""
    subject = "New sign-in to your CashFlow AI account"
    content = f"""<div class="rule"></div>
<h2 class="h1">New sign-in to your account</h2>
<p class="p">Hi {business_name}, we noticed a new sign-in to your CashFlow AI account. If this was you, no action is needed.</p>
<div class="rows">
  <div class="row"><span class="row-label">Device</span><span class="row-val">{device}</span></div>
  <div class="row"><span class="row-label">IP address</span><span class="row-val">{ip_address}</span></div>
  <div class="row"><span class="row-label">Time</span><span class="row-val">{login_time}</span></div>
</div>
<p class="p" style="margin-bottom:0">If you don't recognise this sign-in, change your password immediately from your account settings.</p>"""
    html = _base(
        content=content,
        footer_link=f"{settings.APP_URL}/profile",
        footer_text="Review account security",
        bottom_note="You received this because login alerts are enabled on your account.",
    )
    return subject, html


def invoice_sent_email(
    client_name: str,
    business_name: str,
    amount: str,
    due_date: str,
    invoice_id: str,
) -> tuple[str, str]:
    """Returns (subject, html)"""
    subject = f"Invoice from {business_name} — {amount}"
    content = f"""<div class="rule"></div>
<h2 class="h1">You have a new invoice</h2>
<p class="p">Hi {client_name}, {business_name} has sent you an invoice. Please review and arrange payment before the due date.</p>
<div class="big">{amount}</div>
<div class="big-sub">Due {due_date}</div>
<div class="rows">
  <div class="row"><span class="row-label">From</span><span class="row-val">{business_name}</span></div>
  <div class="row"><span class="row-label">Invoice ID</span><span class="row-val" style="font-family:monospace;font-size:13px;">{invoice_id[:8].upper()}</span></div>
  <div class="row"><span class="row-label">Due date</span><span class="row-val">{due_date}</span></div>
</div>"""
    html = _base(
        content=content,
        footer_link=f"{settings.APP_URL}/pay/{invoice_id}",
        footer_text="View invoice",
        bottom_note=f"You received this because {business_name} sent you an invoice via CashFlow AI.",
    )
    return subject, html
