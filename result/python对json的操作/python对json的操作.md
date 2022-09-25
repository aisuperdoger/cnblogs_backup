原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522393.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <ol><li>将字典转为json</li></ol> 
<pre><code>def delete_imgData(folder):
    files = os.listdir(folder)
    for file in files:
        obj = {}
        obj["version"] = "4.5.7"
        obj["flags"] = {}
        obj["shapes"]=[]


        bbs_xyxy = get_bbs(os.path.join(folder,file))

        for bb in bbs_xyxy:
            obj["shapes"].append({"label":bb[0],
                                  "points":[
                                            [
                                              bb[1],
                                              bb[2]
                                            ],
                                            [
                                              bb[3],
                                              bb[4]
                                            ]
                                          ],
                                  "group_id": None,
                                  "shape_type": "rectangle",
                                  "flags": {}
                                  })

        obj["imagePath"] = "..\\" + file[:-3]+"bmp"
        obj["imageData"] = None
        obj["imageHeight"] = 2160
        obj["imageWidth"] = 3840

        print("json" + "\\" + file[:-3]+"json")
        open("json" + "\\" + file[:-3]+"json", "w").write(
            json.dumps(obj, indent=2, separators=(',', ': '))
        )

</code></pre> 
<p>2.读取json文件</p> 
<pre><code>def delete_imgData(folder):
    # subFolders = os.listdir(folder)

    # for subFolder in subFolders:
    # files = os.listdir(os.path.join(folder, subFolder))

    files = os.listdir(folder)
    for file in files:
        obj = json.load(open(os.path.join(folder, file)))
        print(type(obj["flags"]))
        if obj["imageData"]==None:
            continue
        obj["imageData"]=None
        print("running.....")
        open(os.path.join(folder, file), "w").write(
            json.dumps(obj,indent=2, separators=(',', ': '))
        )
</code></pre>
                