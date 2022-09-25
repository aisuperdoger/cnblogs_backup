原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/09/17/16702840.html
提交日期：Sat, 17 Sep 2022 08:06:00 GMT
博文内容：
# 1. 基础
由于我学了前两篇的东西以后，还是感觉不太懂vim，所以又去看了看[玩转Vim 从放弃到爱不释手【PegasusWan】](https://www.imooc.com/learn/1129)，并做了如下的记录：



## 1.1 vim多文件操作

概念：
```
Buffer: 内存缓冲区

Window: Buffer的可视化分割区域

Tab: 组织Window为一个工作区
```

Buffer：
```
:ls 列举当前缓冲区

:b [num] 跳转到[num]缓冲区

:b [name] 跳转到[name]缓冲区

:bpre/bnext/bfirst/blast 跳转到上一个/下一个/第一个/最后一个缓冲区

:e [name] 打开[name]文件
```
Window:
```
C-w s 水平分割窗口

C-w v 垂直分割窗口

C-w w 循环切换窗口

C-w h/j/k/l 切换到←/↓/↑/→窗口 

C-w H/J/K/L 移动当前窗口向←/↓/↑/→

C-w = 所有窗口等宽高

C-w _/| 当前窗口最大化高度/宽度

[num]C-w _/| 当前窗口高度设为[num]行/列

vim duck.go duck.py -O   # 在两个窗口中打开两个文件
```
tab（用的不是特别多）：
```
:tabnew 新建标签页

:tabe [name] 在新标签页打开[name]文件

:tabc 关闭当前标签页和窗口

:tabo 只保留当前标签页并关闭其他的

C-w T 将当前窗口移动到新标签页【本标签页有两个以上的窗口才能移动】

:tabn [num] 切换到[num]标签页，没有[num]表示下一个  【[num]gt 效果一样】
:tabp [num] 切换到[num]标签页，没有[num]表示上一个  【[num]gT 效果一样】
```


## 1.2 vim复制粘贴与寄存器的使用

vim在Normal模式复制粘贴： 

- Normal模式下复制粘贴分别使用y（yank）和p（put），剪切d和p

- 可以使用v（visual）命令选中所要复制的地方，然后顺遂p粘贴

- 配合文本对象：比如顺遂yiw复制一个单词，yy复制一行


Insert模式下的复制粘贴：如果在vimrc中设置了autoindent，那么在从别的地方复制代码过来的时候，可能会出现代码混乱。这个时候需要使用`:set paste`。如果需要恢复autoindent，只需要执行`:set nopaste`。


什么是vim的寄存器：

- vim里操作的是寄存器而不是系统剪切版，这和其他编辑器不同

- 默认使用d删除或者y复制的内容都放到了“无名寄存器”

- 用x删除一个字符放到无名寄存器，然后p粘贴，可以调换俩字符

深入寄存器（register）：

- 通过`"{register}`前缀可以指定寄存器，不指定默认无名寄存器

- 比如使用`"ayiw`复制一个单词到寄存器a中，`"bdd`删除当前行到寄存器b中

- :reg a查看寄存器a中的内容

- `"a p`粘贴a寄存器中的内容

其他常见寄存器：

除了有名的寄存器a-z，vim中还有一些其他常见寄存器

- 复制专用寄存器`"0`：使用y复制的文本会被拷贝到复制寄存器0和无名寄存器

- 系统剪切版`"+`可以复制到系统剪切版。`:echo has('clipboard')`查看vim是否支持这个功能。如果不支持，试一试安装：sudo apt install xclip -y

- 其他寄存器，比如`"%`当前文件名，`".`上次插入的文本

- :set clipboard=unnamed可以让你直接复制粘贴系统剪切版内容


##  1.3 vim宏（macro）
vim宏：录制一系列操作。
- vim使用q来录制，同时也也是q结束录制
- 使用q{register}选择要保存的寄存器，把录制的命令保存其中

- 使用@{register}回放寄存器中保存的一系列命令



**实例：给文本的每行都加上双引号**
首先我们要录制如何给一行加上双引号，然后将录制的内容回放到所有行。
给一行加上双引号：
```
qa：将操作存储在a寄存器中
I：到行首，加上双引号
A：到行尾，加上双引号
```
将录制的内容回放到所有行：
```
V：按行选取。选择所有行。
按:，然后输入normal @a，从而将寄存器a中的操作进行回放
```
给文本的每行都加上双引号的其他方法：
```
V,G：全选所有行
按:，然后输入normal I"，这样就给所有行加上了前双引号
# 按:，然后键入ctrl p，可复制上一个命令，即normal I"
按:，然后输入normal A"，这样就给所有行加上了后双引号
```



## 1.4 Vim更换配色

- 使用``` :colorscheme``` 显示当前的主题配色，默认是 default

- 用``` :colorscheme  <ctrl + d>``` 可以显示所有的配色 （注意：命令:colorscheme加一个空格再按ctrl+d）。然后用`:colorscheme 配色方案`，即可更换配色方案。


如果在本地没有满意的配色，可以到GitHub中输入vim colorscheme查找vim各种配色
- [vim-hybrid](https://github.com/w0ng/vim-hybrid "vim-hybrid")这个主题也不错。

- 下载到本地，解压。
- 将 `hybrid.vim` 文件移动到 `~/.vim/colors`（如果没有这个目录的话，使用`mkdir ~/.vim/colors -p`先创建文件夹。然后使用`:colorscheme hybrid`就可以更换配色方案。

- 可以下载多个配色到 `~/.vim/colors`即可随时更换


下面几种流行的配色方案：
- vim-hybird 配色: github.com/w0ng/vim-hybrid
- solarized 配色: github.com/altercation/vim-colors-solarized
- gruvbox 配色: github.com/morhetz/gruvbox



## 1.5 vim配置
vim的配置文件放在~/.vimrc中
nvim的配置文件放在~/.config/nvim/init.vim中


下面是视频中提到的一些常用设置：
```
set number " 设置行号
colorscheme hybrid

" 按F2进入粘贴模式。F2代表set paste或set nopaste
set pastetoggle=<F2> 

" 高亮搜索
set hlsearch

" 设置折叠方式
set foldmethod=indent

"   一些方便的映射
let mapleader= ','  # 设置逗号为leader键

let g:mapleader=','

" 使用jj进入normal模式，`^的作用为：进入normal模式，光标位置保持不变
" help `^  可查看对应的含义
inoremap jj <Esc>`^ 

"使用leader+w 直接保存

inoremap <leader>w <Esc> :w<cr>

noremap < leader>w :w<Cr>

" 切换buffer

nnoremap <silent> [b :bprevious<CR>

nnoremap <silent> [n :bnext<CR>

" use ctrl+h/j/k/L switch window
noremap <C-h> <C-w>h

noremap <C-j> <C-w>j

noremap <C-k> <C-w>k

noremap <C-l> <C-w>l



"Sudo to write

cnoremap w!! w !sudo tee % >/dev/null
```




## 1.6 vim映射

插入模式删除整行的操作：
```
:imap <c-d> <Esc>ddi  代表映射插入模式下的快捷键，先按Esc，然后删除整行（dd），最后回到插入模式（i）
```



```
:nmap - dd
:nmap \ -
```
当你按下\时，Vim会解释其为-，而我们又映射了-，Vim会继续解析为dd，即\起到删除整行的作用。(是不是有点类似于递归)

Vim提供了非递归映射,这些命令不会递归解释，如nnoremap/ynoremap/inoremap

任何时候你都应该使用非递归映射，这样比较安全。





# 2.插件

## 2.1 美化插件
- 修改启动界面: https://github.com/mhinz/vim-startify ，vim的打开界面，可以看到我们最近打开的文件
- 状态栏美化: https://github.com/vim-airline/vim-airline
- 增加代码缩进线条: https://github.com/yggdroot/indentline

安装插件的时候，可能需要fanqiang，并且多执行几次:PlugInstall直到 安装成功。


一般插件的github官网上都有插件相关的变量的说明，可以参照进行设置。


## 2.2 寻找需要的插件
直接用英文进行google，然后就可以找到相关的github项目
https://vimawesome.com


## 2.3 taglist 查看源码
taglist：提供源代码符号的结构化视图。
安装见：https://github.com/yegappan/taglist ，使用插件管理器vim-plug安装此插件即可。




## 2.4 ctrlpvim/ctrlp.vim
配置：
```
let g:ctrlp_map = '<c-p>' 　＂ 使用ctrl p调用插件
```
与ctrlp相比，前面我们提到过的leaderf似乎更加强大。


## 2.5 快速跳转
easymotion/vim-easymotion

配置：
```
nmap ss <PLug>(easymotion-s2) " 由于easymotion-s2也是个映射，所以这里使用非递归映射
```
使用方法：输入ss，然后再输入需要跳转位置的前两个单词，有这两个字母的位置会出现红色的的快捷字母，最后按下相关位置的快捷键。

## 2.6 编辑成对符号的插件
https://github.com/tpope/vim-surround

使用方法：
```
normal模式下增加,删除,修改成对内容
ds (delete a surrounding)
cs (change a surrounding)
ys (you add a surrounding)
```
使用实例：
- `ysiw"`：代表使用`ys`开始增加成对内容，此时会自动进入可视模式，使用`iw`代表选择一个单词，最后使用`"`给此单词两边增加双引号。
- `cs"'`：将双引号替换成单引号
- `cs"[`：将双引号替换成[]，这样会有空格，`cs"]`不会有空格（你试试就知道我的空格是啥）
- `ds'`：删除单引号



## 2.7 模糊搜索
vim中可以使用`\`进行精确地搜索，但是不能实现模糊搜索。

模糊搜索插件：https://github.com/junegunn/fzf.vim

配置：
```
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
```
```
使用:Ag [PATTERN]模糊搜索字符串
```
要实现以上功能，需要按照github中的说明，安装相应的依赖，如Ag就需要： `sudo apt-get install silversearcher-ag`


## 2.8 tagbar 浏览源码大纲

preservim/tagbar用于浏览当前文件的源码大纲
需要安装ctag才能实现相应的功能

配置：
```
" tagbar 打开大纲
nnoremap <leader>t :TagbarToggle<CR>
```


# 进阶
我觉得需要继续进阶，可看[链接](https://github.com/wsdjeg/vim-galore-zh_cn)

我只看了一点点，记录在这：
```
:enew：创建未命名文件
:w /tmp/foo：将文件存入/tmp/foo中

g:mapleader：g代表mapleader是全局变量

nvim ~/projects/cpp/muduo/muduo_source/examples/simple/ 使用nvim开启目录。

```
