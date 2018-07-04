# Model查询

## 关联关系查询

(Blog : Entry : Author ==> 1 : N : N)

django提供了支持数据库中JOIN语句的查询。

支持根据“1”一端对象条件查询“N”一端对象。

    # 查询blog的name为'Beathles Blog'的entry对象
    Entry.objects.filter(blog__name='Beatles Blog')

等价于

    SELECT e.* FROM entry e
    INNER JOIN blog b on e.blog_id = b.id
    WHERE b.name = 'Beatles Blog';

同样支持根据“N”一端对象条件查询“N”一端对象。

    # 查询至少包含一个满足headline包含'Lennon'的entry对象的blog对象
    Blog.objects.filter(entry__headline__contains='Lennon')

等价于

    SELECT b.* FROM entry e
    INNER JOIN blog b on e.blog_id = b.id
    WHERE e.headline LIKE '%Lennon%';

支持多个表相关联的查询。

    Blog.objects.filter(entry__authors__name='Lennon')

等价于

    SELECT * FROM entry e
    INNER JOIN blog b on e.blog_id = b.id

    WHERE e.headline LIKE '%Lennon%';


    Blog.objects.filter(entry__authors__name__isnull=True)

    Blog.objects.filter(entry__authors__isnull=False,
        entry__authors__name__isnull=True)