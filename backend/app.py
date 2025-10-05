from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

app = FastAPI()

# Habilitar CORS para permitir que el frontend (localhost:5500) acceda al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a ["http://127.0.0.1:5500"] si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class ImpactRequest(BaseModel):
    diameter_m: float
    density: float
    velocity_kms: float
    angle_deg: float
    lat: float
    lon: float

@app.post("/simulate")
def simulate(request: ImpactRequest):
    # Cálculo de energía cinética (esto está correcto)
    radius = request.diameter_m / 2
    volume = (4/3) * math.pi * (radius**3)
    mass = volume * request.density
    velocity_ms = request.velocity_kms * 1000
    energy = 0.5 * mass * velocity_ms**2

    # ✅ RADIOS DE DAÑO CORREGIDOS - coeficientes 100x más pequeños
    energy_cubic_root = energy ** (1/3)
    radii = {
        "total_destroy": round(0.00005 * energy_cubic_root, 2),
        "severe_damage": round(0.0001 * energy_cubic_root, 2),
        "light_damage": round(0.0002 * energy_cubic_root, 2),
    }

    return {
        "energy_joules": energy,
        "radii_km": radii,
        "location": {"lat": request.lat, "lon": request.lon},
    }

@app.get("/")
def root():
    return {"message": "API funcionando 🚀"}
