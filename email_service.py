import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587, sender_email='', sender_password=''):
        """
        Initialize email service
        
        For Gmail:
        - smtp_server: 'smtp.gmail.com'
        - smtp_port: 587
        - Use App Password (not regular password) if 2FA is enabled
        
        To generate App Password for Gmail:
        1. Go to Google Account settings
        2. Security > 2-Step Verification
        3. App passwords > Generate
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = "anshkedia.04@gmail.com"
        self.sender_password = sender_password
    
    def send_renewal_reminder(self, member_name, member_email, end_date):
        """Send membership renewal reminder email"""
        
        if not self.sender_email or not self.sender_password:
            return False, "Email credentials not configured"
        
        subject = "⚠️ Gym Membership Renewal Reminder"
        
        # Format the end date
        formatted_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B %d, %Y')
        
        body = f"""
Dear {member_name},

This is a friendly reminder that your gym membership is expiring soon.

Membership End Date: {formatted_date}

We hope you've enjoyed your fitness journey with us! To continue your workout routine without interruption, please renew your membership before the expiration date.

Benefits of Renewing:
✓ Uninterrupted access to all gym facilities
✓ Continue your fitness progress
✓ Access to all classes and training sessions
✓ Maintain your workout community

To renew your membership, please contact us at the gym or reply to this email with your renewal plans.

We look forward to continuing your fitness journey together!

Best regards,
Gym Management Team

---
This is an automated reminder. Please do not reply to this email if you have already renewed your membership.
        """
        
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = member_email
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'plain'))
            
            # Connect to server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True, "Email sent successfully"
        
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def send_bulk_renewal_reminders(self, members_df):
        """Send renewal reminders to multiple members"""
        results = []
        
        for _, member in members_df.iterrows():
            success, message = self.send_renewal_reminder(
                member['Name'],
                member['Email'],
                member['Membership End Date'].strftime('%Y-%m-%d')
            )
            
            results.append({
                'Member': member['Name'],
                'Email': member['Email'],
                'Status': 'Sent' if success else 'Failed',
                'Message': message
            })
        
        return results