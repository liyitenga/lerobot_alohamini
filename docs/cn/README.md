
## [English](../../README.md)| 中文说明

AlohaMini 是一款基于 LeRobot 和 SO100 打造的 Aloha 机器人训练套件，集成了软件与硬件，专为科研与教学应用设计。该套件配备了 2 个leader臂、2 个follower臂以及 3 个摄像头，整体固定于一个方形木板上。相较于 LeRobot，AlohaMini 不仅显著增强了调试能力，还统一了数据采集标准。

随着越来越多的研究团队采用 AlohaMini，数据集和模型的复用效率将显著提高（例如，直接使用其它团队分享的数据集或模型，无需再为适配而反复调整间距，角度等）。通过这一标准化平台，不同团队可以专注于算法研发和模型优化，从而提升科研效率和协作质量。

AlohaMini 硬件在出厂前已经进行了必要的配置，仅需要少量的工作就可以开始进行训练和评估。

如果你是在校学生，你可以自行购买零部件进行组装，以节省成本。如果是科研单位或大学实验室，则建议直接购买成品，成品对关键零部件进行了加固，并进行了调校适配，只需一行代码，即可开始数据收集和训练。


## 前言
“AlohaMini 是从 LeRobot 仓库 fork 的一个分支，其保留了LeRobot的全部代码，并增加了debug目录、校准文件和教程文档，如果您不想使用lerobot_alohamini，想继续用lerobot，只需拷贝debug目录和校准文件到lerobot的相应目录即可。



## 开始使用（Ubuntu系统）

*** 强烈建议按顺序进行 ***

### 1. 准备工作，网络环境测试
```
curl https://www.google.com
curl https://huggingface.co
```
首先确保网络通畅


### 2. 克隆lerobot_alohamini仓库

```
cd ~
git clone https://github.com/liyitenga/lerobot_alohamini.git
```

### 3. 串口授权
默认权限无法访问串口，我们需要对端口进行授权，lerobot官方文档的案例是将权限修改为666，实践中发现每次重启电脑都要重新设置，非常麻烦，建议直接将当前用户添加到设备用户组，永久解决该问题。
1. 终端键入`whoami`  //查看当前用户名
2. 键入`sudo usermod -a -G dialout username` //永久添加username到设备用户组
3. 重启电脑，以让权限生效

### 4. 安装conda3及环境依赖

安装conda3
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
source ~/.bashrc
````

初始化conda3
```
conda create -y -n lerobot python=3.10
conda activate lerobot
````

安装环境依赖
````
cd ~/lerobot_alohamini
pip install -e ".[feetech]"

conda install -y -c conda-forge ffmpeg
pip uninstall -y opencv-python
conda install -y -c conda-forge "opencv>=4.10.0"

pip install -e ".[aloha, pusht]"
````

### 5. 配置机械臂端口号
ubuntu系统的逻辑是哪个USB先插入，哪个是ACM0，因此可以在终端直接输入，来依次确认插入的端口号

```
ls /dev/ttyACM*
```

AlohaMini的默认插入顺序：
- 左引导臂（Left Leader），对应ACM0
- 左跟随臂(Left Follower)，对应ACM1
- 右引导臂（Right Leader），对应ACM2
- 右跟随臂(Right Follower)，对应ACM3

如果不按此顺序插入USB接口，需要手工修改lerobot/configs/robot/so100_bimanual.yaml文件，改为相应的端口号。

注：每次重启电脑后，都要执行该操作

### 6. 配置摄像头端口号

#### 1. 运行如下命令，会自动调取摄像头进行拍照，在outputs目录生成诸如camera_06_frame_000002.png这样的文件，这里面的6就是摄像头序号
```
cd ~/lerobot_alohamini

python lerobot/common/robot_devices/cameras/opencv.py \
    --images-dir outputs/images_from_opencv_cameras

