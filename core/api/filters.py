from django_filters import rest_framework as filters

from core.models import User, Restaurant, RestaurantImage, Place, Reservation


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', )


class RestaurantFilter(filters.FilterSet):
    class Meta:
        model = Restaurant
        fields = ('id', 'owner', 'name', 'city', 'address', 'phone', )


class RestaurantImageFilter(filters.FilterSet):
    class Meta:
        model = RestaurantImage
        fields = ('id', 'restaurant', )


class PlaceFilter(filters.FilterSet):
    class Meta:
        model = Place
        fields = ('id', 'restaurant', 'hall_number', 'table_number', 'max_places', )


class ReservationFilter(filters.FilterSet):
    class Meta:
        model = Reservation
        fields = ('id', 'restaurant', 'place', 'reserved_at', 'created_at', 'phone', 'name', 'places', )
