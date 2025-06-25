from ninja import Router, Schema, NinjaAPI
from .models import Grocerydb
from .utils import generate_response 
from django.db import connection 

api = NinjaAPI()


@api.post("/generate/{userid}")
def generate_recipe(request, userid: int, prompt: str):
    data={
  "store": "FreshMart Supermarket",
  "location": "Downtown",
  "last_updated": "2025-06-25T09:15:00",
  "inventory": [
    {
      "item_id": "A101",
      "name": "Tomatoes",
      "category": "Vegetables",
      "quantity_in_stock": 120,
      "unit": "kg",
      "price_per_unit": 28.50
    },
    {
      "item_id": "A102",
      "name": "Bananas",
      "category": "Fruits",
      "quantity_in_stock": 80,
      "unit": "dozen",
      "price_per_unit": 55.00
    },
    {
      "item_id": "A103",
      "name": "Brown Bread",
      "category": "Bakery",
      "quantity_in_stock": 30,
      "unit": "pack",
      "price_per_unit": 45.00
    },
    {
      "item_id": "A104",
      "name": "Milk (1L)",
      "category": "Dairy",
      "quantity_in_stock": 200,
      "unit": "bottle",
      "price_per_unit": 48.00
    },
    {
      "item_id": "A105",
      "name": "Eggs",
      "category": "Poultry",
      "quantity_in_stock": 300,
      "unit": "piece",
      "price_per_unit": 6.00
    },
    {
      "item_id": "A106",
      "name": "Basmati Rice",
      "category": "Grains",
      "quantity_in_stock": 75,
      "unit": "kg",
      "price_per_unit": 110.00
    }
  ]
}
    response = generate_response(prompt, data["inventory"])
    record = Grocerydb.objects.create(
        userid=userid,
        input=prompt,
        output=response
    )
    return {
        "responseid": str(record.id),
        "output": response
    }


@api.get("/db-status")
def db_status(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        total_records = Grocerydb.objects.count()

        return {
            "database": "connected",
            "total_records": total_records
        }
    except Exception as e:
        return {
            "database": "error",
            "message": str(e)
        }