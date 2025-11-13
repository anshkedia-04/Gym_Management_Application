import pandas as pd
import os
from datetime import datetime, timedelta

class GymDatabase:
    def __init__(self, filename='gym_members.xlsx'):
        self.filename = filename
        self.initialize_database()
    
    def initialize_database(self):
        """Create Excel file if it doesn't exist"""
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=[
                'Member ID', 'Name', 'Phone', 'Email', 
                'Joining Date', 'Membership End Date', 
                'Amount Paid', 'Payment Mode', 'Status'
            ])
            df.to_excel(self.filename, index=False)
    
    def generate_member_id(self):
        """Generate unique member ID"""
        df = self.get_all_members()
        if df.empty:
            return 'GYM001'
        
        last_id = df['Member ID'].max()
        num = int(last_id[3:]) + 1
        return f'GYM{num:03d}'
    
    def add_member(self, name, phone, email, joining_date, end_date, amount, payment_mode):
        """Add a new member to the database"""
        df = pd.read_excel(self.filename)
        
        member_id = self.generate_member_id()
        
        # Determine status
        status = 'Active' if datetime.strptime(end_date, '%Y-%m-%d').date() >= datetime.now().date() else 'Expired'
        
        new_member = {
            'Member ID': member_id,
            'Name': name,
            'Phone': phone,
            'Email': email,
            'Joining Date': joining_date,
            'Membership End Date': end_date,
            'Amount Paid': amount,
            'Payment Mode': payment_mode,
            'Status': status
        }
        
        df = pd.concat([df, pd.DataFrame([new_member])], ignore_index=True)
        df.to_excel(self.filename, index=False)
        
        return member_id
    
    def get_all_members(self):
        """Get all members from database"""
        try:
            df = pd.read_excel(self.filename)
            return df
        except:
            return pd.DataFrame()
    
    def update_member(self, member_id, name, phone, email, joining_date, end_date, amount, payment_mode):
        """Update existing member details"""
        df = pd.read_excel(self.filename)
        
        # Determine status
        status = 'Active' if datetime.strptime(end_date, '%Y-%m-%d').date() >= datetime.now().date() else 'Expired'
        
        df.loc[df['Member ID'] == member_id, ['Name', 'Phone', 'Email', 'Joining Date', 
                                                'Membership End Date', 'Amount Paid', 
                                                'Payment Mode', 'Status']] = [
            name, phone, email, joining_date, end_date, amount, payment_mode, status
        ]
        
        df.to_excel(self.filename, index=False)
    
    def delete_member(self, member_id):
        """Delete a member from database"""
        df = pd.read_excel(self.filename)
        df = df[df['Member ID'] != member_id]
        df.to_excel(self.filename, index=False)
    
    def get_active_members_count(self):
        """Get count of active members"""
        df = self.get_all_members()
        if df.empty:
            return 0
        
        df['Membership End Date'] = pd.to_datetime(df['Membership End Date'])
        active_count = len(df[df['Membership End Date'] >= datetime.now()])
        return active_count
    
    def get_expiring_members(self, days=7):
        """Get members whose membership is expiring in next N days"""
        df = self.get_all_members()
        if df.empty:
            return pd.DataFrame()
        
        df['Membership End Date'] = pd.to_datetime(df['Membership End Date'])
        
        today = datetime.now()
        future_date = today + timedelta(days=days)
        
        expiring_df = df[
            (df['Membership End Date'] >= today) & 
            (df['Membership End Date'] <= future_date)
        ]
        
        return expiring_df
    
    def update_all_statuses(self):
        """Update status of all members based on membership end date"""
        df = pd.read_excel(self.filename)
        if df.empty:
            return
        
        df['Membership End Date'] = pd.to_datetime(df['Membership End Date'])
        today = datetime.now()
        
        df['Status'] = df['Membership End Date'].apply(
            lambda x: 'Active' if x >= today else 'Expired'
        )
        
        df.to_excel(self.filename, index=False)