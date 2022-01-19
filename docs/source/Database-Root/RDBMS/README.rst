RDBMS ORM 中的常见问题
==============================================================================


N + 1 问题
------------------------------------------------------------------------------

N + 1 是 ORM (对象关系映射) 关联数据中存在的一个问题.

比如一个 Customer 和 Order 是 1 对多的关系. 一个 Customer 可能曾经下过很多 Order. 在 Order 表中则会有一个 customer_id 的外键与 Customer 表相连.

在查询的时候如果你要查询一个用户以及这个用户下过的所有 Order. 很多新手犯 "在循环中进行查询" 的错误. 也就是先获得 User 对象, 然后遍历 ``user.orders`` 获得 order 的信息. 这样会消耗 1 个 query 在 User 上, 以及 N 个 query 在每个不同的 Order 上, 这其实应该叫 1 + N 问题. 很显然该操作只需要一个简单的 JOIN 即可搞定, 但是在 ORM 中有没有不用写 Join, 还是用这样的语法但是底层却是用 JOIN 来搞定呢? 答案是肯定的.

.. code-block:: python

    user = User.get(id=1)
    for order in user.orders:
        ...

通常各种 ORM 框架对于 N + 1 会有优化, 各种框架的优化方案是不同的. 比如有的框架是在你查询 User 的时候你可以指定想要关联的列. 例如 ``User.get(id=1).with(Order.id)`` (这是伪代码)


Inheritance in the Database
------------------------------------------------------------------------------
在 OOP 中, 继承是非常常用的概念, 但是在 ORM 中实现类的继承的方法并不唯一, 我们来介绍一下这些常用的方法以及优劣.

举例:

.. code-block:: python

    class Person:
        name: str

    class Student(Person):
        program: str

    class Teacher(Person):
        department: str

**1. 单表继承 (Single Table Inheritance)**.

简单来说就是一个表的所有的列是所有父类和子类的属性的并集(总和), 从表的角度看就是这样::

    person
    |--- name: str
    |--- student_program: str
    |--- teacher_department: str
    ...

优点就是简单, 缺点就是对于很多对象是用不到很多列的, 会造成很多列是 NULL, 造成存储浪费. 并且可能最后由于子类的变种很多, 最后一个表有几百列, 难以管理, 甚至达到了数据库的上限.

在该实现中如果你从数据库直接查询一个行而不是通过 ORM 框架查, 你是不知道这一行到底是哪个类的. 所以通常我们会预留一个特殊的列用来表示这一行到底是属于哪个类.

适用场景: 类的总数不多, 总行数不多, 继承扩展的属性不多的情况.

**2. 扩展表 (Class Table Inheritance)**.

每个类单独创建一个表. 例如 ``person``, ``person_student``, ``person_teacher``. 但是每个表只保存他与父类相比多出来的那些列 以及 foreign key 的列.

优点是节约空间, 没有冗余. 缺点是为了查询一个对象, 需要用到 JOIN, 如果是单个继承则是 1 个 JOIN, 如果是多重继承则是多个 JOIN.

适用场景: 继承体系复杂, 结构容易变, 最大程度减少数据冗余的情景.

**3. 具体表 (Concrete Table Inheritance)**.

每个类单独一个表, 并且保存该类的全部属性, 包括父类中的属性. 本质上各个类从数据库的角度看并没有关联, 在数据库迁徙的时候会比较容易, 缺点就是冗余量非常大.

适用场景: 继承关系不复杂, 查询性能要求高, 父类属性少, 子类属性多的情况.

Reference:

- https://cloud.tencent.com/developer/article/1026510
