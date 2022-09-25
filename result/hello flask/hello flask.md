原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/07/26/16522428.html
提交日期：Tue, 26 Jul 2022 11:51:00 GMT
博文内容：

                    <pre>from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/about')
def about():
    return '这是一个用flask建立的小网站'

@app.route('/user/&lt;username&gt;')
def show_user(username):
    return 'User Name is {}'.format(username)

if __name__ == '__main__':
    app.run()</pre>
                