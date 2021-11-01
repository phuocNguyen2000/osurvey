
from functools import wraps
from logging import error, warn
from threading import current_thread
import time
from models import answer, user_event
from models.user import User
from models.user_tag import UserTag
from settings import app,db
import requests
from PIL import Image
from io import BytesIO
import io
import base64
from flask import request,redirect,make_response,jsonify,send_file
from flask import  render_template
import json
import models
import datetime
import hashlib
import hmac
from flask_cors import cross_origin
from werkzeug.security import check_password_hash
import jwt
from apscheduler.schedulers.background import BackgroundScheduler
import schedule
import time
import datetime
import uuid
from random import sample
import fcm_manager
from flask_sock import Sock
from multiprocessing import Process
import numpy as np
import csv

from flask import  Response

def token_required(f):
    @wraps(f)
    def decorated(*args,**kargs):
        token=None
      
        if 'X-Authorization' in request.headers:
            token=request.headers['X-Authorization']
            if  token: 
                try:
                    data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"],options={"verify_exp": False})
                    current_user=models.User.query.filter_by(email=data["email"]).first()
                except:
                    return jsonify({"error":"token is invalid?"}),401
                return f(current_user,*args,**kargs)
            else:
                return jsonify({"error":"token is missing?"}),401
        else:
         return  jsonify({"error":"token is missing?"}),401
    return decorated

sock = Sock(app)


@app.route('/download',methods=["POST"])
def downloadFile():  
    if request.method== "POST":
        if 'event_id' in request.get_json():
            event_id=request.get_json()["event_id"]
            result = db.session.execute(
            "SELECT question.content, count(answer.question_id) as `count`"
            +" FROM "+
                "event,user_event,answer,question,user"
            +" WHERE user_event.event_id=event.event_id "
                +" and event.event_id={}".format(event_id)
                +" and answer.user_event_id=user_event.user_event_id"
                +" and question.question_id=answer.question_id"
                +" and user_event.user_id=user.user_id "+
            "group by user_event.event_id,answer.question_id")
    
            key = ','.join([str(elem) for elem in result.keys()])
            val = ',\n'.join([str(elem).replace(")", "").replace("(", "") for elem in result])
            data=key+"\n"+val+"\n"
                
            print(data)
            s=np.fromstring(data, sep=',')

            return Response(
                data,
                mimetype="text/csv",
                headers={"Content-disposition":
                    "attachment; filename=myplot.csv"}),200

@app.route('/currentUser',methods=["POST"])
@cross_origin(origin='*')
@token_required
def test(current_user):
    print(current_user)
    return jsonify({"first_name":current_user.first_name,"last_name":current_user.last_name,"user_name":current_user.user_name})



@app.route('/ownSurvey',methods=["POST"])
@cross_origin(origin='*')
@token_required
def ownSurvey(current_user):
    if current_user:
        own_surveys=models.Survey.query.filter_by(user_id=current_user.user_id).all()
        ows=None
        if own_surveys:
            ows={"surveys":[{"name":s.name,"id":s.survey_id,"base64":str(s.base64),"description":s.desc,"questions":[
                {"content":i.content,"options":[{"content":o.content,"type":o.type} for o in i.options]
            } for i in s.questions]} for s in own_surveys]}
        else:
            ows={"surveys":[]}
    return jsonify(ows)

@app.route('/ownSurveyLite',methods=["POST"])
@cross_origin(origin='*')
@token_required
def ownSurveyLite(current_user):
    if current_user:
        own_surveyslite=models.Survey.query.filter_by(user_id=current_user.user_id).all()
        owslite=None
        if own_surveyslite:
          
            
            owslite={"surveys":[{"name":s.name,"id":s.survey_id,"description":s.desc,"questions":[
                {"content":i.content,"options":[{"content":o.content,"type":o.type} for o in i.options]
            } for i in s.questions]} for s in own_surveyslite]}
        else:
            owslite={"surveys":[]}
    return jsonify(owslite)

@app.route('/doSurvey',methods=["POST"])
@cross_origin(origin='*')
@token_required
def doSurvey(current_user):
    if request.method=="POST":
        if current_user:
            event=request.get_json()["event"]
            if event:    
                u_e=models.UserEvent.query.filter_by(user_id=current_user.user_id,event_id=event["id"]).first()
                if u_e:
                    for q in event["survey"]["questions"]:
                        for a in q["answers"]:
                            
                            answer= models.Answer(question_id=q["id"],user_event_id=u_e.user_event_id,answer=a["content"])
                            if a['is_different']==True:
                                answer.is_different=True
                            u_e.do=True
                            db.session.add(answer)
                            db.session.commit()
                else:
                    return json.dumps({"error":"not invited"}),401
            else:
                return json.dumps({"error":"require data"}),401
        else:
            return json.dumps({"error":"require user"}),401
    return json.dumps({"message":"completed"}),200




