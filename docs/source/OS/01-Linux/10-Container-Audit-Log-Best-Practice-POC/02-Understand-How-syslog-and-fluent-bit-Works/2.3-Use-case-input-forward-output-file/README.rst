Use case, Input forward, Output file
==============================================================================

**Run fluent-bit service container**::

    # Setup variables
    repo_name="fluent/fluent-bit" # https://hub.docker.com/r/fluent/fluent-bit/
    container_name="fluent-bit-deamon-set"

    # create an empty folder to store fluent-bit log files
    mkdir -p ${HOME}/fluent-bit-log

    # run fluent-bit container
    # input=forward https://docs.fluentbit.io/manual/pipeline/inputs/forward
    # output=standard-out https://docs.fluentbit.io/manual/pipeline/outputs/file
    # for testing, -f 1 specified the flush timeout = 1, it means flushing data to output every 1 sec
    sudo docker run --rm --name "${container_name}" --mount type=bind,source=${HOME}/fluent-bit-log,target=/tmp -p 127.0.0.1:24224:24224 ${repo_name} /fluent-bit/bin/fluent-bit -i forward -o file -p path=/tmp -p format=json_lines

**Run app container, generate some logs**:

    # Setup variables
    repo_name="ubuntu" # https://hub.docker.com/_/ubuntu

    # generate a log message
    sudo docker run --rm --log-driver=fluentd -t ${repo_name} echo Hello World

    # verify log appears in ${HOME}/fluent-bit-log directory
    ls ~/fluent-bit-log
    cat ~/fluent-bit-log/08be78c9ab37
