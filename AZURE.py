import pypyodbc
from flask import Flask, request, render_template
import json
from json import loads, dumps
import redis
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

r = redis.StrictRedis(
    host='veenaazure.redis.cache.windows.net',
    port=6380,
    password='********', ssl=True)

conn = pypyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=tcp:veenaazure.database.windows.net;'
                        'PORT=1433;'
                        'DATABASE=veenaazure;'
                        'UID=********;'
                        'PWD=*******')
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('home.html')


def convert_fig_to_html(fig):
    from io import BytesIO
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    import base64
    # figdata_png = base64.b64encode(figfile.read())
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png

#HISTOGRAM USING PANDAS
@app.route("/histpandas", methods=["POST", "GET"])
def histogrampandas():
    locationSource = str(request.form['locationSource'])
    range1 = float(request.form['range1'])
    range2 = float(request.form['range2'])
    #range3 = float(request.form['range3'])
    #range4 = float(request.form['range4'])
    #range5 = float(request.form['range5'])
    #range6 = float(request.form['range6'])
    df1 = pd.read_csv('static/data/quakes.csv', encoding='latin-1')
    dfq = df1[df1.locationSource == locationSource]
    #dfq = dfq[(dfq.mag > range1) & (dfq.mag < range2) & (dfq.mag > range3) & (dfq.mag < range4) & (dfq.mag > range5) & (dfq.mag < range6)]
    dfq = dfq[(dfq.mag > range1) & (dfq.mag < range2) ]
    dfl = dfq[['locationSource','mag']]
    ax = dfl.plot.hist(bins=5)
    plot = convert_fig_to_html(ax)
    rows=[]
    return render_template('histpandas.html',data1=plot.decode('utf8'), ci=[dfq.to_html(classes='data', header="true")])

    return render_template('histpandas.html')

#HISTOGRAM USING PANDAS
@app.route("/histpandas", methods=["POST", "GET"])
def query7pandas():
    Country = str(request.form['countryname'])
    #range1 = float(request.form['range1'])
    #range2 = float(request.form['range2'])
    #range3 = float(request.form['range3'])
    #range4 = float(request.form['range4'])
    #range5 = float(request.form['range5'])
    #range6 = float(request.form['range6'])
    df1 = pd.read_csv('static/data/v.csv', encoding='latin-1')
    dfq = df1[df1.Country == Country]
    #dfq = dfq[(dfq.mag > range1) & (dfq.mag < range2) & (dfq.mag > range3) & (dfq.mag < range4) & (dfq.mag > range5) & (dfq.mag < range6)]
    #dfq = dfq[(dfq.mag > range1) & (dfq.mag < range2) ]
    dfcc = dfq['Elev']
    #dfl = dfq[['locationSource','mag']]
    ax = dfcc.plot.hist()
    plot = convert_fig_to_html(ax)
    rows=[]
    return render_template('histpandas.html',data1=plot.decode('utf8'), ci=[dfq.to_html(classes='data', header="true")])

    return render_template('histpandas.html')
# @app.route("/showpie", methods=["POST", "GET"])
# def showpie():
#     category = str(request.form.get('category', ''))
#     query1 = "SELECT * FROM groc WHERE category = '" + str(category) + "'"
#     cursor.execute(query1)
#     r1 = cursor.fetchall()
#     return render_template('showpie.html',category=category,rows=r1)

#user enter category veg or nonveg and display all results of that category - pie chart
#quiz 0a
#CHECKKKKKKKKKKKKKKKK
@app.route("/showpiechart", methods=["POST", "GET"])
def showpiechart():
    query1 = "SELECT * FROM voting WHERE StateName  = 'ALASKA'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT * FROM voting WHERE StateName  = 'ILLINOIS'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    rows1 = ([
        ['Item','Quantity'],
        [r1[0][0],r1[0][2]],
        [r1[1][0],r1[1][2]],
        [r1[2][0],r1[2][2]]
        ])
        
    rows2 = ([
        ['Item','Quantity'],
        [r2[0][0],r2[0][2]],
        [r2[1][0],r2[1][2]]
        ])

    return render_template('showpie.html', rows1=rows1, rows2=rows2)

#5-perfect--jus display info 
@app.route("/basic", methods=["POST", "GET"])
def basic():
    query1 = "select StateName from voting where totalpop between 5000 and 10000"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "select StateName from voting where totalpop between 10000 and 50000"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    return render_template('basic.html', rows1=r1, rows2=r2)

