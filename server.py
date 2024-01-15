from flask import Flask, render_template, request, jsonify
import deploy
import sqlite3

app = Flask (__name__)

@app.route ('/')
def homepage():
    return render_template ('index.html')

@app.route ('/logout')
def logout():
    return render_template ('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT email FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            email = result[0]
            f = open('session.txt', 'w')
            f.write(email)
            f.close()
            return render_template('user.htm')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()
        
        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            query = "SELECT email FROM userinfo"
            cursor.execute(query)
            result1 = cursor.fetchall()
            print(result1)
            return render_template('admin.htm', result1=result1)

    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        email = request.form['email']

        query = "SELECT * FROM userinfo where email = '"+email+"'"
        cursor.execute(query)

        result = cursor.fetchall()
        print(result[-1])
        result = result[-1]
        return render_template('admin.htm', result=result)

    return render_template('index.html')

@app.route('/adminreg', methods=['GET', 'POST'])
def adminreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route ('/api/bot', methods = ['POST'])
def say_name ():
    review_text = request.form['review_text']
    rating = request.form['rating']
    verified_purchase =  request.form['verified_purchase']
    product_category = request.form['product_category']
    result =  deploy.get_result(review_text, rating, verified_purchase, product_category)
    print (result)
  
    if result[0] == 1:
            
            if "good" in str(review_text) or "better" in str(review_text) or "best" in str(review_text):
                print ("It is a True and good review")
                return jsonify (result = "It is a True and good review")
            else: 
                print ("It is a True and bad Review")
                return jsonify (result = "It is a True and bad Review")
            

    else:
            
            if "good" in str(review_text) or "better" in str(review_text) or "best" in str(review_text):
                print ("It is a Fake and good review")
                return jsonify (result = "It is a Fake and good review")
            else: 
                print ("It is a Fake and bad Review")
                return jsonify (result = "It is a Fake and bad Review")

@app.route ('/api1/bot1', methods = ['POST'])
def say_name1 ():
    print('ppppppppp')
    review_text = request.form['review_text']
    rating = request.form['rating']
    product_category = request.form['product_category']
    print(review_text, rating, product_category)
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    f = open('session.txt', 'r')
    email = f.read()
    f.close()
    command = """CREATE TABLE IF NOT EXISTS userinfo(email TEXT, review_text TEXT, rating TEXT, product_category TEXT)"""
    cursor.execute(command)

    cursor.execute("INSERT INTO userinfo VALUES ('"+email+"', '"+review_text+"', '"+rating+"', '"+product_category+"')")
    connection.commit()
    return jsonify (result = 'data successfully added')
        
from pyngrok import ngrok

def config_ngrok() :
    app.config['START_NGROK'] = True
    url = ngrok.connect(5000)
    print(' * Public URL:', url)

if __name__ == '__main__':
    config_ngrok()
    app.run ()