@app.route('/ownEvent',methods=["POST"])
@cross_origin(origin='*')
@token_required
def ownEvent(current_user):
    if current_user:
        ows=None
        if current_user.own_events:
            ows={"events":
            [
                {
                    "id":e.event_id,
                    "start":e.start.date(),
                    "end":e.end.date(),
                    "status":e.status_id,
                    "payment":
                    [
                        {
                            "paypal_payment_id":p.paypal_pay_id,
                            "state":p.state
                        }
                         for p in e.payment],
                        "time_stame":e.time_stame,
                         "survey":
                {
                    "survey_id":e.survey_id,
                    "name":e.survey.name,
                    "description":e.survey.desc,
                    "base64":e.survey.base64,
                    "questions":[
                        {
                            "id":q.question_id,
                            "type":q.type,
                            "allow_diffrent_answer":q.allow_diffent_answer,
                            "content":q.content,
                            "options":[
                                {
                                    "id":o.option_id,
                                    "content":o.content
                                } 
                                for o in q.options
                                    ]
                        } 
                        for q in e.survey.questions
                        ]},"tags":[{"id":t.tag_id,"name":t.name} for t in e.tags]} for e in current_user.own_events]}
        else:
            ows={"events":[]}
    return jsonify(ows)

@app.route('/joinEvent',methods=["POST"])
@cross_origin(origin='*')
@token_required
def joinEvent(current_user):
    if current_user:
        ows=None

        if current_user.do_surveys:
            ows={"events":[
            {
            "id":e.event_id,
            "payment":[
                {
                    "paypal_payment_id":p.paypal_pay_id,"state":p.state
                } 
                for p in e.payment
                ],
            "time_stame":e.time_stame,
            "survey":
                {
                    "survey_id":e.survey_id,
                    "name":e.survey.name,
                    "description":e.survey.desc,
                    "base64":e.survey.base64,
                    "questions":[
                        {
                            "id":q.question_id,
                            "type":q.type,
                            "allow_diffrent_answer":q.allow_diffent_answer,
                            "content":q.content,
                            "options":[
                                {
                                    "id":o.option_id,
                                    "content":o.content,
                                    "check":False
                                } 
                                for o in q.options
                                    ]
                        } 
                        for q in e.survey.questions
                        ]},
            "tags":[
                {
                    "id":t.tag_id,
                    "name":t.name
                }
             for t in e.tags
            ]} for e in current_user.do_surveys]}
        else:
            ows={"events":[]}
    return jsonify(ows)

@app.route('/checkout',methods=["GET"])
@cross_origin(origin='*')
def checkout():
    payment_id = request.args.get('paymentId')
    payer_id=request.args.get('PayerID')
    token=request.args.get('token')
    headers={
                        'Content-Type': 'application/json',
                        'Authorization':'Bearer '+ get_access_token()
                }
    data={
        "payer_id":payer_id
    }
    payment=models.Payment.query.filter_by(paypal_pay_id=payment_id).first()
    if payment:
        response = requests.post("https://api.sandbox.paypal.com/v1/payments/payment/"+payment_id+"/execute",data=json.dumps(data), headers=headers)
        if "id" in response.json():
            payment.state=True
            db.session.commit()
        return  json.dumps(response.json()),200
    else:
        return json.dumps({"error":"payment error"}),401



def get_access_token():
    headers={
                        'Content-Type': 'application/x-www-form-urlencoded'
                }
    data={'grant_type': 'client_credentials'}
    response = requests.post("https://api.sandbox.paypal.com/v1/oauth2/token",
    auth=('AWclxyD8OVZu-UlkCAOMgFAcep_rbqGL5jhlazEw-HiXqFMpO6P6mOqLyByoC-BnwmkqZMnQlDT0itxE',
    'ELcrCDJE9TV6gxCRZnS0sWP7116Fa444UnqjBUqMRdzco713VJ9hiI2C67ndfU3GBUz1kUNfLMYOpcvL'), data=data, headers=headers)

    return response.json()["access_token"]


def countUser(ev_users,questions_count):
    count=0
    for event_user in ev_users:
        ans_questions_len=  db.session.query(models.Answer.question_id).group_by(models.Answer.question_id).filter(models.Answer.user_event_id==event_user.user_event_id).all()
        if len(ans_questions_len)>=questions_count*0.7:
            count=count+1
    return count

