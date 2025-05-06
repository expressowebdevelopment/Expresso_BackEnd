from fastapi import FastAPI, Depends
from app.expresso import exp_expresso_user_route
from app.store import store_routes
from app.open import open_routes
from app.customer import customer_route
from app.core.db import create_table
from app.auth import auth_routes
from fastapi.middleware.cors import CORSMiddleware
from app.common.utils.auth_utils import verify_token, restrict_users_for


app = FastAPI()


# ✅ Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    # Replace with ["http://localhost:5500"] or your frontend URL if needed
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await create_table()


common_dependency = [Depends(verify_token), Depends(restrict_users_for)]

app.include_router(auth_routes.router)
app.include_router(open_routes.router)
app.include_router(customer_route.router, dependencies=common_dependency)
app.include_router(store_routes.router, dependencies=common_dependency)
app.include_router(exp_expresso_user_route.router,
                   dependencies=common_dependency)


@app.get("/")
def read_root():
    return {"Hello": "World"}
