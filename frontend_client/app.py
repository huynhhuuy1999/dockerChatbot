from flask import Flask, render_template, request, redirect, url_for, session
from neo4j import GraphDatabase

app = Flask(__name__, static_folder="public", static_url_path="/public")
app.secret_key = "1234"
driver = GraphDatabase.driver(
    "neo4j://localhost:7687", auth=("neo4j", "123456789"), database="test"
)

# def check_user(username, password):
#     with driver.session() as neo4j_session:
#         result = neo4j_session.run("MATCH (u:admin {username: $username, pass: $password}) RETURN u", username=username, password=password)
#         return bool(list(result))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']


#         if check_user(username, password):
#             session['username'] = username
#             return redirect(url_for('quanly'))
#         return "<script>alert('Đăng nhập không thành công. Vui lòng thử lại.');</script>"
#     return render_template('login.html')
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quanly")
def quanly():
    # if 'username' in session:
    with driver.session() as neo4j_session:
        result = neo4j_session.run("Match(i:Intent) return i.name,i.text")
        data = [(record[0], record[1]) for record in result]
    return render_template("quanly.html", data=data)
    # return redirect(url_for('login'))


# @app.route('/intent/<intent_name>')
# def show_intent(intent_name):
#     with driver.session() as session:
#         result = session.run("MATCH (n:Answer)-[:BELONGS_TO]->(i:Intent {name: $intent_name}) RETURN n.ask, n.answer, id(n),i.text,n.nganhhoc,n.entity", intent_name=intent_name)
#         data = [(record[0], record[1], record[2],record[3],record[4],record[5]) for record in result]
#         nganh= session.run("MATCH (n:Nganh) RETURN n.name")
#         entity= session.run("MATCH (n:Intent{name:$intent_name})-[:has_entity]->(e:entity) RETURN e.name,e.text",intent_name=intent_name)
#         datanganh=[(recordnganh[0])for recordnganh in nganh]
#         data_entity=[(record_entity[0],record_entity[1],)for record_entity in entity]
#     return render_template('intent.html', intent_name=intent_name, data=data,datanganh=datanganh,data_entity=data_entity)

# @app.route('/intent/<intent_name>/add', methods=['POST'])
# def add_intent_node(intent_name):
#     if 'question' in request.form and 'entity' not in request.form:
#         question = request.form['question']
#         answer = request.form['answer']
#         with driver.session() as session:
#             session.run("MATCH (i:Intent {name: $intent_name}) CREATE (n:Answer {ask: $question, answer: $answer})-[:BELONGS_TO]->(i)", intent_name=intent_name, question=question, answer=answer)
#     if 'entity' in request.form:
#         question = request.form['question']
#         answer = request.form['answer']
#         entity= request.form['entity']
#         with driver.session() as session:
#             session.run("MATCH (i:Intent {name: $intent_name}) CREATE (n:Answer {ask: $question, answer: $answer, entity:$entity})-[:BELONGS_TO]->(i)", intent_name=intent_name, question=question, answer=answer,entity=entity)
#     elif 'nganh' in request.form:
#         nganh = request.form['nganh']
#         answer = request.form['answer']
#         with driver.session() as session:
#             session.run("MATCH (i:Intent {name: $intent_name}) CREATE (n:Answer {nganhhoc: $nganh, answer: $answer})-[:BELONGS_TO]->(i)", intent_name=intent_name, nganh=nganh, answer=answer)
#     return redirect(url_for('show_intent', intent_name=intent_name))


# @app.route('/intent/<intent_name>/edit', methods=['POST'])
# def edit_intent_node(intent_name):
#     node_id = request.form['node_id']
#     if 'question' in request.form and 'entity' not in request.form:
#         question = request.form['question']
#         answer = request.form['answer']
#         with driver.session() as session:
#             session.run("MATCH (n:Answer) WHERE id(n) = $node_id SET n.ask = $question, n.answer = $answer", node_id=int(node_id), question=question, answer=answer)
#     if 'entity' in request.form:
#         question = request.form['question']
#         answer = request.form['answer']
#         entity= request.form['entity']
#         with driver.session() as session:
#             session.run("MATCH (n:Answer) WHERE id(n) = $node_id SET n.ask = $question, n.answer = $answer,n.entity=$entity", node_id=int(node_id), question=question, answer=answer,entity=entity)
#     elif 'nganh' in request.form:
#         nganh = request.form['nganh']
#         answer = request.form['answer']
#         with driver.session() as session:
#             session.run("MATCH (n:Answer) WHERE id(n) = $node_id SET n.nganhhoc = $nganh, n.answer = $answer", node_id=int(node_id), nganh=nganh, answer=answer)
#     return redirect(url_for('show_intent', intent_name=intent_name))


# @app.route('/intent/<intent_name>/delete', methods=['POST'])
# def delete_intent_node(intent_name):
#     node_id = request.form['node_id']
#     with driver.session() as session:
#         session.run("MATCH (n:Answer) WHERE id(n) = $node_id DETACH DELETE n", node_id=int(node_id))
#     return redirect(url_for('show_intent', intent_name=intent_name))

# @app.route('/nganh/add', methods=['POST'])
# def add_nganh():
#     nganh_name = request.form['nganh_name']
#     with driver.session() as session:
#         session.run("MATCH (i:truongdaihoc)CREATE (n:Nganh {name: $nganh_name})-[:GOM]->(i) WITH n MATCH (f:Intent) WHERE f.name = 'thoigiandaotao' AND f.name = 'manganh' AND f.name = 'tohopxettuyen' AND f.name = 'vitrivieclam' AND f.name = 'chitieunganh' AND  f.name = 'thoigiandaotao' AND  f.name = 'chuongtrinhdaotao' CREATE (f)-[:CO]->(n)", nganh_name=nganh_name)
#     return redirect(url_for('show_nganh'))

# @app.route('/nganh/edit', methods=['POST'])
# def edit_nganh():
#     nganh_name_old = request.form['nganh_name_old']
#     nganh_name = request.form['nganh_name']
#     with driver.session() as session:
#         session.run("MATCH (n:Nganh) WHERE n.name = $nganh_name_old SET n.name = $nganh_name", nganh_name_old=nganh_name_old, nganh_name=nganh_name)
#     return redirect(url_for('show_nganh'))

# @app.route('/nganh/delete', methods=['POST'])
# def delete_nganh():
#     nganh_id = request.form['nganh_id']

#     with driver.session() as session:
#         session.run("MATCH (n:Nganh) WHERE id(n) = $nganh_id DETACH DELETE n", nganh_id=int(nganh_id))
#     return redirect(url_for('show_nganh'))

# @app.route('/nganh', methods=['GET'])
# def show_nganh():
#     with driver.session() as session:
#         result = session.run("MATCH (n:Nganh) RETURN id(n), n.name")
#         nganhs = [(record[0], record[1]) for record in result]
#     return render_template('nganh.html', nganhs=nganhs)

if __name__ == "__main__":
    app.run(debug=True, port=8282, host="0.0.0.0")
