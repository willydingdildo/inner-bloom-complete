from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import hashlib
import secrets
import json

db = SQLAlchemy()

class CryptoPaymentGateway(db.Model):
    __tablename__ = 'crypto_payment_gateways'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # coinpayments, nowpayments, coinbase_commerce
    api_key = db.Column(db.String(255))  # Encrypted API key
    api_secret = db.Column(db.String(255))  # Encrypted API secret
    webhook_secret = db.Column(db.String(255))  # Webhook verification secret
    
    # Configuration
    is_active = db.Column(db.Boolean, default=True)
    is_testnet = db.Column(db.Boolean, default=False)
    supported_currencies = db.Column(db.JSON)  # ['BTC', 'ETH', 'USDT', etc.]
    
    # Fee structure
    transaction_fee_percentage = db.Column(db.Float, default=1.0)  # Gateway fee percentage
    minimum_amount = db.Column(db.Float, default=0.001)  # Minimum transaction amount
    maximum_amount = db.Column(db.Float, default=10000.0)  # Maximum transaction amount
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CryptoCurrency(db.Model):
    __tablename__ = 'crypto_currencies'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)  # BTC, ETH, USDT
    name = db.Column(db.String(50), nullable=False)  # Bitcoin, Ethereum, Tether
    network = db.Column(db.String(20))  # mainnet, polygon, bsc, etc.
    
    # Display information
    icon_url = db.Column(db.String(500))
    decimals = db.Column(db.Integer, default=8)
    
    # Exchange rates (updated periodically)
    usd_rate = db.Column(db.Float, default=0.0)
    last_rate_update = db.Column(db.DateTime)
    
    # Configuration
    is_active = db.Column(db.Boolean, default=True)
    minimum_confirmations = db.Column(db.Integer, default=3)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CryptoWallet(db.Model):
    __tablename__ = 'crypto_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('crypto_currencies.id'), nullable=False)
    
    # Wallet details
    wallet_address = db.Column(db.String(255), nullable=False)
    wallet_label = db.Column(db.String(100))  # User-defined label
    
    # Balance tracking
    balance = db.Column(db.Float, default=0.0)
    pending_balance = db.Column(db.Float, default=0.0)
    last_balance_update = db.Column(db.DateTime)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CryptoTransaction(db.Model):
    __tablename__ = 'crypto_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gateway_id = db.Column(db.Integer, db.ForeignKey('crypto_payment_gateways.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('crypto_currencies.id'), nullable=False)
    
    # Transaction identifiers
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)  # Our internal ID
    external_transaction_id = db.Column(db.String(255))  # Gateway transaction ID
    blockchain_hash = db.Column(db.String(255))  # Blockchain transaction hash
    
    # Transaction details
    transaction_type = db.Column(db.String(20), nullable=False)  # payment, payout, refund
    amount_crypto = db.Column(db.Float, nullable=False)  # Amount in cryptocurrency
    amount_usd = db.Column(db.Float, nullable=False)  # Amount in USD at time of transaction
    exchange_rate = db.Column(db.Float, nullable=False)  # Crypto to USD rate used
    
    # Addresses
    from_address = db.Column(db.String(255))
    to_address = db.Column(db.String(255))
    
    # Fees
    network_fee = db.Column(db.Float, default=0.0)  # Blockchain network fee
    gateway_fee = db.Column(db.Float, default=0.0)  # Payment gateway fee
    platform_fee = db.Column(db.Float, default=0.0)  # Our platform fee
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, failed, cancelled
    confirmations = db.Column(db.Integer, default=0)
    required_confirmations = db.Column(db.Integer, default=3)
    
    # Metadata
    purpose = db.Column(db.String(100))  # subscription, referral_payout, affiliate_earning, etc.
    reference_id = db.Column(db.String(100))  # Reference to related record (subscription_id, payout_id, etc.)
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)  # Payment expiration time

