"""
SQLAlchemy Database Models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    datasets = relationship("Dataset", back_populates="owner")
    licenses = relationship("License", back_populates="user")

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String)
    file_hash = Column(String, unique=True)
    ipfs_uri = Column(String)
    price_apt = Column(Float)
    per_query_price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    nft_minted = Column(Boolean, default=False)
    blockchain_tx = Column(String, nullable=True)
    size_mb = Column(Float)
    format = Column(String)
    tags = Column(String)
    downloads = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="datasets")
    licenses = relationship("License", back_populates="dataset")

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    license_type = Column(Integer)  # 0=unlimited, 1=time-based, 2=per-query
    expires_at = Column(DateTime, nullable=True)
    transaction_hash = Column(String)
    price_paid = Column(Float)
    purchased_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="licenses")
    dataset = relationship("Dataset", back_populates="licenses")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    from_address = Column(String)
    to_address = Column(String)
    amount_apt = Column(Float)
    transaction_type = Column(String)  # mint, purchase, royalty
    blockchain_hash = Column(String, unique=True)
    status = Column(String)  # pending, success, failed
    created_at = Column(DateTime, default=datetime.utcnow)
