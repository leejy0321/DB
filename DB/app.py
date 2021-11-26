import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

connect = psycopg2.connect("dbname=baseball user=postgres password=601603")
cur = connect.cursor()

@app.route('/')
def hello():
    return render_template("main.html")

@app.route('/information', methods=['POST'])
def info():
    send = request.form["send"]
    if send == "INFO" or "BACK":
        return render_template("info.html")

@app.route('/searchinfo', methods=['POST'])
def searchinfo():
    send = request.form["send"]
    if send == "TEAM":
        return render_template("teaminfo.html")
    elif send == "PLAYER":
        return render_template("playerinfo.html")
    elif send == "COACH":
        return render_template("coachinfo.html")

@app.route('/teaminfo', methods=['POST'])
def teaminfo():
    tname = request.form["tname"]
    cname = request.form["cname"]
    year = request.form["year"]
    if year == "":
        year = "between 2018 and 2020"
    else:
        year = "=" + year
    location = request.form["location"]
    stadium = request.form["stadium"]
    send = request.form["send"]
    cur.execute("select * from team where team_name like '%" + tname + "%' and location like '%" + location + "%'"
    "and coach_year " + year + " and stadium like '%" + stadium + "%' and coach_name like '%" + cname + "%';")
    result = cur.fetchall()
    if send == "Search":
        return render_template("result_teaminfo.html", teams=result)

@app.route('/playerinfo', methods=['POST'])
def playerinfo():
    pname = request.form["pname"]
    tname = request.form["tname"]
    year = request.form["year"]
    if year == "":
        year = "between 2018 and 2020"
    else:
        year = "=" + year
    send = request.form["send"]
    cur.execute("select * from player where name like '%" + pname + "%' and team like '%" + tname + "%' and year " + year + ";")
    result = cur.fetchall()
    if send == "Search":
        return render_template("result_playerinfo.html", players=result)

@app.route('/coachinfo', methods=['POST'])
def coachinfo():
    cname = request.form["cname"]
    year = request.form["year"]
    if year == "":
        year = "between 2018 and 2020"
    else:
        year = "=" + year
    send = request.form["send"]
    cur.execute("select * from coach where name like '%" + cname + "%' and year " + year + ";")
    result = cur.fetchall()
    if send == "Search":
        return render_template("result_coachinfo.html", coaches=result)

@app.route('/infowithstats', methods=['POST'])
def iws():
    send = request.form["send"]
    if send == "PITCHER":
        cur.execute("select * from player natural join pitching;")
        result = cur.fetchall()
        return render_template("iws_pitcher.html", pitchers=result)
    elif send == "HITTER":
        cur.execute("select * from player natural join hitting;")
        result = cur.fetchall()
        return render_template("iws_hitter.html", hitters=result)

@app.route('/playerwithteam', methods=['POST'])
def pwt():
    send = request.form["send"]
    if send == "PLAYER":
        cur.execute("select name, number, year, position, birth, height, weight, salary, team, coach, location, stadium "
                    "from player, team "
                    "where team.team_name=player.team and team.coach_name=player.coach and team.coach_year=player.year;")
        result = cur.fetchall()
        return render_template("pwtinfo.html", players=result)

@app.route('/statistics', methods=['POST'])
def stats():
    send = request.form["send"]
    if send == "STATS" or "BACK":
        return render_template("stats.html")

@app.route('/searchstats', methods=['POST'])
def searchstats():
    send = request.form["send"]
    if send == "PITCHER":
        return render_template("pitcherstats.html")
    elif send == "HITTER":
        return render_template("hitterstats.html")

@app.route('/pitcherstats', methods=['POST'])
def pitcherstats():
    pname = request.form["pname"]
    tname = request.form["tname"]
    number = request.form["number"]
    if number == "":
        number = "between 0 and 100"
    else:
        number = "=" + number
    year = request.form["year"]
    if year == "":
        year = "between 2018 and 2020"
    else:
        year = "=" + year
    send = request.form["send"]
    cur.execute("select * from pitching where name like '%" + pname + "%' and team like '%" + tname + "%'"
    "and number " + number + " and year " + year + ";")
    result = cur.fetchall()
    if send == "Search":
        return render_template("result_pitcherstats.html", pitchers=result)

@app.route('/hitterstats', methods=['POST'])
def hitterstats():
    pname = request.form["pname"]
    tname = request.form["tname"]
    number = request.form["number"]
    if number == "":
        number = "between 0 and 100"
    else:
        number = "=" + number
    year = request.form["year"]
    if year == "":
        year = "between 2018 and 2020"
    else:
        year = "=" + year
    send = request.form["send"]
    cur.execute("select * from hitting where name like '%" + pname + "%' and team like '%" + tname + "%'"
    " and number " + number + " and year " + year + ";")
    result = cur.fetchall()
    if send == "Search":
        return render_template("result_hitterstats.html", hitters=result)

@app.route('/deletestats', methods=['POST'])
def deletestats():
    send = request.form["send"]
    if send == "PITCHER":
        return render_template("delpitcherstats.html")
    elif send == "HITTER":
        return render_template("delhitterstats.html")

@app.route('/deletepitcher', methods=['POST'])
def delpitcher():
    pname = request.form["pname"]
    tname = request.form["tname"]
    number = request.form["number"]
    year = request.form["year"]
    cur.execute("select * from pitching where name like '%" + pname + "%' and team like '%" + tname + "%'"
                " and number = " + number + " and year = " + year + ";")
    check = cur.fetchall()
    if check == []:
        return "Error: Cannot find such player."
    cur.execute("delete from pitching where name = '" + pname + "' and team = '" + tname +
                "' and number = " + number + " and year = " + year + ";")
    send = request.form["send"]
    if send == "Delete":
        cur.execute("select * from pitching;")
        result = cur.fetchall()
        return render_template("result_pitcherstats.html", pitchers=result)

