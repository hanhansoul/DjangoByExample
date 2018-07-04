# Model查询

django支持数据库的各类增删查改操作。

为演示django中数据模型的各类操作，本指南通过以下若干model对象进行说明演示。

    from django.db import models

    class Blog(models.Model):
        name = models.CharField(max_length=100)
        tagline = models.TextField()

        def __str__(self):
            return self.name

    class Author(models.Model):
        name = models.CharField(max_length=200)
        email = models.EmailField()

        def __str__(self):
            return self.name

    class Entry(models.Model):
        blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
        headline = models.CharField(max_length=255)
        body_text = models.TextField()
        pub_date = models.DateField()
        mod_date = models.DateField()
        authors = models.ManyToManyField(Author)
        n_comments = models.IntegerField()
        n_pingbacks = models.IntegerField()
        rating = models.IntegerField()

        def __str__(self):
            return self.headline

## 创建对象

django中，每一个model类对应数据库中的一个表，而一个model对象则对应表中的一条记录。

通过构造函数创建一个model对象后，可通过该model对象的`save()`方法将该记录保存到数据库中。

    from blog.models import Blog
    b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    b.save()

以上命令将执行一条INSERT数据库命令，默认的`save()`方法没有返回值。

## 修改对象

在修改model对象的属性值后，调用`save()`方法可将修改保存到数据库中。

    b.name = 'New name'
    b.save()

以上命令将执行一条UPDATE数据库命令。

**无论是创建对象还是修改对象，在调用`save()`方法之前，django都不会对数据库进行操作**

## 修改保存`ForeignKey`与`ManyToManyField`属性

### ForeignKey

修改一个`ForeignKey`与修改一个普通的属性完全一样。

    from blog.models import Blog, Entry
    entry = Entry.objects.get(pk=1)
    cheese_blog = Blog.objects.get(name='Cheddar Talk')
    entry.blog = cheese_blog
    entry.save()

### ManyToManyField

修改一个`ManyToManyField`稍有不同，需要调用该属性的`add()`方法为记录增添一个新的关联关系记录。

    from blog.models import Author
    joe = Author.objects.create(name='Joe')
    entry.authors.add(joe)

当需要为`ManyToManyField`同时添加多条记录。

    john = Author.objects.create(name="John")
    paul = Author.objects.create(name="Paul")
    george = Author.objects.create(name="George")
    ringo = Author.objects.create(name="Ringo")
    entry.authors.add(john, paul, george, ringo)

## 查询返回对象

可通过model类的类属性`Manager`创建的一个`QuerySet`返回查询的对象。

`QuerySet`是一个从数据库返回的对象的集合，可以包含零个、一个或多个查询条件。

一个`QuerySet`等同于一条SELECT数据库语句，而查询条件则为WHERE或LIMIT。

model类通过类属性`Manager`返回`QuerySet`对象，每个model类至少包含一个`Manager`对象，默认的`Manager`对象名为`objects`。

    Blog.objects
    b = Blog(name='Foo', tagline='Bar')
    # error! 对象不包含Manager对象
    # b.objects

### 返回所有对象

`all()`方法返回表中的所有记录。

    all_entries = Entry.objects.all()

### 返回满足查询条件的对象

`filter(**kwargs)`方法返回一个包含满足给定条件的对象的`QuerySet`。

`exclude(**kwargs)`方法返回一个包含不满足给定条件的对象的`QuerySet`。

    Entry.objects.filter(pub_date__year=2006)
    # 等价
    Entry.objects.all().filter(pub_date__year=2006)

`QuerySet`支持链式调用。

    Entry.objects.filter(headline__startswith='What')
                .exclude(pub_date__get=datetime.date.today())
                .filter(pub_date__gte=datetime.date(2005, 1, 30))

每一次查询都会创建一个新的`QuerySet`对象，及`q1`、`q2`与`q3`是三个不同的对象。

    q1 = Entry.objects.filter(headline__startswith="What")
    q2 = q1.exclude(pub_date__gte=datetime.date.today())
    q3 = q1.filter(pub_date__gte=datetime.date.today())

`QuerySet`是懒加载的，即`q`仅在`print(q)`时才执行了一次数据库操作。

    q = Entry.objects.filter(headline__startswith="What")
    q = q.filter(pub_date__lte=datetime.date.today())
    q = q.exclude(body_text__icontains="food")
    print(q)

## 返回单个对象

`QuerySet`返回的是对象的一个集合，而`get()`方法可以返回满足条件的唯一一个对象。

    one_entry = Entry.objects.get(pk=1)

`get()`方法使用与`filter()`方法相同的查询条件。

当`get()`方法返回零条记录时，将抛出一个`DoesNotExist`异常。当`get()`方法返回超过一条记录时，将抛出`MultiplyObjectsReturned`异常。

## 限制查询返回记录数量

通过python的切片特性，可以实现LIMIT或OFFSET数据库语句。

    # 返回前5条记录
    Entry.objects.all()[:5]

    # 返回第6到第10条记录
    Entry.objects.all()[5:10]

python中负数索引此处并不适用。

一般对一个`QuerySet`进行返回一个新的`QuerySet`，但其并不会执行查询操作。但是当指定切片的step时，django将执行新的数据库查询操作。

    Entry.objects.all()[:10:2]

经过切片的`QuerySet`对象不支持进一步的`filter`或`exclude`等查询操作。

## 属性值查询

django为`filter()`、`exclude()`或`get()`函数提供了基本的查询参数，以实现WHERE语句功能。

基本的查询参数名形式为`field__loouptype=value`。

    Entry.objects.filter(pub_date__lte='2006-01-01')

等价于

    SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';

## 常用的查询参数名

### exact

精确匹配。

    Entry.objects.get(headline__exact='Cat bites dog')

等价于

    SELECT * FROM blog_entry WHERE headline = 'Cat bites dog'

`exact`类型查询为在不提供查询类型时的默认查询类型。

    Blog.objects.get(id__exact=14)

等价于

    Blog.objects.get(id=14)

## iexact

大小写不敏感的精确匹配。

## contains

大小写敏感的模糊匹配查询。`icontains`为大小写不敏感的模糊匹配查询。

    Entry.objects.get(headline__contains='Lennon')

等价于

    SELECT * FROM blog_entry WHERE headline LIKE '%Lennon%'

## startswith 与 endswith

字符串前缀与后缀模糊匹配查询。
