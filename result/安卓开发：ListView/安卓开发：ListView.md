原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522423.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <p>一，listView简介</p> 
<p>1，listView的功能：显示列表</p> 
<p>2，创建ListView的三要素：（1）布局（决定每一行可以显示什么东西）（2）<span style="color:#323232;">数据：填入View的文字、图片等内容，或者是某些基本组件； （3）适配器：布局和数据都是先放在这里面的，然后再用ListView1.setAdapter(适配器）来设置ListView1中显示什么东西，即将ListView绑定到适配器上。</span></p> 
<div>
 <span style="color:#000000;">3，适配器有几种呢？</span>
</div> 
<div>
 <span style="color:#000000;">（1）ArrayAdapter</span>
 <span style="color:#000000;">，用来绑定一个数组，显 示一行文字； </span>
</div> 
<div>
 <span style="color:#000000;">（2）SimpleAdapter</span>
 <span style="color:#000000;">，在</span>
 <span style="color:#000000;">xml</span>
 <span style="color:#000000;">中定义的布局 ，绑定所对应的数据； </span>
</div> 
<div>
 <span style="color:#000000;">（3）&nbsp;</span>
 <span style="color:#000000;">SimpleCursorAdapter</span>
 <span style="color:#000000;">，用来绑定游标指向的数据，主要用于绑定数据库； </span>
</div> 
<div>
 <span style="color:#000000;">（4） </span>
 <span style="color:#000000;">BaseAdapter</span>
 <span style="color:#000000;">，通用的基础适配器；</span>
</div> 
<div>
 &nbsp;
</div> 
<p>二，ArrayAdapter介绍</p> 
<p>1，ArrayAdapter(Context contenxt, int resource, List&lt;T&gt; objects)</p> 
<p>(1)Context:一个activity或Service都是一个Context。</p> 
<p>（2）resource：布局的ID</p> 
<p>（3）object：通常是一个字符串数组</p> 
<p>2，在UI界面显示ListView</p> 
<p><span style="color:#000000;">（1</span><span style="color:#000000;">）在</span><span style="color:#000000;">Layout</span><span style="color:#000000;">中添加</span><span style="color:#000000;">ListView</span><span style="color:#000000;">控件； </span></p> 
<div>
 <span style="color:#000000;">（</span>
 <span style="color:#000000;">2</span>
 <span style="color:#000000;">）用</span>
 <span style="color:#000000;">setContentView</span>
 <span style="color:#000000;">加载</span>
 <span style="color:#000000;">ListView</span>
 <span style="color:#000000;">，无需设置</span>
 <span style="color:#000000;">Layout</span>
 <span style="color:#000000;">文件； </span>
</div> 
<div>
 <span style="color:#000000;">（</span>
 <span style="color:#000000;">3</span>
 <span style="color:#000000;">）直接继承系统自带的</span>
 <span style="color:#000000;">ListAcitivity</span>
 <span style="color:#000000;">，该</span>
 <span style="color:#000000;">ListActivity</span>
 <span style="color:#000000;">实现了</span>
 <span style="color:#000000;">ListView</span>
 <span style="color:#000000;">，显示ListView的时候做了优化，不需要使用</span>
 <span style="color:#000000;">setContentView</span>
 <span style="color:#000000;">了。</span>
</div> 
<p>3，具体实例：</p> 
<pre class="has"><code>import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ListView;
import android.widget.ArrayAdapter;

public class MainActivity extends AppCompatActivity {
    private String[] mListStr = {"学校：江苏大学","地址：江苏省镇江市","邮编：212013","前身：江苏理工大学"};
    private ListView listView1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//setContentView(R.layout.activity_main);
        listView1=new ListView(this);
        listView1.setAdapter(new
                ArrayAdapter&lt;String&gt;(this,android.R.layout.simple_expandable_list_item_1,mListStr));
        setContentView(listView1);
    }
}</code></pre> 
<p><span style="color:#000000;">实例说明：</span></p> 
<p><span style="color:#000000;">android.R.layout.</span><span style="color:#660e7a;"><strong><em>simple_expandable_list_item_1为系统自带的布局文件。系统自带的布局一般以</em></strong></span><span style="color:#000000;">android.R.layout.开头，而用户定义的布局文件一般以R.layout.开头。而系统自带的布局文件在哪呢？</span></p> 
<p><span style="color:#000000;">答：</span><span style="color:#474747;">Android\sdk\platforms\</span><span style="color:#ff0000;">android-24</span><span style="color:#474747;">\data\res\layout。而这些布局的参考说明在</span></p> 
<div>
 <span style="color:#474747;">https://developer.android.google.cn/reference/android/R.layout.html </span>
