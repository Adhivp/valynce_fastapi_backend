"""
Seed database with fake data
"""
from database import SessionLocal, init_db
from models import User, Dataset, License, Transaction
from datetime import datetime, timedelta
import random

def seed_database():
    """Populate database with fake data"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Transaction).delete()
        db.query(License).delete()
        db.query(Dataset).delete()
        db.query(User).delete()
        db.commit()
        
        # Create fake users
        users = [
            User(
                wallet_address="0x203e9bf58c965f98b788b20732faaf8dc135a827c2803935e623718226722964",
                username="alice_researcher",
                email="alice@valynce.com"
            ),
            User(
                wallet_address="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                username="bob_data_scientist",
                email="bob@valynce.com"
            ),
            User(
                wallet_address="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
                username="carol_ml_engineer",
                email="carol@valynce.com"
            ),
            User(
                wallet_address="0x9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba",
                username="david_analyst",
                email="david@valynce.com"
            ),
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # Create fake datasets
        datasets_data = [
            {
                "title": "Global Climate Data 2024",
                "description": "Comprehensive climate dataset including temperature, precipitation, and atmospheric data from 10,000+ weather stations worldwide. Updated daily with ML-ready features.",
                "category": "Climate",
                "file_hash": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG",
                "ipfs_uri": "ipfs://QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG",
                "price_apt": 5.5,
                "per_query_price": 0.01,
                "size_mb": 2500.5,
                "format": "CSV, Parquet",
                "tags": "climate,weather,temperature,ml-ready",
                "downloads": 156
            },
            {
                "title": "Medical Imaging Dataset - X-Ray",
                "description": "50,000 annotated chest X-ray images for disease detection. Includes labels for pneumonia, tuberculosis, and normal cases. HIPAA-compliant and de-identified.",
                "category": "Healthcare",
                "file_hash": "QmT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhCxX",
                "ipfs_uri": "ipfs://QmT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhCxX",
                "price_apt": 12.0,
                "per_query_price": 0.05,
                "size_mb": 8450.2,
                "format": "PNG, JSON",
                "tags": "medical,xray,healthcare,ai,computer-vision",
                "downloads": 89
            },
            {
                "title": "Financial Market Data - S&P 500",
                "description": "Historical stock data for all S&P 500 companies (2000-2024). Includes OHLCV, technical indicators, and fundamental data. Perfect for algorithmic trading models.",
                "category": "Finance",
                "file_hash": "QmZkJLbBnqWvTxh4iqMXZfwL8yGjPKvMjz3NxQsXKjPmC7",
                "ipfs_uri": "ipfs://QmZkJLbBnqWvTxh4iqMXZfwL8yGjPKvMjz3NxQsXKjPmC7",
                "price_apt": 8.75,
                "per_query_price": 0.02,
                "size_mb": 1850.0,
                "format": "CSV, JSON",
                "tags": "finance,stock-market,trading,time-series",
                "downloads": 234
            },
            {
                "title": "Natural Language Dataset - Reddit Comments",
                "description": "10 million Reddit comments from 2023 across 500+ subreddits. Pre-processed and cleaned for NLP tasks. Includes sentiment labels and topic categories.",
                "category": "NLP",
                "file_hash": "QmPJM9vkpzYHxLKj8NqWnBvT5RcG3XmF4PqKzNxWnPbdG",
                "ipfs_uri": "ipfs://QmPJM9vkpzYHxLKj8NqWnBvT5RcG3XmF4PqKzNxWnPbdG",
                "price_apt": 6.25,
                "per_query_price": 0.015,
                "size_mb": 4200.8,
                "format": "JSON, TXT",
                "tags": "nlp,text,sentiment,social-media",
                "downloads": 178
            },
            {
                "title": "Autonomous Vehicle Sensor Data",
                "description": "LiDAR, camera, and radar data from 1000+ hours of urban driving. Annotated for object detection, lane detection, and semantic segmentation. Self-driving AI training ready.",
                "category": "Computer Vision",
                "file_hash": "QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco",
                "ipfs_uri": "ipfs://QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco",
                "price_apt": 15.0,
                "per_query_price": 0.08,
                "size_mb": 12500.0,
                "format": "PCD, PNG, JSON",
                "tags": "autonomous,lidar,computer-vision,self-driving",
                "downloads": 67
            },
            {
                "title": "E-Commerce Customer Behavior Dataset",
                "description": "5 million customer transactions, browsing patterns, and purchase history. Includes demographics, session data, and conversion metrics for recommendation systems.",
                "category": "E-Commerce",
                "file_hash": "QmRn4CzT8vkpzYHxLKj8NqWnBvT5RcG3XmF4PqKzNxWnP",
                "ipfs_uri": "ipfs://QmRn4CzT8vkpzYHxLKj8NqWnBvT5RcG3XmF4PqKzNxWnP",
                "price_apt": 4.5,
                "per_query_price": 0.01,
                "size_mb": 1200.5,
                "format": "CSV, Parquet",
                "tags": "ecommerce,recommendation,customer,analytics",
                "downloads": 312
            },
            {
                "title": "Protein Structure Database",
                "description": "3D protein structures for 100,000+ proteins with functional annotations. Ideal for drug discovery and bioinformatics research. AlphaFold predictions included.",
                "category": "Bioinformatics",
                "file_hash": "QmWrT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhC",
                "ipfs_uri": "ipfs://QmWrT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhC",
                "price_apt": 10.0,
                "per_query_price": 0.04,
                "size_mb": 6800.3,
                "format": "PDB, JSON",
                "tags": "bioinformatics,protein,drug-discovery,3d",
                "downloads": 45
            },
            {
                "title": "Satellite Imagery - Urban Development",
                "description": "High-resolution satellite images of 50 major cities (2020-2024). Perfect for urban planning, change detection, and land use classification models.",
                "category": "Geospatial",
                "file_hash": "QmYkJLbBnqWvTxh4iqMXZfwL8yGjPKvMjz3NxQsXKjPmC",
                "ipfs_uri": "ipfs://QmYkJLbBnqWvTxh4iqMXZfwL8yGjPKvMjz3NxQsXKjPmC",
                "price_apt": 18.5,
                "per_query_price": 0.1,
                "size_mb": 15000.0,
                "format": "GeoTIFF, JSON",
                "tags": "satellite,geospatial,urban,remote-sensing",
                "downloads": 92
            },
        ]
        
        for i, ds_data in enumerate(datasets_data):
            dataset = Dataset(
                owner_id=users[i % len(users)].id,
                nft_minted=random.choice([True, False]),
                blockchain_tx=f"0x{''.join(random.choices('0123456789abcdef', k=64))}" if random.choice([True, False]) else None,
                **ds_data
            )
            db.add(dataset)
        
        db.commit()
        
        # Create some fake licenses
        all_datasets = db.query(Dataset).all()
        all_users = db.query(User).all()
        
        for _ in range(15):
            user = random.choice(all_users)
            dataset = random.choice(all_datasets)
            
            # Don't let user license their own dataset
            if user.id == dataset.owner_id:
                continue
            
            license = License(
                user_id=user.id,
                dataset_id=dataset.id,
                license_type=random.choice([0, 1, 2]),
                expires_at=datetime.utcnow() + timedelta(days=random.randint(30, 365)) if random.choice([True, False]) else None,
                transaction_hash=f"0x{''.join(random.choices('0123456789abcdef', k=64))}",
                price_paid=dataset.price_apt
            )
            db.add(license)
        
        db.commit()
        
        # Create some fake transactions
        for _ in range(20):
            tx = Transaction(
                from_address=random.choice(all_users).wallet_address,
                to_address=random.choice(all_users).wallet_address,
                amount_apt=round(random.uniform(0.1, 20.0), 2),
                transaction_type=random.choice(["mint", "purchase", "royalty"]),
                blockchain_hash=f"0x{''.join(random.choices('0123456789abcdef', k=64))}",
                status=random.choice(["success", "success", "success", "pending"])
            )
            db.add(tx)
        
        db.commit()
        
        print("✅ Database seeded with fake data!")
        print(f"   - {len(users)} users")
        print(f"   - {len(datasets_data)} datasets")
        print(f"   - ~15 licenses")
        print(f"   - ~20 transactions")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("\nSeeding database...")
    seed_database()
