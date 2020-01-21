# 招办汇访问人数Hack

## How to Use

### 安装Docker
不展开说，不会的自行Google

### 修改Config
**修改config.py里的内容：**

- fakeVisitorCount 同时开启的线程数，建议不要超过50 &emsp;&emsp;&emsp;&emsp;*建议修改*
- startUserID UserID目前的可用范围估计在0-500000之间，这里建议填写200000-400000之间的某个数字  &emsp;&emsp;&emsp;&emsp;*建议修改*

> 注意 每个UserID只能绑定一次spreadToken，所以尽量错开来使用，以免出现ID全部都被别人用过了的尴尬状况

- spreadToken 每个人固定的分发标志符 &emsp;&emsp;&emsp;&emsp;***必须修改***

> 如何获取你自己的spreadToken？<br/>
> 1.打开招办汇把自己的二维码保存下来 <br/>
> 2.找一个网页端的二维码识别工具识别出你的链接 这里有一个我使用的，点击[传送门](https://webqr.com/)，（如果无法传送，请复制`https://webqr.com/`自行打开）<br/>
> 3.链接应该是类似于`http://www.zhinengdayi.com/hust?spreadToken=xxxxxxxxxxxxxxxxxxx`,后面的xxxxxxxxxxxxxxxxxxx部分就是你的spreadToken，将其填入config里面

- province 你的省份 举个例子，湖北省请填写 `湖北` ，可以填写`其他` &emsp;&emsp;&emsp;&emsp;***必须修改***
- city 你所在的城市（地级市）名称 举个例子，武汉市请填写`武汉` ，可以填写`其他` &emsp;&emsp;&emsp;&emsp;***必须修改***
- scode 学校代码，默认华科（SAIAJP）&emsp;&emsp;&emsp;&emsp;***必须修改***

> 如何获取scode？<br/>
> 1.在上面步骤中获取到你的传播链接<br/>
> 2.打开Chrome，按f12或右键进入'检查'，右侧会出现debug工具<br/>
> 3.在此状态下将传播链接复制进地址栏并回车<br/>
> 4.在右边debug栏中选择network选项卡，往下拉，会看到一个请求`isLogin?sCode=XXXXXX`<br/>
> 5.`XXXXXX`就是你的scode<br/>

- UAs User-Agents 不懂的可以不用理会，如果想要更安全，更与其他人所区分开来，可以自行网上寻找然后填写进去 &emsp;&emsp;&emsp;&emsp;*可以不修改*

### 构建容器

1. 使用`cd`到当前目录
2. 使用`docker build -t zbh-fucker .`来构建容器
3. 构建好之后使用`docker run zbh-fucker`来启动容器

> docker容器可以在服务器部署，避免了本地电脑开着挂机的窘境

## Notice

1. 仅供学习参考使用，请勿用于商业或非法用途
2. 欢迎 star / pull request / issue
3. 不对使用脚本造成的后果负责
