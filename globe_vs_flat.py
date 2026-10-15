#!/usr/bin/env python3
# p2j -o -t globe_vs_flat.ipynb globe_vs_flat.py
# jupyter lab globe_vs_flat.ipynb &
# p2j -o -t globe_vs_flat.ipynb globe_vs_flat.py
# jupyter nbconvert --to html --execute globe_vs_flat.ipynb

import math
import sympy as sp

def get_place_index(city_name, places):
    for i, (_, _, name) in enumerate(places):
        if name.lower() == city_name.lower():
            return i
    return None


def print_results_w_args(origin_name, dest_name):
    # Find indices for each city
    idx1 = get_place_index(origin_name, places)
    idx2 = get_place_index(dest_name, places)

    if idx1 is None:
        raise ValueError(f"Origin city '{origin_name}' not found.")
    if idx2 is None:
        raise ValueError(f"Destination city '{dest_name}' not found.")

    # Extract coordinates
    phi1_deg, lambda1_deg, _ = places[idx1]
    phi2_deg, lambda2_deg, _ = places[idx2]

    # Build substitution dictionary
    subs = {
        R: 6371.0,
        phi_1: math.radians(phi1_deg),
        lambda_1: math.radians(lambda1_deg),
        phi_2: math.radians(phi2_deg),
        lambda_2: math.radians(lambda2_deg)
    }

    # Compute distances and Print results
    flat_distance_km = flat_distance_eq.rhs.evalf(subs=subs)
    print(f"Flat Earth Model Distance ({origin_name} -> {dest_name}): {flat_distance_km:.2f} km")

    globe_distance_km = globe_distance_eq.rhs.evalf(subs=subs)
    print(f"Globe Model Distance ({origin_name} -> {dest_name}): {globe_distance_km:.2f} km")

# --------------------------------

# ## GLOBE
# Define symbolic variables for radius, departure (lat/long),
# and destination (lat/long)
R = sp.Symbol('R')
# Departure latitude & longitude
phi_1, lambda_1 = sp.symbols('phi_1 lambda_1')
# Destination latitude & longitude
phi_2, lambda_2 = sp.symbols('phi_2 lambda_2')

# Build the Haversine formula for spherical great-circle distance
d_haversine = 2 * R * sp.asin(
    sp.sqrt(
        sp.sin((phi_2 - phi_1) / 2)**2 +
        sp.cos(phi_1) * sp.cos(phi_2) * sp.sin((lambda_2 - lambda_1) / 2)**2
    )
)

# Define symbolic equation d = d_haversine
globe_distance_eq = sp.Eq(sp.Symbol('d'), d_haversine)
display(globe_distance_eq)

# --------------------------------

# ## FLAT
# Radial distance from North Pole to each point on a flat plane
r1 = R * (sp.pi / 2 - phi_1)
r2 = R * (sp.pi / 2 - phi_2)

# Flat Earth planar distance equation (Polar Law of Cosines)
d_flat = sp.sqrt(r1**2 + r2**2 - 2 * r1 * r2 * sp.cos(lambda_2 - lambda_1))
flat_distance_eq = sp.Eq(sp.Symbol('d_{flat}'), d_flat)
display(flat_distance_eq)

# --------------------------------

# # RESULTS

# To calculate $d$: surface distance in kilometers. based on 
# $\Delta\theta$: difference in degrees of latitude is
# $d = \Delta\theta \times \frac{\pi \times 6,371}{180}$,
# which simplifies to approximately
# $d \approx 111.19 \times \Delta\theta$ kilometers.

# ## Here's a boring agreement case:
places = [
    (59.9311, 30.3609, "St. Petersburg"),
    (-26.2041, 28.0473, "Johannesburg"),
    (-34.6037, -58.3816, "BuenosAires"),
    (-33.8688, 151.2093, "Sydney"),
    (48.8566, 2.3522, "Paris"),
    (-31.96035535624528, 115.89605085411458, "Perth"),
    (-30.2924414225275, 153.1208075182979, "CoffsHarbourAustralia"),
    (40.7128, -74.0060, "New York")
]
print_results_w_args("St. Petersburg", "Johannesburg")