#6-perfect---give range as 1 or 2 
@app.route('/regscatter', methods=['POST', 'GET'])
def regscatter():
    m1 = int(request.form.get('m1', ''))
    m2 = int(request.form.get('m2', ''))
    m1 = m1 * 1000
    m2 = m2 * 1000


    query1 = "SELECT sum(Registered) FROM voting WHERE TotalPop BETWEEN '"+str(m1)+"' AND '"+str(m2)+"'"
    cursor.execute(query1)
    s1 = cursor.fetchall()


    rows = ([
        ['reg', 'pop'],
        [str(m1)+'-'+str(m2), s1[0][0]]
        ])
    return render_template('regscatter.html', rows1=rows)

#7-perfect give range as 100
@app.route("/bar", methods=["POST", "GET"])
def quiz7():
    range1 = int(request.form.get('range',''))
    rangeStart = 0
    rangeEnd = range1
    maxQuery = "Select max(mag) from quakes"
    
    cursor.execute(maxQuery)
    maxResult = cursor.fetchall()
    maxPopulation = maxResult[0][0]
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < maxPopulation:
        query = "Select count(mag) from quakes where mag between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        
        cursor.execute(query)
        resultSet = cursor.fetchall()
        countResult = resultSet[0][0]
        storeResult.append(countResult)
        start.append(rangeStart)
        end.append(rangeEnd)
        rangeStart = rangeEnd
        rangeEnd = rangeEnd + range1
        counter = counter + 1
    list_a = []
    list_a.append(['Mag','Number of Quakes'])
    for i in range(0,counter):
        list_a.append([str(start[i]) + '-' + str(end[i]),storeResult[i]])
    return render_template('bar.html',rows=list_a)

# 8-perefct give range as 1 or 2 
# horizontal bar graph show number on each digit generated
@app.route("/horizontalbar", methods=["POST", "GET"])
def horizontalbar():

 

    r1 = []
    range1 = int(request.form.get('range', ''))
    range1 = range1+1
    for i in range(range1):
        modulo = (i**2) + 1
        r1.append(modulo)
    
    r2=[]
    
    for i in range(range1):
        count=r1.count(r1[i])
        r2.append(count)
    
    rows = []
    rows.append(['Range Value', 'Number of Times'])
    
    for i in range(1,range1):
        rows.append([r1[i],r2[i]])
    
    return render_template('bar.html', rows=rows)

    
#perfect-jus list the count why arent the values working
@app.route("/list", methods=["POST", "GET"])
def list():
    # depthrange1 = float(request.form.get('depthrange1', ''))
    # query1="SELECT * FROM quakes WHERE latitude >= '" + str(latitude1) + "' AND latitude <= '" + str(latitude2) + "' AND longitude >= '" + str(longitude1) + "' AND longitude <= '" + str(longitude2) + "'"
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()
    return render_template('list.html', rows1=r1, rows2=r2, rows3=r3)


@app.route("/showpie", methods=["POST", "GET"])
def showpie():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = int(request.form.get('range1', ''))
    range2 = int(request.form.get('range2', ''))
    range3 = int(request.form.get('range3', ''))
    range4 = int(request.form.get('range4', ''))
    range5 = int(request.form.get('range5', ''))
    range6 = int(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of quakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]

    ])

    return render_template('showpie.html', rows=rows)

#SHOWPIE TRIAL

@app.route("/quizpie", methods=["POST", "GET"])
def pietrial():
   
    range1 = int(request.form.get('range1', ''))
    range2 = int(request.form.get('range2', ''))
   

    query1 = "SELECT count(*) FROM minnow WHERE Fare = 100 AND Age between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM minnow WHERE Fare = 200 AND Age between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM minnow WHERE Fare = 300 AND Age between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    query4 = "SELECT count(*) FROM minnow WHERE Fare = 400 AND Age between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query4)
    r4 = cursor.fetchall()

    query5 = "SELECT count(*) FROM minnow WHERE Fare = 500 AND Age between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query5)
    r5 = cursor.fetchall()

    rows = ([
        ['Age', 'Count'],
        ['100' + str(range1) + '-' + str(range2), r1[0][0]],
        ['200' + str(range1) + '-' + str(range2), r2[0][0]],
        ['300' + str(range1) + '-' + str(range2), r3[0][0]],
        ['400' + str(range1) + '-' + str(range2), r4[0][0]],
        ['500' + str(range1) + '-' + str(range2), r5[0][0]]
       

    ])

    return render_template('quizpie.html', rows=rows)


