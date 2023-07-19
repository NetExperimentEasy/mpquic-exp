mpquic (xquic) 在minitopo实验

# 运行本实验，你首先需要安装mininet和minitopo
参考这个仓库：https://github.com/NetExperimentEasy/sigcomm20_mptp_tutorial_for_CN

# 运行前，还得向minitopo增加xquic实验脚本
向minitopo的experiments目录下增加本目录experiments中的xquic.py

# 在tmp目录下进行实验
- `cd tmp`
- `mprun -t ../topo -x ../exp`

> 本仓库附带的server和client已经将MAX_BUF_SIZE调大 >> https://github.com/NetExperimentEasy/static-build-xquic

> 更多实验控制，需要修改xquic.py

> 目前数据分析只能通过wireshark分析pcap包


# 多路径对比图

链路情况：

```
    40ms,20mbps
 /-sw---bl---sw-\ 
c                r                s
 \-sw---bl---sw-/ \-sw---bl---sw-/
    40ms,30mbps
```

拥塞算法:bbr

单路径：
![](./pics/2023-03-10_14-11-%E5%8D%95%E8%B7%AF%E5%BE%84.png)

多路径：
![](./pics/2023-03-10_14-13-%E5%A4%9A%E8%B7%AF%E5%BE%84.png)

> 为确保试验性能，编译xquic时尽量编译Release，运行测试时 -l e 指定log为error级别而非debug级别（很吃性能）
