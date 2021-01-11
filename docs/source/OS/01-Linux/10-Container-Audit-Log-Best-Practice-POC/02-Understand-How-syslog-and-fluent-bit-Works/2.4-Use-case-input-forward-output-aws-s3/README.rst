Use case, Input forward, Output aws s3
==============================================================================

Make sure your EC2 have AWS S3 IAM Role attached.

**Run fluent-bit service container**::

    # Setup variables
    repo_name="fluent/fluent-bit" # https://hub.docker.com/r/fluent/fluent-bit/
    container_name="fluent-bit-deamon-set"
    s3_bucket="ociso-for-everything"

    # output example3 - AWS S3
    # input=forward https://docs.fluentbit.io/manual/pipeline/inputs/forward
    # output=standard-out https://docs.fluentbit.io/manual/pipeline/outputs/s3
    #
    # note that fluent-bit don't write logs to s3 bucket immediately when receives it
    # it store it in buffer and write to it when reaching the upload_chunk_size (minimal 5M)
    # or upload_timeout (minimal 1M)
    sudo docker run --rm --name "${container_name}" -p 127.0.0.1:24224:24224 ${repo_name} /fluent-bit/bin/fluent-bit -i forward -o s3 -p region=us-east-1 -p bucket=${s3_bucket} -p total_file_size=1M -p upload_timeout=1m -f 1

**Run app container, generate some logs**::

    # Setup variables
    repo_name="ubuntu" # https://hub.docker.com/_/ubuntu

    # Since fluent-bit s3 only write to S3 when
    # reaching minimal upload_timeout, which is 1m in this case
    # reaching upload_chunk_size, which is 5M in this case,
    # in order to see the log immediately, I create a simple python script
    # generate_big_file.py
    # that creating a 5MB text file, and then log the content to it.

    # copy the python script to generate_big_file.py
    vi generate_big_file.py

    # create big file: big-file.txt
    python generate_big_file.py

    # send some log
    sudo cat big-file.txt | sudo docker run --log-driver=fluentd -t ubuntu echo

    # or just send some small log and wait for 1 min
    sudo docker run --log-driver=fluentd -t ubuntu echo Hello World

    # go to s3 console to view the log
    https://s3.console.aws.amazon.com/s3/buckets/ociso-for-everything?region=us-east-1&prefix=fluent-bit-logs/

**What if fluent-bit container crushed, Do we lose the data in buffer**?

If the fluent-bit container doesn't bind to any volume, YES your lose the data in buffer. That's why from the official doc https://docs.fluentbit.io/manual/pipeline/outputs/s3, it recommends to send to s3 more frequently.

From the AWS document https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html, all of ECS, Fargate, EKS supports using data volume. So we should have no problem.
