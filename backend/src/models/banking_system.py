from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import json
from enum import Enum

db = SQLAlchemy()

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(20), nullable=False)  # business, user, escrow
    account_name = db.Column(db.String(100), nullable=False)
    
    # Bank details
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(50))  # Encrypted
    routing_number = db.Column(db.String(20))  # Encrypted
    swift_code = db.Column(db.String(20))
    iban = db.Column(db.String(50))
    
    # Account holder information
    account_holder_name = db.Column(db.String(100))
    account_holder_address = db.Column(db.Text)
    
    # Balance tracking
    current_balance = db.Column(db.Float, default=0.0)
    available_balance = db.Column(db.Float, default=0.0)  # Balance minus pending transactions
    reserved_balance = db.Column(db.Float, default=0.0)  # Reserved for pending payouts
    
    # Configuration
    currency = db.Column(db.String(3), default='USD')
    is_active = db.Column(db.Boolean, default=True)
    is_primary = db.Column(db.Boolean, default=False)
    
    # Security
    encryption_key_id = db.Column(db.String(50))  # Reference to encryption key
    last_balance_update = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserBankAccount(db.Model):
    __tablename__ = 'user_bank_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Bank account details
    account_holder_name = db.Column(db.String(100), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)  # Encrypted
    routing_number = db.Column(db.String(20), nullable=False)  # Encrypted
    account_type = db.Column(db.String(20), default='checking')  # checking, savings
    
    # International support
    swift_code = db.Column(db.String(20))
    iban = db.Column(db.String(50))
    country_code = db.Column(db.String(2))
    
    # Verification status
    verification_status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    verification_method = db.Column(db.String(20))  # micro_deposits, instant, manual
    verification_attempts = db.Column(db.Integer, default=0)
    
    # Micro deposit verification
    micro_deposit_1 = db.Column(db.Float)  # Encrypted
    micro_deposit_2 = db.Column(db.Float)  # Encrypted
    micro_deposit_sent_at = db.Column(db.DateTime)
    micro_deposit_verified_at = db.Column(db.DateTime)
    
    # Security and compliance
    is_active = db.Column(db.Boolean, default=True)
    is_primary = db.Column(db.Boolean, default=False)
    risk_score = db.Column(db.Float, default=0.0)  # 0-100 risk assessment
    
    # Metadata
    nickname = db.Column(db.String(50))  # User-defined nickname
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)

