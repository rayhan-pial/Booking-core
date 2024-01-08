from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework import serializers

from boat import models


class BoatSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Boat
        fields = [
            "highlight",
            "cancellation_policy",
            "longitude",
            "average_rating",
            "amenities",
            "boat_type",
            "latitude",
            "terms_Information",
            "discount",
            "description",
            "boat_name",
            "is_active",
            "boat_image",
            "owner",
            "location",
        ]
        read_only_fields = ("average_rating", 'location', )


class BoatBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatBooking
        fields = [
            "total_time",
            "booking_number",
            "total_cost",
            "total_day",
            "start_time",
            "star_date",
            "end_date",
            "customer",
            "boat",
            "ticket_type",
            'confirm_booking',
        ]
        read_only_fields = ('total_cost', 'booking_number', 'customer', "end_date", 'confirm_booking', )

    def validate(self, data):
        start_time = data.get('start_time')
        total_time = data.get('total_time')
        total_day = data.get('total_day')
        star_date = data.get('star_date')
        ticket_type = data.get('ticket_type')
        boat = data.get('boat')

        if start_time is None or star_date is None or ticket_type is None:
            raise serializers.ValidationError("Start date and end date are required.")
        if total_time == 0 and total_day == 0:
            raise serializers.ValidationError(
                "Either total time or total day is required. Please provide at least one.")
        elif total_time and total_day:
            raise serializers.ValidationError("You can only provide either total time or total day, not both.")
        if total_day and total_day > 0:
            end_date = star_date + timedelta(days=total_day)
            if models.BoatBooking.objects.filter(
                    Q(boat=boat, star_date__lte=star_date, end_date__gte=star_date) |
                    Q(boat=boat, star_date__lte=end_date, end_date__gte=end_date)
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError("The boat is already booked for the given time period.")
        if total_time and total_time > 0:
            # print("Roooooooooooooooooooooooooooooooo")
            total_hours = total_time + start_time.hour + start_time.minute / 60
            end_time = star_date + timedelta(hours=total_hours)
            # print("start",start_time)
            # print("===============================")
            # print("end",end_time)

            if models.BoatBooking.objects.filter(
                    Q(boat=boat, star_date=star_date) &
                    ((Q(start_time__lte=start_time, end_date__gte=start_time) |
                      Q(start_time__gte=start_time, end_date__lte=end_time)))
                ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError("The boat is already booked for the given time period.")

        # if total_time > 0:
        #     end_time = start_time + timedelta(hours=total_time)
        #     print(start_time)
        #     print("===============================")
        #     print(end_time)
        #     if models.BoatBooking.objects.filter(
        #             Q(boat=boat, star_date__lte=star_date, end_date__gte=star_date) |
        #             Q(boat=boat, star_date__lte=end_time, end_date__gte=end_time) |
        #             Q(boat=boat, star_date__gte=star_date, end_date__lte=end_time)
        #     ).exclude(pk=self.instance.pk if self.instance else None).exists():
        #         raise serializers.ValidationError("The boat is already booked for the given time period.")

        return data

        # start_time_str = start_time.strftime('%H:%M') if isinstance(start_time, datetime) else start_time
        #
        # parsed_time = datetime.strptime(start_time, '%H:%M').time()
        #
        # if not (0 <= parsed_time.hour <= 23) or not (0 <= parsed_time.minute <= 59):
        #     raise serializers.ValidationError(
        #         "Invalid start time. Hours must be in the range 0 to 23, and minutes must be in the range 0 to 59.")

#
#             start_datetime = datetime.combine(star_date, start_time.time())
#             end_datetime = start_datetime + datetime.timedelta(hours=total_time)
# # Have to use 2 exta fields in model start_datetime & end _datetime
#             overlapping_bookings = models.BoatBooking.objects.filter(
#                 boat=boat,
#                 star_date__lt=end_datetime,
#                 star_date__gt=start_datetime
#             ).exclude(pk=self.instance.pk if self.instance else None)
#
#             if overlapping_bookings.exists():
#                 raise serializers.ValidationError("This boat is already booked for the selected time range.")
#         return data


class BoatDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatDetails
        fields = [
            "length",
            "speed",
            "max_guest",
            "cabin",
            "boat",
        ]


class BoatFAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatFAQ
        fields = [
            "faq",
            "boat",
        ]


class BoatPricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatPricing
        fields = [
            "fixed_price",
            "extra_price",
            "price",
            "boat",
            "ticket_type",
        ]


class BoatReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatReview
        fields = [
            "rating",
            "review_time",
            "review",
            "customer",
            "boat",
        ]
        read_only_fields = ('customer', "review_time")

    def validate(self, data):

        rating = data.get('rating')
        boat = data.get('boat')

        if boat is None:
            raise serializers.ValidationError(" Rating and boat is required.")

        if (0 > rating or rating > 5):
            raise serializers.ValidationError(" Rating Must be positive integer and can not be more then 5")

        return data


class BoatSpecsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatSpecs
        fields = [
            "engines",
            "year",
            "fuel",
            "total_crew",
            "boat_model",
            "boat_skipper",
            "boat_manufacturer",
            "boat",
        ]


class BoatTicketTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BoatTicketType
        fields = [
            "is_active",
            "total_ticket",
            "ticket_type",
        ]
