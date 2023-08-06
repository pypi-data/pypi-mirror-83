'''

generate markdown report by template or custom template

author: xujing
date: 2020-10-23

'''

import codecs
import collections
# import pprint
from prettytable import PrettyTable
import datetime
import os
import shutil
import numpy as np


def RenderData():
    RenderDict = collections.OrderedDict()
    DickNames = ["Title","Label2en",'SplitRate',"TrainNum","DevNum",'TrainLabelStat',"TestNum","TestLabelStat",
        "ModelDes","TestStatVOC","VOCPR","TestSatCOCO","COCOPR"]

    RenderDict = RenderDict.fromkeys(DickNames)

    GetRenderDes()
    return RenderDict

def GetRenderDes():
    table = PrettyTable(['编号',"属性","说明","类型","样例","ID"])
    table.add_row(['1', "Title", "测试文档标题","string","EUS目标检测测试报告",0])
    table.add_row(['2', "Label2en", "中英文Label的字典","dict","{癌：cancer}",2])
    table.add_row(['3', "SplitRate", "训练和验证集的划分结果","string","9:1",3])
    table.add_row(['4', "TrainNum", "训练数据的样本量","string/numeric","1000",4])
    table.add_row(['5', "DevNum", "验证集(开发集)的样本量","string/numeric","1000",5])
    table.add_row(['6', "TrainLabelStat", "分类别的训练集的统计","dict","{Cancer:100}",6])
    table.add_row(['7', "TestNum", "测试集的样本数量","string/numeric","1000",7])
    table.add_row(['8', "TestLabelStat", "分类别的测试集的统计","dict","{Cancer：1000}",8])
    table.add_row(['9', "ModelDes", "训练模型的描述","list","[模型采用YOLO v3, 优化器采用SGD]",9])
    table.add_row(['10', "TestStatVOC", "测试结果，该数据由库中函数返回值填充","\\","\\",10])
    table.add_row(['11', "VOCPR", "提供图片保存的路径","path","./P-R-Curve-VOC.png",11])
    table.add_row(['12', "TestSatCOCO", "测试结果列表长度为11","list","[0.1,0.2]",12])
    table.add_row(['13', "COCOPR", "提供图片保存的路径","path","./P-R-Curve-COCO.png",13])

    print(table)

def read_md(fname):
    return codecs.open(fname,encoding='utf-8').read()

def write_md(file,data,mode="a"):
    fw = codecs.open(file,mode,'utf-8')
    fw.write(data)
    fw.close()

def gen_markdown_table_2d(head_name, rows_name, cols_name, data):
    """
    Params:
        head_name: {str} table head 
        rows_name, cols_name: {list[str]} project name， like 1,2,3
        data: {ndarray(H, W)}
    
    Returns:
        table: {str}
    """
    ELEMENT = " {} |"

    try:
        H, W = data.shape
    except:
        H, W = 0, 0

    LINE = "|" + ELEMENT * W
    
    lines = []

    
    lines += ["| {} | {} |".format(head_name, ' | '.join(cols_name))]

    # split line
    SPLIT = ":{}:"
    line = "| {} |".format(SPLIT.format('-'*len(head_name)))
    for i in range(W):
        line = "{} {} |".format(line, SPLIT.format('-'*len(cols_name[i])))
    lines += [line]
    
    # date
    for i in range(H):
        d = list(map(str, list(data[i])))
        lines += ["| {} | {} |".format(rows_name[i], ' | '.join(d))]

    table = '\n'.join(lines)
    return table

def gen_markdown_img(imgpath):
    img_slot = "\n![]({})\n".format(imgpath)

    return img_slot

def gen_markdown_list(data_list):

    m_list = "\n"

    for d_list in data_list:
        m_list += "+ " + str(d_list) + "\n"

    return m_list


