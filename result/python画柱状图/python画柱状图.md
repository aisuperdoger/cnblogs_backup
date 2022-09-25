原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522392.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <pre><code># 利用条形图展示各个置信度区间的框数
def show_bar(bbox_lists, TP_lists, gt_folder):
    # plt中需要输入list
    bbox_lists = bbox_lists.tolist()
    TP_lists = TP_lists.tolist()

    gts = gt_num(gt_folder)

    for i, (bbNum, tpNum) in enumerate(zip(bbox_lists, TP_lists)):
        if i==0:
            sub_show_bar(bbNum, tpNum,gts['gtPersonNum']+gts['gtLifeJacketNum'])
        elif i==1:
            sub_show_bar(bbNum, tpNum, gts['gtPersonNum'])
            print("Recall:",np.sum(tpNum)/gts['gtPersonNum'])
        elif i ==2:
            sub_show_bar(bbNum, tpNum, gts['gtLifeJacketNum'])

def sub_show_bar(bbNum, tpNum, gtNum):
    # 这两行代码解决 plt 中文显示的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 输入统计数据
    conf_lists = ('0.3~0.35', '0.35~0.4', '0.4~0.45', '0.45~0.5.',
                  '0.5~0.55', '0.55~0.6', '0.6~0.65', '0.65~0.7',
                  '0.7~0.75', '0.75~0.8', '0.8~0.85', '0.85~0.9',
                  '0.9~0.95', '0.95~1', 'gt', 'tp_bb')

    bar_width = 0.45  # 条形宽度
    index_bbox_lists = np.arange(len(conf_lists))  # 预测的所有框的条形图的横坐标
    index_TP_lists = index_bbox_lists + bar_width  # 预测正确框的条形图的横坐标

    plt.barh(index_TP_lists, width=tpNum + [gtNum, np.sum(tpNum)], # np.sum(tpNum)不是总数，只是IOU大于0.3的总数
             height=bar_width, color='g', label='预测正确的框')
    plt.barh(index_bbox_lists, width=bbNum + [gtNum, np.sum(bbNum)],
             height=bar_width, color='b', label='预测出的框')

    plt.legend()  # 显示图例
    plt.yticks(index_bbox_lists + bar_width / 2,
               conf_lists)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置
    plt.xlabel('框数')  # 纵坐标轴标题

    # 在图像上添加文字

    for a, b in zip(index_bbox_lists, bbNum + [gtNum, np.sum(bbNum)]):
        plt.text(b + 0.1, a - 0.1, str(b), size=8, ha='center')

    for a, b in zip(index_TP_lists,tpNum + [gtNum, np.sum(tpNum)]):
        plt.text(b + 0.1, a - 0.1, str(b), size=8, ha='center')

    plt.show()

</code></pre>
                