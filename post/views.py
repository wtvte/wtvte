from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from post.serializers import PostSerializers


class PostListAPIView(APIView):
    def get(self, request):
        post = Post.objects.all()
        serializer = PostSerializers(post, many=True)
        return Response(serializer.data)


class PostCreateAPIView(APIView):
    def post(self, request):
        req_data = request.data
        # Post.objects.create(req_data)
        print(req_data)
        if 'image' in req_data.keys():
            image = req_data['image']
        else:
            image = None
        Post.objects.create(
            title=req_data['title'],
            content=req_data['content'],
            image=image,
            user=request.user
        )
        return Response({"post": "created"}, status=status.HTTP_200_OK)


class PostUpdateAPIView(APIView):
    def put(self, request):
        pk = request.data["pk"]
        if not pk:
            return Response({"error": "pk is required"}, status=404)
        try:
            instance = Post.objects.get(id=pk)
        except:
            return Response({"error": "object does not exists"})
        if request.user == instance.user:
            serializer = PostSerializers(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"post": serializer.data})


class PostDestroyAPIView(APIView):
    # permission_classes = []
    # authentication_classes = []

    def delete(self, request, pk=None):
        pk = request.data["pk"]
        if not pk:
            return Response({"error": "pk is required"}, status=404)
        try:
            instance = Post.objects.get(id=pk)
            instance.delete()
        except:
            if request.user == instance.user:
                return Response({"error": "object does not exists"})
                return Response({"post": f"post with id = {pk} deleted"})


class PostRetrieveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        post = Post.objects.get(id=request.data["pk"])
        serializer = PostSerializers(post)
        return Response(serializer.data)


