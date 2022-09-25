原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522431.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <h2>intent介绍</h2> 
<ol><li>那我们到底是怎么从一个窗口跳转到另个窗口的，一个窗口的信息是怎么传递给另一个窗口的呢？没错，就是通过intent。下面我们来简单的介绍一下intent。</li><li>Android中使用Intent的方式有两种，分别为显式Intent和隐式Intent。</li></ol>
<pre class="has"><code>//显式intent（这一个代码块，只介绍一个窗口怎么跳到另一个窗口）
//方法一：
//创建Intent对象，指定启动的类名。就是如果intent对象被启动那么窗口就会从MainActivity所对应的
//窗口跳转到SecondActivity所对应的窗口

SecondActivity Intent intent=new Intent(MainActivity.this, SecondActivity.class); 

//启动intent

startActivity(intent);

//方法二：除了通过指定类名的方式来跳转窗口外，显式Intent还可以根据目标组件的包名、全路径来指
//定要跳转的窗口。
//setClassName(“包名”,“类的全路径名称”);
intent.setClassName(“com.jxust.cn”,“com.jxust.cn.chapter_shengtime”);
//启动Activity
startActivity(intent);


//隐式intent（我不懂，但我把别人的笔记放在下面）：
在程序中没有明确指定需要启动的Activity,Android系统会根据在Androidmanifest.xml文件当中设置
//的动作（action）、类别（category）、数据（Uri和数据类型）来启动合适的组件。

&lt;activity android:name=".MainActivity"&gt;
  &lt;intent-filter&gt;
&lt;!—设置action属性，根据name设置的值来指定启动的组件--&gt;
    &lt;action android:name="android.intent.action.MAIN" /&gt;
    &lt;category android:name="android.intent.category.LAUNCHER" /&gt;
            &lt;/intent-filter&gt;
        &lt;/activity&gt;

//说明：&lt;action&gt;标签指定了当前Activity可以响应的动作为android.intent.action.MAIN，而
//&lt;category&gt;标签则包含了一些类别信息，只有当这两者中的内容同时匹配时，Activity才会启动。
ntent intent=new Intent();
Intent.setAction(“android.intent.action.MAIN”);
StartActivity(intent);
</code></pre> 
<pre class="has"><code>//窗口和窗口之间的跳转实现了，那么窗口和窗口之间的信息怎么传递？下面我们来介绍一下
Intent intent=new Intent(this,SecondActivity.class);
//传递参数
intent.putExtra(键, 值);//“值“可以是任意类型的数据，”键“就是给“值”取一个名字就叫“键”，
                       //“键”可以用来索引
startActivity(intent);



如果需要传递的参数比多时，就需要使用putExtras()方法传递数据，该方法传递的是Bundle对象，具体的代码如下:
Intent intent=new Intent(this,SecondActivity.class);
Bundle bundle=new Bundle();
bundle.putString("phone","123456");
bundle.putString("sex","男");
bundle.putString("age","18"); 
intent.putExtras(bundle);
startActivity(intent); 




//被启动的窗口怎么接受到数据的呢？
Intent intent=this.getIntent();
String receive_str=intent.getStringExtra(键);//”键“在这里就被用到了</code></pre> 
<pre class="has"><code>利用onActivityResult获取跳转到的目标窗口的返回值：


如果启动一个Activity，并且希望返回结果给当前的Activity，那么可以使用startActivityForResult()方法来启动Activity


startActivityForResult(Intent intent, int requestCode)
第一个参数为普通Intent，指定要启动的NewActivity
第二个参数为请求码，即调用startActivityForResult()传递过去的值


为了获取被启动Activity的返回结果，需要执行以下两个步骤：
1.被启动的Activity需要调用setResult(int resultCode,Intent data)方法设置返回的结果数据
2.跳转前的Activity要重写onActivityResult(int requestCode,int resultCode,Intent intent)方法接收结果数据