class PaymentProcessor(db.Model):
    __tablename__ = 'payment_processors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # stripe, paypal, venmo, wise, etc.
    processor_type = db.Column(db.String(20), nullable=False)  # bank_transfer, digital_wallet, crypto
    
    # API Configuration
    api_key = db.Column(db.String(255))  # Encrypted
    api_secret = db.Column(db.String(255))  # Encrypted
    webhook_secret = db.Column(db.String(255))  # Encrypted
    environment = db.Column(db.String(10), default='production')  # sandbox, production
    
    # Supported features
    supports_payouts = db.Column(db.Boolean, default=True)
    supports_instant_transfer = db.Column(db.Boolean, default=False)
    supports_international = db.Column(db.Boolean, default=False)
    
    # Fee structure
    payout_fee_fixed = db.Column(db.Float, default=0.0)  # Fixed fee per payout
    payout_fee_percentage = db.Column(db.Float, default=0.0)  # Percentage fee
    minimum_payout = db.Column(db.Float, default=1.0)
    maximum_payout = db.Column(db.Float, default=10000.0)
    
    # Processing times
    standard_processing_days = db.Column(db.Integer, default=3)
    instant_processing_fee = db.Column(db.Float, default=0.0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    last_health_check = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AutomatedPayoutSchedule(db.Model):
    __tablename__ = 'automated_payout_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Schedule configuration
    frequency = db.Column(db.String(20), nullable=False)  # weekly, monthly, quarterly
    day_of_week = db.Column(db.Integer)  # 0-6 for weekly (0=Monday)
    day_of_month = db.Column(db.Integer)  # 1-31 for monthly
    
    # Payout preferences
    minimum_amount = db.Column(db.Float, default=25.0)
    preferred_method = db.Column(db.String(20), default='bank_transfer')  # bank_transfer, paypal, venmo, crypto
    processor_id = db.Column(db.Integer, db.ForeignKey('payment_processors.id'))
    
    # Bank account or payment method details
    bank_account_id = db.Column(db.Integer, db.ForeignKey('user_bank_accounts.id'))
    paypal_email = db.Column(db.String(120))
    venmo_username = db.Column(db.String(50))
    crypto_address = db.Column(db.String(255))
    crypto_currency = db.Column(db.String(10))
    
    # Status and control
    is_active = db.Column(db.Boolean, default=True)
    auto_approve = db.Column(db.Boolean, default=False)  # Auto-approve payouts under certain conditions
    
    # Execution tracking
    last_execution = db.Column(db.DateTime)
    next_execution = db.Column(db.DateTime)
    total_payouts_made = db.Column(db.Integer, default=0)
    total_amount_paid = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BankTransaction(db.Model):
    __tablename__ = 'bank_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable=False)
    
    # Transaction details
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    external_transaction_id = db.Column(db.String(255))  # Bank's transaction ID
    
    # Transaction type and details
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, withdrawal, transfer, fee
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    
    # Parties involved
    from_account = db.Column(db.String(100))
    to_account = db.Column(db.String(100))
    counterparty_name = db.Column(db.String(100))
    
    # Description and categorization
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # user_payout, referral_bonus, subscription_revenue, etc.
    reference_id = db.Column(db.String(100))  # Reference to related record
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    
    # Fees and charges
    bank_fee = db.Column(db.Float, default=0.0)
    processor_fee = db.Column(db.Float, default=0.0)
    
    # Timestamps
    initiated_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Reconciliation
    reconciled = db.Column(db.Boolean, default=False)
    reconciled_at = db.Column(db.DateTime)

class PayoutBatch(db.Model):
    __tablename__ = 'payout_batches'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(50), unique=True, nullable=False)
    
    # Batch details
    batch_type = db.Column(db.String(20), default='scheduled')  # scheduled, manual, emergency
    processor_id = db.Column(db.Integer, db.ForeignKey('payment_processors.id'), nullable=False)
    
    # Batch statistics
    total_payouts = db.Column(db.Integer, default=0)
    total_amount = db.Column(db.Float, default=0.0)
    total_fees = db.Column(db.Float, default=0.0)
    
    # Status tracking
    status = db.Column(db.String(20), default='preparing')  # preparing, submitted, processing, completed, failed
    
    # Processing details
    submitted_to_processor_at = db.Column(db.DateTime)
    processor_batch_id = db.Column(db.String(100))
    
    # Results
    successful_payouts = db.Column(db.Integer, default=0)
    failed_payouts = db.Column(db.Integer, default=0)
    
    # Approval workflow
    requires_approval = db.Column(db.Boolean, default=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    approved_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class PayoutTransaction(db.Model):
    __tablename__ = 'payout_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('payout_batches.id'))
    
    # Transaction identifiers
    payout_id = db.Column(db.String(100), unique=True, nullable=False)
    external_payout_id = db.Column(db.String(255))  # Processor's payout ID
    
    # Payout details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    
    # Payment method
    payment_method = db.Column(db.String(20), nullable=False)  # bank_transfer, paypal, venmo, crypto
    processor_id = db.Column(db.Integer, db.ForeignKey('payment_processors.id'), nullable=False)
    
    # Destination details
    bank_account_id = db.Column(db.Integer, db.ForeignKey('user_bank_accounts.id'))
    paypal_email = db.Column(db.String(120))
    venmo_username = db.Column(db.String(50))
    crypto_address = db.Column(db.String(255))
    
    # Fees
    processor_fee = db.Column(db.Float, default=0.0)
    network_fee = db.Column(db.Float, default=0.0)  # For crypto
    final_amount = db.Column(db.Float, nullable=False)  # Amount after fees
    
    # Status and tracking
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed, cancelled
    failure_reason = db.Column(db.String(200))
    
    # Source of funds
    earnings_breakdown = db.Column(db.JSON)  # Breakdown of earnings being paid out
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

class FinancialLedger(db.Model):
    __tablename__ = 'financial_ledger'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Ledger entry details
    entry_type = db.Column(db.String(20), nullable=False)  # debit, credit
    account_type = db.Column(db.String(50), nullable=False)  # revenue, expense, liability, asset
    category = db.Column(db.String(50), nullable=False)  # subscription_revenue, referral_expense, etc.
    
    # Transaction details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    description = db.Column(db.Text, nullable=False)
    
    # References
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reference_type = db.Column(db.String(50))  # subscription, referral, payout, etc.
    reference_id = db.Column(db.String(100))
    transaction_id = db.Column(db.String(100))
    
    # Accounting period
    accounting_date = db.Column(db.Date, nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)
    
    # Status
    is_reconciled = db.Column(db.Boolean, default=False)
    reconciled_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ComplianceReport(db.Model):
    __tablename__ = 'compliance_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Report details
    report_type = db.Column(db.String(50), nullable=False)  # tax_1099, annual_summary, quarterly_report
    reporting_period_start = db.Column(db.Date, nullable=False)
    reporting_period_end = db.Column(db.Date, nullable=False)
    
    # Report data
    total_payments_made = db.Column(db.Float, default=0.0)
    total_users_paid = db.Column(db.Integer, default=0)
    report_data = db.Column(db.JSON)  # Detailed report data
    
    # File storage
    report_file_path = db.Column(db.String(500))  # Path to generated report file
    
    # Status
    status = db.Column(db.String(20), default='generating')  # generating, completed, failed
    
    # Generation details
    generated_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

# Utility functions for banking system

def initialize_payment_processors():
    """Initialize payment processors"""
    processors = [
        {
            'name': 'stripe',
            'processor_type': 'bank_transfer',
            'supports_payouts': True,
            'supports_instant_transfer': True,
            'supports_international': True,
            'payout_fee_percentage': 0.25,
            'minimum_payout': 1.0,
            'standard_processing_days': 2
        },
        {
            'name': 'paypal',
            'processor_type': 'digital_wallet',
            'supports_payouts': True,
            'supports_instant_transfer': True,
            'supports_international': True,
            'payout_fee_fixed': 0.25,
            'minimum_payout': 1.0,
            'standard_processing_days': 1
        },
        {
            'name': 'venmo',
            'processor_type': 'digital_wallet',
            'supports_payouts': True,
            'supports_instant_transfer': True,
            'supports_international': False,
            'payout_fee_percentage': 1.75,
            'minimum_payout': 1.0,
            'standard_processing_days': 1
        },
        {
            'name': 'wise',
            'processor_type': 'bank_transfer',
            'supports_payouts': True,
            'supports_instant_transfer': False,
            'supports_international': True,
            'payout_fee_percentage': 0.5,
            'minimum_payout': 1.0,
            'standard_processing_days': 1
        }
    ]
    
    for processor_data in processors:
        existing_processor = PaymentProcessor.query.filter_by(name=processor_data['name']).first()
        if not existing_processor:
            processor = PaymentProcessor(**processor_data)
            db.session.add(processor)
    
    db.session.commit()

def create_business_bank_account():
    """Create the main business bank account"""
    existing_account = BankAccount.query.filter_by(account_type='business', is_primary=True).first()
    if not existing_account:
        business_account = BankAccount(
            account_type='business',
            account_name='Inner Bloom Business Account',
            bank_name='Chase Business Banking',
            account_holder_name='Inner Bloom LLC',
            current_balance=0.0,
            available_balance=0.0,
            is_primary=True,
            currency='USD'
        )
        db.session.add(business_account)
        db.session.commit()
        return business_account
    return existing_account

def calculate_user_available_earnings(user_id):
    """Calculate user's available earnings for payout"""
    from src.models.affiliate_tracking import UserEarnings
    
    user_earnings = UserEarnings.query.filter_by(user_id=user_id).first()
    if not user_earnings:
        return 0.0
    
    # Available earnings = pending payout (already calculated with refund period checks)
    return user_earnings.pending_payout

def create_automated_payout_schedule(user_id, frequency, payment_method, **kwargs):
    """Create automated payout schedule for user"""
    # Check if user already has a schedule
    existing_schedule = AutomatedPayoutSchedule.query.filter_by(user_id=user_id, is_active=True).first()
    if existing_schedule:
        # Update existing schedule
        existing_schedule.frequency = frequency
        existing_schedule.preferred_method = payment_method
        
        # Update payment method details
        if payment_method == 'bank_transfer':
            existing_schedule.bank_account_id = kwargs.get('bank_account_id')
        elif payment_method == 'paypal':
            existing_schedule.paypal_email = kwargs.get('paypal_email')
        elif payment_method == 'venmo':
            existing_schedule.venmo_username = kwargs.get('venmo_username')
        elif payment_method == 'crypto':
            existing_schedule.crypto_address = kwargs.get('crypto_address')
            existing_schedule.crypto_currency = kwargs.get('crypto_currency')
        
        # Calculate next execution
        existing_schedule.next_execution = calculate_next_execution_date(frequency, kwargs.get('day_of_week'), kwargs.get('day_of_month'))
        
        db.session.commit()
        return existing_schedule
    
    # Create new schedule
    schedule = AutomatedPayoutSchedule(
        user_id=user_id,
        frequency=frequency,
        preferred_method=payment_method,
        day_of_week=kwargs.get('day_of_week'),
        day_of_month=kwargs.get('day_of_month'),
        minimum_amount=kwargs.get('minimum_amount', 25.0),
        bank_account_id=kwargs.get('bank_account_id'),
        paypal_email=kwargs.get('paypal_email'),
        venmo_username=kwargs.get('venmo_username'),
        crypto_address=kwargs.get('crypto_address'),
        crypto_currency=kwargs.get('crypto_currency')
    )
    
    # Calculate next execution
    schedule.next_execution = calculate_next_execution_date(frequency, kwargs.get('day_of_week'), kwargs.get('day_of_month'))
    
    db.session.add(schedule)
    db.session.commit()
    
    return schedule

def calculate_next_execution_date(frequency, day_of_week=None, day_of_month=None):
    """Calculate next execution date for payout schedule"""
    now = datetime.utcnow()
    
    if frequency == 'weekly':
        # Find next occurrence of the specified day of week
        days_ahead = day_of_week - now.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return now + timedelta(days=days_ahead)
    
    elif frequency == 'monthly':
        # Find next occurrence of the specified day of month
        if day_of_month > now.day:
            # This month
            return now.replace(day=day_of_month, hour=12, minute=0, second=0, microsecond=0)
        else:
            # Next month
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=day_of_month, hour=12, minute=0, second=0, microsecond=0)
            else:
                next_month = now.replace(month=now.month + 1, day=day_of_month, hour=12, minute=0, second=0, microsecond=0)
            return next_month
    
    elif frequency == 'quarterly':
        # Next quarter, same day of month
        current_quarter = (now.month - 1) // 3 + 1
        next_quarter_month = current_quarter * 3 + 1
        if next_quarter_month > 12:
            next_quarter_month = 1
            year = now.year + 1
        else:
            year = now.year
        
        return datetime(year, next_quarter_month, day_of_month or 1, 12, 0, 0)
    
    # Default to weekly if frequency not recognized
    return now + timedelta(days=7)