def addUserToEvent():
    statusofevs=models.StatusForEvent.query.all()
    for i in statusofevs[0].events:
        if i.end.date()==datetime.datetime.now().date() and i.payment.state==True:
            i.status=statusofevs[3]
            db.session.commit()
            ev_users=models.UserEvent.query.filter_by(event_id=i.event_id).all()
            count=countUser(ev_users=ev_users,questions_count=len(i.survey.questions))
            for event_user in ev_users:
                user=models.User.query.filter_by(user_id=event_user.user_id).first()
                ans_questions_len=  db.session.query(models.Answer.question_id).group_by(models.Answer.question_id).filter(models.Answer.user_event_id==event_user.user_event_id).all()
                if len(ans_questions_len)>=len(i.questions)*0.7:
                    if i.price/count>0:
                        gift=models.Gift(price=i.price/count,user_event=event_user)
                        headers={
                        'Content-Type': 'application/json',
                        'Authorization':'Bearer '+ get_access_token()
                        }
                        data={
                        "sender_batch_header": {
                            "sender_batch_id":str(gift.gift_id),
                            "email_subject": "You have a payout!",
                            "email_message": "You have received a payout! Thanks for using our service!"
                        },
                        "items": [
                            {
                            "recipient_type": "EMAIL",
                            "amount": {
                                "value": str(i.price/count*0.00044),
                                "currency": "USD"
                            },
                            "note": "Thanks for your patronage!",
                            "sender_item_id": str(gift.gift_id),
                            "receiver":user.email
                            },
                            
                        ]
                        }
                        response = requests.post("https://api-m.sandbox.paypal.com/v1/payments/payouts",data=json.dumps(data), headers=headers)
                        if "batch_header" in response.json():
                            db.session.commit()
    for i in statusofevs[1].events:
        if len(i.payment)>0:
            if  datetime.datetime.now().date()>=i.start.date()  and i.payment[0].state==True:
                # i.status=statusofevs[0]
                db.session.execute("UPDATE event SET status_id="+str(statusofevs[0].status_for_event_id) +" where event_id="+str(i.event_id)+"")
                db.session.commit()
                users=models.User.query.all()
                print(len(users))
                suitable_users=[u for u in users if checkTags(user=u,event=i)==True and u.user_id!=i.survey.user_id]
                print(len(suitable_users))
                if  len(suitable_users)>i.limit:
                    suitable_users=sample(suitable_users,i.limit)
                for u in suitable_users:
                    n_us_ev=models.UserEvent(event_id=i.event_id,user_id=u.user_id)
                    print(n_us_ev)
                    db.session.add(n_us_ev)
                    db.session.commit()


def checkTags(user,event):
    check=False
    for utag in user.tags:
        if utag in event.tags:
            check=True
    return check





