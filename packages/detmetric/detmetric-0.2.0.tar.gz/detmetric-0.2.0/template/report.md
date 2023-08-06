## {0} 

**测试日期： {1}**

------

### 1.数据集的情况

1. 检测类别的中英文对用关系：
{2}

2. 训练集和验证集(开发集)的划分比例：**{3}**，其中训练集共：**{4}**张，验证集(开发集)共 : **{5}**张，其每个类别的标注框的统计情况如下表：
{6}
3. 在测试集上的图像数量为：**{7}**张，其每个类别的标注框的统计情况如下表：
{8}


------

### 2.训练算法说明

{9}


------

### 3.测试结果

在测试集上，测试提供了每个类别的，Precision, Recall, F-Score, TP, FP, 及VOC的AP及mAP的模型统计指标，其统计结果如下：

{10}

同时绘制了在该测试数据下的P-R曲线，其曲线下的面积即为AP。

{11}

基于该测试集的COCO AP的计算结果如下表所示：

{12}

其对应的P-R曲线为：

{13}


*注：* 关于上述评级指标的详细定义，可以参考**附录：评价指标说明**部分，内有详细的推导和评价指标的解释。


------
------

### 附录：评价指标说明

> (1) 图像检测阈值定义

首先预测的实例(框)A会经过概率阈值的筛选，当预测概率小于概率阈值时，将删除该预测实例(框)

图像检测需要使用矩形框将目标检测物体选中，根据用户检测结果和目标框之间重叠比率大于IoU阈值，视为合格候选，预测的实例A和真实实例B之间的IoU (Intersection over Union)的计算公式为：
$$
IoU(A,B)=\frac{{A\cap B}}{{A\cup B}}
$$

![](static/iou.png)

即当IoU大于IoU阈值时，认为该预测实例(框)A与真实实例(框)(GT) B，在Box预测层面算是真阳性(FP)预测。

对于每一个GT Box,最终可能出现的预测结果有：

![](static/predict_type.png)

**Fig1: 预测结果示意图**



> (2) 评价指标定义

**精确率(Precision):**

**精确率(Precision)又叫查准率**，它是针对预测结果而言的（即Fig1中的粉红色Box), 它的含义是在所有被预测为正的样本中实际为正的样本概率，其定义为：
$$
Precision=\frac{{检测正确的目标数量(Fig1 情况1)}}{{检测正确的目标数量+检测错误的目标数量(Fig1, 所有粉红色的框)}}
$$


精准率和准确率看上去有些类似，但是完全不同的两个概念。精准率代表对正样本结果中的预测准确程度，而准确率则代表整体的预测准确程度，既包括正样本，也包括负样本。

**召回率(Recall):**

**召回率**(Recall)又叫**查全率**，它是针对Ground Truth而言的，它的含义是**在实际为正的样本中被预测为正样本的概率**，其公式如下：
$$
Recall=\frac{{检测正确的目标数量(Fig1 情况1)}}{{检测正确的目标数量+漏检的目标数量+检测错误的目标数量(Fig1，所有绿色GT框)}}
$$


**F-score：**

Precision和Recall指标有时是此消彼长的，即精准率高了，召回率就下降，在一些场景下要兼顾精准率和召回率，最常见的方法就是F-Measure，又称F-Score。F-Measure是P和R的**加权调和平均**，即：
$$
F_{{\beta}}=\frac{{(1+\beta^2)\times Precision \times Recall}}{{(\beta^2\times Precision)+Recall}}
$$

+ 关于超参数$\beta$需要根据，具体任务进行调整
+ 当$\beta=1$时，也就是常见的F1-Score,是Precision和Recall的调和平均
+ 当F1-Score越大时，模型的性能越好



> (3) 评价指标的置信区间

上述过程中对于 Precision， Recall, F-Score的指标的估计均为**点估计**，数理统计中我们可以对上述评价指标或评价指标的**均值**进行区间估计(confidence interval), 一般我们会计算置信度为$1-\alpha$,(统计学中$\alpha$往往取值为0.05)的置信区间，被称为95%置信区间。

1. 如果我们想对Precision, Recall, F-Score做区间估计，则我们必须找到Precision, Recall, F-Score的概率分布，往往我们通过经验分布去代替概率分布，即如果我们得到Precision, Recall, F-Score的经验分布，就可以近似替代概率分布同时计算出这些统计量的置信区间估计。

