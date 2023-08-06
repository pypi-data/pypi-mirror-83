#! /bin/bash
# Arguments [PARTIAL_DATA flag]

set -e # stop and fail if anything stops
cd `dirname "$0"`
PARTIAL_DATA=$1
data_source=$( [ "$PARTIAL_DATA" == true ] &&  echo download || echo download-all )
echo "*** Using data source: $data_source"

# Download the code from PyTorch's examples repository
[ -f code/main.py ] || wget -O code/main.py https://raw.githubusercontent.com/pytorch/examples/master/imagenet/main.py

# Download the data
ssm process -p ex-imagenet -t $data_source -v 400 \
    --entrypoint "/bin/bash" --dependencies ./code \
    -o ./output/$data_source \
    -- -c "bash /opt/ml/processing/input/code/code/$data_source.sh \$SSM_OUTPUT/data"

run_training () { # args: task_name, instance_type, additional_command_params, [description] [epochs] [additional_args]
    EPOCHS=${5:-10}  # 20 epochs by default
    ADDITIONAL_ARGS=${6:-"--no_spot --force_running --cs"} # 

    echo ===== Training $EPOCHS epochs, $4...
    ssm shell -p ex-imagenet -t $1 --dir_files ./code -o ./output/$1 -v 280 \
        --iit train $data_source output FullyReplicated data/train \
        --iit val $data_source output FullyReplicated data/val \
        --md "loss" "Epoch:.*Loss\s+([e\-+0-9\\.]*) \(" --md "acc1" "Epoch:.*Acc@1\s+([e\-+0-9\\.]*) \(" --md "acc5" "Epoch:.*Acc@5\s+([e\-+0-9\\.]*) \(" \
        --md "time" "Epoch:.*Time\s+([e\-+0-9\\.]*) \(" --md "data_time" "Epoch:.*Data\s+([e\-+0-9\\.]*) \(" \
        --md "test_loss" "Test:.*Loss\s+([e\-+0-9\\.]*) \(" --md "test_acc1" "Test:.*Acc@1\s+([e\-+0-9\\.]*) \(" --md "test_acc5" "Test:.*Acc@5\s+([e\-+0-9\\.]*) \(" \
        --download_model --download_output --download_state \
        --it $2 $ADDITIONAL_ARGS \
        --cmd_line  "./extract.sh \$SM_CHANNEL_TRAIN/.. && \ 
                    CODE_DIR=\`pwd\` && cd \$SSM_INSTANCE_STATE && START=\$SECONDS && \
                    python \$CODE_DIR/main.py --epochs $EPOCHS --resume checkpoint.pth.tar --workers 8 \$SM_CHANNEL_TRAIN/.. $3 2>&1 && \
                    echo Total time: \$(( SECONDS - START )) seconds"

    exit $?
}

DESC="a single GPU"
run_training train-1gpu ml.p3.2xlarge "" "$DESC" &
DESC="distributed training, a single GPU"
run_training train-dist-1gpu ml.p3.2xlarge "--multiprocessing-distributed --dist-url env:// --world-size 1 --rank 0 --seed 123" "$DESC" &
DESC="distributed training, 8 GPUs"
run_training train-dist-8gpus ml.p2.8xlarge "--multiprocessing-distributed --dist-url env:// --world-size 1 --rank 0 --seed 123" "$DESC" &
DESC="distributed training, 3 instances, total 3 GPUs"
run_training train-dist-3nodes-3gpus ml.p3.2xlarge '--multiprocessing-distributed --dist-url env:// --world-size $SSM_NUM_NODES --rank $SSM_HOST_RANK --seed 123' "$DESC" \
        "" "--no_spot --ic 3 --force_running --cs" &

wait
echo "FINISHED!"
exit

