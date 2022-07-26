import xml.etree.ElementTree as ET
import os
import requests
import re

 # 将文章中图片下载到images_path，并修改md文件中的图片路径为本地
def  downloadImage(descirption,dir_path,images_path):
    
    images_links = re.findall("https://img.*?.png",descirption)
    for i in images_links:
        # 获取网络图片资源
        r = requests.get(i)
        # 判断响应状态
        if r.status_code == 200:
            # 创建文件保存图片
            local_images_path = os.path.join(os.path.join(dir_path,images_path), re.findall('https://.*?/.*?/.*?/.*?/(.*?.png)',i)[0])
            with open(local_images_path,'wb') as f:
                # 将图片字节码写入创建的文件中
                f.write(r.content)      

            # 使用本地图片替换descirption中的链接图片、
            descirption = re.sub(i, os.path.join(images_path,re.findall('https://.*?/.*?/.*?/.*?/(.*?.png)',i)[0]), descirption)
        else:
            print('获取失败')
        
        
    return descirption



if __name__ == "__main__":
    tree = ET.parse("CNBlogs_BlogBackup.xml")
    # 根节点
    rss = tree.getroot()
    # 标签名
    # channel = rss[0]
    # print('root_tag:',root[0].tag)
    i = 0
    for channel in rss:
        # 前面七个标签没什么用

        for item in channel:
            i += 1
            if (i >7):
                print("第"+str(i-7)+"篇")
                title = item[0].text.replace('/', '／') # 标题中有/时，会被当成目录的分隔符，所以这里进行了替换
                link = item[1].text
                pubDate = item[4].text
                descirption = item[6].text
                
                dir_path = os.path.join("result",title)
                if not os.path.exists( dir_path):
                    os.makedirs(dir_path)
                else:
                    print("博客标题重复："+title)
                    continue

                with open(os.path.join( dir_path,title+".md"), 'w', encoding='utf-8') as file:
                    file.write('原文链接：'+link)
                    file.write('\r\n提交日期：'+pubDate)
                    
                    images_path = os.path.join(dir_path,title+"_img")
                    if not os.path.exists(images_path):
                        os.makedirs(images_path)
                    else:
                        print("图片存储路径重复添加！")
                        continue

                    # 将文章中图片下载到images_path，并修改md文件中的图片路径为本地
                    descirption_re = downloadImage(descirption,dir_path,title+"_img")
                    file.write("\r\n博文内容：\r\n"+descirption_re)

