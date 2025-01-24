
## English | [中文说明](docs/cn/1_新手指南.md)


AlohaMini is a training suite for the Aloha robot, developed based on LeRobot and SO100. It integrates both hardware and software and is specifically designed for research and educational purposes. This suite comes with 2 leader arms, 2 follower arms, and 3 cameras, all mounted on a square wooden board. Compared with LeRobot, AlohaMini significantly enhances debugging capabilities and standardizes data collection.

As more and more research teams adopt AlohaMini, the reuse efficiency of datasets and models will increase dramatically (for example, researchers can directly use datasets or models shared by other teams without repeatedly adjusting spacing, angles, etc.). Through this standardized platform, different teams can focus on algorithm development and model optimization, thereby improving research efficiency and collaboration quality.

The AlohaMini hardware is preconfigured before shipment, requiring only minimal work to start training and evaluation.

- If you are a student, you can purchase components and assemble them yourself to save costs.
- If you are a research institution or university laboratory, it is recommended to purchase a finished product. The finished product has reinforced key components and is calibrated; you only need one line of code to start data collection and training.

## Preface 
“AlohaMini is a branch forked from the LeRobot repository. It retains all of LeRobot’s code, plus a debug directory, calibration files, and tutorial documentation. If you do not wish to use lerobot_alohamini and instead want to continue using lerobot, you can simply copy the debug directory and the calibration files into the corresponding directories of lerobot.”




## Getting Started (Ubuntu System)

*** Strongly recommended to follow the steps in order ***

### 1. Preparation and Network Environment Test
```
curl https://www.google.com
curl https://huggingface.co
```
First, make sure your network is working properly.


### 2. Clone the lerobot_alohamini Repository

```
cd ~
git clone https://github.com/liyitenga/lerobot_alohamini.git
```

### 3. Serial Port Authorization
By default, you do not have permission to access the serial port, so we need to grant access. The official LeRobot documentation suggests changing the permission to 666 each time, but in practice, you have to reconfigure it after every reboot, which is quite inconvenient. It is recommended to add the current user to the device user group once and for all:

1. Type `whoami` in the terminal // to see your current username
2. Type `sudo usermod -a -G dialout username` // permanently add the user “username” to the device user group
3. Reboot the computer to make the permission settings take effect

### 4. Install conda3 and Environment Dependencies

Install conda3 
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
source ~/.bashrc
````

Initialize conda3
```
conda create -y -n lerobot python=3.10
conda activate lerobot
````

Install environment dependencies
````
cd ~/lerobot_alohamini
pip install -e ".[feetech]"

conda install -y -c conda-forge ffmpeg
pip uninstall -y opencv-python
conda install -y -c conda-forge "opencv>=4.10.0"

pip install -e ".[aloha, pusht]"
````

### 5. Configure the Robot Arm Port Numbers
In Ubuntu, the order of insertion determines which device is assigned to ACM0, ACM1, etc. You can check the port number as you connect each USB device by using:

```
ls /dev/ttyACM*
```

By default, for AlohaMini, the sequence of insertion is:

Left Leader Arm: ACM0
Left Follower Arm: ACM1
Right Leader Arm: ACM2
Right Follower Arm: ACM3


If you do not follow this order, you need to manually modify the file `lerobot/configs/robot/so100_bimanual.yaml` with the corresponding port numbers.

Note: You need to perform this operation every time you reboot the computer.

### 6. Configure Camera Port Numbers

1. Run the following command, which will automatically activate the cameras and take a snapshot. It will generate files such as `camera_06_frame_000002.png` in the outputs directory, where the “6” in this example is the camera index:
```
cd ~/lerobot_alohamini

python lerobot/common/robot_devices/cameras/opencv.py \
    --images-dir outputs/images_from_opencv_cameras

```

Notes:

- On Ubuntu, the default pattern is 0, 2, 4, 6 in the order of camera insertion.
- Multiple cameras cannot be plugged into a single USB hub; only one camera per hub is supported.
- Most laptops come with a built-in default camera, which we do not need for this project, so ignore it.
- You need to perform this operation every time you reboot the computer.

2. Modify `configs/robot/so100_bimanual.yaml`, setting the correct camera indices.

### 7. Teleoperation Test

Once the robot arms and cameras are plugged in, and you have confirmed the port numbers are correct, you can run a teleoperation test:

```
python lerobot/scripts/control_robot.py teleoperate \
    --robot-path lerobot/configs/robot/so100_bimanual.yaml
