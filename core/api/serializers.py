from rest_framework import serializers

from core.models import User, Restaurant, RestaurantImage, Place, Reservation


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    token = serializers.SerializerMethodField(source='get_token')

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'token')
        read_only_fields = ['email', 'id']

    def get_token(self, user):
        token = user.auth_tokens.first()
        if token:
            return token.key


class RestaurantImageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = RestaurantImage
        fields = ('id', 'restaurant', 'image', )


class RestaurantSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    images = RestaurantImageSerializer(many=True, read_only=True, source='restaurant_images')

    class Meta:
        model = Restaurant
        fields = ('id', 'owner', 'name', 'city', 'address', 'phone', 'images')


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Place
        fields = ('id', 'restaurant', 'hall_number', 'table_number', 'max_places', 'image', )


class ReservationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ('id', 'restaurant', 'place', 'reserved_at', 'created_at', 'phone', 'name', 'places', )

