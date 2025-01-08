## 0-物料清单

- 3D打印件
- 19kg或30kg的飞特sts3215舵机
- 5v或12v DC电源
- 飞雪舵机驱动板

## 1-环境安装（Ubuntu系统）

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

- lerobot_alohamini保留了lerobot的全部源码，并增强了debug能力，这个debug能力我们日后会经常用到

- 如果你已经有lerobot，且对lerobot的目录结构非常了解，可以仅拷贝debug目录到你的lerobot

- lerobot和lerobot_alohamini不要共用conda环境


### 3. 安装conda3及环境依赖

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
conda create -y -n lerobot_alohamini python=3.10
conda activate lerobot_alohamini
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

### 4. 配置机械臂端口号
ubuntu系统的逻辑是哪个USB先插入，哪个是ACM0，因此可以在终端直接输入，来依次确认插入的端口号

```
ls /dev/ttyACM*
```

lerobot官方脚本（不推荐）：
```
python lerobot/scripts/find_motors_bus_port.py
```

### 5. 串口授权
默认权限无法访问串口，我们需要对端口进行授权，lerobot官方文档的案例是将权限修改为666，实践中发现每次重启电脑都要重新设置，非常麻烦，建议直接将当前用户添加到设备用户组，永久解决该问题。
1. 终端键入`whoami`  //查看当前用户名
2. 键入`sudo usermod -a -G dialout username` //永久添加username到设备用户组
3. 重启电脑，以让权限生效