class CryptoPaymentRequest(db.Model):
    __tablename__ = 'crypto_payment_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Payment details
    amount_usd = db.Column(db.Float, nullable=False)
    currency_symbol = db.Column(db.String(10), nullable=False)  # BTC, ETH, USDT
    amount_crypto = db.Column(db.Float, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    
    # Payment addresses
    payment_address = db.Column(db.String(255), nullable=False)
    qr_code_url = db.Column(db.String(500))  # QR code for payment
    
    # Request details
    purpose = db.Column(db.String(100), nullable=False)  # subscription, product_purchase, etc.
    description = db.Column(db.Text)
    reference_id = db.Column(db.String(100))  # Reference to subscription, product, etc.
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, paid, expired, cancelled
    payment_received = db.Column(db.Float, default=0.0)
    
    # Expiration
    expires_at = db.Column(db.DateTime, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)

class CryptoPayoutRequest(db.Model):
    __tablename__ = 'crypto_payout_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Payout details
    amount_usd = db.Column(db.Float, nullable=False)
    currency_symbol = db.Column(db.String(10), nullable=False)
    amount_crypto = db.Column(db.Float, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    
    # Destination
    destination_address = db.Column(db.String(255), nullable=False)
    destination_tag = db.Column(db.String(100))  # For currencies that require tags (XRP, etc.)
    
    # Fees
    network_fee = db.Column(db.Float, default=0.0)
    processing_fee = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, nullable=False)  # Amount after fees
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, processing, sent, failed
    transaction_hash = db.Column(db.String(255))
    
    # Approval
    approved_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'))
    approved_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

class CryptoExchangeRate(db.Model):
    __tablename__ = 'crypto_exchange_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    currency_symbol = db.Column(db.String(10), nullable=False)
    
    # Exchange rates
    usd_rate = db.Column(db.Float, nullable=False)
    btc_rate = db.Column(db.Float, default=0.0)  # Rate in BTC
    eth_rate = db.Column(db.Float, default=0.0)  # Rate in ETH
    
    # Market data
    market_cap = db.Column(db.Float, default=0.0)
    volume_24h = db.Column(db.Float, default=0.0)
    change_24h = db.Column(db.Float, default=0.0)  # Percentage change
    
    # Data source
    source = db.Column(db.String(50), default='coingecko')  # coingecko, coinmarketcap, etc.
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CryptoWebhookLog(db.Model):
    __tablename__ = 'crypto_webhook_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    gateway_id = db.Column(db.Integer, db.ForeignKey('crypto_payment_gateways.id'), nullable=False)
    
    # Webhook details
    webhook_type = db.Column(db.String(50), nullable=False)  # payment_received, payment_confirmed, etc.
    payload = db.Column(db.JSON)  # Full webhook payload
    signature = db.Column(db.String(255))  # Webhook signature for verification
    
    # Processing
    processed = db.Column(db.Boolean, default=False)
    processing_result = db.Column(db.String(20))  # success, failed, ignored
    error_message = db.Column(db.Text)
    
    # Related transaction
    transaction_id = db.Column(db.String(100))
    
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

# Utility functions for crypto payments

def initialize_crypto_currencies():
    """Initialize supported cryptocurrencies"""
    currencies = [
        {
            'symbol': 'BTC',
            'name': 'Bitcoin',
            'network': 'mainnet',
            'decimals': 8,
            'minimum_confirmations': 3
        },
        {
            'symbol': 'ETH',
            'name': 'Ethereum',
            'network': 'mainnet',
            'decimals': 18,
            'minimum_confirmations': 12
        },
        {
            'symbol': 'USDT',
            'name': 'Tether USD',
            'network': 'ethereum',
            'decimals': 6,
            'minimum_confirmations': 12
        },
        {
            'symbol': 'USDT_TRC20',
            'name': 'Tether USD (TRC20)',
            'network': 'tron',
            'decimals': 6,
            'minimum_confirmations': 1
        }
    ]
    
    for currency_data in currencies:
        existing_currency = CryptoCurrency.query.filter_by(symbol=currency_data['symbol']).first()
        if not existing_currency:
            currency = CryptoCurrency(**currency_data)
            db.session.add(currency)
    
    db.session.commit()

def create_payment_request(user_id, amount_usd, currency_symbol, purpose, reference_id=None):
    """Create a crypto payment request"""
    # Get currency
    currency = CryptoCurrency.query.filter_by(symbol=currency_symbol, is_active=True).first()
    if not currency:
        raise ValueError(f"Currency {currency_symbol} not supported")
    
    # Get current exchange rate
    exchange_rate = get_current_exchange_rate(currency_symbol)
    if not exchange_rate:
        raise ValueError(f"Unable to get exchange rate for {currency_symbol}")
    
    # Calculate crypto amount
    amount_crypto = amount_usd / exchange_rate
    
    # Generate payment address (in production, this would use the gateway API)
    payment_address = generate_payment_address(currency_symbol)
    
    # Create payment request
    payment_request = CryptoPaymentRequest(
        user_id=user_id,
        amount_usd=amount_usd,
        currency_symbol=currency_symbol,
        amount_crypto=amount_crypto,
        exchange_rate=exchange_rate,
        payment_address=payment_address,
        purpose=purpose,
        reference_id=reference_id,
        expires_at=datetime.utcnow() + timedelta(hours=2)  # 2 hour expiration
    )
    
    db.session.add(payment_request)
    db.session.commit()
    
    return payment_request

def create_payout_request(user_id, amount_usd, currency_symbol, destination_address):
    """Create a crypto payout request"""
    # Get currency
    currency = CryptoCurrency.query.filter_by(symbol=currency_symbol, is_active=True).first()
    if not currency:
        raise ValueError(f"Currency {currency_symbol} not supported")
    
    # Get current exchange rate
    exchange_rate = get_current_exchange_rate(currency_symbol)
    if not exchange_rate:
        raise ValueError(f"Unable to get exchange rate for {currency_symbol}")
    
    # Calculate crypto amount
    amount_crypto = amount_usd / exchange_rate
    
    # Calculate fees
    network_fee = calculate_network_fee(currency_symbol, amount_crypto)
    processing_fee = amount_usd * 0.01  # 1% processing fee
    final_amount = amount_crypto - (network_fee / exchange_rate)
    
    # Create payout request
    payout_request = CryptoPayoutRequest(
        user_id=user_id,
        amount_usd=amount_usd,
        currency_symbol=currency_symbol,
        amount_crypto=amount_crypto,
        exchange_rate=exchange_rate,
        destination_address=destination_address,
        network_fee=network_fee,
        processing_fee=processing_fee,
        final_amount=final_amount
    )
    
    db.session.add(payout_request)
    db.session.commit()
    
    return payout_request

def get_current_exchange_rate(currency_symbol):
    """Get current exchange rate for a currency"""
    # Check if we have a recent rate
    recent_rate = CryptoExchangeRate.query.filter_by(currency_symbol=currency_symbol)\
                                         .filter(CryptoExchangeRate.created_at > datetime.utcnow() - timedelta(minutes=5))\
                                         .first()
    
    if recent_rate:
        return recent_rate.usd_rate
    
    # In production, this would fetch from a real API like CoinGecko
    # For demo purposes, return mock rates
    mock_rates = {
        'BTC': 45000.0,
        'ETH': 3000.0,
        'USDT': 1.0,
        'USDT_TRC20': 1.0
    }
    
    rate = mock_rates.get(currency_symbol, 1.0)
    
    # Store the rate
    exchange_rate = CryptoExchangeRate(
        currency_symbol=currency_symbol,
        usd_rate=rate,
        source='mock_api'
    )
    db.session.add(exchange_rate)
    db.session.commit()
    
    return rate

def generate_payment_address(currency_symbol):
    """Generate a payment address for the currency"""
    # In production, this would use the payment gateway API
    # For demo purposes, generate mock addresses
    
    if currency_symbol == 'BTC':
        return f"1{secrets.token_hex(16)}"
    elif currency_symbol == 'ETH' or currency_symbol == 'USDT':
        return f"0x{secrets.token_hex(20)}"
    elif currency_symbol == 'USDT_TRC20':
        return f"T{secrets.token_hex(16)}"
    else:
        return f"mock_{currency_symbol}_{secrets.token_hex(8)}"

def calculate_network_fee(currency_symbol, amount):
    """Calculate network fee for a transaction"""
    # Mock network fees (in production, get from gateway API)
    base_fees = {
        'BTC': 0.0005,  # ~$22.50 at $45k
        'ETH': 0.002,   # ~$6 at $3k
        'USDT': 5.0,    # ~$5 in USDT
        'USDT_TRC20': 1.0  # ~$1 in USDT
    }
    
    return base_fees.get(currency_symbol, 0.001)

def process_webhook(gateway_name, payload, signature):
    """Process incoming webhook from payment gateway"""
    # Get gateway
    gateway = CryptoPaymentGateway.query.filter_by(name=gateway_name, is_active=True).first()
    if not gateway:
        return False
    
    # Verify signature (implementation depends on gateway)
    if not verify_webhook_signature(gateway, payload, signature):
        return False
    
    # Log webhook
    webhook_log = CryptoWebhookLog(
        gateway_id=gateway.id,
        webhook_type=payload.get('type', 'unknown'),
        payload=payload,
        signature=signature
    )
    db.session.add(webhook_log)
    
    try:
        # Process based on webhook type
        if payload.get('type') == 'payment_received':
            process_payment_received(payload)
        elif payload.get('type') == 'payment_confirmed':
            process_payment_confirmed(payload)
        elif payload.get('type') == 'payout_completed':
            process_payout_completed(payload)
        
        webhook_log.processed = True
        webhook_log.processing_result = 'success'
        webhook_log.processed_at = datetime.utcnow()
        
    except Exception as e:
        webhook_log.processed = True
        webhook_log.processing_result = 'failed'
        webhook_log.error_message = str(e)
        webhook_log.processed_at = datetime.utcnow()
    
    db.session.commit()
    return True

def verify_webhook_signature(gateway, payload, signature):
    """Verify webhook signature"""
    # Implementation depends on the specific gateway
    # For demo purposes, always return True
    return True

def process_payment_received(payload):
    """Process payment received webhook"""
    transaction_id = payload.get('transaction_id')
    amount = payload.get('amount')
    currency = payload.get('currency')
    
    # Find the payment request
    payment_request = CryptoPaymentRequest.query.filter_by(
        payment_address=payload.get('address')
    ).first()
    
    if payment_request:
        payment_request.payment_received = amount
        payment_request.status = 'paid'
        payment_request.paid_at = datetime.utcnow()
        
        # Create transaction record
        transaction = CryptoTransaction(
            user_id=payment_request.user_id,
            gateway_id=1,  # Default gateway
            currency_id=CryptoCurrency.query.filter_by(symbol=currency).first().id,
            transaction_id=f"TX_{secrets.token_hex(8)}",
            external_transaction_id=transaction_id,
            transaction_type='payment',
            amount_crypto=amount,
            amount_usd=payment_request.amount_usd,
            exchange_rate=payment_request.exchange_rate,
            to_address=payment_request.payment_address,
            purpose=payment_request.purpose,
            reference_id=payment_request.reference_id,
            status='confirmed'
        )
        db.session.add(transaction)

def process_payment_confirmed(payload):
    """Process payment confirmed webhook"""
    # Update transaction confirmations
    transaction = CryptoTransaction.query.filter_by(
        external_transaction_id=payload.get('transaction_id')
    ).first()
    
    if transaction:
        transaction.confirmations = payload.get('confirmations', 0)
        transaction.blockchain_hash = payload.get('hash')
        
        if transaction.confirmations >= transaction.required_confirmations:
            transaction.status = 'confirmed'
            transaction.confirmed_at = datetime.utcnow()

def process_payout_completed(payload):
    """Process payout completed webhook"""
    payout_request = CryptoPayoutRequest.query.filter_by(
        id=payload.get('payout_id')
    ).first()
    
    if payout_request:
        payout_request.status = 'sent'
        payout_request.transaction_hash = payload.get('hash')
        payout_request.processed_at = datetime.utcnow()

def get_supported_currencies():
    """Get list of supported cryptocurrencies"""
    return CryptoCurrency.query.filter_by(is_active=True).all()

def get_user_crypto_balance(user_id):
    """Get user's crypto balance across all currencies"""
    balances = db.session.query(
        CryptoWallet.currency_id,
        CryptoCurrency.symbol,
        CryptoCurrency.name,
        db.func.sum(CryptoWallet.balance).label('total_balance')
    ).join(CryptoCurrency, CryptoWallet.currency_id == CryptoCurrency.id)\
     .filter(CryptoWallet.user_id == user_id, CryptoWallet.is_active == True)\
     .group_by(CryptoWallet.currency_id, CryptoCurrency.symbol, CryptoCurrency.name).all()
    
    return [
        {
            'currency_id': balance.currency_id,
            'symbol': balance.symbol,
            'name': balance.name,
            'balance': balance.total_balance
        }
        for balance in balances
    ]

