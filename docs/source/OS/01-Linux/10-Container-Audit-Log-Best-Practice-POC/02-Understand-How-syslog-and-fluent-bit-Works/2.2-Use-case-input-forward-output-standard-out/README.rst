Use case, Input forward, Output standard out
==============================================================================

**Run fluent-bit service container**::

    # Setup variables
    repo_name="fluent/fluent-bit" # https://hub.docker.com/r/fluent/fluent-bit/
    container_name="fluent-bit-deamon-set"

    # display help info
    sudo docker run --rm --name "${container_name}" -p 127.0.0.1:24224:24224 ${repo_name} /fluent-bit/bin/fluent-bit -h

    # check fluent bit version
    sudo docker run --rm --name "${container_name}" -p 127.0.0.1:24224:24224 ${repo_name} /fluent-bit/bin/fluent-bit --version

    # run fluent-bit container
    # input=forward https://docs.fluentbit.io/manual/pipeline/inputs/forward
    # output=standard-out https://docs.fluentbit.io/manual/pipeline/outputs/standard-output
    # for testing, -f 1 specified the flush timeout = 1, it means flushing data to output every 1 sec
    sudo docker run --rm --name "${container_name}" -p 127.0.0.1:24224:24224 ${repo_name} /fluent-bit/bin/fluent-bit -i forward -o stdout -p format=json_lines -f 1

**Run app container, generate some logs**:

    # Setup variables
    repo_name="ubuntu" # https://hub.docker.com/_/ubuntu

    # generate a log message
    sudo docker run --rm --log-driver=fluentd -t ${repo_name} echo Hello World

Switch to your fluent-bit service container terminal to see outputs.
