from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import timedelta
from apps.tracking.models import LocationModel
from apps.tracking.serializers.serializers import LocationSerializer
from apps.device.models import DeviceModel


class LocationViewSet(ModelViewSet):
    queryset = LocationModel.objects.all()
    serializer_class = LocationSerializer

    @action(detail=True, methods=['get'])
    def last_locations(self, request, pk=None):
        try:
            device = DeviceModel.objects.get(pk=pk)
        except DeviceModel.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get last 6 or fewer locations
        locations = LocationModel.objects.filter(device=device).order_by('-created_at')[:6]

        if not locations.exists():
            return Response({"error": "No location data available"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(locations, many=True)

        # Reverse to chronological order
        locs = list(locations)[::-1]

        if len(locs) > 1:
            # Average delta across consecutive pairs (smoother prediction)
            deltas = [
                (locs[i + 1].latitude - locs[i].latitude,
                 locs[i + 1].longitude - locs[i].longitude)
                for i in range(len(locs) - 1)
            ]

            avg_delta_lat = sum(d[0] for d in deltas) / len(deltas)
            avg_delta_lon = sum(d[1] for d in deltas) / len(deltas)

            last = locs[-1]

            predicted_lat = last.latitude + avg_delta_lat
            predicted_lon = last.longitude + avg_delta_lon

            predicted_location = {
                "latitude": predicted_lat,
                "longitude": predicted_lon,
                "thana": last.thana,
                "district": last.district,
                "accuracy": 10,  # Accuracy calculation (currently fixed at max = 10)
                "signal_strength": last.signal_strength,
                "network_type": last.network_type,
                "predicted_time": last.created_at + timedelta(seconds=10),
            }

        else:
            # Only one location → repeat same point
            last = locs[-1]
            predicted_location = {
                "latitude": last.latitude,
                "longitude": last.longitude,
                "thana": last.thana,
                "district": last.district,
                "accuracy": 10,  # Accuracy calculation (currently fixed at max = 10)
                "signal_strength": last.signal_strength,
                "network_type": last.network_type,
                "predicted_time": last.created_at + timedelta(seconds=10),
                "note": "Only one point available — no movement prediction possible",
            }

        return Response({
            "last_locations": serializer.data,
            "next_predicted_location": predicted_location
        }, status=status.HTTP_200_OK)
