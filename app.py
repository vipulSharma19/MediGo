""" Welcome, need to write logics for MEDIGO """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from your controller files
from controllers.delivery_controller import router as delivery_router
from controllers.delivery_person_controller import router as delivery_person_router
from controllers.order_controller import router as order_router
from controllers.payment_controller import router as payment_router
from controllers.store_controller import router as store_router
from controllers.user_controller import router as user_router
from controllers.entity_controller import router as entity_router  # Import Entity router

# Create FastAPI app
app = FastAPI(
    title="MediGo API",
    description="API for 11-minute medicine delivery system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(delivery_router, prefix="/deliveries", tags=["Deliveries"])
app.include_router(delivery_person_router, prefix="/delivery-persons", tags=["Delivery Persons"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(payment_router, prefix="/payments", tags=["Payments"])
app.include_router(store_router, prefix="/stores", tags=["Stores"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(entity_router, prefix="/entities", tags=["Entities"])  # Add Entity router
