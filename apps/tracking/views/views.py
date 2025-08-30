from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now, timedelta
from apps.tracking.models import LocationModel
from drf_spectacular.utils import extend_schema
from apps.tracking.serializers.serializers import LocationSerializer
from apps.device.models import DeviceModel
from external.pagination import CustomPagination
import math

@extend_schema(tags=['Tracking'])
class LocationViewSet(ModelViewSet):
    queryset = LocationModel.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_next_location(self, request):

        try:
            device = DeviceModel.objects.get(user=request.user)
        except DeviceModel.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the last ≤6 locations of the device
        locations = LocationModel.objects.filter(device=device).order_by('-created_at')[:6]

        if not locations.exists():
            return Response({"error": "No location data available"}, status=status.HTTP_404_NOT_FOUND)

        # Reverse into chronological order
        locs = list(locations)[::-1]

        if len(locs) > 1:
            # Calculate average delta between consecutive locations
            deltas = [
                (locs[i + 1].latitude - locs[i].latitude,
                 locs[i + 1].longitude - locs[i].longitude)
                for i in range(len(locs) - 1)
            ]

            avg_delta_lat = sum(d[0] for d in deltas) / len(deltas)
            avg_delta_lon = sum(d[1] for d in deltas) / len(deltas)

            last = locs[-1]

            next_lat = last.latitude + avg_delta_lat
            next_lon = last.longitude + avg_delta_lon

            # Compute simple "accuracy" using Euclidean distance
            distance_error = math.sqrt((next_lat - last.latitude)**2 + 
                                       (next_lon - last.longitude)**2)
            # Convert to 1-10 scale: smaller distance → higher accuracy
            accuracy = max(1, min(10, 10 - distance_error*10))  # tweak scale factor if needed

            next_location = {
                "device": device,
                "latitude": next_lat,
                "longitude": next_lon,
                "thana": last.thana,
                "district": last.district,
                "accuracy": round(accuracy, 2),
                "signal_strength": last.signal_strength,
                "network_type": last.network_type,
                "created_at": last.created_at + timedelta(seconds=10), 
            }

        else:
            # Only one location -> repeat same point
            last = locs[-1]
            next_location = {
                "device": device,
                "latitude": last.latitude,
                "longitude": last.longitude,
                "thana": last.thana,
                "district": last.district,
                "accuracy": 10,  # single point → perfect match
                "signal_strength": last.signal_strength,
                "network_type": last.network_type,
                "created_at": now(),
            }

        serializer = self.serializer_class(data=next_location)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(next_location, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
