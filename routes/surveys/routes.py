from datetime import datetime
from functools import wraps
from os import name
from flask.json import jsonify
from flask_cors.decorator import cross_origin
import jwt
from flask import redirect,make_response,send_file
from flask import request
import models
from models import survey
from models import event_tag
from models import user
from models import event
from settings import app, db
import json
import requests
def token_required(f):
    @wraps(f)
    def decorated(*args,**kargs):
        token=None
        print(request.headers)
        if 'X-Authorization' in request.headers:
            token=request.headers['X-Authorization']
            if  token:
                print("token",token)    
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

@app.route('/createSurvey', methods=["POST"])
@cross_origin(origin='*')
@token_required
def createSurvey(current_user):
    if request.method=="POST":
        if "name" in request.get_json() and "questions"in request.get_json()  and "description"in request.get_json():
            res=request.get_json()
            print(res)
            if res["name"]:
                n_survey=models.Survey(name=res["name"],desc=res["description"],user=current_user)
                db.session.add(n_survey)
                db.session.commit()
                questions=res["questions"]
                for question in questions:
                    typeq=question["type"]
                    content=question["content"]
                    allow_diffrent_answer=question["allow_diffrent_answer"] 
                    n_question=models.Question(content=content,survey=n_survey,allow_diffent_answer=allow_diffrent_answer ,type=typeq)
                    db.session.add(n_question)
                    db.session.commit()
                    for option in question["options"]:
                        print(option["content"])
                        n_option=models.Option(content=option["content"],question=n_question)
                        db.session.add(n_option)
                        db.session.commit()           
            else:
                return json.dumps({"error":"data not found"}),401
            return  json.dumps({"message":"create survey completed"}),200
        else:
            return json.dumps({"error":"data not found"}),401

def get_access_token():
    headers={
                        'Content-Type': 'application/x-www-form-urlencoded'
                }
    data={'grant_type': 'client_credentials'}
    response = requests.post("https://api.sandbox.paypal.com/v1/oauth2/token",
    auth=('AWclxyD8OVZu-UlkCAOMgFAcep_rbqGL5jhlazEw-HiXqFMpO6P6mOqLyByoC-BnwmkqZMnQlDT0itxE',
    'ELcrCDJE9TV6gxCRZnS0sWP7116Fa444UnqjBUqMRdzco713VJ9hiI2C67ndfU3GBUz1kUNfLMYOpcvL'), data=data, headers=headers)

    return response.json()["access_token"]

def create_checkout():
    headers={
                        'Content-Type': 'application/json',
                        'Authorization':'Bearer '+ get_access_token()
                }
    data={
  "intent": "sale",
  "payer": {
    "payment_method": "paypal"
  },
  "transactions": [
    {
      "amount": {
        "total": "30.11",
        "currency": "USD",
        "details": {
          "subtotal": "30.00",
          "tax": "0.07",
          "shipping": "0.03",
          "handling_fee": "1.00",
          "shipping_discount": "-1.00",
          "insurance": "0.01"
        }
      },
      "description": "The payment transaction description.",
      "custom": "EBAY_EMS_90048630024435",
      "invoice_number": "48787589673",
      "payment_options": {
        "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
      },
      "soft_descriptor": "ECHI5786786",
      "item_list": {
        "items": [
          {
            "name": "hat",
            "description": "Brown hat.",
            "quantity": "5",
            "price": "3",
            "tax": "0.01",
            "sku": "1",
            "currency": "USD"
          },
          {
            "name": "handbag",
            "description": "Black handbag.",
            "quantity": "1",
            "price": "15",
            "tax": "0.02",
            "sku": "product34",
            "currency": "USD"
          }
        ],
        "shipping_address": {
          "recipient_name": "Brian Robinson",
          "line1": "4th Floor",
          "line2": "Unit #34",
          "city": "San Jose",
          "country_code": "US",
          "postal_code": "95131",
          "phone": "011862212345678",
          "state": "CA"
        }
      }
    }
  ],
  "note_to_payer": "Contact us for any questions on your order.",
  "redirect_urls": {
    "return_url": "http://localhost/",
    "cancel_url": "https://example.com/cancel"
  }
}
    response = requests.post("https://api.sandbox.paypal.com/v1/payments/payment",data=json.dumps(data), headers=headers)

    print(response.json())

        

@app.route('/editSurvey', methods=["POST"])
@cross_origin(origin='*')
@token_required
def editSurveys(current_user):
    if current_user:
        if request.method=="POST":
            if "id" in request.get_json():
                res=request.get_json()
                survey=models.Survey.query.filter_by(survey_id=res["id"]).first()
                if survey.status_id==2:
                    if res["name"]:
                        survey.name=res["name"]
                    if res["description"]:
                        survey.desc=res["description"]
                    db.session.commit()
                    db.session.delete(survey.questions)
                    db.session.commit();       
                    questions=res["questions"]
                    for question in questions:
                        contentt=question["content"]
                        n_question=models.Question(content=contentt,survey=survey)
                        db.session.add(n_question)
                        db.session.commit()
                        for option in question["options"]:
                            print(option['content'])
                            n_option=models.Option(content=option['content'],question=question)
                            db.session.add(n_option)
                            db.session.commit()
                    return json.dumps({"message":"survey created"}),200
                else:
                    return json.dumps({"error":"survey is in event"}),401
            else:
                return  json.dumps({"error":"required id survey"}),401
    else:
        return  json.dumps({"error":"required user"}),401

