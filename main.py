from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn
from database import test_db_connection, init_db
from aptos_routes import router as aptos_router
from dataset_routes import router as dataset_router

# Initialize FastAPI app
app = FastAPI(
    title="Valynce API",
    description="Dataset Marketplace with Aptos Blockchain Integration",
    version="2.0.0"
)

# Test database connection and initialize on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Valynce API...")
    test_db_connection()
    init_db()
    print("✅ Database initialized!")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(aptos_router)
app.include_router(dataset_router)

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[datetime] = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

# In-memory storage (replace with database in production)
items_db: List[Item] = []
item_counter = 1

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning API information"""
    return {
        "message": "Welcome to Valynce - Dataset Marketplace",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "aptos": "/aptos",
        "datasets": "/api/datasets"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = test_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Valynce API",
        "database": "connected" if db_status else "disconnected"
    }

# Get all items
@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items"""
    return items_db

# Get item by ID
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Create new item
@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    """Create a new item"""
    global item_counter
    item.id = item_counter
    item.created_at = datetime.now()
    item_counter += 1
    items_db.append(item)
    return item

# Update item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate):
    """Update an existing item"""
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            updated_data = item_update.dict(exclude_unset=True)
            updated_item = item.copy(update=updated_data)
            items_db[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(idx)
            return {"message": f"Item {item_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
