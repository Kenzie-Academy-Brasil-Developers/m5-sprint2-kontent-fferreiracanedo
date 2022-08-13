from rest_framework.views import APIView, status, Response, Request
from django.forms.models import model_to_dict

from .validators import ContentSerializer
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

    def post(self, request: Request):

        serializer = ContentSerializer(**request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        saveOnDb = Content.objects.create(**serializer.data)
        saveOnDb_dict = model_to_dict(saveOnDb)
        return Response(saveOnDb_dict, status.HTTP_201_CREATED)


class ContentByIDView(APIView):
    def get(self, request, content_id: int):

        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not Found"}, status.HTTP_404_NOT_FOUND)

        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_200_OK)

    def delete(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not Found"}, status.HTTP_404_NOT_FOUND)

        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"message": "Content not Found"}, status.HTTP_404_NOT_FOUND)

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
