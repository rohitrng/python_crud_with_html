import mysql.connector
from flask import Flask , render_template , redirect , request , url_for

app = Flask(__name__)

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "blogs"
)

corsor = db.cursor()

@app.route('/')
def index():
    # list all blog post
    corsor.execute("select * from blog")
    blogs = corsor.fetchall()
    return render_template("index.html",blogs = blogs)

@app.route('/create' , methods = ['GET' , 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        corsor.execute(" insert into blog (title,content) values (%s,%s)" , (title,content))
        db.commit()
        return redirect("/")
    return render_template("create.html")

@app.route('/edit/<int:blog_id>' , methods = ['GET' , 'POST'] )
def edit(blog_id):
    corsor.execute("select * from blog where id = %s" , (blog_id,))
    blog = corsor.fetchone()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        corsor.execute("update blog set title = %s , content = %s where id = %s" , (title , content , blog_id))
        db.commit()
        return redirect('/')

    return render_template("edit.html", blog = blog)

@app.route('/delete/<int:blog_id>')
def delete(blog_id):
    corsor.execute("delete from blog where id = %s",(blog_id,))
    db.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