@app.route('/deleteSurvey', methods=["POST"])
@cross_origin(origin='*')
@token_required
def deleteSurvey(current_user):
    if request.method=="POST":
        if "id" in request.get_json():
            res=request.get_json()
            survey=models.Survey.query.filter_by(survey_id=res["id"]).first()
            if survey.status_id==2:    
                db.session.commit()
                db.session.delete(survey)
                return jsonify({"message":"delete complete"},200)
            else:
                jsonify({"error":"survey is in event"},401)
        else:
            return  jsonify({"error":"required id survey"},401)


@app.route('/createEvent', methods=["POST"])
@cross_origin(origin='*')
@token_required
def createEvent(current_user):
    if request.method=="POST":
        if "start" in request.get_json() and "end" in request.get_json() and "survey" in request.get_json() and "limit" in request.get_json() and "tags" in request.get_json():
            res=request.get_json()
            survey=models.Survey.query.filter_by(survey_id=res["survey"]["id"],user=current_user).first()
            
            start=datetime.strptime(res["start"].split(".")[0],'%Y-%m-%d %H:%M:%S')
           
            
            end=datetime.strptime(res["end"].split(".")[0],'%Y-%m-%d %H:%M:%S')
            if start.date()>=datetime.now().date() and start.date() < end.date():
              price=res["price"]
              give_away=res["give_away"]
              n_event=models.Event(limit=res["limit"],user=current_user,survey=survey,start=start,end=end,price=price,give_away=give_away)
              db.session.add(n_event)
              db.session.commit()
              tags=[e["id"]  for e in res["tags"] if e["selected"]==True]
              if 1 in tags:
                  ev_tag=models.EventTag(tag_id=1,event_id=n_event.event_id)
                  db.session.add(ev_tag)
                  db.session.commit()

                  
              if 2 in tags:
                  ev_tag=models.EventTag(tag_id=2,event_id=n_event.event_id)
                  db.session.add(ev_tag)
                  db.session.commit()
                  
              if 3 in tags:
                  ev_tag=models.EventTag(tag_id=3,event_id=n_event.event_id)
                  db.session.add(ev_tag)
                  db.session.commit()
                  
              if 4 in tags:
                  ev_tag=models.EventTag(tag_id=4,event_id=n_event.event_id)
                  db.session.add(ev_tag)
                  db.session.commit()
                  
              if 5 in tags:
                  ev_tag=models.EventTag(tag_id=5,event_id=n_event.event_id)
                  db.session.add(ev_tag)
                  db.session.commit()
                  
              headers={
                          'Content-Type': 'application/json',
                          'Authorization':'Bearer '+ get_access_token()
                  }
              x=round(res["total"]*0.000044,2)
              n_pay=models.Payment(user=current_user,event=n_event,total=res["total"])
              print(x)
              year=str(datetime.now().year)
              month=str(datetime.now().month)
              day=str(datetime.now().day)
              hour=str(datetime.now().hour)
              minu=str(datetime.now().minute)
              second=str(datetime.now().second)
              print(year+month+day+hour+minu+second)
              data={
                "intent": "sale",
                "payer": {
                  "payment_method": "paypal"
                },
                "transactions": [
                  {
                    "amount": {
                      "total": str(x+0.05),
                      "currency": "USD",
                      "details": {
                        "subtotal": str(x),
                        "tax": "0.01",
                        "shipping": "0.03",
                        "handling_fee": "1.00",
                        "shipping_discount": "-1.00",
                        "insurance": "0.01"
                      }
                    },
                    "description": "The payment transaction description.",
                    "custom": "EBAY_EMS_90048630024435",
                    "invoice_number": str(n_pay.payment_id)+year+month+day+hour+minu+second,
                    "payment_options": {
                      "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
                    },
                    "soft_descriptor": "ECHI5786786",
                    "item_list": {
                      "items": [
                        {
                          "name": "event",
                          "description": "Brown hat.",
                          "quantity": "1",
                          "price": str(x),
                          "tax": "0.01",
                          "sku": "1",
                          "currency": "USD"
                        },
                        
                      ],
                      "shipping_address": {
                        "recipient_name": "Brian Robinson",
                        "line1": "4th Floor",
                        "line2": "Unit #34",
                        "city": "San Jose",
                        "country_code": "US",
                        "postal_code": "95131",
                        "phone": "011862212345678",
                        "state": "CA"
                      }
                    }
                  }
                ],
                "note_to_payer": "Contact us for any questions on your order.",
                "redirect_urls": {
                  "return_url": "https://osurvey-server.herokuapp.com/checkout",
                  "cancel_url": "https://example.com/cancel"
                }
              }
  
              response = requests.post("https://api.sandbox.paypal.com/v1/payments/payment",data=json.dumps(data), headers=headers)
              print(response.json())
              paypal_pay_id=response.json()["id"]
              s=None
              for link in response.json()["links"]:
                if link["method"]=='REDIRECT':
                      s=link['href'].split("token=")[1]
              checkout_token=s
              n_pay.paypal_pay_id=paypal_pay_id
              n_pay.checkout_token=checkout_token
              db.session.add(n_pay)
              db.session.commit()
              return  json.dumps({"pay_token":s}),200
        else:
            return  json.dumps({"error":"required id even data"}),401
    else:
        return  json.dumps({"error":"required id event data"}),401



    
    
