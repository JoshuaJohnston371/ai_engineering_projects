import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from dotenv import load_dotenv

from agents import Agent, function_tool

load_dotenv(override=True)


def _send_email_impl(subject: str, html_body: str) -> Dict[str, str]:
    """
    Internal implementation of send_email (not decorated).
    This can be called directly for testing.
    
    Send an email with the given subject and HTML body using SMTP.
    Requires environment variables:
    - SMTP_SERVER: SMTP server address (e.g., 'smtp.gmail.com')
    - SMTP_PORT: SMTP port (e.g., 587 for TLS, 465 for SSL)
    - SMTP_USERNAME: Your email address
    - SMTP_PASSWORD: Your email password or app password
    - FROM_EMAIL: Sender email address
    - TO_EMAIL: Recipient email address
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")
    to_email = os.getenv("TO_EMAIL")
    
    # Validate required environment variables
    if not all([smtp_server, smtp_username, smtp_password, from_email, to_email]):
        missing = []
        if not smtp_server:
            missing.append("SMTP_SERVER")
        if not smtp_username:
            missing.append("SMTP_USERNAME")
        if not smtp_password:
            missing.append("SMTP_PASSWORD")
        if not from_email:
            missing.append("FROM_EMAIL")
        if not to_email:
            missing.append("TO_EMAIL")
        
        error_msg = f"Missing required environment variables: {', '.join(missing)}"
        print(f"Error: {error_msg}")
        return {"status": "error", "message": error_msg}
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        # Create HTML part
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Determine if we should use SSL or TLS
        use_ssl = smtp_port == 465
        
        # Connect to server and send email
        if use_ssl:
            # Use SSL (port 465)
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            # Use TLS (port 587 or 25)
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
        
        # Login and send
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return {"status": "success", "message": f"Email sent to {to_email}"}
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP authentication failed: {e}"
        print(f"Error: {error_msg}")
        
        # Provide helpful guidance for Outlook/Microsoft accounts
        if "outlook.com" in str(e).lower() or "microsoft" in str(e).lower() or "basic authentication is disabled" in str(e).lower():
            help_msg = (
                "\n⚠️  Outlook/Microsoft Account Issue Detected:\n"
                "\nMicrosoft has disabled Basic Authentication for SMTP in Exchange Online.\n"
                "Even with an App Password, basic auth may be blocked.\n"
                "\nSOLUTIONS:\n"
                "\nOption 1: Use Gmail instead (Recommended - Easier)\n"
                "  - Gmail still supports app passwords\n"
                "  - Update your .env:\n"
                "    SMTP_SERVER=smtp.gmail.com\n"
                "    SMTP_PORT=587\n"
                "    SMTP_USERNAME=your_gmail@gmail.com\n"
                "    SMTP_PASSWORD=your_gmail_app_password\n"
                "\nOption 2: Use Personal Outlook.com (if not Exchange Online)\n"
                "  - Try: SMTP_SERVER=smtp-mail.outlook.com\n"
                "  - Port: 587\n"
                "  - Make sure you're using a personal account, not work/school\n"
                "\nOption 3: Use Microsoft Graph API (Advanced)\n"
                "  - Requires OAuth 2.0 setup\n"
                "  - More complex but more secure\n"
                "\nFor personal Outlook.com accounts:\n"
                "1. Verify you're using a personal account (not work/school)\n"
                "2. Go to https://account.microsoft.com/security\n"
                "3. Enable 2-Step Verification\n"
                "4. Generate App Password at: https://account.microsoft.com/security/app-passwords\n"
                "5. Use that app password (16 characters, no spaces)\n"
            )
            print(help_msg)
            error_msg += help_msg
        
        return {"status": "error", "message": error_msg}
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error occurred: {e}"
        print(f"Error: {error_msg}")
        return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error sending email: {e}"
        print(f"Error: {error_msg}")
        return {"status": "error", "message": error_msg}


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body using SMTP."""
    return _send_email_impl(subject, html_body)


INSTRUCTIONS = """You are an email agent that sends research reports via email.
You will be given a RESEARCH REPORT.
When you receive the research report (typically in markdown format), you should:
1. Convert the markdown report into clean, well-formatted HTML
2. Create an appropriate subject line based on the report content
3. Use your send_email tool to send the formatted HTML email

The report will be provided to you when another agent hands off to you. Extract the report content 
and format it professionally as HTML before sending."""

email_agent = Agent(
    name="EmailAgentSMTP",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)

