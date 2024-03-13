from flask import Flask, request, render_template
from flaskwebgui import FlaskUI 
from solution import SolutionSMO1Await, SolutionSMO1Reject, SolutionSMOMultiReject, SolutionSMOMultiAwait
app = Flask(__name__, static_folder='./static', template_folder='./templates')

@app.route('/')
def run():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def ping():
    """
    Проверка работы сервера
    """
    return {"status": 200}

@app.route('/api/solveSMO1Await', methods=['POST'])
def solve_smo1_await():
    """
    Одноканальные СМО с ожиданием
    """
    params = request.json["data"]
    sol = SolutionSMO1Await([float(params["t"]), float(params["l"]), int(params["m"])])
    sol.solve()
    return {"msg": sol.result}
    
@app.route('/api/solveSMO1reject', methods=['POST'])
def solve_smo1_reject():
    """
    Одноканальные СМО с отказами
    """
    params = request.json["data"]
    sol = SolutionSMO1Reject([float(params["t"]), float(params["l"]), int(params["m"])])
    sol.solve()
    return {"msg": sol.result}

@app.route('/api/solveSMOMultiReject', methods=['POST'])
def solve_smo_multi_reject():
    """
    Многоканальная СМО с отказами
    """
    params = request.json["data"]
    sol = SolutionSMOMultiReject([float(params["t"]), float(params["l"]), int(params["m"])])
    sol.solve()
    return {"msg": sol.result}

@app.route('/api/solveSMOMultiAwait', methods=['POST'])
def solve_smo_multi_await():
    """
    Многоканальная СМО с ожиданием
    """
    params = request.json["data"]

    sol = SolutionSMOMultiAwait([float(params["t"]), float(params["l"]), int(params["m"]),  params["n"], bool(params["inf"])])
    sol.solve()
    return {"msg": sol.result}

FlaskUI(app=app, server="flask", width=700, height=700).run()

# if __name__ == "__main__":
#     app.run()