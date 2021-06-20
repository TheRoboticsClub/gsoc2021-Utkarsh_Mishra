
for seed in 3; do
	python train.py --data_dir ../datasets/complete_dataset \
		--curve_dir ../datasets/curves_only \
		--model_path trained_models \
		--log_dir log \
		--base_dir 06Jun${seed} \
		--comment 'Initial training on Tamino on stacked images' \
		--horizon ${seed} \
		--num_epochs 100 \
		--lr 3e-3 \
		--test_split 0.2 \
		--shuffle True \
		--batch_size 256 \
		--save_iter 50 \
		--print_terminal True \
		--seed 123
done
