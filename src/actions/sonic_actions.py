import logging
import os
from dotenv import load_dotenv
from src.action_handler import register_action


logger = logging.getLogger("actions.sonic_actions")

@register_action("get-token-by-ticker") # gets the token address by ticker symbol
def get_token_by_ticker(agent, **kwargs):
    """Get token address by ticker symbol"""
    try:
        ticker = kwargs.get("ticker")
        if not ticker:
            logger.error("No ticker provided")
            return None
            
        token_address = agent.connection_manager.connections["sonic"].get_token_by_ticker(ticker)
        
        if token_address:
            logger.info(f"Found token address for {ticker}: {token_address}")
        else:
            logger.info(f"No token found for ticker {ticker}")
            
        return token_address

    except Exception as e:
        logger.error(f"Failed to get token by ticker: {str(e)}")
        return None

@register_action("get-sonic-balance") # gets the balance of $S or a token
def get_sonic_balance(agent, **kwargs):
    """Get $S or token balance"""
    try:
        address = kwargs.get("address")
        token_address = kwargs.get("token_address")
        
        if not address:
            load_dotenv()
            private_key = os.getenv('SONIC_PRIVATE_KEY')
            web3 = agent.connection_manager.connections["sonic"]._web3
            account = web3.eth.account.from_key(private_key)
            address = account.address

        balance = agent.connection_manager.connections["sonic"].get_balance(
            address=address,
            token_address=token_address
        )
        
        if token_address:
            logger.info(f"Token Balance: {balance}")
        else:
            logger.info(f"$S Balance: {balance}")
            
        return balance

    except Exception as e:
        logger.error(f"Failed to get balance: {str(e)}")
        return None

@register_action("send-sonic") # sends $S tokens to an address
def send_sonic(agent, **kwargs):
    """Send $S tokens to an address"""
    try:
        to_address = kwargs.get("to_address")
        amount = float(kwargs.get("amount"))

        tx_url = agent.connection_manager.connections["sonic"].transfer(
            to_address=to_address,
            amount=amount
        )

        logger.info(f"Transferred {amount} $S to {to_address}")
        logger.info(f"Transaction URL: {tx_url}")
        return tx_url

    except Exception as e:
        logger.error(f"Failed to send $S: {str(e)}")
        return None

@register_action("send-sonic-token") # sends tokens on the sonic chain
def send_sonic_token(agent, **kwargs):
    """Send tokens on Sonic chain"""
    try:
        to_address = kwargs.get("to_address")
        token_address = kwargs.get("token_address")
        amount = float(kwargs.get("amount"))

        tx_url = agent.connection_manager.connections["sonic"].transfer(
            to_address=to_address,
            amount=amount,
            token_address=token_address
        )

        logger.info(f"Transferred {amount} tokens to {to_address}")
        logger.info(f"Transaction URL: {tx_url}")
        return tx_url

    except Exception as e:
        logger.error(f"Failed to send tokens: {str(e)}")
        return None

@register_action("swap-sonic")
def swap_sonic(agent, **kwargs):
    try:
        token_in = kwargs.get("token_in")
        token_out = kwargs.get("token_out")
        amount = float(kwargs.get("amount"))
        slippage = float(kwargs.get("slippage", 0.5))
        agent.connection_manager.connections["sonic"].swap(
            token_in=token_in,
            token_out=token_out,
            amount=amount,
            slippage=slippage
        )
        return
    except Exception as e:
        logger.error(f"Failed to swap tokens: {str(e)}")
        return None
    
@register_action("get-sonic-price") # gets a token price on the sonic chain
def get_sonic_price(agent, **kwargs):
    """Get token price on Sonic chain"""
    try:
        token = kwargs.get("token")
        price = agent.connection_manager.connections["sonic"].get_price(token)
        logger.info(f"Price for {token}: {price}")
        return price
    except Exception as e:
        logger.error(f"Failed to get price: {str(e)}")
        return None