</div> 
<div>
 <span style="color:#474747;">由此我们引出一个问题，那就是那几个系统自带的布局文件是比较常用的呢？</span>
</div> 
<div>
 <span style="color:#474747;">下面介绍一个常用的几个系统自带的布局</span>
</div> 
<div>
 <span style="color:#474747;">4，常用系统自带的布局</span>
</div> 
<div>
 <span style="color:#323232;">（1）通过指定</span>
 <span style="color:#323232;">android.R.layout.simple_list_item_checked</span>
 <span style="color:#323232;">这个资源，实现带选择（打勾）的ListView</span>
 <span style="color:#323232;">。需要用 </span>
</div> 
<div>
 <span style="color:#323232;">setChoiceMode()</span>
 <span style="color:#323232;">方法设定选择为多选还是单选； </span>
</div> 
<div>
 <span style="color:#323232;">（2）</span>
 <span style="color:#323232;">通过指</span>
 <span style="color:#323232;">android.R.layout.simple_list_item_multiple_choice这个资源实现带CheckBox</span>
 <span style="color:#323232;">的</span>
 <span style="color:#323232;">ListView</span>
 <span style="color:#323232;">。同样需要用setChoiceMode()方法来设置单选或者多选； </span>
</div> 
<div>
 <span style="color:#323232;">（3）</span>
 <span style="color:#323232;">通过指定</span>
 <span style="color:#323232;">android.R.layout.simple_list_item_single_choice这个资源实现带RadioButton</span>
 <span style="color:#323232;">的</span>
 <span style="color:#323232;">ListView</span>
 <span style="color:#323232;">，是多选还是单选 要通过setChoiceMode()</span>
 <span style="color:#323232;">方法来指定；</span>
</div> 
<p>具体例子：</p> 
<pre class="has"><code>import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.ArrayAdapter;
import android.widget.AdapterView.OnItemClickListener;
public class Main3Activity extends AppCompatActivity {
    private String[] mListStr = {"学校：江苏大学","地址：江苏省镇江市","邮编：212013","前身：江苏理工大学","电话：0511-88780030"};
    private ListView listView3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        listView3=(ListView)findViewById(R.id.list3);
//listView3.setAdapter(newArrayAdapter&lt;String&gt;(this,android.R.layout.simple_list_item_1,mListStr));
//listView3.setAdapter(newArrayAdapter&lt;String&gt;(this,android.R.layout.simple_list_item_checked,mListStr) );
//listView3.setAdapter(newArrayAdapter&lt;String&gt;(this,android.R.layout.simple_list_item_multiple_choice,mListStr) );
//listView3.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
        listView3.setAdapter(new
                ArrayAdapter&lt;String&gt;(this,android.R.layout.simple_list_item_single_choice,mListStr) );
        listView3.setChoiceMode(ListView.CHOICE_MODE_SINGLE);
        listView3.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView&lt;?&gt; parent, View view, int position, long id)
            {
                setTitle("你点击了第"+position+"行");
            }
        });
    } }</code></pre> 