@app.route("/pie", methods=["POST", "GET"])
def pie():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows1 = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    query8 = "select count(*) from quakes where mag > 5.0 and depth > 5"
    cursor.execute(query8)
    r8 = cursor.fetchall()
    query9 = "select count(*) from quakes where mag > 5.0 and depth < 5"
    cursor.execute(query9)
    r9 = cursor.fetchall()

    rows2 = ([
        ['Magnitude and Depth Error', 'Number of Earthquakes'],
        ['Depth Error > 5', r8[0][0]],
        ['Depth Error < 5', r9[0][0]]

    ])

    return render_template('pie.html', rows=[rows1, rows2])


@app.route("/bar", methods=["POST", "GET"])
def bar():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('bar.html', rows=rows)

#BARTRIAL

@app.route("/bartrial", methods=["POST", "GET"])
def bartrial():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = int(request.form.get('range1', ''))
    range2 = int(request.form.get('range2', ''))
    

    query1 = "SELECT count(*) FROM minnow WHERE Survived = 'True' AND Decklevel between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM minnow WHERE Survived = 'False' AND Decklevel between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    

    rows1 = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range1) + '-' + str(range2), r2[0][0]],
        
    ])

   

    return render_template('bartrial.html', rows1=rows1)

@app.route("/scattern", methods=["POST", "GET"])
def scatter():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('scattern.html', rows=rows)

@app.route("/quizscatter", methods=["POST", "GET"])
def quizscatter():
    
    range1 = int(request.form.get('range1', ''))
    range2 = int(request.form.get('range2', ''))

    query1 = "SELECT count(CabinNum) FROM minnow WHERE Age between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    rows = ([
        ['Cabin Number', 'Age'],
        [str(range1) + '-' + str(range2), r1[0][0]]
        
    ])

    return render_template('quizscatter.html', rows=rows)


@app.route("/line", methods=["POST", "GET"])
def line():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))
    range3 = float(request.form.get('range3', ''))
    range4 = float(request.form.get('range4', ''))
    range5 = float(request.form.get('range5', ''))
    range6 = float(request.form.get('range6', ''))

    query1 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of Earthquakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
    ])

    return render_template('line.html', rows=rows)


