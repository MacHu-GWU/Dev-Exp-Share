DynamoDB 实现 论坛 应用
==============================================================================

Entity and relationship

- User, user can write post, can reply to a post.
- Post, user can write post.
- Comment, user can reply to a post, comment has to associate with a post.
- Board, a forum has multiple board, each board has many many post
- Security Group, each user is associated with a security group, a security group is authorized to perform list of actions.
- Action, forum operation action


Home page view
------------------------------------------------------------------------------
without login home page shows list of boards, and:

1. how many users are online
2. how many post each board has

with login, except things listed above, user can see see himself username.


Post list page view in a Board
------------------------------------------------------------------------------

1. post are ordered by last reply time.
2. several post are pined to the top.


Post view
------------------------------------------------------------------------------

1. first display the title and the first post.
2. then display comments / replies.
3. display up to 10 comments at one time.


Search view
------------------------------------------------------------------------------

1. user can find his own post.
2. user can find his own replies.
3. user can search post title with in a given board.
4. 3) can be combined with 1) and 2).


Message Box
------------------------------------------------------------------------------
