from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Musel/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app) #dataya appı tanıttık

# / <= Bu yere geldikten sonra indexi göster
@app.route("/")
def index():
    todos = Todo.query.all() # Todo'da ki tüm db verilerini al
    return render_template("index.html",todos=todos) # Todosu içine attık

@app.route("/add",methods=["POST"]) #add yerinden post isteği gelirse :
def addTodo():
    title = request.form.get("title") #title içindeki veriyi al
    content = request.form.get("content") #content içindeki veriyi al
    newTodo = Todo(title=title, content=content,complete = False) #Todonun içine title content verisini at
    db.session.add(newTodo) #databaseye newTodoyu ekle
    db.session.commit() #verileri dataya işle
    return redirect(url_for("index")) #ve sonra indexi göster

@app.route("/complete/<string:id>",methods=["GET"]) #complete'den gelen veriyi ve id'yi al
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first() #aldığı verideki id ye uyfula
    if (todo.complete == False): #aldığı veri complete değilse
        todo.complete = True #true döndür
    else: # eğer değilse
        todo.complete = False #completeyi false yap
    db.session.commit() #dataya işle
    return redirect(url_for("index")) #indexi döndür
 
@app.route("/delete/<string:id>") # delete'deki veriyi al
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first() #eşleşen id ye uygula
    db.session.delete(todo) #eşleşen id yi datadan sil
    db.session.commit() #Veriyi kaydet
    return redirect(url_for("index")) #indexi döndür

@app.route("/detail/<string:id>") #veiyi al
def detailTodo(id):
    todo = Todo.query.filter_by(id=id).first() #eşleşen id ye uygula
    return render_template("detail.html",todo=todo) #detail.html'e todoyu at (eşleşen ip ye)

#Modelleri oluşturduk (title, id, content vs.)
class Todo(db.Model):
    """
    primary_key=true : her id'den sadece 1 tane olsun
    String(80) en fazla 80 karakter olsun
    """
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

#App'ı başlat
if __name__ == "__main__":
    app.run(debug=True)