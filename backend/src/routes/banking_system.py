from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.banking_system import (
    BankAccount, UserBankAccount, PaymentProcessor, AutomatedPayoutSchedule,
    BankTransaction, PayoutBatch, PayoutTransaction, FinancialLedger, ComplianceReport,
    initialize_payment_processors, create_business_bank_account,
    calculate_user_available_earnings, create_automated_payout_schedule,
    process_scheduled_payouts, create_payout_transaction, reconcile_bank_account,
    generate_compliance_report, get_financial_summary, db
)
from src.models.user import User
from datetime import datetime, timedelta
import json

banking_system_bp = Blueprint('banking_system', __name__)

# Initialize payment processors on first load
# Note: Initialization moved to main app startup
def setup_banking_system():
    """Initialize banking system"""
    initialize_payment_processors()
    create_business_bank_account()

# Bank Account Management Routes
@banking_system_bp.route('/banking/user-accounts/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_bank_accounts(user_id):
    """Get user's bank accounts"""
    try:
        bank_accounts = UserBankAccount.query.filter_by(user_id=user_id, is_active=True).all()
        
        accounts_data = [
            {
                'id': account.id,
                'account_holder_name': account.account_holder_name,
                'bank_name': account.bank_name,
                'account_type': account.account_type,
                'verification_status': account.verification_status,
                'is_primary': account.is_primary,
                'nickname': account.nickname,
                'country_code': account.country_code,
                'created_at': account.created_at.isoformat(),
                'verified_at': account.verified_at.isoformat() if account.verified_at else None
            }
            for account in bank_accounts
        ]
        
        return jsonify({
            'bank_accounts': accounts_data,
            'total_count': len(accounts_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/user-accounts', methods=['POST'])
@cross_origin()
def add_user_bank_account():
    """Add a bank account for user"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'account_holder_name', 'bank_name', 'account_number', 'routing_number']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if this is the user's first bank account
        existing_accounts = UserBankAccount.query.filter_by(user_id=data['user_id'], is_active=True).count()
        is_primary = existing_accounts == 0
        
        bank_account = UserBankAccount(
            user_id=data['user_id'],
            account_holder_name=data['account_holder_name'],
            bank_name=data['bank_name'],
            account_number=data['account_number'],  # In production, encrypt this
            routing_number=data['routing_number'],  # In production, encrypt this
            account_type=data.get('account_type', 'checking'),
            swift_code=data.get('swift_code'),
            iban=data.get('iban'),
            country_code=data.get('country_code', 'US'),
            nickname=data.get('nickname', f"{data['bank_name']} Account"),
            is_primary=is_primary
        )
        
        db.session.add(bank_account)
        db.session.commit()
        
        return jsonify({
            'bank_account_id': bank_account.id,
            'verification_status': bank_account.verification_status,
            'message': 'Bank account added successfully. Verification required.'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/user-accounts/<int:account_id>/verify', methods=['POST'])
@cross_origin()
def verify_bank_account(account_id):
    """Verify bank account with micro deposits"""
    try:
        data = request.get_json()
        
        bank_account = UserBankAccount.query.get_or_404(account_id)
        
        if bank_account.verification_status == 'verified':
            return jsonify({'message': 'Account already verified'}), 200
        
        # For demo purposes, accept any two amounts between 0.01 and 0.99
        deposit_1 = data.get('deposit_1', 0.0)
        deposit_2 = data.get('deposit_2', 0.0)
        
        if 0.01 <= deposit_1 <= 0.99 and 0.01 <= deposit_2 <= 0.99:
            bank_account.verification_status = 'verified'
            bank_account.verified_at = datetime.utcnow()
            bank_account.micro_deposit_verified_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'message': 'Bank account verified successfully',
                'verification_status': 'verified'
            }), 200
        else:
            bank_account.verification_attempts += 1
            
            if bank_account.verification_attempts >= 3:
                bank_account.verification_status = 'rejected'
            
            db.session.commit()
            
            return jsonify({
                'error': 'Incorrect deposit amounts',
                'attempts_remaining': max(0, 3 - bank_account.verification_attempts)
            }), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payment Processor Routes
@banking_system_bp.route('/banking/processors', methods=['GET'])
@cross_origin()
def get_payment_processors():
    """Get available payment processors"""
    try:
        processors = PaymentProcessor.query.filter_by(is_active=True).all()
        
        processors_data = [
            {
                'id': processor.id,
                'name': processor.name,
                'processor_type': processor.processor_type,
                'supports_payouts': processor.supports_payouts,
                'supports_instant_transfer': processor.supports_instant_transfer,
                'supports_international': processor.supports_international,
                'payout_fee_fixed': processor.payout_fee_fixed,
                'payout_fee_percentage': processor.payout_fee_percentage,
                'minimum_payout': processor.minimum_payout,
                'maximum_payout': processor.maximum_payout,
                'standard_processing_days': processor.standard_processing_days
            }
            for processor in processors
        ]
        
        return jsonify({
            'processors': processors_data,
            'total_count': len(processors_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Automated Payout Schedule Routes
@banking_system_bp.route('/banking/payout-schedule/<int:user_id>', methods=['GET'])
@cross_origin()
def get_payout_schedule(user_id):
    """Get user's payout schedule"""
    try:
        schedule = AutomatedPayoutSchedule.query.filter_by(user_id=user_id, is_active=True).first()
        
        if not schedule:
            return jsonify({'schedule': None}), 200
        
        schedule_data = {
            'id': schedule.id,
            'frequency': schedule.frequency,
            'day_of_week': schedule.day_of_week,
            'day_of_month': schedule.day_of_month,
            'minimum_amount': schedule.minimum_amount,
            'preferred_method': schedule.preferred_method,
            'bank_account_id': schedule.bank_account_id,
            'paypal_email': schedule.paypal_email,
            'venmo_username': schedule.venmo_username,
            'crypto_address': schedule.crypto_address,
            'crypto_currency': schedule.crypto_currency,
            'auto_approve': schedule.auto_approve,
            'last_execution': schedule.last_execution.isoformat() if schedule.last_execution else None,
            'next_execution': schedule.next_execution.isoformat() if schedule.next_execution else None,
            'total_payouts_made': schedule.total_payouts_made,
            'total_amount_paid': schedule.total_amount_paid
        }
        
        return jsonify({'schedule': schedule_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/payout-schedule', methods=['POST'])
@cross_origin()
def create_payout_schedule():
    """Create or update automated payout schedule"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'frequency', 'preferred_method']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate frequency-specific fields
        if data['frequency'] == 'weekly' and 'day_of_week' not in data:
            return jsonify({'error': 'day_of_week required for weekly frequency'}), 400
        
        if data['frequency'] in ['monthly', 'quarterly'] and 'day_of_month' not in data:
            return jsonify({'error': 'day_of_month required for monthly/quarterly frequency'}), 400
        
        # Validate payment method specific fields
        payment_method = data['preferred_method']
        if payment_method == 'bank_transfer' and 'bank_account_id' not in data:
            return jsonify({'error': 'bank_account_id required for bank transfer'}), 400
        elif payment_method == 'paypal' and 'paypal_email' not in data:
            return jsonify({'error': 'paypal_email required for PayPal'}), 400
        elif payment_method == 'venmo' and 'venmo_username' not in data:
            return jsonify({'error': 'venmo_username required for Venmo'}), 400
        elif payment_method == 'crypto' and ('crypto_address' not in data or 'crypto_currency' not in data):
            return jsonify({'error': 'crypto_address and crypto_currency required for crypto'}), 400
        
        schedule = create_automated_payout_schedule(
            user_id=data['user_id'],
            frequency=data['frequency'],
            payment_method=payment_method,
            day_of_week=data.get('day_of_week'),
            day_of_month=data.get('day_of_month'),
            minimum_amount=data.get('minimum_amount', 25.0),
            bank_account_id=data.get('bank_account_id'),
            paypal_email=data.get('paypal_email'),
            venmo_username=data.get('venmo_username'),
            crypto_address=data.get('crypto_address'),
            crypto_currency=data.get('crypto_currency')
        )
        
        return jsonify({
            'schedule_id': schedule.id,
            'next_execution': schedule.next_execution.isoformat(),
            'message': 'Payout schedule created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payout Transaction Routes
@banking_system_bp.route('/banking/payouts', methods=['GET'])
@cross_origin()
def get_payout_transactions():
    """Get payout transactions"""
    try:
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')
        limit = request.args.get('limit', 50, type=int)
        
        query = PayoutTransaction.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        
        payouts = query.order_by(PayoutTransaction.created_at.desc()).limit(limit).all()
        
        payouts_data = [
            {
                'id': payout.id,
                'payout_id': payout.payout_id,
                'user_id': payout.user_id,
                'amount': payout.amount,
                'final_amount': payout.final_amount,
                'currency': payout.currency,
                'payment_method': payout.payment_method,
                'processor_fee': payout.processor_fee,
                'status': payout.status,
                'failure_reason': payout.failure_reason,
                'created_at': payout.created_at.isoformat(),
                'processed_at': payout.processed_at.isoformat() if payout.processed_at else None,
                'completed_at': payout.completed_at.isoformat() if payout.completed_at else None
            }
            for payout in payouts
        ]
        
        return jsonify({
            'payouts': payouts_data,
            'total_count': len(payouts_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/payouts/manual', methods=['POST'])
@cross_origin()
def create_manual_payout():
    """Create a manual payout"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'amount', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate minimum amount
        if data['amount'] < 1.0:
            return jsonify({'error': 'Minimum payout amount is $1.00'}), 400
        
        # Check user's available earnings
        available_earnings = calculate_user_available_earnings(data['user_id'])
        if data['amount'] > available_earnings:
            return jsonify({
                'error': f'Insufficient earnings. Available: ${available_earnings:.2f}'
            }), 400
        
        payout = create_payout_transaction(
            user_id=data['user_id'],
            amount=data['amount'],
            payment_method=data['payment_method']
        )
        
        return jsonify({
            'payout_id': payout.payout_id,
            'amount': payout.amount,
            'final_amount': payout.final_amount,
            'processor_fee': payout.processor_fee,
            'status': payout.status,
            'message': 'Manual payout created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/earnings/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_earnings_summary(user_id):
    """Get user's earnings summary"""
    try:
        available_earnings = calculate_user_available_earnings(user_id)
        
        # Get recent payouts
        recent_payouts = PayoutTransaction.query.filter_by(user_id=user_id)\
                                               .order_by(PayoutTransaction.created_at.desc())\
                                               .limit(5).all()
        
        # Calculate total lifetime earnings
        total_payouts = db.session.query(db.func.sum(PayoutTransaction.amount))\
                                 .filter_by(user_id=user_id, status='completed').scalar() or 0.0
        
        earnings_data = {
            'available_earnings': available_earnings,
            'total_lifetime_payouts': total_payouts,
            'recent_payouts': [
                {
                    'payout_id': payout.payout_id,
                    'amount': payout.amount,
                    'payment_method': payout.payment_method,
                    'status': payout.status,
                    'created_at': payout.created_at.isoformat()
                }
                for payout in recent_payouts
            ]
        }
        
        return jsonify(earnings_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Scheduled Payout Processing
@banking_system_bp.route('/banking/process-scheduled-payouts', methods=['POST'])
@cross_origin()
def process_scheduled_payouts_endpoint():
    """Process all scheduled payouts (admin only)"""
    try:
        processed_count = process_scheduled_payouts()
        
        return jsonify({
            'message': f'Processed {processed_count} scheduled payouts',
            'processed_count': processed_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Financial Reporting Routes
@banking_system_bp.route('/banking/financial-summary', methods=['GET'])
@cross_origin()
def get_financial_summary_endpoint():
    """Get financial summary"""
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str)
        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str)
        
        summary = get_financial_summary(start_date, end_date)
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/ledger', methods=['GET'])
@cross_origin()
def get_ledger_entries():
    """Get financial ledger entries"""
    try:
        account_type = request.args.get('account_type')
        category = request.args.get('category')
        user_id = request.args.get('user_id', type=int)
        limit = request.args.get('limit', 100, type=int)
        
        query = FinancialLedger.query
        
        if account_type:
            query = query.filter_by(account_type=account_type)
        if category:
            query = query.filter_by(category=category)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        entries = query.order_by(FinancialLedger.created_at.desc()).limit(limit).all()
        
        entries_data = [
            {
                'id': entry.id,
                'entry_type': entry.entry_type,
                'account_type': entry.account_type,
                'category': entry.category,
                'amount': entry.amount,
                'currency': entry.currency,
                'description': entry.description,
                'user_id': entry.user_id,
                'reference_type': entry.reference_type,
                'reference_id': entry.reference_id,
                'accounting_date': entry.accounting_date.isoformat(),
                'fiscal_year': entry.fiscal_year,
                'fiscal_quarter': entry.fiscal_quarter,
                'is_reconciled': entry.is_reconciled,
                'created_at': entry.created_at.isoformat()
            }
            for entry in entries
        ]
        
        return jsonify({
            'ledger_entries': entries_data,
            'total_count': len(entries_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Compliance and Reporting
@banking_system_bp.route('/banking/compliance-report', methods=['POST'])
@cross_origin()
def generate_compliance_report_endpoint():
    """Generate compliance report (admin only)"""
    try:
        data = request.get_json()
        
        required_fields = ['report_type', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
        
        report = generate_compliance_report(
            report_type=data['report_type'],
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'report_id': report.id,
            'report_type': report.report_type,
            'total_payments_made': report.total_payments_made,
            'total_users_paid': report.total_users_paid,
            'status': report.status,
            'generated_at': report.generated_at.isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/compliance-reports', methods=['GET'])
@cross_origin()
def get_compliance_reports():
    """Get compliance reports (admin only)"""
    try:
        reports = ComplianceReport.query.order_by(ComplianceReport.generated_at.desc()).limit(20).all()
        
        reports_data = [
            {
                'id': report.id,
                'report_type': report.report_type,
                'reporting_period_start': report.reporting_period_start.isoformat(),
                'reporting_period_end': report.reporting_period_end.isoformat(),
                'total_payments_made': report.total_payments_made,
                'total_users_paid': report.total_users_paid,
                'status': report.status,
                'generated_at': report.generated_at.isoformat()
            }
            for report in reports
        ]
        
        return jsonify({
            'reports': reports_data,
            'total_count': len(reports_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin Routes
@banking_system_bp.route('/banking/admin/reconcile/<int:bank_account_id>', methods=['POST'])
@cross_origin()
def reconcile_bank_account_endpoint(bank_account_id):
    """Reconcile bank account (admin only)"""
    try:
        reconciled_count = reconcile_bank_account(bank_account_id)
        
        return jsonify({
            'message': f'Reconciled {reconciled_count} transactions',
            'reconciled_count': reconciled_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@banking_system_bp.route('/banking/admin/business-accounts', methods=['GET'])
@cross_origin()
def get_business_bank_accounts():
    """Get business bank accounts (admin only)"""
    try:
        business_accounts = BankAccount.query.filter_by(account_type='business').all()
        
        accounts_data = [
            {
                'id': account.id,
                'account_name': account.account_name,
                'bank_name': account.bank_name,
                'current_balance': account.current_balance,
                'available_balance': account.available_balance,
                'reserved_balance': account.reserved_balance,
                'currency': account.currency,
                'is_primary': account.is_primary,
                'last_balance_update': account.last_balance_update.isoformat() if account.last_balance_update else None
            }
            for account in business_accounts
        ]
        
        return jsonify({
            'business_accounts': accounts_data,
            'total_count': len(accounts_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analytics Routes
@banking_system_bp.route('/banking/analytics', methods=['GET'])
@cross_origin()
def get_banking_analytics():
    """Get banking system analytics"""
    try:
        # Get key metrics
        total_users_with_accounts = db.session.query(db.func.count(db.distinct(UserBankAccount.user_id)))\
                                             .filter_by(is_active=True).scalar() or 0
        
        total_verified_accounts = UserBankAccount.query.filter_by(verification_status='verified', is_active=True).count()
        
        total_payouts_this_month = PayoutTransaction.query.filter(
            PayoutTransaction.created_at >= datetime.utcnow().replace(day=1),
            PayoutTransaction.status == 'completed'
        ).count()
        
        total_payout_amount_this_month = db.session.query(db.func.sum(PayoutTransaction.amount))\
                                                  .filter(
                                                      PayoutTransaction.created_at >= datetime.utcnow().replace(day=1),
                                                      PayoutTransaction.status == 'completed'
                                                  ).scalar() or 0.0
        
        # Get payout method breakdown
        payout_methods = db.session.query(
            PayoutTransaction.payment_method,
            db.func.count(PayoutTransaction.id).label('count'),
            db.func.sum(PayoutTransaction.amount).label('total_amount')
        ).filter_by(status='completed')\
         .group_by(PayoutTransaction.payment_method).all()
        
        analytics_data = {
            'overview': {
                'total_users_with_accounts': total_users_with_accounts,
                'total_verified_accounts': total_verified_accounts,
                'verification_rate': (total_verified_accounts / total_users_with_accounts * 100) if total_users_with_accounts > 0 else 0,
                'total_payouts_this_month': total_payouts_this_month,
                'total_payout_amount_this_month': total_payout_amount_this_month
            },
            'payout_methods': [
                {
                    'method': method.payment_method,
                    'transaction_count': method.count,
                    'total_amount': float(method.total_amount or 0)
                }
                for method in payout_methods
            ]
        }
        
        return jsonify(analytics_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@banking_system_bp.route('/banking/health', methods=['GET'])
@cross_origin()
def banking_system_health():
    """Banking system health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'supported_methods': ['bank_transfer', 'paypal', 'venmo', 'crypto'],
        'version': '1.0.0'
    }), 200

