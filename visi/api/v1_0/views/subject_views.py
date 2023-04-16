from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from visi.api.v1_0.serializers.subject_serializers import SubjectSerializer


class SubjectListCreateView(ListCreateAPIView):
    serializer_class = SubjectSerializer
    queryset = SubjectSerializer.Meta.model.objects.all()


class SubjectRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer
