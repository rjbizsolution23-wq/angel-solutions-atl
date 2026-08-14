"""
Stripe data retrieval endpoints.
"""
from fastapi import APIRouter, HTTPException
from core.stripe_client import get_stripe_client
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/balance")
async def get_balance():
    """Get account balance."""
    try:
        client = get_stripe_client()
        balance = client.retrieve_balance()
        return {"balance": balance}
    except Exception as e:
        logger.error(f"Error retrieving balance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customers")
async def list_customers(limit: int = 10):
    """List customers."""
    try:
        client = get_stripe_client()
        customers = client.list_customers(limit=limit)
        return {"customers": customers.data}
    except Exception as e:
        logger.error(f"Error listing customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products")
async def list_products(limit: int = 10):
    """List products."""
    try:
        client = get_stripe_client()
        products = client.list_products(limit=limit)
        return {"products": products.data}
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subscriptions")
async def list_subscriptions(limit: int = 10):
    """List subscriptions."""
    try:
        client = get_stripe_client()
        subscriptions = client.list_subscriptions(limit=limit)
        return {"subscriptions": subscriptions.data}
    except Exception as e:
        logger.error(f"Error listing subscriptions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transactions")
async def list_transactions(limit: int = 10):
    """List balance transactions."""
    try:
        client = get_stripe_client()
        transactions = client.list_balance_transactions(limit=limit)
        return {"transactions": transactions.data}
    except Exception as e:
        logger.error(f"Error listing transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))
