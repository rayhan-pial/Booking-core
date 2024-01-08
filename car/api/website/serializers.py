from datetime import timezone

from rest_framework import serializers

from car import models


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Car
        fields = [
            "car_image",
            "description",
            "car_features",
            "is_active",
            "car_name",
            "car_type",
            "discount",
            "highlight",
            "longitude",
            "latitude",
            "average_rating",
            "owner",
            "location",

        ]
        read_only_fields = ('average_rating', "location", )


class CarBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarBooking
        fields = [
            "end_date",
            "star_date",
            "total_cost",
            "quantity",
            "booking_number",
            "car",
            "customer",
            "confirm_booking",
        ]
        read_only_fields = ('total_cost', 'booking_number', 'customer', "confirm_booking",)

    def validate(self, data):

        start_date = data.get('star_date')
        end_date = data.get('end_date')
        car = data.get('car')

        if start_date is None or end_date is None:
            raise serializers.ValidationError("Start date and end date are required.")

        if end_date < start_date:
            raise serializers.ValidationError("End date must be equal to or after the start date.")

        overlapping_bookings = models.CarBooking.objects.filter(
            car=car,
            end_date__gte=start_date,
            star_date__lte=end_date
        ).exclude(pk=self.instance.pk if self.instance else None)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This car is already booked during the specified time.")

        return data


class CarDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarDetails
        fields = [
            "gear_shift",
            "door",
            "total_passengers",
            "baggage",
            "car",
        ]


class CarFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarFAQ
        fields = [
            "faq",
            "car",
        ]


class CarPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarPricing
        fields = [
            "price",
            "fixed_price",
            "extra_price",
            "car",
        ]


class CarReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarReview
        fields = [
            "review",
            "review_time",
            "rating",
            "car",
            "customer",
        ]
        read_only_fields = ('customer', "review_time")

    def validate(self, data):

        rating = data.get('rating')
        car = data.get('car')

        if car is None:
            raise serializers.ValidationError(" Rating and car is required.")

        if (0 > rating or rating > 5):
            raise serializers.ValidationError(" Rating Must be positive integer and can not be more then 5")

        return data

    # def validate(self, data):
    #     customer = self.context.get('request')
    #     # customer = user.customer if hasattr(user, 'customer') else None
    #     #
    #     # if not customer:
    #     #     raise serializers.ValidationError("User is not a customer")
    #
    #     # Check if the customer has booked the car
    #     car_id = data.get("car").id
    #     if not models.CarBooking.objects.filter(customer=customer, car_id=car_id).exists():
    #         raise serializers.ValidationError("Customer has not booked this car")
    #
    #     # Set review_time as the current time
    #     data["customer"] = customer
    #     data["review_time"] = timezone.now()
    #
    #     return data

    # def validate(self, data):
    #
    #     review = data.get('review')
    #     rating = data.get('rating')
    #     car = data.get('car')
    #
    #
    #     if end_date < start_date:
    #         raise serializers.ValidationError("End date must be equal to or after the start date.")
    #
    #     overlapping_bookings = models.CarBooking.objects.filter(
    #         car=car,
    #         end_date__gte=start_date,
    #         star_date__lte=end_date
    #     ).exclude(pk=self.instance.pk if self.instance else None)
    #
    #     if overlapping_bookings.exists():
    #         raise serializers.ValidationError("This car is already booked during the specified time.")
    #
    #     return data
