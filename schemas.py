"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class CandyBox(BaseModel):
    """
    Candy boxes featuring natural Swedish sweets
    Collection name: "candybox"
    """
    title: str = Field(..., description="Box name")
    description: Optional[str] = Field(None, description="Short description of what's inside")
    price: float = Field(..., ge=0, description="Price in dollars")
    is_limited: bool = Field(False, description="If this is a limited edition box")
    tags: List[str] = Field(default_factory=list, description="Flavor and dietary tags like 'vegan', 'gluten-free'")
    image: Optional[str] = Field(None, description="Cover image URL")

class OrderItem(BaseModel):
    box_id: str = Field(..., description="CandyBox document id")
    quantity: int = Field(..., ge=1, description="How many of this box")

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    email: str = Field(..., description="Contact email")
    address: str = Field(..., description="Shipping address")
    items: List[OrderItem] = Field(..., description="List of boxes and quantities")
    notes: Optional[str] = Field(None, description="Optional gift note or delivery instructions")
    total: float = Field(..., ge=0, description="Order total amount")
    status: str = Field("pending", description="Order status: pending, confirmed, shipped, delivered")

# Note: The Flames database viewer can read these via /schema endpoint if exposed.