import atexit
scheduler = BackgroundScheduler()
scheduler.add_job(func=addUserToEvent, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
		
@app.route('/signUp',methods=["POST"])
@cross_origin(origin='*')
def signup(): 
    if request.method=="POST":
        url = 'https://api.fpt.ai/vision/idr/vnm'
        requesJson=request.get_json()
        
        if 'image64' in requesJson and "email" in requesJson and 'password' in requesJson and "user_name" in requesJson :
            data= requesJson['image64']
            tokens=[]
            tokens.append(requesJson['device_key'])
            if data:
                
                im = Image.open(BytesIO(base64.b64decode(data)))
                
                byteIO = io.BytesIO()
                im.save(byteIO, format='PNG')
                im.save("s"+".PNG", format='PNG')   
                    
                byteArr = byteIO.getvalue()
                print(requesJson['device_key'])
                        
                files = {'image': byteArr}
                headers = {
    'api-key': 'wEGzmFlGFGJZVhRiWmbIp77SFu5uvl7S'
}
                    
                response = requests.post(url, files=files, headers=headers)
                values= response.json()
               
                
                print(values)
                if "data" in values:
                    if values["data"]:
                        name=values["data"][0]['name'].split()
                        first_name=name[0]
                        print(first_name)
                        name=name[1:]
                        last_name = ' '.join([str(elem) for elem in name])
                        id_recognition=values["data"][0]['id']
                        province=values["data"][0]["address_entities"]['province']
                        district=values["data"][0]["address_entities"]['district']
                        ward=values["data"][0]["address_entities"]['ward']
                        street=values["data"][0]["address_entities"]['street']
                        dob=values["data"][0]['dob']
                        nationality=values["data"][0]['nationality']
                        sex=values["data"][0]['sex']
                        email=requesJson['email']
                        password=requesJson['password']
                        user_name=requesJson['user_name']
                        n_user=models.User(first_name=first_name,
                        user_name=user_name,
                        last_name=last_name,
                        id_recognition=id_recognition,
                        dob=dob,nationality=nationality,
                        sex=sex,email=email)
                        n_user.set_password(password)
                        if (db.session.query(models.User).filter_by(email=n_user.email).count() == 0 and db.session.query(models.User).filter_by(id_recognition=id_recognition).count()==0):
                            db.session.add(n_user)
                            db.session.commit()
                            n_address=models.Address(province=province,street=street,ward=ward,district=district,user=n_user)
                            db.session.add(n_address)
                            db.session.commit()
                            n_device=models.DeviceKey(key=requesJson['device_key'],user=n_user)
                            db.session.add(n_device)
                            db.session.commit()
                            datetime.datetime.now().year
                            print(n_user.dob)
                            t=n_user.dob.replace("/", "-")
                            n_year=datetime.datetime.strptime(t, '%d-%m-%Y')
                            print(n_year.year)
                            if (datetime.datetime.now().year -
                            n_year.year)>17  and (datetime.datetime.now().year -
                            n_year.year)<40:
                                ntag= models.UserTag(user_id=n_user.user_id,tag_id=1)
                                db.session.add(ntag)
                                db.session.commit()
                            if (datetime.datetime.now().year -
                            n_year.year)>=40  and (datetime.datetime.now().year -
                            n_year.year)<60:
                                ntag= models.UserTag(user_id=n_user.user_id,tag_id=2)
                                db.session.add(ntag)
                                db.session.commit()
                            if (datetime.datetime.now().year -
                            n_year.year)>=60:
                                ntag= models.UserTag(user_id=n_user.user_id,tag_id=3)
                                db.session.add(ntag)
                                db.session.commit()
                            if n_user.sex=="Nam":
                                ntag= models.UserTag(user_id=n_user.user_id,tag_id=4)
                                db.session.add(ntag)
                                db.session.commit()
                            if n_user.sex=="Nữ":
                                ntag= models.UserTag(user_id=n_user.user_id,tag_id=5)
                                db.session.add(ntag)
                                db.session.commit()
                            fcm_manager.sendPush(title="Wellcome to oSurvey",msg="Hello",re_token= tokens)
                            return json.dumps({"success ":"account is created !"}),200
                        else:
                            return json.dumps({"error":'Email or Id recognition is alrealy exsits!'}),411
                    else:
                        
                        if values['errorCode']==3:
                            return json.dumps({"error":"Unable to find ID card in the image"}),411

                else:
                    return json.dumps({"error":"Invalid Id recognition"}),411
                # im.save("ddd"+".PNG", format='PNG')
                # with open(response.json()['data'][0]['id']+".json", 'w', encoding='utf-8') as f:
                #                 json.dump(response.json(), f, ensure_ascii=False, indent=4)
     
            else: return json.dumps({"error":"Invalid value image64 null"}),411
        else:
            return json.dumps({"error":"Invalid values"}),411
    
    

@app.route('/signIn',methods=["POST"])
@cross_origin(origin='*')
def signin():
    if request.method=="POST":
        s=request.get_json()
        if s: 
            print(json.dumps(s))
            user=models.User.query.filter_by(email=s["email"]).first()
            if user:
                if user.check_password(s['password']):
                    print(s['device_key']
                    )
                    fcm_manager.sendPush(title="Wellcome to oSurvey",msg="Hello",re_token= [s['device_key']])
                    token=jwt.encode({"email":user.email,"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'], algorithm="HS256")
                    print(type(token))
                    key=models.DeviceKey.query.filter_by(user_id=user.user_id,key=s['device_key']).first()
                    if key==None:
                        n_key=models.DeviceKey(key=s['device_key'],user=user)
                        db.session.add(n_key)
                        db.session.commit()
                    user=models.User.query.filter_by(email=s["email"]).first()
                    tokens=[i.key for i in user.device_keys]
                    fcm_manager.sendPush(title="Wellcome to oSurvey",msg="Hello",re_token= tokens)
                    return jsonify({"token":token})
                else:
                    return make_response('Could not verify password error',401,{'WWW-Authenticate':'Basic realm="Login required!"'})
            else:
                return make_response('Could not verify user error',401,{'WWW-Authenticate':'Basic realm="Login required!"'})
                
    else:
        return make_response('Could not verify user error',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

