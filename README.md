# Anubis
---
使用Python实现的工作流框架。

支持树形结构的运行顺序。

支持并发运行。

支持定制化插件。

多平台和多操作系统支持，无特殊依赖。

## 部署

> 需要python2.7及以上运行环境

直接克隆仓库即可

`$ git clone git@gitlab.fantasyfancy.com:tools/Anubis.git`

## 运行

`$ python anubis.py {arguments}`

### 运行时参数

> 参数以  -argument argv 形式传递

- **h 帮助选项**

  `$ python anubis.py -h`

  列出所有参数列表

- **c 指定配置文件**

  > 与 -t 为互斥参数，不可同时使用

  可以使用当前路径的相对路径，也可以使用绝对路径

- **l 指定log文件**

  可选参数，指定log文件地址，log为**追加写模式**，需要定时清理，anubis不提供log清理功能。

  默认值为 `./task.log`，即当前运行路径下的task.log文件

- **e 指定error log文件**

  可选参数，同l参数

  默认值为`./error.log`，即当前运行路径下error.log 文件

  > errorlog 禁止与log相同文件，指定相同路径将引发异常

- **t 指定任务名**

  > 与-c为互斥参数，不可同时使用

  使用该参数后将会从工作流框架中的`custom/{taskname}`目录读取配置文件，根据情况需要和-k参数联合使用

- **k 指定配置文件关键字**

  Eg: `$ python anubis.py -t test -k testconfig`

  可选参数，和-t参数联合使用，指定`custom/{taskname}/{key}.json`为任务的配置文件

  默认值为**default**，即`custom/{taskname}/default.json`作为配置文件

- **tn 线程池大小**

  可选参数，指定运行时开辟的线程池大小，默认值为**10**

- **p 参数列表**

  该参数必须位于所有参数的最后，该参数会将其之后的所有参数以`pName=pValue`形式加载，如果格式错误会引发异常

  Eg: `$ python anubis.py -t test -tn 15 -p test1=1 test2=2 test3=3`

## 配置文件

anubis以json格式进行配置

### 示例配置文件

```python
{
  "name": "test",
  "desc": "testtest",
  "plugins": [
    ["TimePlugin",{}]
  ],
  "params": {
    "test": {
      "type": "int",
      "default": 1
    }
  },
  "nodes": [
    {
      "desc":"节点1",
      "id":"node1",
      "parent":[
        "node4"
      ],
      "plugins": [],
      "action": [
      ]
    },
    {
      "desc":"节点2",
      "id":"node2",
      "parent":[
        "node4"
      ],
      "plugins": [],
      "action": {

      }
    },
    {
      "desc":"节点3",
      "id":"node3",
      "parent":[
        "node1",
        "node2",
        "node4"
      ],
      "plugins": [],
      "action": {

      }
    },
    {
      "desc":"节点4",
      "id":"node4",
      "parent":[
      ],
      "action": {

      }
    }
  ]
}
```

### 参数含义说明

#### Task参数

- name

  类型：string

  必要参数

  Task名称

- desc 

  类型：string

  必要参数

  Task描述

- plugins

  类型：list

  可选参数

  默认值: []

  Task注册的插件列表，插件内容见[插件][# plugin]

- nodes

  类型： list

  必要参数

  nodes参数配置当前Task的运行节点，节点内容见[Node参数][# node]


#### <span id="node">Node参数</span>

- id

  类型: string

  必要参数

  节点id

- desc

  类型：string

  必要参数

  节点描述

- parent

  类型：list

  可选参数

  默认值：[]

  当前节点的前置节点，内容为前置节点的id，前置节点未完成时当前节点不会运行，注意节点依赖关系不要出现环路，出现环路将引发异常

- action

  类型：list

  必要参数

  当前节点执行的命令列表，暂时只支持shell命令

  > 多个命令之间环境相互独立

#### <span id="plugin">插件</span>

##### 配置参数

- 每一个插件配置为一个2元素列表list[2]
- list[0]为插件名，**以插件名命名的类**必须在`pkg/plugin/Plugin.py`或`custom/plugin/Plugin.py`中存在，不存在将会引发异常
- list[1]为插件所需参数，类型为map/dict，键为参数名，值为参数值，**参数名必须与插件类构造函数的形参完全匹配**，否则会引发异常，**但是参数顺序不影响**

##### 自定义插件

- 自定义插件在`custom/plugin/Plugin.py`中编写

- 插件示例

  插件代码：

  ```python
  class Test(PluginBase):
      def __init__(self, test1, test2):
          self.test1 = test1
          self.test2 = test2
  
      def beforeRun(self):
          print("This is a test plugin")
  
      def afterRun(self):
          print("This is a test plugin")
        
  ```

  配置文件：

  ```
  {
  ...
  plugins
  ...
  }
  ```

  

  说明：

  1. 插件类需要继承PluginBase类
  2. 插件类需要实现构造函数，beforeRun和afterRun
  3. 构造函数的参数即为配置中填写的参数
  4. beforeRun为插件修饰的task或node运行前执行内容
  5. afeterRun为插件修饰的task或node运行后执行内容
  6. `pkg/plugin/Plugin.py` 和 `custom/plugin/Plugin.py`中如果有同名插件，会优先取前者的插件；如果同名插件参数不一样传递是后者的插件参数会引发异常
  7. 插件禁止调用python built-in print方法