设 $x_1,x_2,⋯,x_n$是总体 $F$的一组容量为 $n$ 的样本观测值(对于Precision的观测值，我们需要重复对dev或test数据集进行重复独立抽样$n$次，然后测试计算得到Precision的观测值$p_1,p_2,..,p_n$)，一般的，将它们按从小到大的顺序重新排列得到次序统计量($x_ {{(1)}}< x_ {{(2)}}<...< x_ {{(n)}}$,通过次序统计量近似逼近统计量的分布进而求得置信区间。

则统计量$X$的$1-\alpha$置信区间定义为：
$$
X \in [x_{{(int(n\times\alpha)}}),x_{{(int(n\times(1-\alpha))}}]
$$


2. 往往我们会估计评价指标**均值**的区间估计，其更能反应模型评价指标的稳定性， 对于Precision, Recall, F-Score均值的区间估计，其一般步骤如下:

我们可以估计该随机变量的均值和方差：
$$
\bar{{x}}=\frac{{1}}{{n}}\sum_{{i=1}}^nx_i
$$
他是总体分布均值的无偏估计
$$
s^2=\frac{{1}}{{n-1}}\sum_{{i=1}}^n(x_i-\bar{{x}})^2
$$
是总体方差的无偏估计。

根据**辛钦大数定律**: 设随机变量$x_1,x_2,...,x_n$独立同分布（注意这里可以是任意分布），则随机变量$\bar{{X}}$的分布收敛于正态分布，即：
$$
\bar{{X}}\to N(\mu,\frac{{\sigma^2}}{{n}})
$$
这里的$\mu,\sigma$是随机变量$X$分布的期望和方差，可以用其无偏估计代替，即：
$$
\bar{{X}}\to N(\bar{{x}},\frac{{s^2}}{{n}})
$$
化简后得到：
$$
\frac{{\sqrt{{n}}(\bar{{X}}-\bar{{x}})}}{{s}} \to N(0,1)
$$


该定理可以知道，无论总体分布如何，从中抽取容量为$n$的样本，当$n$足够大时比如(1000,5000,...)，其样本平均数的分布就趋于**正态分布**


基于上述定理，我们可以很容易的计算Precision,Recall, F-Score的**均值**的置信度为$1-\alpha$的置信区间为：
$$
X\in [\bar{{x}}+\frac{{s}}{{\sqrt{{n}}}}Z_{{\alpha}},\bar{{x}}+\frac{{s}}{{\sqrt{{n}}}}Z_{{1-\alpha}}]
$$
这里的$Z_{{1-\alpha}}$是标准正态分布的上$\alpha$分位数，$Z_\alpha$是标准正态分布的下$\alpha$分位数


综上，我们就得到了Precision,Recall, F-Score的置信区间和其均值的置信区间 ，**这里建议使用均值的置信区间，其更稳健**。



> (4) P-R曲线

我们将通过一个检测的例子来说明P-R曲线的画法：

考虑下面的识别结果：

![](static/sample.png)

这里有7张测试图像，15个GT Box(绿色)，24个预测的Box(红色)，通过A,...,Y标注预测框的序号，后接该类别预测的置信度(概率)。

整理上述结果成如下图：

![](static/table1.png)

对于图像中出现了一个GT Box,会有多个预测Box与之对应的情况比如(Images2,3,4,5,6,7), **~~则IoU最高的那个被认为是TP,其他的被认为是FP~~**,~~这个规则和PASCAL VOC 2012的规则是保持一致的~~,**则Confidence最高的那个被认为是TP其他的被认为是FP**。

我们需要对上表按照概率进行排序，然后计算累积的Precision和Recall，如下表所示：

![](static/table2.png)

根据上表我们就可以画出P-R Curve:

![](static/prcurve1.png)



> (5) mAP


+ **AP的计算**

我们有三种不同的方式计算**average precision(AP)**,一种方法叫**11-point interpolation**,另一种方法叫**interpolating all points**,最后是COCO的计算方式，我们将列出这几种方法，供选择。

方式1： 11-point interpolation(Pascal Voc 2008 的AP计算方式)

取Recall的11个点(0,  0.1，0.2， 0.3， 0.4， 0.5， 0.6， 0.7， 0.8， 0.9， 1)，11个点对应的Precision的取值为，Recall 大于当前Recall阈值(比如Recall>0.3)的所有precision中最大的那个值，是该Recall该点下对应的Precision.

![](static/prcurve2.png)

基于这11个Recall的点，计算AP:


![](static/ap1.png)


方式2： interpolating all points （PASCAL VOC 自2010年后就换了另一种计算方法）

新的计算方法假设这N个样本中有M个正例，那么我们会得到M个Recall值(1/M, 2/M, …, M/M),对于每个Recall值r，我们可以计算出对应(r’ > r)的最大precision，然后对这M个precision值取平均即得到最后的AP值。

这种情况更接近于积分的形式：

![](static/ap2.png)

![](static/prcurve3.png)

查看上图，我们可以分为4个区域(A1，A2，A3和A4)：

![](static/prcurve4.png)

计算总面积，我们得到AP：

![](static/ap3.png)

方式3： COCO AP

最新的目标检测相关论文都使用coco数据集来展示自己模型的效果。对于coco数据集来说，使用的也是Interplolated AP的计算方式。与Voc 2008不同的是，为了提高精度，在PR曲线上采样了100个点进行计算，并且COCO不再区分AP和mAP, 对于COCO来说 AP即指的mAP，是对所有类别取平均后的AP的值

+ **mAP的计算**

情形1： VOC mAP的计算

对于VOC而言，AP的计算仅考虑了1个IoU阈值，比如IoU>0.5的每个类别的AP我们能够通过上述方式计算出来，然后对所有类别的AP取平均就是mAP

情形2： COCO mAP的计算

对于COCO来说，AP和mAP的概念是一致的，COCO AP即是VOC的mAP，但是COCO计算了IoU从0.5到0.95每隔0.05的所有10个IoU阈值的COCO AP的平均作为最终的COCO AP的结果。即，COCO AP即mAP,并且其比VOC的mAP多做了一步基于IoU阈值的平均。