@app.route('/deletehitter', methods=['POST'])
def delhitter():
    pname = request.form["pname"]
    tname = request.form["tname"]
    number = request.form["number"]
    year = request.form["year"]
    cur.execute("select * from hitting where name like '%" + pname + "%' and team like '%" + tname + "%'"
                " and number = " + number + " and year = " + year + ";")
    check = cur.fetchall()
    if check == []:
        return "Error: Cannot find such player."
    cur.execute("delete from hitting where name = '" + pname + "' and team = '" + tname +
                "' and number = " + number + " and year = " + year + ";")
    send = request.form["send"]
    if send == "Delete":
        cur.execute("select * from hitting;")
        result = cur.fetchall()
        return render_template("result_hitterstats.html", hitters=result)

@app.route('/teamaverage', methods=['POST'])
def average():
    send = request.form["send"]
    if send == "ERA":
        cur.execute("select team, year, avg(ERA) from pitching group by team, year order by year;")
        result = cur.fetchall()
        return render_template("teamera.html", ERAs=result)
    elif send == "AVG":
        cur.execute("select team, year, avg(AVG) from hitting group by team, year order by year;")
        result = cur.fetchall()
        return render_template("teamavg.html", AVGs=result)

@app.route('/salary', methods=['POST'])
def salary():
    send = request.form["send"]
    if send == "SALARY" or "BACK":
        return render_template("salary.html")

@app.route('/salarylist', methods=['POST'])
def salarylist():
    send = request.form["send"]
    if send == "COACH":
        cur.execute("select name, birth, year, salary from coach;")
    elif send == "PLAYER":
        cur.execute("select name, birth, year, salary from player;")
    result = cur.fetchall()
    return render_template("salarylist.html", salaries=result)

@app.route('/insert', methods=['POST'])
def insert():
    send = request.form["send"]
    if send == "INSERT":
        return render_template("insertsalary.html")

@app.route('/insertcoachsalary', methods=['POST'])
def ics():
    cname = request.form["cname"]
    year = request.form["year"]
    birth = request.form["birth"]
    salary = request.form["salary"]
    cur.execute("insert into coach values('" + cname + "'," + year + "," + birth + "," + salary + ");")
    send = request.form["send"]
    if send == "INSERT":
        cur.execute("select name, birth, year, salary from coach;")
        result = cur.fetchall()
        return render_template("salarylist.html", salaries=result)

@app.route('/insertplayersalary', methods=['POST'])
def ips():
    pname = request.form["pname"]
    team = request.form["team"]
    number = request.form["number"]
    year = request.form["year"]
    salary = request.form["salary"]
    cur.execute("select * from player where name like '%" + pname + "%' and team like '%" + team + "%' and number =" + number + ";")
    result = cur.fetchall()
    if result != []:
        name, team, num, yr, pos, coach, birth, height, weight, sal = result[-1]
        cur.execute("insert into player values('" + name + "','" + team + "'," + str(num) + "," + year +
                    ",'" + pos + "',null," + str(birth) + "," + str(height) + "," + str(weight) + "," + salary + ");")
    else:
        cur.execute("insert into player values('" + pname + "','" + team + "'," + number + "," + year +
                    ", null, null, null, null, null," + salary + ");")
    send = request.form["send"]
    if send == "INSERT":
        cur.execute("select name, birth, year, salary from player;")
        result = cur.fetchall()
        return render_template("salarylist.html", salaries=result)

@app.route('/update', methods=['POST'])
def update():
    send = request.form["send"]
    if send == "UPDATE":
        return render_template("updatesalary.html")

@app.route('/updatecoachsalary', methods=['POST'])
def ucs():
    cname = request.form["cname"]
    year = request.form["year"]
    salary = request.form["salary"]
    cur.execute("update coach set salary =" + salary + " where name = '" + cname + "' and year = " + year + ";")
    send = request.form["send"]
    if send == "UPDATE":
        cur.execute("select name, birth, year, salary from coach;")
        result = cur.fetchall()
        return render_template("salarylist.html", salaries=result)

@app.route('/updateplayersalary', methods=['POST'])
def ups():
    pname = request.form["pname"]
    team = request.form["team"]
    number = request.form["number"]
    year = request.form["year"]
    salary = request.form["salary"]
    cur.execute("update player set salary =" + salary + " where name = '" + pname + "' and team = '" + team +
                "' and number = " + number + " and year = " + year + ";")
    send = request.form["send"]
    if send == "UPDATE":
        cur.execute("select name, birth, year, salary from player;")
        result = cur.fetchall()
        return render_template("salarylist.html", salaries=result)

@app.route('/highestsalary', methods=['POST'])
def highestsalary():
    send = request.form["send"]
    if send == "HIGHEST":
        return render_template("highestsalary.html")

@app.route('/highestresult', methods=['POST'])
def highestresult():
    team = request.form["team"]
    year = request.form["year"]
    cur.execute("select name, team, year, salary from player where team like '%" + team + "%' and year = " + year +
                " and salary >= all (select salary from player where team like '%" + team + "%' and year = " + year + ");")
    result = cur.fetchall()
    send = request.form["send"]
    if send == "Search":
        return render_template("result_highest.html", salaries=result)

if __name__ == '__main__':
    app.run()