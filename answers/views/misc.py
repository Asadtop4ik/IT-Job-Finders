from rest_framework import viewsets, permissions
from answers.models import SmallWin
from answers.serializers import SmallWinSerializer
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter
class SmallWinViewSet(viewsets.ModelViewSet):
    queryset = SmallWin.objects.all()
    serializer_class = SmallWinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SmallWin.objects.filter(user=user)

    def get_period_queryset(self, period):
        user = self.request.user
        now = timezone.now()

        if period == 'week':
            start_date = now - timedelta(days=now.weekday())
        elif period == 'month':
            start_date = now.replace(day=1)
        elif period == 'year':
            start_date = now.replace(month=1, day=1)
        else:
            return SmallWin.objects.none()

        return SmallWin.objects.filter(user=user, date_created__gte=start_date)


    @extend_schema(
        parameters=[
            OpenApiParameter(name='period', description='Filter by period (week, month, year)', required=False, type=str),
        ]
    )
    def list(self, request, *args, **kwargs):
        period = request.query_params.get('period')
        if period:
            self.queryset = self.get_period_queryset(period)
        return super().list(request, *args, **kwargs)
