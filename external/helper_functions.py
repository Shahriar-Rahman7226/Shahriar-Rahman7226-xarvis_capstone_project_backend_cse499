import math
from django.utils import timezone

SLOT_SECONDS = 10

def slot_of(dt):
    # 10s time buckets; uses server time
    return int(dt.timestamp()) // SLOT_SECONDS

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    to_rad = math.pi / 180.0
    dlat = (lat2 - lat1) * to_rad
    dlon = (lon2 - lon1) * to_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1*to_rad)*math.cos(lat2*to_rad)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def match_percent(distance_m, good=25.0, bad=200.0):
    # 100% if ≤good m, 0% if ≥bad m; linear between
    if distance_m <= good: return 100
    if distance_m >= bad:  return 0
    return int(round(100 * (1 - (distance_m - good) / (bad - good))))
