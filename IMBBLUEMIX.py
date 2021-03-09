from flask import Flask, render_template, request
import os
import ibm_db
app = Flask(__name__)

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=******;PWD=******;","","")

port = int(os.getenv('PORT', 5000))



@app.route('/')
def hello_world():
    '''
    if request.method == "POST":
        # fetch form data
        userDet = request.form
        name = userDet['name']
        email = userDet['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email) VALUES(%s,%s) ", (name, email))
        mysql.connection.commit()
        cur.close()
        return "Success"
    return render_template('search.html')
    '''

    query = "SELECT * FROM PEOPLE"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.execute(stmt)
    rows = []
    result = ibm_db.fetch_assoc(stmt)
    while result != False:
        rows.append(result.copy())
        result = ibm_db.fetch_assoc(stmt)
        # ibm_db.close(conn)

    return render_template('search.html', data=rows)

@app.route('/data', methods=['GET', 'POST'])
def salary_greater():
    if request.method == 'POST':
        print("bye")
        # fetch form data

        name = request.form['name']
       
        query2 = 'SELECT * FROM PEOPLE where  "SALARY" <= '+ name + ''
        
        print(name)
        
        stmt1 = ibm_db.prepare(conn, query2)
        ibm_db.execute(stmt1)
        rows1 = []
        result1 = ibm_db.fetch_assoc(stmt1)
        while result1 != False:
            rows1.append(result1.copy())
            result1 = ibm_db.fetch_assoc(stmt1)

        return render_template('searching.html', data=rows1)
    return render_template('searching.html')


@app.route('/updatesal', methods=['GET', 'POST'])
def update_sal():
    if request.method == 'POST':
        print("bye")
        # fetch form data

        name = request.form['name']
        sal = request.form['sal']
        
        

        query3='UPDATE PEOPLE SET "SALARY" = \''  + sal + '\' WHERE "FNAME" = \''  + name + '\''
        stmt2 = ibm_db.prepare(conn, query3)
        ibm_db.execute(stmt2)
        
        
        print(name)
        
        '''
        rows1 = []
        result1 = ibm_db.fetch_assoc(stmt2)
        while result1 != False:
            rows1.append(result1.copy())
            result1 = ibm_db.fetch_assoc(stmt2)
        '''
       
        return render_template('updating_sal.html')#, data=rows1)
    return render_template('updating_sal.html')

@app.route('/updatedesc', methods=['GET', 'POST'])
def update_desc():
    if request.method == 'POST':
        print("bye")
        # fetch form data

        name = request.form['name']
        
        desc = request.form['desc']
        
        query6 = 'UPDATE PEOPLE SET "DESCRIPTION" = \''  + desc + '\' WHERE "FNAME" = \''  + name + '\''
        stmt6 = ibm_db.prepare(conn, query6)
        ibm_db.execute(stmt6)
        
        print(name)
        
        '''
        rows1 = []
        result1 = ibm_db.fetch_assoc(stmt6)
        while result1 != False:
            rows1.append(result1.copy())
            result1 = ibm_db.fetch_assoc(stmt6)
        '''
       
        return render_template('updating_desc.html')#, data=rows1)
    return render_template('updating_desc.html')



@app.route('/name', methods=['GET', 'POST'])
def search_name():
    if request.method == 'POST':
        print("bye")
        # fetch form data

        name = request.form['name']
        query2 = 'SELECT * FROM PEOPLE where "FNAME" =\''  + name + '\''
        
        print(name)
        
        stmt1 = ibm_db.prepare(conn, query2)
        ibm_db.execute(stmt1)
        rows1 = []
        result1 = ibm_db.fetch_assoc(stmt1)
        while result1 != False:
            rows1.append(result1.copy())
            result1 = ibm_db.fetch_assoc(stmt1)

        return render_template('byname.html', data=rows1)
    return render_template('byname.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    if request.method == 'POST':
        print("bye")
        # fetch form data

        fname = request.form['name']
       
        query4 = 'DELETE FROM PEOPLE WHERE "FNAME" =\'' + fname + '\''
        print(fname)
        
        stmt4 = ibm_db.prepare(conn, query4)
        ibm_db.execute(stmt4)
        '''
        rows1 = []
        result1 = ibm_db.fetch_assoc(stmt1)
        while result1 != False:
            rows1.append(result1.copy())
            result1 = ibm_db.fetch_assoc(stmt1)
        '''
        return render_template('delete.html')
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