def GenmdReport(render=None,templates="typical"):
    i = datetime.datetime.now()
    save_name = str(i).replace(" ","-").replace(":","-").replace(".","-")

    today_date = str(i.year)+"-"+str(i.month)+"-"+str(i.day)

    # 将orderdict处理成markdodn字符串，如果是None，填充为空字符串（或暂时没有计算该指标）
    render_0 = render["Title"]
    if render_0 is None:
        render_0 = "测试报告"

    render_1 = today_date

    render_2_ = render["Label2en"]
    if not render_2_ is None:
        render_2 = gen_markdown_table_2d(head_name="中文\英文", 
            rows_name=list(render_2_.keys()), cols_name=["Label"], data=np.array(list(render_2_.values())).reshape((-1,1)))
    else:
        render_2 = gen_markdown_table_2d(head_name="中文\英文", 
            rows_name=[], cols_name=["Label"], data=np.array([]))+"\n|   |"

    render_3 = render["SplitRate"]
    if render_3 is None:
        render_3 = "暂无"

    render_4 = render["TrainNum"]
    if render_4 is None:
        render_4 = "暂无"

    render_5 = render["DevNum"]
    if render_5 is None:
        render_5 = "暂无"

    render_6_ = render["TrainLabelStat"]
    if not render_6_ is None:
        render_6 = gen_markdown_table_2d(head_name="类别\标注框数量", 
            rows_name=list(render_6_.keys()), cols_name=["数量"], data=np.array(list(render_6_.values())).reshape((-1,1)))
    else:
        render_6 = gen_markdown_table_2d(head_name="类别\标注框数量", 
            rows_name=[], cols_name=["数量"], data=np.array([])) + "\n|   |"

    render_7 = render["TestNum"]
    if render_7 is None:
        render_7 = "暂无"

    render_8_ = render["TestLabelStat"]
    if not render_8_ is None:
        render_8 = gen_markdown_table_2d(head_name="类别\标注框数量", 
            rows_name=list(render_8_.keys()), cols_name=["数量"], data=np.array(list(render_8_.values())).reshape((-1,1)))
    else:
        render_8 = gen_markdown_table_2d(head_name="类别\标注框数量", 
            rows_name=[], cols_name=["数量"], data=np.array([]))+"\n|   |"

    render_9_ = render["ModelDes"]
    if render_9_ is None:
        render_9 = ""
    else:
        render_9 = gen_markdown_list(render_9_)


    render_10_ = render["TestStatVOC"]

    if render_10_ is None:
        head_name_10 = "Class"
        rows_name_10 = ['P', 'R', 'F-Score',  'total TP', 'total FP','VOC AP']
        render_10 = gen_markdown_table_2d(head_name_10, [], rows_name_10,  data=np.array([]))+"\n|   |"
    else:
        metricsPerClass,metricsAll = render["TestStatVOC"][0], render["TestStatVOC"][1]
        head_name_10 = "Class"
        rows_name_10 = ['P', 'R', 'F-Score',  'total TP', 'total FP','VOC AP']

        cols_name_10 = []
        data_10 = []
        for mc in metricsPerClass:
            # Get metric values per each class
            cols_name_10.append(mc['class'])
            precision = mc['precision']
            recall = mc['recall']
            f_score = mc['f_score']
            average_precision = mc['AP']
            tp = mc['total TP']
            fp = mc['total FP']

            data_10.extend([round(precision[-1],4),round(recall[-1],4),round(f_score,4),int(tp),int(fp),round(average_precision,4)])


        all_precision = round(metricsAll["all_precision"],4)
        all_recall = round(metricsAll["all_recall"],4)
        all_f_score = round(metricsAll["all_f_score"],4)
        all_ap = round(metricsAll["total_map"],4)

        cols_name_10.append("all")
        data_10.extend([all_precision,all_recall,all_f_score,"\\", "\\", "VOC mAP:{}".format(all_ap)])
     
        render_10 = gen_markdown_table_2d(head_name_10, cols_name_10, rows_name_10,np.array(data_10).reshape((-1,6)))


    render_11_ = render["VOCPR"]
    try:
       render_11 = gen_markdown_img(render_11_) 
    except:
        render_11 = ""

    render_12_ = render["TestSatCOCO"]
    if render_12_ is None:
        render_12 = gen_markdown_table_2d(head_name="COCO AP", 
            rows_name=[], 
            cols_name=["AP"], 
            data=np.array([]))+"\n|   |"
    else:
        render_12 = gen_markdown_table_2d(head_name="COCO AP", 
            rows_name=["AP@50","AP@55","AP@60","AP@65","AP@70","AP@75","AP@80","AP@85","AP@90","AP@95","AP@50:95"], 
            cols_name=["AP"], 
            data=np.array(render_12_).reshape((-1,1)))

    render_13_ = render["COCOPR"]
    try:
       render_13 = gen_markdown_img(render_13_) 
    except:
        render_13 = ""

    if templates == "typical":
        md_file = os.path.join(os.path.join(os.path.expanduser('~'),".detmetric/template"),"report.md")
        static_files = os.listdir(os.path.join(os.path.expanduser('~'),".detmetric/template/static"))

        content = read_md(md_file)
        # 将上述字符串format到markdown文档。
        render_dat = (render_0,render_1,render_2,render_3,render_4,render_5,
            render_6,render_7,render_8,render_9,render_10,render_11,render_12,
            render_13)
        render_content = content.format(*render_dat)

        if not os.path.exists("./detect_report"):
            os.makedirs("./detect_report")

        if not os.path.exists("./detect_report/static"):
            os.makedirs("./detect_report/static")

        for file in static_files:
            shutil.copy(os.path.join(os.path.expanduser('~'),".detmetric/template/static")+"/"+file, "./detect_report/static/"+file)

        # shutil.copy(os.path.join(os.path.dirname(__file__), "template/report.md"), "./detect_report/"+save_name+".md")
        write_md("./detect_report/"+save_name+".md",render_content)
        print("[INFO] 测试报告保存在了： {}".format("./detect_report/"+save_name))
    else:
        if not templates.split(".")[-1] in ['md','markdown']:
            raise "[detmetric Error]: There is no valid markdown template in this path."
        md_file = templates
        static_files = os.listdir(os.path.join(os.path.expanduser('~'),".detmetric/template/static"))

        content = read_md(md_file)
        # 将上述字符串format到markdown文档。
        render_dat = (render_0,render_1,render_2,render_3,remder_4,render_5,
            render_6,render_7,render_8,render_9,render_10,render_11,render_12,
            render_13)
        render_content = content.format(*render_dat)

        if not os.path.exists("./detect_report"):
            os.makedirs("./detect_report")

        if not os.path.exists("./detect_report/static"):
            os.makedirs("./detect_report/static")

        for file in static_files:
            shutil.copy(os.path.join(os.path.expanduser('~'),".detmetric/template/static")+"/"+file, "./detect_report/static/"+file)

        # shutil.copy(md_file, "./detect_report/"+save_name+".md")

        write_md("./detect_report/"+save_name+".md",render_content)
        print("[INFO] 测试报告保存在了： {}".format("./detect_report/"+save_name))


