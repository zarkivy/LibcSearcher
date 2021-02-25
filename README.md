# LibcSearcher-ng
<br>

## Introduction

- 这里是全新的 LibcSearcher 实现。基于 [libc-database](https://github.com/niklasb/libc-database) 云端数据库而非本地数据库。
- [原版 LibcSearcher 仓库](https://github.com/lieanu/LibcSearcher)由于年久失修，经测试发现其基本失效。
- 选择新建一个项目而非基于原有 LibcSearcher 继续开发的原因如下：
  - 原仓库基于 libc-database ，拷贝其数据库中的部分常用 libc 文件，在本地进行求解。这一方案有两个问题：
    - libc 库不完整，仅包含了常用 libc 文件。若下载整个数据库则磁盘占用和下载成本过大。
    - 上游数据库更新时不方便及时获悉，且需要手动更新本地数据库。
  - libc-database 现已提供 web-api，可直接向其服务发起请求获取查询结果，解决了上述两个问题。
- 同时为了确保师傅们以前的 exp 的可用性，LibcSearcher-ng 将以与原 LibcSearcher 完全相同的接口来构建。
- 比起原版 LibcSearcher 只多了一个缺点：断网就不可用了。🤣
- 若需要基于本地数据库的~~可以抵御断网攻击的~~ LibcSearcher，github 上已有其他师傅维护了相应实现的 LibcSearcher 仓库。

<br>

## Installation

#### 使用 PIP

```shell
sudo pip3 install LibcSearcher
```

更新

```python
sudo pip3 install -U LibcSearcher
```

#### 使用本仓库

```shell
git clone https://github.com/IZAY01/LibcSearcher.git
cd LibcSearcher
sudo python3 setup.py develop
```

> 如要更新，只需拉取最新代码后，重新在仓库目录内执行 `sudo python3 setup.py develop`

<br>

## Usage

```python
from LibcSearcher import *
obj = LibcSearcher("fgets", 0x7ff39014bd90) # 使用一个已知符号地址作为初始约束，初始化 LibcSearcher
obj.add_condition("atoi", 218528) # 添加一个约束条件
obj.dump("printf") # 根据已有约束条件，查询某个符号在 Libc 中的地址
```

> 此外，比起以上原版接口，添加了如下些许姿势

```python
len(obj) # 返回在当前约束条件下，可能的 Libc 数量

print(obj) # 若 Libc 已被唯一确定，打印其详细信息

for libc in obj :
    print(libc) # 实现了迭代器，打印(或其它操作)当前所有可能的 Libc 

obj.select_libc() # 打印可能的 Libc 列表，手动选择一个认为正确的 Libc
obj.select_libc(2) # 手动选择 2 号 Libc 作为正确的 Libc
```