onActivityResult(int requestCode, int resultCode, Intent data) 
第一个参数为请求码，即调用startActivityForResult()传递过去的值
第二个参数为结果码，结果码用于标识返回数据来自哪个新Activity
第三个参数为返回的数据，来自NewActivity
</code></pre> 
<pre class="has"><code>利用onActivityResult获取返回值与intent.getStringExtra获取返回值的区别？
坑，未填。。。。。。。。。
</code></pre> 
<h2>我们来实战一下吧。。。</h2> 
<h2>目标：</h2> 
<ol><li> <p>做一个登入和注册的界面：在登入界面中点击注册按钮，就跳转到注册界面。注册完了之后，点击完成，就会跳转到登入页面。此时的登入页面已经自动填写了已注册的信息。点击登入，跳转到一个界面上，这个界面上显示“欢迎 小明”</p> </li><li> <p>我们要创建三个窗口，那我们就要创建三个activity，三个layout。三个activity分别是：MainActivity（登入） Activity2（点击登入后跳转到的欢迎界面）Activity3（注册）。这个三个activity分别对应三个layout为：<strong><em><span style="color:#660e7a;"><strong><em>activity_main、mylayout2</em></strong></span></em></strong><span style="color:#000000;">、</span><strong><em><span style="color:#660e7a;"><strong><em>mylayout</em></strong></span></em></strong></p> </li></ol>
<p>&nbsp;</p> 
<p>1，在MainActivity中填入：</p> 
<pre class="has"><code>package com.example.lesson3;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {

    //创建两个Button用于登入和注册，创建两个EditText，用于输入账号和密码
    private Button btnLogin,btnReg;
    private EditText edtName,edtPwd;
    private final int REQUEST_CODE=101;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        btnLogin = (Button) findViewById(R.id.btnLogin);
        btnReg = (Button) findViewById(R.id.btnReg);
        edtName = (EditText) findViewById(R.id.edtName);
        edtPwd = (EditText) findViewById(R.id.edtPwd);

        //点击登入，向Activity2传递用户名
        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent=new Intent(MainActivity.this, Activity2.class);
                String name=edtName.getText().toString();
                String pwd=edtPwd.getText().toString();
                intent.putExtra("name",name);
                intent.putExtra("pwd",pwd);
                startActivity(intent);
            }
        });

        //点击注册，跳转到Activity3。进行注册，
        btnReg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent=new Intent(MainActivity.this, Activity3.class);
                startActivityForResult(intent,REQUEST_CODE);
            }
        });
    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if(requestCode==REQUEST_CODE){
            String name=data.getStringExtra("name");
            String pwd=data.getStringExtra("pwd");
            edtName.setText(name);
            edtPwd.setText(pwd);
        }
    }

}
</code></pre> 
<p>2，在Activity3中填入：</p> 
<pre class="has"><code>package com.example.lesson3;

import android.app.Activity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class Activity3 extends Activity {
    private Button btnReg;
    private EditText edtName, edtPwd, edtRePwd;
    private static final int RESULT_CODE = 101;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.mylayout);
        btnReg = (Button) findViewById(R.id.btnReg);
        edtName = (EditText) findViewById(R.id.edtName);
        edtPwd = (EditText) findViewById(R.id.edtPwd);
        edtRePwd = (EditText) findViewById(R.id.edtRepwd);

        btnReg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String name = edtName.getText().toString();
                String pwd = edtPwd.getText().toString();
                String repwd = edtRePwd.getText().toString();
                if (!"".equals(pwd) &amp;&amp; pwd.equals(repwd)) {
                    //获得启动该Activity的Intent对象
                    Intent intent = getIntent();
                    intent.putExtra("name", name);
                    intent.putExtra("pwd", pwd);
                    //设置结果码，并设置结束后返回的Activity
                    setResult(RESULT_CODE, intent);
                    //结束RegActivity
                    Activity3.this.finish();
                } else {
                    Toast.makeText(Activity3.this, "密码输入不一致", Toast.LENGTH_LONG).show();
                }
            }
        });
    }
}
</code></pre> 
<p>3，在Activity2中填入：</p> 
<pre class="has"><code>package com.example.lesson3;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;

public class Activity2 extends Activity {
    private TextView welcome;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.mylayout2);
        welcome=(TextView)findViewById(R.id.welcome);
        Intent intent=this.getIntent();
        String name=intent.getStringExtra("name");
        welcome.setText("Hello "+name);
    }
}
</code></pre> 
<p>4，在<span style="color:#000000;">在AndroidManifest.xml中</span></p> 
<pre class="has"><code>4，在AndroidManifest.xml中
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.lesson3"&gt;

    &lt;application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"&gt;
        &lt;activity android:name=".MainActivity"&gt;
            &lt;intent-filter&gt;
                &lt;action android:name="android.intent.action.MAIN" /&gt;

                &lt;category android:name="android.intent.category.LAUNCHER" /&gt;
            &lt;/intent-filter&gt;
        &lt;/activity&gt;

//下面两个activity为新添加的：
       &lt;activity android:name=".Activity3"&gt;
        &lt;/activity&gt;
        &lt;activity android:name=".Activity2"&gt;
        &lt;/activity&gt;
    &lt;/application&gt;

&lt;/manifest&gt;</code></pre> 
<p>5，<span style="color:#000000;">在layout拖拽，形成界面</span></p> 
<p style="margin-left:0pt;">&nbsp;</p> 
<p style="margin-left:0pt;">&nbsp;</p>
                