from rest_framework.views import APIView, status, Response
from django.forms.models import model_to_dict

from content.serializers import ContentSerializer
from .models import Content


class ContentView(APIView):
    def get(self, request):

        contents = Content.objects.all()

        content_dict = []

        for content in contents:
            c = model_to_dict(content)
            content_dict.append(c)

        return Response(
            content_dict,
        )

    def post(self, request):

        serializer = ContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class ContentByIDView(APIView):
    def get(self, request, content_id: int):

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not Found"})

        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_200_OK)

    def delete(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not Found"})

        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not Found"}.status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(content, key, value)
        content.save()

        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_200_OK)


class ContentSearchView(APIView):
    def get(self, request):
        name_param = request.query_params.get("title")

        contents = Content.objects.filter(title__icontains=name_param)

        filtered_content = [model_to_dict(content) for content in contents]

        return Response(filtered_content, status.HTTP_200_OK)