def process_scheduled_payouts():
    """Process all scheduled payouts that are due"""
    now = datetime.utcnow()
    
    # Get all schedules that are due for execution
    due_schedules = AutomatedPayoutSchedule.query.filter(
        AutomatedPayoutSchedule.is_active == True,
        AutomatedPayoutSchedule.next_execution <= now
    ).all()
    
    processed_count = 0
    
    for schedule in due_schedules:
        try:
            # Check if user has sufficient earnings
            available_earnings = calculate_user_available_earnings(schedule.user_id)
            
            if available_earnings >= schedule.minimum_amount:
                # Create payout transaction
                payout = create_payout_transaction(
                    user_id=schedule.user_id,
                    amount=available_earnings,
                    payment_method=schedule.preferred_method,
                    schedule_id=schedule.id
                )
                
                if payout:
                    processed_count += 1
                    
                    # Update schedule
                    schedule.last_execution = now
                    schedule.next_execution = calculate_next_execution_date(
                        schedule.frequency,
                        schedule.day_of_week,
                        schedule.day_of_month
                    )
                    schedule.total_payouts_made += 1
                    schedule.total_amount_paid += available_earnings
        
        except Exception as e:
            # Log error but continue processing other schedules
            print(f"Error processing payout for user {schedule.user_id}: {str(e)}")
            continue
    
    db.session.commit()
    return processed_count

def create_payout_transaction(user_id, amount, payment_method, schedule_id=None):
    """Create a payout transaction"""
    # Generate unique payout ID
    payout_id = f"PO_{secrets.token_hex(8).upper()}"
    
    # Get appropriate processor
    processor = PaymentProcessor.query.filter_by(
        processor_type='bank_transfer' if payment_method == 'bank_transfer' else 'digital_wallet',
        is_active=True
    ).first()
    
    if not processor:
        raise ValueError(f"No active processor found for payment method: {payment_method}")
    
    # Calculate fees
    processor_fee = calculate_payout_fee(processor, amount)
    final_amount = amount - processor_fee
    
    # Create payout transaction
    payout = PayoutTransaction(
        user_id=user_id,
        payout_id=payout_id,
        amount=amount,
        payment_method=payment_method,
        processor_id=processor.id,
        processor_fee=processor_fee,
        final_amount=final_amount,
        status='pending'
    )
    
    # Set payment method specific details based on user's schedule
    if schedule_id:
        schedule = AutomatedPayoutSchedule.query.get(schedule_id)
        if schedule:
            payout.bank_account_id = schedule.bank_account_id
            payout.paypal_email = schedule.paypal_email
            payout.venmo_username = schedule.venmo_username
            payout.crypto_address = schedule.crypto_address
    
    db.session.add(payout)
    
    # Create ledger entry
    create_ledger_entry(
        entry_type='debit',
        account_type='liability',
        category='user_payout',
        amount=amount,
        description=f'Payout to user {user_id}',
        user_id=user_id,
        reference_type='payout',
        reference_id=payout_id
    )
    
    db.session.commit()
    return payout

def calculate_payout_fee(processor, amount):
    """Calculate payout fee for a processor"""
    fee = processor.payout_fee_fixed + (amount * processor.payout_fee_percentage / 100)
    return round(fee, 2)

def create_ledger_entry(entry_type, account_type, category, amount, description, user_id=None, reference_type=None, reference_id=None):
    """Create a financial ledger entry"""
    now = datetime.utcnow()
    
    ledger_entry = FinancialLedger(
        entry_type=entry_type,
        account_type=account_type,
        category=category,
        amount=amount,
        description=description,
        user_id=user_id,
        reference_type=reference_type,
        reference_id=reference_id,
        accounting_date=now.date(),
        fiscal_year=now.year,
        fiscal_quarter=(now.month - 1) // 3 + 1
    )
    
    db.session.add(ledger_entry)
    return ledger_entry

def reconcile_bank_account(bank_account_id):
    """Reconcile bank account with ledger entries"""
    bank_account = BankAccount.query.get(bank_account_id)
    if not bank_account:
        return False
    
    # Get all unreconciled transactions
    unreconciled_transactions = BankTransaction.query.filter_by(
        bank_account_id=bank_account_id,
        reconciled=False
    ).all()
    
    reconciled_count = 0
    
    for transaction in unreconciled_transactions:
        # Find matching ledger entry
        ledger_entry = FinancialLedger.query.filter_by(
            transaction_id=transaction.transaction_id,
            is_reconciled=False
        ).first()
        
        if ledger_entry:
            # Mark both as reconciled
            transaction.reconciled = True
            transaction.reconciled_at = datetime.utcnow()
            
            ledger_entry.is_reconciled = True
            ledger_entry.reconciled_at = datetime.utcnow()
            
            reconciled_count += 1
    
    # Update bank account balance
    total_credits = db.session.query(db.func.sum(BankTransaction.amount)).filter_by(
        bank_account_id=bank_account_id,
        transaction_type='deposit'
    ).scalar() or 0.0
    
    total_debits = db.session.query(db.func.sum(BankTransaction.amount)).filter_by(
        bank_account_id=bank_account_id,
        transaction_type='withdrawal'
    ).scalar() or 0.0
    
    bank_account.current_balance = total_credits - total_debits
    bank_account.last_balance_update = datetime.utcnow()
    
    db.session.commit()
    return reconciled_count

