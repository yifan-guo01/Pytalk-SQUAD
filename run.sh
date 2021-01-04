# This is an example script to start a CodaLab run. There are often several
# things to configure, including the docker image, compute resources, bundle
# dependencies (code and data), and custom arguments to pass to the command.
# Factoring all this into a script makes it easier to run and track different
# configurations.

### CodaLab arguments
CODALAB_ARGS="cl run"

# Name of bundle (can customize however you want)
CODALAB_ARGS="$CODALAB_ARGS -n run-predictions -d run-predictions"
# Docker image doctalk4docker/doctalk_centos:corenlpnltkbert 
CODALAB_ARGS="$CODALAB_ARGS --request-docker-image doctalk4docker/doctalk_centos:corenlpnltkbert"
# Control the amount of RAM your run needs
CODALAB_ARGS="$CODALAB_ARGS --request-memory 10g"

# Bundle dependencies
CODALAB_ARGS="$CODALAB_ARGS dev-v1.1.json:dev-v1.1.json" # Dataset
CODALAB_ARGS="$CODALAB_ARGS  src:src"                              # Code

### Command to execute (these flags can be overridden) from the command-line
#dev-v1.1.json is dataset,  predictions.json is output
CMD="python src/eval.py dev-v1.1.json predictions.json"

# Create the run on CodaLab!
FINAL_COMMAND="$CODALAB_ARGS '$CMD'"
echo $FINAL_COMMAND
exec bash -c "$FINAL_COMMAND"