@app.route("/hist", methods=["POST", "GET"])
def histogramgo():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = request.form.get('range1', '')
    range2 = request.form.get('range2', '')
    range3 = request.form.get('range3', '')
    range4 = request.form.get('range4', '')
    range5 = request.form.get('range5', '')
    range6 = request.form.get('range6', '')
    range7 = request.form.get('range7', '')
    range8 = request.form.get('range8', '')

    query1 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

    query4 = "SELECT count(*) FROM quakes WHERE locationSource = '" + str(locationSource) + "' AND mag between '" + str(
        range7) + "' AND '" + str(range8) + "'"
    cursor.execute(query4)
    r4 = cursor.fetchall()

    rows = ([
        ['Magnitude', 'Number of quakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]],
        [str(range7) + '-' + str(range8), r4[0][0]]
    ])

    return render_template('hist.html', rows=rows)


@app.route("/histd3", methods=["POST", "GET"])
def histogramd3():
    locationSource = str(request.form.get('locationSource', ''))
    range1 = request.form.get('range1', '')
    range2 = request.form.get('range2', '')
    range3 = request.form.get('range3', '')
    range4 = request.form.get('range4', '')
    range5 = request.form.get('range5', '')
    range6 = request.form.get('range6', '')
    

    query1 = "SELECT count(*) FROM quakes WHERE mag between '" + str(range1) + "' AND '" + str(range2) + "'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    query2 = "SELECT count(*) FROM quakes WHERE mag between '" + str(range3) + "' AND '" + str(range4) + "'"
    cursor.execute(query2)
    r2 = cursor.fetchall()

    query3 = "SELECT count(*) FROM quakes WHERE mag between '" + str(range5) + "' AND '" + str(range6) + "'"
    cursor.execute(query3)
    r3 = cursor.fetchall()

 

    rows = ([
        ['Magnitude', 'Number of quakes'],
        [str(range1) + '-' + str(range2), r1[0][0]],
        [str(range3) + '-' + str(range4), r2[0][0]],
        [str(range5) + '-' + str(range6), r3[0][0]]
        
    ])

    return render_template('histd3.html', rows=rows)

#PANDAS CODE FOR PLOTTING
@app.route('/scatterpandas', methods=['GET', 'POST'])
def rangecsv4():
    

    if request.method == 'POST':
       
        range1 = float(request.form['range1'])
        range2 = float(request.form['range2'])
        df1=pd.read_csv('static/data/quakes.csv', encoding='latin-1')
        
       
        dfc = df1[(df1.mag > range1) & (df1.mag < range2)]

        dfcc = dfc['depth']

        x= dfc['mag'].to_list()
        y= dfc['depth'].to_list()
        

        #ax = dfn.plot(x, y ,style=['o','rx'])
        ax = plt.scatter(x,y)
        plot = convert_fig_to_html(ax)
        rows=[]
        return render_template('scatterpandas.html',data1=plot.decode('utf8'))


@app.route("/query5", methods=["POST", "GET"])
def query5():
    countryname = request.form.get('countryname','')
    range1 = 500
    rangeStart = 0
    rangeEnd = range1
    maxQuery = "Select max(Elev) from v"
    #maxQuery = maxQuery * 100
    cursor.execute(maxQuery)
    maxResult = cursor.fetchall()
    maxPopulation = maxResult[0][0]
    storeResult = []
    start = []
    end = []
    counter = 0
    while rangeStart < maxPopulation:
        #query = "Select count(statename) from voting where totalpop between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        query = "Select count(Country) from v where Country = '" +str(countryname)+ "' and  Elev between '" +str(rangeStart)+ "' and '" +str(rangeEnd)+"'"
        
        cursor.execute(query)
        resultSet = cursor.fetchall()
        countResult = resultSet[0][0]
        storeResult.append(countResult)
        start.append(rangeStart)
        end.append(rangeEnd)
        rangeStart = rangeEnd
        rangeEnd = rangeEnd + range1
        counter = counter + 1
    list_a = []
    list_a.append(['Population Range','Number of States'])
    for i in range(0,counter):
        list_a.append([str(start[i]) + '-' + str(end[i]),storeResult[i]])
    return render_template('query5.html',rows=list_a)

#PANDAS CODE FOR PLOTTING
@app.route('/query6', methods=['GET', 'POST'])
def query6():
    

    if request.method == 'POST':
       
        range1 = float(request.form['range1'])
        range2 = float(request.form['range2'])
        df1=pd.read_csv('static/data/v.csv', encoding='latin-1')
        
       
        dfc = df1[(df1.Latitude > range1) & (df1.Latitude < range2)]

        dfcc = dfc['Elev']

        x= dfc['Latitude'].to_list()
        y= dfc['Elev'].to_list()
        

        #ax = dfn.plot(x, y ,style=['o','rx'])
        ax = plt.scatter(x,y)
        plt.xlabel('Latitude')
        plt.ylabel('Elevation')       
        plot = convert_fig_to_html(ax)
        rows=[]
        return render_template('query6.html',data=plot.decode('utf8'))

@app.route("/scatter", methods=["POST", "GET"])
def scattern():
    range1 = float(request.form.get('range1', ''))
    range2 = float(request.form.get('range2', ''))

    query1 = "SELECT Latitude from v where Latitude between '" +str(range1)+ "' and '" +str(range2)+"'"
    cursor.execute(query1)
    r1 = cursor.fetchall()

    rows = ([
        ['Lat', 'Elevation'],
        [str(range1) + '-' + str(range2), r1[0][0]]
    ])

    return render_template('scatter.html', rows=rows)

    #HISTOGRAM USING PANDAS
@app.route("/query7", methods=["POST", "GET"])
def query7():
    Country = str(request.form['Country'])
   
    df1 = pd.read_csv('static/data/v.csv', encoding='latin-1')
    dfc = df1[df1.Country == Country]
    
    dfcc = dfc['Elev']
    x= dfc['Country'].to_list()
    y= dfc['Elev'].to_list()
    
    ax = dfcc.plot.bar()
    plt.xlabel('COUNTRY')
    plt.ylabel('ELEVATION') 
    plot = convert_fig_to_html(ax)
    rows=[]
    return render_template('histpandas.html',data1=plot.decode('utf8'))

    




if __name__ == '__main__':
    app.run()
