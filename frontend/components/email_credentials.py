from typing import Optional

from frontend.ui.factory import UIFactory
from frontend.ui.interfaces.base import InputInterface
from frontend.ui.interfaces.state import StateInterface
from frontend.ui.interfaces.markup import MarkupInterface

def generate_gmail_app_password_help():
    """
    Help section for generating an app password for Gmail.
    """
    help_text = """
    ## How to Generate an App Password for Gmail

    If you want to send emails from your application using a Gmail account, you need to generate an app password. This is especially important if you have two-factor authentication (2FA) enabled on your Google account. Here's how to do it:

    ### Steps to Generate an App Password:

    1. **Sign in to your Google Account**:
       - Go to [Google Account](https://myaccount.google.com/).
       - Sign in with your Gmail credentials.

    2. **Navigate to Security Settings**:
       - In the left navigation panel, click on **Security**.

    3. **Enable Two-Step Verification**:
       - If you haven't already enabled 2FA, you will need to do so. 
       - Under the "Signing in to Google" section, click on **2-Step Verification** and follow the prompts to set it up.

    4. **Generate App Password**:
       - Once 2FA is enabled, go back to the **Security** section.
       - Under the "Signing in to Google" section, you will see **App passwords**. Click on it.
       - You may need to sign in again.
       - In the "Select app" dropdown, choose **Other (Custom name)** and enter a name for your app (e.g., "My Email App").
       - Click **Generate**.

    5. **Copy the App Password**:
       - A 16-character password will be generated. Copy this password as you will need it to configure your email settings in your application.

    6. **Use the App Password in Your Application**:
       - When configuring your email settings in your application, use the app password instead of your regular Gmail password.

    ### Important Notes:
    - App passwords are specific to the application you created them for. If you ever change your password or remove the app, you will need to generate a new app password.
    - Keep your app password secure and do not share it with anyone.

    If you have any questions or need further assistance, feel free to ask!
    """
    return help_text

def render_email_credentials(
    ui: Optional[InputInterface] = None,
    state: Optional[StateInterface] = None,
    markup: Optional[MarkupInterface] = None
):
    """Render the email credentials input section."""
    ui = ui or UIFactory.create_ui()
    state = state or UIFactory.create_state()
    markup = markup or UIFactory.create_markup()

    # Initialize session state for email credentials
    state.init_default("email", "")
    state.init_default("password", "")

    markup.markdown("### Email Credentials")
    email = ui.text_input("Enter your email address:", value=state.get("email"))
    # Add help text for password input
    password = ui.text_input(
        "Enter your email password:", 
        type="password", 
        value=state.get("password"),
        help=generate_gmail_app_password_help()
    )

    # Store credentials in session state
    state.set("email", email)
    state.set("password", password) 