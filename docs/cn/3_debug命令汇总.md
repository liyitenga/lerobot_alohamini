#### 查看所有舵机状态
```
python lerobot/debug/motors.py get_motors_states \
  --port /dev/ttyACM0
```

#### 卸掉机械臂的扭矩
```
python lerobot/debug/motors.py reset_motors_torque  \
  --port /dev/ttyACM1
```

#### 让指定编号的舵机进行旋转
```
python lerobot/debug/motors.py move_motor_to_position \
  --id 1 \
  --position 2048 \
  --port /dev/ttyACM0
```

#### 让机械臂执行脚本动作
```
python lerobot/debug/motors.py move_motors_by_script \
   --script_path action_scripts/test_dance.txt  \
   --port /dev/ttyACM0
```

#### 获取偏移计算后的角度
```
python lerobot/debug/motors.py position_to_angle_with_offset  \
  --offset_str="[-2048, 3072, -1024, -2048, 2048, -2048]"  \
  --port /dev/ttyACM0
```


#### 设置舵机的ID
```
python lerobot/debug/motors.py configure_motor_id \
  --id 1 \
  --set_id 6 \
  --port /dev/ttyACM1
```

#### 重置当前位置为电机中位
```
python lerobot/debug/motors.py reset_motors_to_midpoint \
  --port /dev/ttyACM0
```