<p>三，SimpleAdapter：每行显示有图片和文字时用</p> 
<p>1，SimpleAdapter（Context context， List&lt;? extends Map&lt;String,?&gt;&gt; data, int resource ,String[] from, int[] to)</p> 
<p>context：一个activity或Service都是一个Context。</p> 
<p>data:是Map类型的列表，每一行是一个Map类型的数据，<span style="color:#000000;">每一行要与from中指定条目一致</span>（说明：<span style="color:#323232;">使用SimpleAdapter的数据一般都是用</span><span style="color:#323232;">HashMap</span><span style="color:#323232;">构成的列表（hashMap在后面介绍），列表的每一节对应ListView的每一行。通过</span><span style="color:#323232;">SimpleAdapter</span><span style="color:#323232;">的构造函数，将</span><span style="color:#323232;">HashMap</span><span style="color:#323232;">每个键的数据映射到布局文件中对应控件上。这个布局文件一般根据自己的需要来自己定义。</span>）</p> 
<p>resource：布局的ID</p> 
<p>from：<span style="color:#000000;">data的列名</span></p> 
<p>to：<span style="color:#000000;">是一个int</span><span style="color:#000000;">数组，数组里面的</span><span style="color:#000000;">id</span><span style="color:#000000;">是自定义布局中各个控件的id</span><span style="color:#000000;">，需要与上面的</span><span style="color:#000000;">from</span><span style="color:#000000;">对应</span></p> 
<p>2，SimpleAdapter的使用步骤</p> 
<p>（1）定义ListView每行要显示什么东西（如你要显示图片加文字）</p> 
<p>（2）<span style="color:#323232;">定义一个</span><span style="color:#323232;">HashMap</span><span style="color:#323232;">构成的列表，将数据以键值对的方式存放在里面。 </span></p> 
<div>
 <span style="color:#323232;">（</span>
 <span style="color:#323232;">3</span>
 <span style="color:#323232;">）构造</span>
 <span style="color:#323232;">SimpleAdapter</span>
 <span style="color:#323232;">对象。 </span>
</div> 
<div>
 <span style="color:#323232;">（</span>
 <span style="color:#323232;">4</span>
 <span style="color:#323232;">）将</span>
 <span style="color:#323232;">LsitView</span>
 <span style="color:#323232;">绑定到</span>
 <span style="color:#323232;">SimpleAdapter</span>
 <span style="color:#323232;">上</span>
</div> 
<div>
 &nbsp;
</div> 
<div>
 <span style="color:#323232;">3，HashMap</span>
</div> 
<pre class="has"><code>//List基本上都是以Array为基础; 
//Map放键值对的，一个Map可以放很多个键值对
        ArrayList&lt;HashMap&lt;String, Object&gt;&gt; listItem = new ArrayList&lt;HashMap&lt;String, Object&gt;&gt;();
        for (int i=0;i&lt;10;i++){
            HashMap&lt;String, Object&gt; map = new HashMap&lt;String, Object&gt;();
            map.put("Itemimage",R.drawable.test);//加入图片
            map.put("ItemtextView", "第"+i+"行");
            map.put("ItemtextView2", "这是第"+i+"行");
            listItem.add(map);
        }</code></pre> 
<p>用上面的listItem去建立ListView，则每行显示的就是一张图片和两个文字信息</p> 
<p>4，SimpleAdapter具体实例</p> 
<p><img alt="" class="has" height="229" src="https://img-blog.csdnimg.cn/20191127094618396.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQyNzc1OTM4,size_16,color_FFFFFF,t_70" width="726"></p> 
<pre class="has"><code>public class MainActivity extends AppCompatActivity {
    private ListView listView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        listView = (ListView)findViewById(R.id.list);
        ArrayList&lt;HashMap&lt;String, Object&gt;&gt; listItem = new ArrayList&lt;HashMap&lt;String, Object&gt;&gt;();
        for (int i=0;i&lt;10;i++){
            HashMap&lt;String, Object&gt; map = new HashMap&lt;String, Object&gt;();
            map.put("Itemimage",R.drawable.test);//加入图片
                                           //请把名为“test.png”的图片放在res/drawable内
            map.put("ItemtextView", "第"+i+"行");
            map.put("ItemtextView2", "这是第"+i+"行");
            listItem.add(map);
        }
        SimpleAdapter simpleAdapter = new SimpleAdapter(this, listItem, R.layout.item,
                new String[]{"Itemimage", "ItemtextView", "ItemtextView2"},
                new int[] {R.id.Itemimage, R.id.ItemtextView, R.id.ItemtextView2});
        listView.setAdapter(simpleAdapter);
    }
}</code></pre> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p> 
<p>&nbsp;</p>
                