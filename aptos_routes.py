"""
FastAPI routes for Aptos blockchain operations
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from aptos_service import aptos_service
from aptos_sdk.account import Account

router = APIRouter(prefix="/aptos", tags=["Aptos Blockchain"])

# Request/Response Models
class CreateAccountResponse(BaseModel):
    address: str
    private_key: str
    public_key: str
    message: str

class FundAccountRequest(BaseModel):
    address: str
    amount: Optional[int] = 100000000  # 1 APT

class MintDatasetRequest(BaseModel):
    private_key: str
    dataset_id: int
    hash: str
    uri: str

class GrantLicenseRequest(BaseModel):
    private_key: str
    dataset_id: int
    user_address: str
    duration_secs: int
    license_type: int  # 0 = unlimited, 1 = time-based, 2 = per-query

class SetPriceRequest(BaseModel):
    private_key: str
    dataset_id: int
    base_price: int
    per_query_price: int

class PayForLicenseRequest(BaseModel):
    buyer_private_key: str
    seller_address: str
    dataset_id: int

class SetRoyaltyRequest(BaseModel):
    private_key: str
    dataset_id: int
    contributors: List[str]
    share_percentage: int

class BalanceResponse(BaseModel):
    address: str
    balance: int
    balance_apt: float

@router.get("/")
async def aptos_info():
    """Get Aptos service information"""
    return {
        "node_url": aptos_service.node_url,
        "contract_address": aptos_service.contract_address or "Not deployed yet",
        "status": "connected"
    }

@router.post("/account/create", response_model=CreateAccountResponse)
async def create_account():
    """Create a new Aptos account"""
    account_info = aptos_service.create_account()
    return {
        **account_info,
        "message": "Account created successfully. Save your private key securely!"
    }

@router.get("/account/balance/{address}", response_model=BalanceResponse)
async def get_balance(address: str):
    """Get account balance"""
    balance = aptos_service.get_account_balance(address)
    return {
        "address": address,
        "balance": balance,
        "balance_apt": balance / 100000000  # Convert to APT
    }

@router.post("/account/fund")
async def fund_account(request: FundAccountRequest):
    """Fund account from testnet faucet"""
    success = aptos_service.fund_account_from_faucet(request.address, request.amount)
    if success:
        return {
            "success": True,
            "message": f"Account funded with {request.amount / 100000000} APT",
            "address": request.address
        }
    raise HTTPException(status_code=500, detail="Failed to fund account")

@router.post("/dataset/mint")
async def mint_dataset(request: MintDatasetRequest):
    """Mint a dataset NFT on Aptos"""
    try:
        account = Account.load_key(request.private_key)
        result = await aptos_service.mint_dataset_nft(
            account,
            request.dataset_id,
            request.hash,
            request.uri
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/license/grant")
async def grant_license(request: GrantLicenseRequest):
    """Grant a license to access a dataset"""
    try:
        account = Account.load_key(request.private_key)
        result = await aptos_service.grant_license(
            account,
            request.dataset_id,
            request.user_address,
            request.duration_secs,
            request.license_type
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payment/set-price")
async def set_price(request: SetPriceRequest):
    """Set pricing for a dataset"""
    try:
        account = Account.load_key(request.private_key)
        result = await aptos_service.set_dataset_price(
            account,
            request.dataset_id,
            request.base_price,
            request.per_query_price
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payment/pay-license")
async def pay_license(request: PayForLicenseRequest):
    """Pay for a dataset license"""
    try:
        buyer_account = Account.load_key(request.buyer_private_key)
        result = await aptos_service.pay_for_license(
            buyer_account,
            request.seller_address,
            request.dataset_id
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/royalty/set")
async def set_royalty(request: SetRoyaltyRequest):
    """Set royalty configuration for a dataset"""
    try:
        account = Account.load_key(request.private_key)
        result = await aptos_service.set_royalty_config(
            account,
            request.dataset_id,
            request.contributors,
            request.share_percentage
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transaction/{tx_hash}")
async def get_transaction(tx_hash: str):
    """Get transaction status"""
    return aptos_service.get_transaction_status(tx_hash)