```
You will see three camera windows, and the Leader arms and Follower arms should be able to move in sync.


### 8. Local Evaluation Test
Run the following test to confirm that both the hardware drivers and the lerobot environment are working properly.

CPU evaluation:
```
python lerobot/scripts/eval.py -p lerobot/diffusion_pusht eval.n_episodes=10 eval.batch_size=10 device=cpu
```

CUDA evaluation:
```
python lerobot/scripts/eval.py -p lerobot/diffusion_pusht eval.n_episodes=10 eval.batch_size=10 device=cuda

```

Below are reference run times for different hardware:
- macos i7 model-cpu  1178s
- ubuntu i7m model-cpu 2427s
- macos M1 model-mps  706s（error） //ValueError: cannot convert float NaN to integer
- macos M1 model-cpu  3237s
- ubuntu i7m+4070M model-cuda 228s


### 9. Collect Training Data

#### 9.1 Register on HuggingFace, Obtain and Configure Your Key

1.Go to the Hugging Face website (huggingface.co) and get your {Key}, ensuring it has read/write permissions.

2.Add the API token to your Git credentials:

```
git config --global credential.helper store

huggingface-cli login --token {key}--add-to-git-credential

```

#### 2 Run the Command


```
HF_USER=$(huggingface-cli whoami | head -n 1)
echo $HF_USER

python lerobot/scripts/control_robot.py record \
    --robot-path lerobot/configs/robot/so100_bimanual.yaml \
    --fps 30 \
    --repo-id $HF_USER/so100_bi_test \
    --tags so100 tutorial \
    --warmup-time-s 5 \
    --episode-time-s 40 \
    --reset-time-s 10 \
    --num-episodes 2 \
    --resume 1 \
    --push-to-hub 1 \
    --single-task test1 \
    --root data/so100_bi_test

```
Parameters:

* --resume: 1 continues from the previous dataset; 0 starts a new dataset
* --push-to-hub: 0 does not upload the dataset; 1 uploads the dataset to HF
* --root: specify the storage directory for the dataset
* --local_files_only: 1 will fetch files from the root directory without automatically connecting to the HF repository


### 10. Visualization
```
python lerobot/scripts/visualize_dataset_html.py \
  --repo-id $HF_USER/so100_bi_test
```


### 11. Replay the Dataset
```
python lerobot/scripts/control_robot.py replay \
    --robot-path lerobot/configs/robot/so100_bimanual.yaml \
    --fps 30 \
    --repo-id $HF_USER/so100_bi_test \
    --episode 2
```

### 12. Local Training


```
python lerobot/scripts/train.py \
  dataset_repo_id=$HF_USER/so100_bi_test \
  policy=act_so100_real \
  env=so100_real_bimanual \
  hydra.run.dir=outputs/train/act_so100_test \
  hydra.job.name=act_so100_test \
  device=cuda \
  wandb.enable=false
```

### 13. Remote Training

Taking AutoDL as an example:

Request a machine with a 4070 GPU, choose the Python 3.8 (ubuntu20.04) Cuda 11.8 or higher container image, and log in to the terminal.

```
// Enter the remote terminal and initialize conda
conda init

// Restart the terminal, then create an environment
conda create -y -n lerobot python=3.10
conda activate lerobot

// Academic acceleration
source /etc/network_turbo

// Get lerobot
git clone https://github.com/liyitenga/lerobot_alohamini.git

// Install necessary files
cd ~/lerobot
pip install -e ".[feetech,aloha,pusht]"
```

On your local machine, install FileZilla:

````
sudo apt install filezilla -y
````

Use SSH as the protocol to copy the configuration files to the corresponding directory on the remote server:

`lerobot/configs/env/so100_real_bimanual.yaml`  
`lerobot/configs/policy/act_so100_real.yaml`


Run the following command to start training:

```
    HYDRA_FULL_ERROR=1 python lerobot/scripts/train.py \
    dataset_repo_id=liyitenga/so100_bi_giveme5 \
    policy=act_so100_real \
    env=so100_real_bimanual \
    device=cuda \
    wandb.enable=false

```

### 14. Evaluate the Trained Model

Use FileZilla to copy the trained model back to your local machine. Then run:


```
python lerobot/scripts/control_robot.py record \
  --robot-path lerobot/configs/robot/so100_bimanual.yaml \
  --fps 30 \
  --repo-id ${HF_USER}/eval_so100_bi_giveme5 \
  --tags so100_bi_givme5 eval \
  --warmup-time-s 5 \
  --episode-time-s 40 \
  --reset-time-s 10 \
  --num-episodes 10 \
  --single-task test1 \
  -p outputs/train/2024-12-26/19-27-02_real_world_act_default/checkpoints/080000/pretrained_model
````

