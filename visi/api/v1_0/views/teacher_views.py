from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from visi.api.v1_0.serializers.teacher_serializers import TeacherSerializer


class TeacherListCreateView(ListCreateAPIView):
    serializer_class = TeacherSerializer
    queryset = TeacherSerializer.Meta.model.objects.all()


class TeacherRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer
