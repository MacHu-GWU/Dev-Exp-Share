
三种情况

api.github.com/v1/user

- ``GET /user``
- ``GET /user/<user_id>``
- ``GET /user?<param1>=<value1>&...``, example: ``/user?create_date_later_than=2018-01-01``
- ``POST /user``, example: ``requests.post"("/user", payload={"create_date_later_than": "2018-01-01"})``


``GET /user/<user_id>``

Method Request:

- Request Paths: Name = user_id

Mapping Templates:

- Content Type = application/json, Template = ``{"user_id": "$input.params('user_id')"}``, 将 URL 转换成 ``{"user_id": "xxx"}`` 传入 Lambda 中


``POST /user``

什么都不用设置, 你的 Payload 就是 Lambda 中的 Event