```

注意：
- Ubuntu系统上的默认规律是先插入的是0，第二个插入的是2，然后是4，6
- 多个摄像头不能插在一个Hub上，1个Hub上仅支持1个摄像头
- 笔记本电脑通常都自带一个默认摄像头，这个摄像头我们用不上，忽略掉它即可
- 每次重启电脑后，都要执行该操作


#### 2. 修改configs/robot/so100_bimanual.yaml，配置为正确的摄像头序号

### 7. 摇操测试
当插好机械臂和摄像头，并确认端口号无误后，我们就可以进行摇操测试了

运行代码：

```
python lerobot/scripts/control_robot.py teleoperate \
    --robot-path lerobot/configs/robot/so100_bimanual.yaml
```
我们将看到3个摄像头窗体，并且Leader臂和Follower臂可以联动了

### 8. 本机评估测试
运行这个测试，以确认硬件驱动和lerobot环境没有问题

使用CPU评估：
```
python lerobot/scripts/eval.py -p lerobot/diffusion_pusht eval.n_episodes=10 eval.batch_size=10 device=cpu
```

使用cuda评估
```
python lerobot/scripts/eval.py -p lerobot/diffusion_pusht eval.n_episodes=10 eval.batch_size=10 device=cuda

```

不同硬件的耗时参考如下：
- macos i7 model-cpu  1178s
- ubuntu i7m model-cpu 2427s
- macos M1 model-mps  706s（报错） //ValueError: cannot convert float NaN to integer
- macos M1 model-cpu  3237s
- ubuntu i7m+4070M model-cuda 228s


### 9. 收集训练集

#### 1 注册huggingface，获取并配置key

1.进入HuggingFace网站（huggingface.co），申请{Key}，记得带读写权限

2.将API token添加到Git凭据中

```
git config --global credential.helper store

huggingface-cli login --token {key}--add-to-git-credential

```

#### 2 运行脚本


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
参数：
--resume  //1继续原来的数据集,0重新开始一个数据集
--push-to-hub  //0数据集不上传,1数据集上传至HF
--root //指定数据集的存储目录
---local_files_only  //1 从root目录获取文件，不自动连接HF仓库


### 10. 可视化
```
python lerobot/scripts/visualize_dataset_html.py \
  --repo-id $HF_USER/so100_bi_test
```


### 11. 重新播放数据集
```
python lerobot/scripts/control_robot.py replay \
    --robot-path lerobot/configs/robot/so100_bimanual.yaml \
    --fps 30 \
    --repo-id $HF_USER/so100_bi_test \
    --episode 2
```

### 12. 本地训练


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

### 13. 远程训练
以AutoDL为例：
申请一张4070显卡，容器镜像选择Python  3.8(ubuntu20.04) Cuda  11.8或以上，并用终端登录
```
//进入远程终端，初始化conda
conda init

//重启终端，创建环境
conda create -y -n lerobot python=3.10
conda activate lerobot

//学术加速
source /etc/network_turbo

//获取lerobot
git clone https://github.com/liyitenga/lerobot_alohamini.git

//安装必要文件
cd ~/lerobot
pip install -e ".[feetech,aloha,pusht]"
```

本机操作如下：
安装FileZilla
````
sudo apt install filezilla -y
````

协议选择SSH，拷贝配置文件到远程服务器相应目录下

//env文件
lerobot/configs/env/so100_real_bimanual.yaml
//policy文件
lerobot/configs/policy/act_so100_real.yaml

运行如下命令，开始训练：

```
    HYDRA_FULL_ERROR=1 python lerobot/scripts/train.py \
    dataset_repo_id=liyitenga/so100_bi_giveme5 \
    policy=act_so100_real \
    env=so100_real_bimanual \
    device=cuda \
    wandb.enable=false

```

### 14. 评估训练集

用filezilla将训练好的模型拷贝到本地，并运行如下命令即可：

```
python lerobot/scripts/control_robot.py record \
  --robot-path lerobot/configs/robot/so100_bimanual.yaml \
  --fps 30 \
  --repo-id ${HF_USER}/so100_bi_giveme5 \
  --tags so100_bi_givme5 eval \
  --warmup-time-s 5 \
  --episode-time-s 40 \
  --reset-time-s 10 \
  --num-episodes 10 \
  --single-task test1 \
  -p outputs/train/2024-12-26/19-27-02_real_world_act_default/checkpoints/080000/pretrained_model
````

