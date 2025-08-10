from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.models.crypto_payments import (
    CryptoPaymentGateway, CryptoCurrency, CryptoWallet, CryptoTransaction,
    CryptoPaymentRequest, CryptoPayoutRequest, CryptoExchangeRate,
    initialize_crypto_currencies, create_payment_request, create_payout_request,
    get_current_exchange_rate, get_supported_currencies, get_user_crypto_balance,
    process_webhook, db
)
from src.models.user import User
from datetime import datetime, timedelta
import json

crypto_payments_bp = Blueprint('crypto_payments', __name__)

# Initialize crypto currencies on first load
# Note: Initialization moved to main app startup
def setup_crypto_currencies():
    """Initialize crypto currencies"""
    initialize_crypto_currencies()

# Currency and Exchange Rate Routes
@crypto_payments_bp.route('/crypto/currencies', methods=['GET'])
@cross_origin()
def get_currencies():
    """Get supported cryptocurrencies"""
    try:
        currencies = get_supported_currencies()
        
        currencies_data = [
            {
                'id': currency.id,
                'symbol': currency.symbol,
                'name': currency.name,
                'network': currency.network,
                'decimals': currency.decimals,
                'usd_rate': currency.usd_rate,
                'minimum_confirmations': currency.minimum_confirmations,
                'icon_url': currency.icon_url
            }
            for currency in currencies
        ]
        
        return jsonify({
            'currencies': currencies_data,
            'total_count': len(currencies_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crypto_payments_bp.route('/crypto/exchange-rates', methods=['GET'])
@cross_origin()
def get_exchange_rates():
    """Get current exchange rates"""
    try:
        currency_symbol = request.args.get('currency')
        
        if currency_symbol:
            rate = get_current_exchange_rate(currency_symbol)
            return jsonify({
                'currency': currency_symbol,
                'usd_rate': rate,
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        else:
            # Get all rates
            rates = CryptoExchangeRate.query.filter(
                CryptoExchangeRate.created_at > datetime.utcnow() - timedelta(hours=1)
            ).all()
            
            rates_data = [
                {
                    'currency': rate.currency_symbol,
                    'usd_rate': rate.usd_rate,
                    'btc_rate': rate.btc_rate,
                    'change_24h': rate.change_24h,
                    'updated_at': rate.created_at.isoformat()
                }
                for rate in rates
            ]
            
            return jsonify({
                'exchange_rates': rates_data,
                'total_count': len(rates_data)
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payment Request Routes
@crypto_payments_bp.route('/crypto/payment-request', methods=['POST'])
@cross_origin()
def create_crypto_payment_request():
    """Create a crypto payment request"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'amount_usd', 'currency_symbol', 'purpose']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        payment_request = create_payment_request(
            user_id=data['user_id'],
            amount_usd=data['amount_usd'],
            currency_symbol=data['currency_symbol'],
            purpose=data['purpose'],
            reference_id=data.get('reference_id')
        )
        
        return jsonify({
            'payment_request_id': payment_request.id,
            'payment_address': payment_request.payment_address,
            'amount_crypto': payment_request.amount_crypto,
            'amount_usd': payment_request.amount_usd,
            'currency_symbol': payment_request.currency_symbol,
            'exchange_rate': payment_request.exchange_rate,
            'expires_at': payment_request.expires_at.isoformat(),
            'qr_code_url': f"/api/crypto/payment-request/{payment_request.id}/qr"
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crypto_payments_bp.route('/crypto/payment-request/<int:request_id>', methods=['GET'])
@cross_origin()
def get_payment_request(request_id):
    """Get payment request details"""
    try:
        payment_request = CryptoPaymentRequest.query.get_or_404(request_id)
        
        return jsonify({
            'id': payment_request.id,
            'user_id': payment_request.user_id,
            'amount_usd': payment_request.amount_usd,
            'amount_crypto': payment_request.amount_crypto,
            'currency_symbol': payment_request.currency_symbol,
            'exchange_rate': payment_request.exchange_rate,
            'payment_address': payment_request.payment_address,
            'purpose': payment_request.purpose,
            'status': payment_request.status,
            'payment_received': payment_request.payment_received,
            'created_at': payment_request.created_at.isoformat(),
            'expires_at': payment_request.expires_at.isoformat(),
            'paid_at': payment_request.paid_at.isoformat() if payment_request.paid_at else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crypto_payments_bp.route('/crypto/payment-request/<int:request_id>/qr', methods=['GET'])
@cross_origin()
def get_payment_qr_code(request_id):
    """Generate QR code for payment request"""
    try:
        payment_request = CryptoPaymentRequest.query.get_or_404(request_id)
        
        # In production, generate actual QR code
        # For demo, return QR code data
        qr_data = {
            'address': payment_request.payment_address,
            'amount': payment_request.amount_crypto,
            'currency': payment_request.currency_symbol,
            'label': f'Inner Bloom - {payment_request.purpose}'
        }
        
        return jsonify({
            'qr_data': qr_data,
            'qr_string': f"{payment_request.currency_symbol.lower()}:{payment_request.payment_address}?amount={payment_request.amount_crypto}"
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payout Routes
@crypto_payments_bp.route('/crypto/payout-request', methods=['POST'])
@cross_origin()
def create_crypto_payout_request():
    """Create a crypto payout request"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'amount_usd', 'currency_symbol', 'destination_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate minimum payout amount
        if data['amount_usd'] < 25.0:
            return jsonify({'error': 'Minimum payout amount is $25'}), 400
        
        payout_request = create_payout_request(
            user_id=data['user_id'],
            amount_usd=data['amount_usd'],
            currency_symbol=data['currency_symbol'],
            destination_address=data['destination_address']
        )
        
        return jsonify({
            'payout_request_id': payout_request.id,
            'amount_crypto': payout_request.amount_crypto,
            'amount_usd': payout_request.amount_usd,
            'currency_symbol': payout_request.currency_symbol,
            'destination_address': payout_request.destination_address,
            'network_fee': payout_request.network_fee,
            'processing_fee': payout_request.processing_fee,
            'final_amount': payout_request.final_amount,
            'status': payout_request.status
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crypto_payments_bp.route('/crypto/payout-requests', methods=['GET'])
@cross_origin()
def get_payout_requests():
    """Get payout requests for a user"""
    try:
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')
        
        query = CryptoPayoutRequest.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        
        payout_requests = query.order_by(CryptoPayoutRequest.created_at.desc()).limit(50).all()
        
        requests_data = [
            {
                'id': req.id,
                'user_id': req.user_id,
                'amount_usd': req.amount_usd,
                'amount_crypto': req.amount_crypto,
                'currency_symbol': req.currency_symbol,
                'destination_address': req.destination_address,
                'network_fee': req.network_fee,
                'processing_fee': req.processing_fee,
                'final_amount': req.final_amount,
                'status': req.status,
                'transaction_hash': req.transaction_hash,
                'created_at': req.created_at.isoformat(),
                'processed_at': req.processed_at.isoformat() if req.processed_at else None
            }
            for req in payout_requests
        ]
        
        return jsonify({
            'payout_requests': requests_data,
            'total_count': len(requests_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Wallet Routes
@crypto_payments_bp.route('/crypto/wallets/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_wallets(user_id):
    """Get user's crypto wallets"""
    try:
        wallets = CryptoWallet.query.filter_by(user_id=user_id, is_active=True).all()
        
        wallets_data = [
            {
                'id': wallet.id,
                'currency_id': wallet.currency_id,
                'wallet_address': wallet.wallet_address,
                'wallet_label': wallet.wallet_label,
                'balance': wallet.balance,
                'pending_balance': wallet.pending_balance,
                'is_verified': wallet.is_verified,
                'last_balance_update': wallet.last_balance_update.isoformat() if wallet.last_balance_update else None
            }
            for wallet in wallets
        ]
        
        return jsonify({
            'wallets': wallets_data,
            'total_count': len(wallets_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crypto_payments_bp.route('/crypto/wallets', methods=['POST'])
@cross_origin()
def add_user_wallet():
    """Add a crypto wallet for user"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'currency_id', 'wallet_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if wallet already exists
        existing_wallet = CryptoWallet.query.filter_by(
            user_id=data['user_id'],
            currency_id=data['currency_id'],
            wallet_address=data['wallet_address']
        ).first()
        
        if existing_wallet:
            return jsonify({'error': 'Wallet already exists'}), 409
        
        wallet = CryptoWallet(
            user_id=data['user_id'],
            currency_id=data['currency_id'],
            wallet_address=data['wallet_address'],
            wallet_label=data.get('wallet_label', 'My Wallet')
        )
        
        db.session.add(wallet)
        db.session.commit()
        
        return jsonify({
            'wallet_id': wallet.id,
            'message': 'Wallet added successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Transaction Routes
@crypto_payments_bp.route('/crypto/transactions', methods=['GET'])
@cross_origin()
def get_crypto_transactions():
    """Get crypto transactions"""
    try:
        user_id = request.args.get('user_id', type=int)
        transaction_type = request.args.get('type')
        status = request.args.get('status')
        
        query = CryptoTransaction.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if transaction_type:
            query = query.filter_by(transaction_type=transaction_type)
        if status:
            query = query.filter_by(status=status)
        
        transactions = query.order_by(CryptoTransaction.created_at.desc()).limit(100).all()
        
        transactions_data = [
            {
                'id': tx.id,
                'transaction_id': tx.transaction_id,
                'user_id': tx.user_id,
                'transaction_type': tx.transaction_type,
                'amount_crypto': tx.amount_crypto,
                'amount_usd': tx.amount_usd,
                'currency_symbol': CryptoCurrency.query.get(tx.currency_id).symbol,
                'exchange_rate': tx.exchange_rate,
                'from_address': tx.from_address,
                'to_address': tx.to_address,
                'network_fee': tx.network_fee,
                'gateway_fee': tx.gateway_fee,
                'status': tx.status,
                'confirmations': tx.confirmations,
                'blockchain_hash': tx.blockchain_hash,
                'purpose': tx.purpose,
                'created_at': tx.created_at.isoformat(),
                'confirmed_at': tx.confirmed_at.isoformat() if tx.confirmed_at else None
            }
            for tx in transactions
        ]
        
        return jsonify({
            'transactions': transactions_data,
            'total_count': len(transactions_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crypto_payments_bp.route('/crypto/balance/<int:user_id>', methods=['GET'])
@cross_origin()
def get_crypto_balance(user_id):
    """Get user's crypto balance"""
    try:
        balances = get_user_crypto_balance(user_id)
        
        # Calculate total USD value
        total_usd_value = 0.0
        for balance in balances:
            rate = get_current_exchange_rate(balance['symbol'])
            balance['usd_value'] = balance['balance'] * rate
            total_usd_value += balance['usd_value']
        
        return jsonify({
            'balances': balances,
            'total_usd_value': total_usd_value,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Webhook Routes
@crypto_payments_bp.route('/crypto/webhook/<gateway_name>', methods=['POST'])
@cross_origin()
def handle_crypto_webhook(gateway_name):
    """Handle webhook from crypto payment gateway"""
    try:
        payload = request.get_json()
        signature = request.headers.get('X-Signature') or request.headers.get('X-Webhook-Signature')
        
        success = process_webhook(gateway_name, payload, signature)
        
        if success:
            return jsonify({'status': 'processed'}), 200
        else:
            return jsonify({'error': 'Failed to process webhook'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin Routes
@crypto_payments_bp.route('/crypto/admin/gateways', methods=['GET'])
@cross_origin()
def get_payment_gateways():
    """Get payment gateways (admin only)"""
    try:
        gateways = CryptoPaymentGateway.query.all()
        
        gateways_data = [
            {
                'id': gateway.id,
                'name': gateway.name,
                'is_active': gateway.is_active,
                'is_testnet': gateway.is_testnet,
                'supported_currencies': gateway.supported_currencies,
                'transaction_fee_percentage': gateway.transaction_fee_percentage,
                'minimum_amount': gateway.minimum_amount,
                'maximum_amount': gateway.maximum_amount
            }
            for gateway in gateways
        ]
        
        return jsonify({
            'gateways': gateways_data,
            'total_count': len(gateways_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@crypto_payments_bp.route('/crypto/admin/payout/<int:payout_id>/approve', methods=['POST'])
@cross_origin()
def approve_crypto_payout(payout_id):
    """Approve crypto payout request (admin only)"""
    try:
        data = request.get_json() or {}
        
        payout_request = CryptoPayoutRequest.query.get_or_404(payout_id)
        
        if payout_request.status != 'pending':
            return jsonify({'error': 'Payout request is not pending'}), 400
        
        payout_request.status = 'processing'
        payout_request.approved_by = data.get('admin_id', 1)  # Default admin ID
        payout_request.approved_at = datetime.utcnow()
        
        # In production, this would trigger actual payout via gateway API
        # For demo, simulate successful payout
        payout_request.status = 'sent'
        payout_request.transaction_hash = f"0x{secrets.token_hex(32)}"
        payout_request.processed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payout approved and processed',
            'transaction_hash': payout_request.transaction_hash
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analytics Routes
@crypto_payments_bp.route('/crypto/analytics', methods=['GET'])
@cross_origin()
def get_crypto_analytics():
    """Get crypto payment analytics"""
    try:
        # Get payment statistics
        total_payments = CryptoTransaction.query.filter_by(transaction_type='payment').count()
        total_payouts = CryptoTransaction.query.filter_by(transaction_type='payout').count()
        
        total_payment_volume = db.session.query(
            db.func.sum(CryptoTransaction.amount_usd)
        ).filter_by(transaction_type='payment', status='confirmed').scalar() or 0.0
        
        total_payout_volume = db.session.query(
            db.func.sum(CryptoTransaction.amount_usd)
        ).filter_by(transaction_type='payout', status='confirmed').scalar() or 0.0
        
        # Get currency breakdown
        currency_stats = db.session.query(
            CryptoCurrency.symbol,
            db.func.count(CryptoTransaction.id).label('transaction_count'),
            db.func.sum(CryptoTransaction.amount_usd).label('total_volume')
        ).join(CryptoTransaction, CryptoCurrency.id == CryptoTransaction.currency_id)\
         .group_by(CryptoCurrency.symbol).all()
        
        analytics_data = {
            'overview': {
                'total_payments': total_payments,
                'total_payouts': total_payouts,
                'total_payment_volume': total_payment_volume,
                'total_payout_volume': total_payout_volume,
                'net_volume': total_payment_volume - total_payout_volume
            },
            'currency_breakdown': [
                {
                    'currency': stat.symbol,
                    'transaction_count': stat.transaction_count,
                    'total_volume': float(stat.total_volume or 0)
                }
                for stat in currency_stats
            ]
        }
        
        return jsonify(analytics_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@crypto_payments_bp.route('/crypto/health', methods=['GET'])
@cross_origin()
def crypto_payments_health():
    """Crypto payments health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'supported_currencies': ['BTC', 'ETH', 'USDT', 'USDT_TRC20'],
        'version': '1.0.0'
    }), 200

