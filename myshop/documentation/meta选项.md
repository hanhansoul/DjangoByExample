# Model Meta选项

- abstract
- app_label
- db_table
- get_latest_by
- managed
- order_with_respect_to
- ordering
- indexes
- unique_together
- index_together
- verbose_name 与 verbose_name_plural
- label 与 label_lower

## abstract

如果abstract为True，该model为抽象Model基类。

抽象Model基类不会创建数据库表和manager，同时也不能实例化或保存。其他Model类可以继承抽象基类，基类中的域可以被覆盖或删除。

抽象基类为数据库中的公有数据提供一种统一管理方式。

    class CommonInfo(models.Model):
        name = models.CharField(max_length=100)
        age = models.PositiveIntegerField()
        grades = models.IntegerField()

        class Meta:
            abstract = True

    class Student(CommonInfo):
        home_group = models.CharField(max_length=5)
        age = models.IntegerField() # 覆盖原field
        grades = None # 删除

## app_label

如果一个model没有在INSTALLED_APPS的任何一个应用中定义，则该model必须声明其属于哪一个应用。

## db_table

指定该model对应的数据库表名。model对应的默认表名为<app_name>_<model_name>。

## db_tablespace

指定该model对应的数据库tablespace。

## base_manager_name

指定model的_base_manager作为该model的基本manager。

## default_manager_name

指定model的_default_manager作为该model的默认manager。

## default_related_name

与该model外联关系的model中关联对象名，默认为<model_name>_set。

## get_latest_by

指明model的Manager.latest()和Manager.earliest()方法使用的一个或多个field名，一般为DateField、DateTimeField和InteregerField。

    # Latest by ascending order_date.
    get_latest_by = "order_date"

    # Latest by priority descending, order_date ascending.
    get_latest_by = ['-priority', 'order_date']

## managed

默认为True，表名django为负责管理该model对应数据库表的生命周期。

如果为False，表明django不会负责为该model创建或删除对应的数据库表，适用于数据库表已经存在的情况。

除此之外，managed的值不会影响对该model和数据库的其他操作。

## order_with_respect_to

设置model的一对多关系中ForeignKey对应model的排序操作，当设置了order_with_respect_to变量后，model生成两个
方法，get_<related>_order()和set_<related>_order()，分别用于返回排序后的ForeignKey对应的所有model和
设置model排序顺序。

    from django.db import models

    class Question(models.Model):
        text = models.TextField()
        # ...

    class Answer(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        # ...

        class Meta:
            order_with_respect_to = 'question'

    question = Question.objects.get(id=1)
    question.get_answer_order() # [1, 2, 3]
    question.set_answer_order([3, 1, 2])

同时为ForeignKey关联的model提供了两个方法，get_next_in_order()和get_previous_in_order()，用于有序遍历model。

    >>> answer = Answer.objects.get(id=2)
    >>> answer.get_next_in_order()
    <Answer: 3>
    >>> answer.get_previous_in_order()
    <Answer: 1>

## ordering

查询返回结果的排序顺序。

## permissions

除了添加、删除和修改，在权限表中添加额外的权限。

## default_permissions

默认为('add', 'change', 'delete')，指定django对该model对应数据库表的操作权限。

## proxy

如果proxy为True，该model为proxy model。

## required_db_features

## required_db_vendor

## select_on_save

默认为False，一般不需要设置。

该选项决定是否采用旧版本的Model.save()算法，旧算法使用select判断是否存在需要更新的行，新算法直接尝试使用update。

## indexes

为model定义索引列表。

    from django.db import models

    class Customer(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)

        class Meta:
            indexes = [
                models.Index(fields=['last_name', 'first_name']),
                models.Index(fields=['first_name'], name='first_name_idx'),
            ]

## unique_together

对多个域指定联合的unique约束，该属性是一个tuple，包含多个联合约束时通过其中多个不同的tuple指定。

    unique_together = (("driver", "restaurant"),)

ManyToManyField不能包含在unique_together中。

## index_together

对多个域指定联合索引，该属性是一个list，包含多个联合索引时通过其中多个不同的list指定。

    index_together = [
        ["pub_date", "deadline"],
    ]

## verbose_name 与 verbose_name_plural

verbose_name给定一个易于理解和表述的单数形式的model名称，默认值为按类名中的大写字母分隔。

verbose_name_plural与verbose_name类似，但是为复数形式。

## label 与 label_lower

label给定model对象路径名，返回app_label.object_name，如'polls.Question'。

label_lower与label类似，返回app_lavel.model_name，如'polls.question'。
