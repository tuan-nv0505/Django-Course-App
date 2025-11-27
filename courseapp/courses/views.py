from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from courses import models, serializers, paginators, my_permissions


class CategoryView(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseView(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.ItemPaginator

    def get_queryset(self):
        query = self.queryset

        q = self.request.query_params.get("q")
        if q:
            query = query.filter(subject__icontains=q)

        category_id = self.request.query_params.get("category_id")
        if category_id:
            query = query.filter(category_id=category_id)

        return query

    @action(methods=['get'], url_path="lessons", detail=True)
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonView(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = models.Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonSerializer

    def get_permissions(self):
        if self.action == 'get_comments' and self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'post'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            s = serializers.CommentSerializer(data={
                'content': request.data.get('content'),
                'user': self.request.user.pk,
                'lesson': pk
            })
            s.is_valid(raise_exception=True)
            c = s.save()
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)


        comments = self.get_object().comment_set.select_related('user').filter(active=True)

        p = paginators.CommentPaginator()
        page = p.paginate_queryset(comments, self.request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return p.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)


class UserView(viewsets.ViewSet, generics.CreateAPIView):
     queryset = models.User.objects.filter(is_active=True)
     serializer_class = serializers.UserSerializer
     parser_classes = [parsers.MultiPartParser]

     @action(methods=['get', 'patch'], url_path='current-user', detail=False, permission_classes=[my_permissions.IsAuthenticated])
     def get_current_user(self, request):
         user = request.user
         if request.method.__eq__('PATCH'):
             for k, v in request.data.items():
                 setattr(user, k, v)
             user.save()
         return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)

class CommentView(viewsets.ViewSet, generics.DestroyAPIView):
    queryset = models.Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [my_permissions.CommentOwner]