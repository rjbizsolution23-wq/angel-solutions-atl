"""
LangChain tools for Stripe balance and reporting.
"""
from langchain.tools import tool
from core.stripe_client import get_stripe_client
import logging

logger = logging.getLogger(__name__)


@tool
def get_balance_tool() -> str:
    """
    Get the current Stripe account balance.
    
    Returns:
        Balance information for all currencies
    """
    try:
        client = get_stripe_client()
        balance = client.retrieve_balance()
        
        result = "Account Balance:\n"
        
        # Available balance
        if balance.available:
            result += "Available:\n"
            for bal in balance.available:
                amount = bal.amount / 100
                result += f"  - {bal.currency.upper()}: ${amount:.2f}\n"
        
        # Pending balance
        if balance.pending:
            result += "Pending:\n"
            for bal in balance.pending:
                amount = bal.amount / 100
                result += f"  - {bal.currency.upper()}: ${amount:.2f}\n"
        
        return result
    except Exception as e:
        logger.error(f"Error retrieving balance: {e}")
        return f"Error retrieving balance: {str(e)}"


@tool
def list_recent_transactions_tool(limit: int = 10) -> str:
    """
    List recent balance transactions.
    
    Args:
        limit: Number of transactions to return (default: 10)
    
    Returns:
        List of recent transactions
    """
    try:
        client = get_stripe_client()
        transactions = client.list_balance_transactions(limit=limit)
        
        if not transactions.data:
            return "No transactions found."
        
        result = "Recent Transactions:\n"
        for txn in transactions.data:
            amount = txn.amount / 100
            fee = txn.fee / 100
            net = txn.net / 100
            result += f"- {txn.type}: ${amount:.2f} (Fee: ${fee:.2f}, Net: ${net:.2f}) - {txn.description or 'No description'}\n"
        
        return result
    except Exception as e:
        logger.error(f"Error listing transactions: {e}")
        return f"Error listing transactions: {str(e)}"
