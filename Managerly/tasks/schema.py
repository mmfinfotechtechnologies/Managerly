import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from .models import Tasklist,Comment


class TaskType(DjangoObjectType):
    class Meta:
        model = Tasklist

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    tasklist = graphene.List(TaskType,id=graphene.Int())
    singletask = graphene.Field(TaskType, id=graphene.Int())
    usertask = graphene.List(TaskType,assigned_to=graphene.Int())
    viewcomment = graphene.List(CommentType, task_id=graphene.Int())


    def resolve_tasklist(self, info, **kwargs):
        return Tasklist.objects.all()

    def resolve_singletask(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Tasklist.objects.get(pk=id)

        return None

    def resolve_usertask(self, info, **kwargs):
        usertask = kwargs.get('assigned_to')
        if usertask is not None:
            return Tasklist.objects.all().filter(assigned_to=usertask)

        return None

    def resolve_viewcomment(self, info, **kwargs):
        id = kwargs.get('task_id')
        if id is not None:
            return Comment.objects.all().filter(task_id=id)

        return None

class CreateTask(graphene.Mutation):
    id = graphene.Int()
    task_name = graphene.String()
    task_description = graphene.String()
    start_date = graphene.types.datetime.Date()
    end_date = graphene.types.datetime.Date()
    assigned_by = graphene.Field(UserType)
    assigned_to = graphene.Field(UserType)
    status = graphene.Int()

    class Arguments:
        task_name = graphene.String()
        task_description = graphene.String()
        start_date = graphene.types.datetime.Date()
        end_date = graphene.types.datetime.Date()
        assigned_by = graphene.Int()
        assigned_to = graphene.Int()
        status = graphene.Int()

    def mutate(self, info, task_name, task_description,start_date,end_date,assigned_by,assigned_to,status):
        user = info.context.user or None

        tasklist = Tasklist(
            task_name=task_name,
            task_description=task_description,
            start_date=start_date,
            end_date=end_date,
            assigned_by=assigned_by,
            assigned_to=assigned_to,
            status=status
        )
        tasklist.save()

        return CreateTask(
            id=tasklist.id,
            task_name=tasklist.task_name,
            task_description=tasklist.task_description,
            start_date=tasklist.start_date,
            end_date=tasklist.end_date,
            assigned_by=tasklist.assigned_by,
            assigned_to=tasklist.assigned_to,
            status=tasklist.status
        )

class UpdateTask(graphene.Mutation):
    obj = graphene.Field(TaskType)
    id = graphene.Int()
    status = graphene.Int()

    class Arguments:
        id = graphene.Int()
        status = graphene.Int()

    def mutate(self, info,**kwargs):
        user = info.context.user or None
        id = kwargs.get('id')
        statusn = kwargs.get('status')
        obj = Tasklist.objects.get(pk=id)
        obj.status = statusn
        obj.save()

        return UpdateTask(
            id=obj.id,
            status=obj.status
        )

class AddComment(graphene.Mutation):
    task_id = graphene.Int()
    comment_by = graphene.Int()
    description = graphene.String()
    date = graphene.types.datetime.Date()

    class Arguments:
        task_id = graphene.Int()
        comment_by = graphene.Int()
        description = graphene.String()
        date = graphene.types.datetime.Date()

    def mutate(self, info, task_id, comment_by,description,date):
        user = info.context.user or None

        comment = Comment(
            task_id=task_id,
            comment_by=comment_by,
            description=description,
            date=date,
        )
        comment.save()

        return AddComment(
            task_id=comment.task_id,
            comment_by=comment.comment_by,
            description=comment.description,
            date=comment.date,
        )


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    add_comment = AddComment.Field()