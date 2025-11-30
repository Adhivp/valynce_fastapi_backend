"""
Dataset API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import Dataset, User, License, Transaction
from datetime import datetime

router = APIRouter(prefix="/api/datasets", tags=["Datasets"])

# Pydantic models
class DatasetResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price_apt: float
    per_query_price: float
    size_mb: float
    format: str
    tags: str
    downloads: int
    nft_minted: bool
    owner_id: int
    owner_username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DatasetCreate(BaseModel):
    title: str
    description: str
    category: str
    file_hash: str
    ipfs_uri: str
    price_apt: float
    per_query_price: float
    size_mb: float
    format: str
    tags: str
    owner_wallet: str

class LicenseCreate(BaseModel):
    dataset_id: int
    user_wallet: str
    license_type: int
    duration_days: Optional[int] = None

class LicenseResponse(BaseModel):
    id: int
    dataset_id: int
    dataset_title: str
    license_type: int
    expires_at: Optional[datetime]
    price_paid: float
    purchased_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[DatasetResponse])
async def get_all_datasets(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all datasets with optional filtering"""
    query = db.query(Dataset)
    
    if category and category != "All":
        query = query.filter(Dataset.category == category)
    
    if search:
        query = query.filter(Dataset.title.ilike(f"%{search}%"))
    
    datasets = query.all()
    
    result = []
    for ds in datasets:
        result.append({
            **ds.__dict__,
            "owner_username": ds.owner.username if ds.owner else "Unknown"
        })
    
    return result

@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get a specific dataset by ID"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return {
        **dataset.__dict__,
        "owner_username": dataset.owner.username if dataset.owner else "Unknown"
    }

@router.post("/", response_model=DatasetResponse)
async def create_dataset(dataset: DatasetCreate, db: Session = Depends(get_db)):
    """Create a new dataset"""
    # Find or create user
    user = db.query(User).filter(User.wallet_address == dataset.owner_wallet).first()
    
    if not user:
        user = User(
            wallet_address=dataset.owner_wallet,
            username=f"user_{dataset.owner_wallet[:8]}"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create dataset
    new_dataset = Dataset(
        title=dataset.title,
        description=dataset.description,
        category=dataset.category,
        file_hash=dataset.file_hash,
        ipfs_uri=dataset.ipfs_uri,
        price_apt=dataset.price_apt,
        per_query_price=dataset.per_query_price,
        size_mb=dataset.size_mb,
        format=dataset.format,
        tags=dataset.tags,
        owner_id=user.id
    )
    
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    
    return {
        **new_dataset.__dict__,
        "owner_username": user.username
    }

@router.post("/mint/{dataset_id}")
async def mint_dataset_nft(
    dataset_id: int,
    transaction_hash: str,
    db: Session = Depends(get_db)
):
    """Mark dataset as minted on blockchain"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    dataset.nft_minted = True
    dataset.blockchain_tx = transaction_hash
    
    db.commit()
    
    return {
        "success": True,
        "message": "Dataset NFT minted successfully",
        "transaction_hash": transaction_hash
    }

@router.post("/purchase")
async def purchase_license(license_data: LicenseCreate, db: Session = Depends(get_db)):
    """Purchase a license for a dataset"""
    # Find dataset
    dataset = db.query(Dataset).filter(Dataset.id == license_data.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Find or create user
    user = db.query(User).filter(User.wallet_address == license_data.user_wallet).first()
    if not user:
        user = User(
            wallet_address=license_data.user_wallet,
            username=f"user_{license_data.user_wallet[:8]}"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create license
    from datetime import timedelta
    expires_at = None
    if license_data.duration_days:
        expires_at = datetime.utcnow() + timedelta(days=license_data.duration_days)
    
    license = License(
        user_id=user.id,
        dataset_id=dataset.id,
        license_type=license_data.license_type,
        expires_at=expires_at,
        transaction_hash=f"0x{'pending'}",
        price_paid=dataset.price_apt
    )
    
    db.add(license)
    dataset.downloads += 1
    db.commit()
    
    return {
        "success": True,
        "message": "License purchased successfully",
        "license_id": license.id
    }

@router.get("/user/{wallet_address}/licenses", response_model=List[LicenseResponse])
async def get_user_licenses(wallet_address: str, db: Session = Depends(get_db)):
    """Get all licenses for a user"""
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    
    if not user:
        return []
    
    licenses = db.query(License).filter(License.user_id == user.id).all()
    
    result = []
    for lic in licenses:
        result.append({
            **lic.__dict__,
            "dataset_title": lic.dataset.title if lic.dataset else "Unknown"
        })
    
    return result

@router.get("/user/{wallet_address}/owned", response_model=List[DatasetResponse])
async def get_user_datasets(wallet_address: str, db: Session = Depends(get_db)):
    """Get all datasets owned by a user"""
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    
    if not user:
        return []
    
    datasets = db.query(Dataset).filter(Dataset.owner_id == user.id).all()
    
    result = []
    for ds in datasets:
        result.append({
            **ds.__dict__,
            "owner_username": user.username
        })
    
    return result

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all unique categories"""
    categories = db.query(Dataset.category).distinct().all()
    return [cat[0] for cat in categories]
