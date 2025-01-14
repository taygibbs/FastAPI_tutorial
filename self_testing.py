# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 22:37:35 2025

@author: tayta
"""

from fastAPI import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    

inventory = {}

@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {'Error': 'Item ID already exists!'}
    inventory[item_id] = item
    return inventory[item_id] #to show that something did get added.