def generate_compliance_report(report_type, start_date, end_date):
    """Generate compliance report"""
    # Get all payouts in the period
    payouts = PayoutTransaction.query.filter(
        PayoutTransaction.created_at >= start_date,
        PayoutTransaction.created_at <= end_date,
        PayoutTransaction.status == 'completed'
    ).all()
    
    # Calculate totals
    total_payments = sum(payout.amount for payout in payouts)
    total_users = len(set(payout.user_id for payout in payouts))
    
    # Generate detailed report data
    report_data = {
        'summary': {
            'total_payments_made': total_payments,
            'total_users_paid': total_users,
            'total_transactions': len(payouts),
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat()
        },
        'by_payment_method': {},
        'by_user': []
    }
    
    # Group by payment method
    for payout in payouts:
        method = payout.payment_method
        if method not in report_data['by_payment_method']:
            report_data['by_payment_method'][method] = {
                'count': 0,
                'total_amount': 0.0
            }
        
        report_data['by_payment_method'][method]['count'] += 1
        report_data['by_payment_method'][method]['total_amount'] += payout.amount
    
    # Group by user (for tax reporting)
    user_totals = {}
    for payout in payouts:
        if payout.user_id not in user_totals:
            user_totals[payout.user_id] = 0.0
        user_totals[payout.user_id] += payout.amount
    
    # Only include users who received $600+ (1099 threshold)
    for user_id, total_amount in user_totals.items():
        if total_amount >= 600.0:
            from src.models.user import User
            user = User.query.get(user_id)
            report_data['by_user'].append({
                'user_id': user_id,
                'username': user.username if user else 'Unknown',
                'email': user.email if user else 'Unknown',
                'total_amount': total_amount
            })
    
    # Create compliance report record
    compliance_report = ComplianceReport(
        report_type=report_type,
        reporting_period_start=start_date,
        reporting_period_end=end_date,
        total_payments_made=total_payments,
        total_users_paid=total_users,
        report_data=report_data,
        status='completed'
    )
    
    db.session.add(compliance_report)
    db.session.commit()
    
    return compliance_report

def get_financial_summary(start_date=None, end_date=None):
    """Get financial summary for a period"""
    if not start_date:
        start_date = datetime.utcnow().replace(day=1)  # Start of current month
    if not end_date:
        end_date = datetime.utcnow()
    
    # Revenue
    revenue_entries = FinancialLedger.query.filter(
        FinancialLedger.account_type == 'revenue',
        FinancialLedger.accounting_date >= start_date.date(),
        FinancialLedger.accounting_date <= end_date.date()
    ).all()
    
    total_revenue = sum(entry.amount for entry in revenue_entries)
    
    # Expenses
    expense_entries = FinancialLedger.query.filter(
        FinancialLedger.account_type == 'expense',
        FinancialLedger.accounting_date >= start_date.date(),
        FinancialLedger.accounting_date <= end_date.date()
    ).all()
    
    total_expenses = sum(entry.amount for entry in expense_entries)
    
    # Payouts (liabilities)
    payout_entries = FinancialLedger.query.filter(
        FinancialLedger.category == 'user_payout',
        FinancialLedger.accounting_date >= start_date.date(),
        FinancialLedger.accounting_date <= end_date.date()
    ).all()
    
    total_payouts = sum(entry.amount for entry in payout_entries)
    
    return {
        'period_start': start_date.isoformat(),
        'period_end': end_date.isoformat(),
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'total_payouts': total_payouts,
        'net_income': total_revenue - total_expenses - total_payouts,
        'payout_ratio': (total_payouts / total_revenue * 100) if total_revenue > 0 else 0
    }

