from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # GET /messages: return all messages ordered by created_at ascending
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.to_dict() for message in messages])
    
    elif request.method == 'POST':
        # POST /messages: create a new message
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)
    
    if request.method == 'PATCH':
        # PATCH /messages/<id>: update message body
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())
    
    elif request.method == 'DELETE':
        # DELETE /messages/<id>: delete message
        db.session.delete(message)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(port=5555)
