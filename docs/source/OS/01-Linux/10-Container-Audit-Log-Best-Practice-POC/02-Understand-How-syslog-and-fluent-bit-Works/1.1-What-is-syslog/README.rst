What is rsyslog
==============================================================================

TODO ..


Difference between syslog, syslog-ng, rsyslog
------------------------------------------------------------------------------

``syslog`` is the first, it started on 1980, and it becomes part of Linux Kernel code.

``syslog-ng`` started on 1998, it is a open source project. it extends the protocal to support:

- content based filter
- log in to database
- allow using TCP instead of UDP
- TLS encrytpion

``rsyslog`` started on 2004, it is also a open source project. :

- support RELP protocol
- buffer

Now they are three projects maintained by different team, and gradually grow and borrow idea from each other all together.


Reference
------------------------------------------------------------------------------

- syslog: it is part of linux kernel.
- syslog-ng: https://www.syslog-ng.com/
- Rsyslog Official: https://www.rsyslog.com/
