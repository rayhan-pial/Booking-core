from rest_framework import serializers

from space import models


class SpaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Space
        fields = [
            "space_name",
            "amenities",
            "latitude",
            "is_active",
            "average_rating",
            "description",
            "longitude",
            "space_image",
            "space_type",
            "highlights",
            "discount",
            "owner",
            "location",
        ]
        read_only_fields = ("average_rating", "location", )


class SpaceBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpaceBooking
        fields = [
            "booking_number",
            "star_date",
            "total_cost",
            "end_date",
            "customer",
            "space",
            "ticket_type",
            "ticket_quantity",
            "confirm_booking"
        ]
        read_only_fields = ('total_cost', 'booking_number', 'customer', 'confirm_booking', )

    def validate(self, data):

        start_date = data.get('star_date')
        end_date = data.get('end_date')
        ticket_type = data.get('ticket_type')
        ticket_quantity = data.get('ticket_quantity')
        space = data.get('space')

        if start_date is None or end_date is None or space is None or ticket_type is None or ticket_quantity is None:
            raise serializers.ValidationError(" required.")

        if end_date < start_date:
            raise serializers.ValidationError("End date must be equal to or after the start date.")

        overlapping_bookings = models.SpaceBooking.objects.filter(
            space=space,
            end_date__gte=start_date,
            star_date__lte=end_date
        ).exclude(pk=self.instance.pk if self.instance else None)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This space is already booked during the specified time.")

        return data


class SpaceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpaceDetails
        fields = [
            "is_active",
            "total_bed",
            "total_bathroom",
            "max_people",
            "size",
            "space",
        ]


class SpaceFAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpaceFAQ
        fields = [
            "faq",
            "space",
        ]


class SpacePricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpacePricing
        fields = [
            "extra_price",
            "fixed_price",
            "price",
            "space",
            "ticket_type",
        ]


class SpaceReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpaceReview
        fields = [
            "rating",
            "review",
            "review_time",
            "customer",
            "space",
        ]
        read_only_fields = ('customer', "review_time")

    def validate(self, data):

        rating = data.get('rating')
        space = data.get('space')

        if space is None:
            raise serializers.ValidationError(" Rating and space is required.")

        if (0 > rating or rating > 5):
            raise serializers.ValidationError(" Rating Must be positive integer and can not be more then 5")

        return data


class SpaceTicketTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SpaceTicketType
        fields = [
            "is_active",
            "ticket_type",
        ]
