rm err.err
rm out.out
rm -rf daisy_logs
bsub -P cellmap -n 12 -o out.out -e err.err cellmap_flow_blockwise_processor 20251215_er.yaml