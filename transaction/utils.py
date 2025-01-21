from django.db.models import Q
import random
from datetime import date, timedelta, datetime
import csv
from io import StringIO, BytesIO
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from .models import Card, Transaction
from bankaccount.models import BankAccount, Notifications


def generate_otp():
    return random.randint(100000, 999999)

def generate_otp_expiry():
    return datetime.now() + timedelta(minutes=5)  # OTP valid for 5 minutes


def generate_card_number():
    remaining_digits = ''.join(random.choice('0123456789') for _ in range(12))
    card_number = '4444' + remaining_digits
    return card_number

def card_expiry_date():
    today = date.today()
    expiry_date = today + timedelta(days=5*365)
    return expiry_date

def get_transactions_total(user):
    try:
        bank_account = BankAccount.objects.get(user=user)
        
        # Fetch transactions where the user's bank account is either sender or receiver
        transactions = Transaction.objects.filter(Q(from_acc=bank_account) | Q(to_acc=bank_account))
        
        credit_total = 0
        debit_total = 0
        
        for trx in transactions:
            if trx.from_acc == bank_account:
                # Transaction is a debit from the user's bank account
                debit_total += trx.amount
            elif trx.to_acc == bank_account:
                # Transaction is a credit to the user's bank account
                credit_total += trx.amount
        
        return credit_total, debit_total
    
    except BankAccount.DoesNotExist:
        # Handle case where the user's bank account does not exist
        return 0, 0
    except Exception as e:
        # Handle other exceptions gracefully
        print(f"An error occurred: {str(e)}")
        return 0, 0
    

def create_notification(user, content):
    notification = Notifications(user=user, content=content)
    notification.save()


def export_transactions_to_csv(transactions):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Transaction ID', 'Description', 'From Account', 'To Account', 'Amount', 'Status'])
    
    for transaction in transactions:
        writer.writerow([
            transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            transaction.transaction_id,
            getattr(transaction, 'description', ''),
            transaction.from_acc.account_number if transaction.from_acc else 'N/A',
            transaction.to_acc.account_number if transaction.to_acc else 'N/A',
            f"${transaction.amount:,.2f}",
            getattr(transaction, 'status', 'Completed')
        ])
    
    return output.getvalue()

def export_transactions_to_pdf(transactions, user):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    elements.append(Paragraph("Transaction History", title_style))
    elements.append(Spacer(1, 12))
    
    # Add user info
    elements.append(Paragraph(f"Account Holder: {user.get_full_name()}", styles['Normal']))
    elements.append(Paragraph(f"Generated Date: {timezone.now().strftime('%Y-%m-d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Create table data
    data = [['Date', 'Transaction ID', 'Description', 'From Account', 'To Account', 'Amount', 'Status']]
    
    for trx in transactions:
        data.append([
            trx.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            trx.transaction_id,
            trx.description if hasattr(trx, 'description') else '',
            trx.from_acc.account_number if trx.from_acc else 'N/A',
            trx.to_acc.account_number if trx.to_acc else 'N/A',
            f"${trx.amount:,.2f}",
            trx.status if hasattr(trx, 'status') else 'Completed'
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (-2, 0), (-2, -1), 'RIGHT'),
    ]))
    
    elements.append(table)
    
    # Add footer
    elements.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey
    )
    elements.append(Paragraph("This is a computer-generated document. No signature is required.", footer_style))
    elements.append(Paragraph("For any queries, please contact our customer support.", footer_style))
    
    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def format_currency(amount):
    return f"${amount:,.2f}"