# BOTH the Globe Model and the North Pole Azimuthal Equidistant 
# Projection (the exact map used as the standard Flat Earth model) 
# agree with each on distances where the  longitude is the same on 
# origin and destination.

# ## Now things get interesting, someone might be wrong ;)

print_results_w_args("Perth", "CoffsHarbourAustralia")

# That's a difference of about 5,068 km, meaning the flat-map route 
# is roughly 2.4 times longer.
# 
# If the flat-AE distance of 8,599 km were correct, that would 
# create a major problem:
# 
# * The Perth to Coffs Harbour itinerary would be longer than many 
# transcontinental and transoceanic routes.
# 
# * Airlines would need substantially more fuel than they actually 
# load.
# 
# * Published schedules would be impossible to maintain.
# 
# * GPS navigation and airline flight-management systems would 
# consistently fail to match reality.

# A Private Non-Stop Flights Perth-to-Coffs is actually nice, 
# because it # is entirely over land, removing the usual "maybe 
# they're taking a shortcut over the ocean" objection.

# If a Private Non-Stop Flight is too expensive, a zig zag route
# by car is 4030km, at which point the flat-brainers could say
# oh but the odometer is rigged.

# In the event we encounter the good ole'

# > "hur dur I can't do trigonometry and geometry."

# we would have to make a disc and globe model on the table.
# and put pins into them and measure the string to show how the
# string matches the math.

# at some point they have to admit that

# > "maps don't work"

# or

# > We use the spherical star system to measure distance across
# > the flat disc

# and let's not even mention the ice wall in Antarctica.

# ## Most people never get past the memes, We’re running code.
# This is what science actually looks like:

# - Define the model  
# - Compute its predictions  
# - Compare with reality  
# - See which model collapses

# We’re not just debating globe vs. flat models in the abstract.
# 
# We’re building actual mathematical models, running real 
# computations, and comparing real-world city pairs.
#  
# That’s the right way to approach any geometric claim: formalize 
# it, compute it, test it.


# On a flat AE map, the distance becomes absurdly large - often 
# **2× to 3×** the globe distance - which contradicts:
# 
# - flight times  
# - fuel loads  
# - airline economics  
# - known aircraft ranges

# --------------------------------

# P and S waves are the two main types of body waves generated
# inside the Earth during an Earthquake

# --------------------------------

# ## VISIBILITY OVER A SPHERE

# So we are going to build 2x towers on the water 8m higher than 
# the water around it each with an observer 2m eye level, how far 
# apart do we have to build them, such that they cannot see the 
# tower of the person, just the feet of the other observer.

# Let's Create a solution using 3 circles each with radius 6371km, 
# (6371km+18m), (6378km+20m)

R = sp.Symbol('R', positive=True)

h_eye = sp.Symbol('h_eye', positive=True)
h_tower = sp.Symbol('h_tower', positive=True)

# Horizon angles from Earth center
theta_eye = sp.acos(R / (R + h_eye))
theta_tower = sp.acos(R / (R + h_tower))

# Maximum visible arc distance
d_visible = R * (theta_eye + theta_tower)

visibility_eq = sp.Eq(sp.Symbol('d_visible'), d_visible)

display(visibility_eq)

subs = {
    R: 6371.0,
    h_eye: 0.006,     # 6 m
    h_tower: 0.004    # 4 m
}

print(
    f"Maximum separation before tower top disappears: "
    f"{visibility_eq.rhs.evalf(subs=subs):.3f} km"
)

# Basically if you travel 10miles from someone and you stand on top 
# of a ladder so your feet are 25ft from the ground, and your 
# friend is also on a ladder with his feet 25ft from the ground, 
# neither of you will be ablve to see anything below each others 
# feet.

# If the earth were flat you would be able to see the ladder.

# Heat haze makes things wavy, and mirages invert them. Neither 
# acts like a digital mask that cleanly deletes a 25-foot ladder 
# while leaving the human on top untouched and clearly visible.
 
# Physics bends light uniformly, not selectively.
