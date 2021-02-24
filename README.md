# LibcSearcher-ng
> LibcSearcher-ng, actively maintianed

## Introduction
- 这里是全新的 LibcSearcher 实现。[原版 LibcSearcher 的仓库](https://github.com/lieanu/LibcSearcher)由于缺乏维护，个人测试后发现其基本失效。
- 选择新开一个项目而非基于原有 LibcSearcher 继续开发的原因如下：
  - 保证积极维护带来的可用性。
  - 原仓库基于 [libc-database](https://github.com/niklasb/libc-database) ，拷贝其数据库中的部分常用 libc 文件，在本地进行求解。这一方案有两个问题：
    - libc 库不完整，仅包含了常用 libc 文件。若下载整个数据库则磁盘占用和下载成本过大。
    - 上游数据库更新时不方便及时获悉，且需要手动更新本地数据库。
  - 上游 libc-database 现已提供 web-api，可直接向其服务发起请求获取查询结果，解决了上述两个问题。故采用这种新的实现方案。