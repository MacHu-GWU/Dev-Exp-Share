.. _dynamodb-many-to-many-modeling:


Dynamodb Many to Many Modeling
==============================================================================

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:

Reference:

- How to model one-to-one, one-to-many and many-to-many relationships in DynamoDB: https://stackoverflow.com/questions/55152296/how-to-model-one-to-one-one-to-many-and-many-to-many-relationships-in-dynamodb


Method 1 Auxiliary Table
------------------------------------------------------------------------------

Doctor Table

Partition Key = ``DoctorId``::

    ╔══════════╦═══════╗
    ║ DoctorId ║ Name  ║
    ╠══════════╬═══════╣
    ║ D1       ║ Anita ║
    ║ D2       ║ Mary  ║
    ║ D3       ║ Paul  ║
    ╚══════════╩═══════╝

Patient Table

Partition Key = ``PatientId``::

    ╔═══════════╦═════════╦════════════╗
    ║ PatientId ║ Name    ║ Illness    ║
    ╠═══════════╬═════════╬════════════╣
    ║ P1        ║ Barry   ║ Headache   ║
    ║ P2        ║ Cathryn ║ Itchy eyes ║
    ║ P3        ║ Zoe     ║ Munchausen ║
    ╚═══════════╩═════════╩════════════╝

DoctorPatientTable

Partition Key = ``DoctorId``, Sort Key = ``PatientId``::

    ╔══════════╦═══════════╦══════════════╗
    ║ DoctorId ║ PatientId ║ Last Meeting ║
    ╠══════════╬═══════════╬══════════════╣
    ║ D1       ║ P1        ║ 01/01/2018   ║
    ║ D1       ║ P2        ║ 02/01/2018   ║
    ║ D2       ║ P2        ║ 03/01/2018   ║
    ║ D2       ║ P3        ║ 04/01/2018   ║
    ║ D3       ║ P3        ║ 05/01/2018   ║
    ╚══════════╩═══════════╩══════════════╝

DoctorPatient table GSI

Partition Key = ``PatientId``, Sort Key = ``DoctorId``::

    ╔═══════════╦══════════╦══════════════╗
    ║ PatientId ║ DoctorId ║ Last Meeting ║
    ╠═══════════╬══════════╬══════════════╣
    ║ P1        ║ D1       ║ 01/01/2018   ║
    ║ P2        ║ D1       ║ 02/01/2018   ║
    ║ P2        ║ D2       ║ 03/01/2018   ║
    ║ P3        ║ D2       ║ 04/01/2018   ║
    ║ P3        ║ D3       ║ 05/01/2018   ║
    ╚═══════════╩══════════╩══════════════╝

Method 3 Graph Schema
------------------------------------------------------------------------------

AWS have previously referred to this as the Adjacency List pattern. It is more commonly referred to as a Graph database or a Triple Store.

I have previously answered this question on the AWS Adjancey List Pattern which seems to have helped some people understand it.

And there is a recent presentation by AWS that talks a lot about this pattern here

The approach involves putting all of the data in just one table.

I've just drawn some example rows rather than the whole table::

    ╔═════════╦═════════╦═══════╦═════════════╦══════════════╗
    ║ Key1    ║ Key2    ║ Name  ║   illness   ║ Last Meeting ║
    ╠═════════╬═════════╬═══════╬═════════════╬══════════════╣
    ║ P1      ║ P1      ║ Barry ║ Headache    ║              ║
    ║ D1      ║ D1      ║ Anita ║             ║              ║
    ║ D1      ║ P1      ║       ║             ║ 01/01/2018   ║
    ╚═════════╩═════════╩═══════╩═════════════╩══════════════╝

    ╔═════════╦═════════╦═══════╦═════════════╦══════════════╗
    ║ Key2    ║ Key1    ║ Name  ║   illness   ║ Last Meeting ║
    ╠═════════╬═════════╬═══════╬═════════════╬══════════════╣
    ║ P1      ║ P1      ║ Barry ║ Headache    ║              ║
    ║ D1      ║ D1      ║ Anita ║             ║              ║
    ║ P1      ║ D1      ║       ║             ║ 01/01/2018   ║
    ╚═════════╩═════════╩═══════╩═════════════╩══════════════╝

This model has some strengths in some specific circumstances - it can perform well in highly connected data. If you format your data well, you can achieve extremely fast and scalable models. It is flexible in that you can store any entity or relationship in the table without updating your schema/tables. If you are provisioning throughput capacity it can be efficient as all of the throughput is available to any operation across the application.

This model suffers from some huge downsides if used incorrectly or without serious consideration.

You lose any direct mapping between your business objects and your tables. This almost always results in unreadable spaghetti code. Performing even simple queries can feel very complex. Managing data quality becomes difficult as there is no obvious mapping between the code and the database. Most projects I've seen that use this approach end up writing various utilities, some of which become products in their own right, just to manage the database.

Another minor problem is that every attribute for every item in your model has to exist on one table. This usually results in a table that has hundreds of columns. In itself this is not a problem, but trying to work on a table with that many columns usually throws up simple problems like difficulty in viewing the data.

In short I think AWS have probably released what should have been a useful article in a set of articles, but by failing to introduce other (simpler) concepts for managing many-to-many relationships, they have confused lots of people. So to be clear, the adjacency list pattern can be useful, but its not the only option for modelling many-to-many relationships in DynamoDB. By all means use it if it works for your circumstances such as seriously Big Data, but if not, try one of the simpler models.
