# slack-training-monitor-bot
Slack Monitoring bot for training

## Configuration
* Fill it with your slack app settings

```json
{
  "token": "your token",
  "group_id": "your group id",
  "channel_name": "(option)channel name"
}
```

## Available Commands

```json
{
  "command_list" : [
    {
      "category": "test",
      "name": "simple",
      "file": "simple_task.py",
      "args": ""
    },
    {
      "category": "training",
      "name": "cifar10_train",
      "file": "/home/haejung/PycharmProjects/mathplottest/exam_cifar10/cifar10_multi_gpu_train.py",
      "args": "--data_dir=./data_dir --train_dir=./train_dir --max_steps=50000"
    },
    {
      "category": "evaluation",
      "name": "cifar10_eval",
      "file": "/home/haejung/PycharmProjects/mathplottest/exam_cifar10/cifar10_eval.py",
      "args": "--run_once=True --data_dir=./data_dir --eval_dir=./eval_dir --checkpoint_dir=./train_dir"
    }
  ]
}
```

## Run
```
# python3 training_basic.py
```
