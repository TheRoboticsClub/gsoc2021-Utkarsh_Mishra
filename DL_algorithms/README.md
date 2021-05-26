# DL Algorithms: Implementation and Baseline

It contains some deep learning regression models.

The models implemented are derived from:
1. PilotNet for Autonomous Driving with Behaviour Metrics dataset
2. DeepPilot-CNN for Autonomous Drone Racing with DeepPilot dataset

The DL algorithms are modular and can adapt to various other datasets. 

## Preparing Dataset

For PilotNet, we use our custom datasets:
- Complete dataset: contains images with annotations from different circuits [https://drive.google.com/file/d/1Xdiu69DLj7lKK37F94qrUWsXkVg4ymGv/view?usp=sharing](https://drive.google.com/file/d/1Xdiu69DLj7lKK37F94qrUWsXkVg4ymGv/view?usp=sharing)
- Curves dataset: contains images with annotations from many_curves circuit: [https://drive.google.com/file/d/1zCJPFJRqCa34Q6jvktjDBY8Z49bIbvLJ/view?usp=sharing](https://drive.google.com/file/d/1zCJPFJRqCa34Q6jvktjDBY8Z49bIbvLJ/view?usp=sharing)

For DeepPilot, we use their own dataset:
- Complete Mosaic Data: [https://inaoepedu-my.sharepoint.com/:f:/g/personal/carranza_inaoe_edu_mx/EslxVDqc9zBMmiV4mDH48KUBAcAHu0Ypt1rZLL6ifOjyoA?e=VYtMyT](https://inaoepedu-my.sharepoint.com/:f:/g/personal/carranza_inaoe_edu_mx/EslxVDqc9zBMmiV4mDH48KUBAcAHu0Ypt1rZLL6ifOjyoA?e=VYtMyT)

```
DL_algorithms
    ├── datasets
        ├── DeepPilot                               # Extract DeepPilot dataset here
        |   ├── train                               
        |   |   ├── Images/                         # Train Images
        |   |   └── data.txt                        # Annotations for training
        |   └── test                               
        |       ├── Images/                         # Test Images
        |       └── data.txt                        # Ground Truth labels
        |
        └── PilotNet                                # Extract PilotNet dataset here
            ├── complete_dataset                    # Extract PilotNet complete_dataset here           
            |   ├── Images/                         # Train and Test Images
            |   └── data.json                       # Annotations
            └── curves_dataset                      # Extract PilotNet curves_dataset here  
                ├── Images/                         # Train and Test Images
                └── data.json                       # Annotations
```

## Hyperparameters for the code

```
# For PilotNet

-h, --help                            show this help message and exit
--data_dir            DATA_DIR        Directory to find Data
--curve_dir           CURVE_DIR       Directory to find Curves data
--model_path          MODEL_PATH      Directory to store model
--log_dir             LOG_DIR         Directory to store tensorboard
--base_dir            BASE_DIR        Directory to save everything
--comment             COMMENT         Comment to know the experiment
--num_epochs          NUM_EPOCHS      Number of Epochs
--lr                  LR              Learning rate for Policy Net
--test_split          TEST_SPLIT      Train test Split
--shuffle             SHUFFLE         Shuffle dataset
--batch_size          BATCH_SIZE      Batch size
--save_iter           SAVE_ITER       Iterations to save the model
--print_terminal      PRINT_TERMINAL  Print progress in terminal
--seed                SEED            Seed for reproducing

# For DeepPilot

-h, --help                            show this help message and exit
--data_dir            DATA_DIR        Directory to find Data
--model_path          MODEL_PATH      Directory to store model
--log_dir             LOG_DIR         Directory to store tensorboard
--base_dir            BASE_DIR        Directory to save everything
--comment             COMMENT         Comment to know the experiment
--num_epochs          NUM_EPOCHS      Number of Epochs
--lr                  LR              Learning rate for Policy Net
--test_split          TEST_SPLIT      Train test Split
--shuffle             SHUFFLE         Shuffle dataset
--batch_size          BATCH_SIZE      Batch size
--save_iter           SAVE_ITER       Iterations to save the model
--print_terminal      PRINT_TERMINAL  Print progress in terminal
--seed                SEED            Seed for reproducing

```

## Running the Code

```
source ~/pyenvs/gsoc21/bin/activate
cd gsoc21code/DL_algorithms/

# For PilotNet

cd PilotNet
python train.py 


# For DeepPilot

cd DeepPilot
python train.py 


```

The results are saved in the `./experiments/` directory and the structure is given below. 
Tensorboard can be launched with `./experiments/log` directory.