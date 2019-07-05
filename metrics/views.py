from django.shortcuts import render
from rest_framework import viewsets, generics
from metrics.models import Metrics
# from metrics.serializers import MetricSerializer

# from metrics.models import Metrics
from rest_framework import serializers

from django_filters import rest_framework as filters
from django.db.models import Sum

VALID_GROUPBY_FIELDS = ('date','channel','country','os')
VALID_SHOW_FIELDS = ('impressions', 'clicks', 'installs', 'spend', 'revenue')

class MetricsFilters(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')
    # date = filters.DateFromToRangeFilter()
    sort = filters.OrderingFilter(
        # Enable all fields in models to be used in sorting 
        fields = tuple((field.name, field.name) for field in Metrics._meta.fields)
    )
    group_by = filters.CharFilter(method='groupby_filter')
    show = filters.CharFilter(method='show_filter')
    
    def show_filter(self, queryset, name, value):
        """
        Pass queryset forward. 
        show filter is used to simply keeps query_params in self.data
        """
        return queryset

    def groupby_filter(self, queryset, name, value):
        groupby_fields = value.split(',')
        groupby_fields = [x for x in groupby_fields if x in VALID_GROUPBY_FIELDS]
    
        show_params = self.data.get('show', None)
        show_fields = []    # fields to sum
        if show_params is not None:
            show_fields = [x for x in show_params.split(',') if x in VALID_SHOW_FIELDS]
        if len(show_fields) == 0:
            show_fields = VALID_SHOW_FIELDS
        # valid field for sort should be the union of groupby and show
        valid_sort_fields = list(set(show_fields) | set(groupby_fields))

        sort_params = self.data.get('sort', None)
        sort_fields = []
        if sort_params is not None:
            sort_fields = [x for x in sort_params.split(',') if x.lstrip('-') in valid_sort_fields]
        if len(sort_fields) == 0:
            sort_fields = show_fields[:1]

        qs = queryset
        if len(groupby_fields) != 0:
            qs = qs.values(*groupby_fields).order_by(*groupby_fields)\
            .annotate(**{key:Sum(key) for key in show_fields})

            # re-sort the queryset because after group by the original sort will be invalid
            qs = qs.order_by(*sort_fields)
        return qs

    class Meta:
        model = Metrics
        fields = ('channel', 'country', 'os', 'date_from', 'date_to', 'sort')

class MetricSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        """For every field set required=False"""
        super(MetricSerializer, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    class Meta:
        model = Metrics
        fields = '__all__'

# Create your views here.
class MetricsView(generics.ListAPIView):
    queryset = Metrics.objects.all()
    serializer_class = MetricSerializer
    filterset_class = MetricsFilters