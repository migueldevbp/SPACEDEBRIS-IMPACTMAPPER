import math

MT_TO_J = 4.184e15

def mass_from_diameter(d_m, density=3000):
    r = d_m / 2.0
    return (4.0 / 3.0) * math.pi * r**3 * density

def energy_joules(mass_kg, velocity_kms):
    v = velocity_kms * 1000.0
    return 0.5 * mass_kg * v**2

def energy_megatons(E_j):
    return E_j / MT_TO_J

def approx_crater_diameter(d_m, velocity_kms):
    C = 1.3
    return C * (d_m**0.78) * (velocity_kms**0.44)

def damage_radii_km(E_mt):
    base = E_mt**(1/3.0) if E_mt > 0 else 0
    return {
        "total_destroy": round(0.5 * base, 2),
        "serious_damage": round(2.0 * base, 2),
        "light_damage": round(10.0 * base, 2)
    }