def GetmdTemplates(templates='typical'):
    i = datetime.datetime.now()
    save_name = str(i).replace(" ","-").replace(":","-").replace(".","-")

    if templates == "typical":
        md_file = os.path.join(os.path.join(os.path.expanduser('~'),".detmetric/template"),"report.md")
        static_files = os.listdir(os.path.join(os.path.expanduser('~'),".detmetric/template/static"))

        content = read_md(md_file)

        if not os.path.exists("./templates"):
            os.makedirs("./templates")

        if not os.path.exists("./templates/static"):
            os.makedirs("./templates/static")

        for file in static_files:
            shutil.copy(os.path.join(os.path.expanduser('~'),".detmetric/template/static")+"/"+file, "./templates/static/"+file)

        shutil.copy(os.path.join(os.path.join(os.path.expanduser('~'),".detmetric/template"),"report.md"), "./templates/"+save_name+".md")
        print("[INFO] 拉取模板：{}，空模板保存在：{}".format(templates,"./templates/"+save_name+".md"))

if __name__ == "__main__":
    pass
    # import numpy as np
    # head_name = "姓名\科目"
    # rows_name = ["小妖", "小怪", "小兽"]
    # cols_name = ["A", "B", "C", "D"]
    # data = np.arange(4*3).reshape(3, 4)
    # # print(data) # rows 

    # table = gen_markdown_table_2d(head_name, rows_name, cols_name, data)
    # # print(r"哈哈，你好$f(x)=\frac{{1}}{{3}}$\n"+table)
    # write_md("test.md","哈哈，你好$f(x)=\\frac{{1}}{{3}}$\n"+table+gen_markdown_img("./P-R-Curve-VOC.png"))

    head_name = "姓名\科目"
    cols_name = ["Label","label2"]
    rows_name = ["1","2","3"]
    data = np.array([1,2,3,4,5,6]).reshape((-1,2))

    table = gen_markdown_table_2d(head_name, rows_name, cols_name, data)


    # head_name = "姓名\科目"
    # cols_name = ["Label"]
    # rows_name = []
    # data = np.array([])

    # table = gen_markdown_table_2d(head_name, rows_name, cols_name, data) +"\n|   |"
    write_md("test.md","哈哈，你好$f(x)=\\frac{{1}}{{3}}$\n"+table+gen_markdown_img("./P-R-Curve-VOC.png"))
