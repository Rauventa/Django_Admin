from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.api.filters import UserFilter, RestaurantFilter, RestaurantImageFilter, PlaceFilter, ReservationFilter
from core.api.serializers import UserSerializer, RestaurantSerializer, RestaurantImageSerializer, PlaceSerializer, \
    ReservationSerializer
from core.models import User, Restaurant, RestaurantImage, Place, Reservation


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    filter_class = UserFilter
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    @action(methods=['get'], detail=False)
    def me(self, *args, **kwargs):
        try:
            instance = self.get_object()
        except User.DoesNotExist:
            raise Http404
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['patch'], detail=False)
    def edit(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RestaurantViewSet(ModelViewSet):
    filter_class = RestaurantFilter
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class RestaurantImageViewSet(ModelViewSet):
    filter_class = RestaurantImageFilter
    queryset = RestaurantImage.objects.all()
    serializer_class = RestaurantImageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(restaurant__owner=self.request.user)


class PlaceViewSet(ModelViewSet):
    filter_class = PlaceFilter
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(restaurant__owner=self.request.user)


class ReservationViewSet(ModelViewSet):
    filter_class = ReservationFilter
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(restaurant__owner=self.request.user)
