import csv
import sqlalchemy as sqAl

metadata = sqAl.MetaData()
engine = sqAl.create_engine('sqlite:///%s' % 'survey.db')
metadata.bind = engine

mytable = sqAl.Table('event', metadata, autoload=True)
db_connection = engine.connect()

select = sqAl.sql.select([mytable])
result = db_connection.execute("SELECT user.user_id,user.last_name,user.dob,question.content, count(answer.question_id) as `count`  FROM event,user_event,answer,question,user WHERE user_event.event_id=event.event_id and event.event_id=1 and answer.user_event_id=user_event.user_event_id and question.question_id=answer.question_id and user_event.user_id=user.user_id group by user_event.user_id,answer.question_id")

fh = open('data.csv', 'w')
outcsv = csv.writer(fh)

outcsv.writerow(result.keys())
outcsv.writerows(result)

fh.close