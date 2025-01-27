以下为lerobot自带的命令脚本，请根据情况修改参数。


#### 寻找USB端口
```
python lerobot/scripts/find_motors_bus_port.py
```
#### 寻找和相机端口
```
python lerobot/common/robot_devices/cameras/opencv.py \
    --images-dir outputs/images_from_opencv_cameras
```

#### 摇操测试
```
python lerobot/scripts/control_robot.py teleoperate \
--robot-path lerobot/configs/robot/am_solo.yaml
```

#### 摇操测试(不带相机)
```
python lerobot/scripts/control_robot.py teleoperate \
--robot-path lerobot/configs/robot/am_solo.yaml \
--robot-overrides '~cameras' \
--display-cameras 0
```

#### 录制数据集

先到huggingface网站申请key，然后执行
```
huggingface-cli login --token {key} --add-to-git-credential
```

//录制数据集
```
	python lerobot/scripts/control_robot.py record \
    --robot-path lerobot/configs/robot/am_solo.yaml \
    --fps 30 \
    --repo-id liyitenga/so100_pick_taffy8 \
    --tags so100 tutorial \
    --warmup-time-s 5 \
    --episode-time-s 60 \
    --reset-time-s 10 \
    --num-episodes 22 \
    --resume 0 \
    --push-to-hub 1 \
    --single-task test1 \
    --root data/so100_pick_taffy8
```


//resume 0 代表全新数据集  1代表续传  
//repo-id 在huggingface网站上的创建的仓库名称，如果是第一次录则自动创建  
//root 数据集在本地的存储路径，显示指定，方便日后上传到远程服务器训练  
//push-to-hub 是否上传到huggingface网站，0不上传，1上传  


#### 可视化
```
python lerobot/scripts/visualize_dataset_html.py \
  --repo-id liyitenga/so100_pick_taffy5
```

#### 重新播放数据集
```
python lerobot/scripts/control_robot.py replay \
    --robot-path lerobot/configs/robot/am_solo.yaml \
    --fps 30 \
    --repo-id liyitenga/so100_pick_taffy1 \
    --episode 1
```

#### 本地训练
```
    HYDRA_FULL_ERROR=1 python lerobot/scripts/train.py \
    dataset_repo_id=liyitenga/so100_pick_taffy8 \
    policy=act_so100_real \
    env=so100_real \
    device=cuda \
    wandb.enable=false \
	hydra.run.dir=outputs/train/taffy8-22-80000
```

#### 远程训练

```
    HYDRA_FULL_ERROR=1 python lerobot/scripts/train.py \
    dataset_repo_id=liyitenga/so100_pick_taffy7 \
    policy=act_so100_real \
    env=so100_real \
    device=cuda \
    wandb.enable=false \
    resume=false \
    hydra.run.dir=/root/autodl-tmp/train/taffy7-22-80000
```


#### 评估训练集
```
python lerobot/scripts/control_robot.py record \
  --robot-path lerobot/configs/robot/am_solo.yaml \
  --fps 30 \
  --repo-id liyitenga/eval_so100_pick_taffy_42 \
  --tags so100_pick_taffy1 eval \
  --warmup-time-s 5 \
  --episode-time-s 500 \
  --reset-time-s 10 \
  --num-episodes 1 \
  --single-task test2 \
  --push-to-hub 0 \
  -p outputs/train/taffy8-22-80000/checkpoints/080000/pretrained_model
```

