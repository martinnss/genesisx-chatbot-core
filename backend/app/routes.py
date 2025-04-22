from flask import Blueprint, request, jsonify
from .models import db, User, Conversation, Message
from .utils import call_anthropic_api, format_history, get_api_call_count

bp = Blueprint("routes", __name__)

@bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "No se encuentra el usuario o el mensaje"}), 400

    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id)
        db.session.add(user)

    if len(user.conversations) >= 10:
        return jsonify({"error": "Se ha alcanzado el límite de conversaciones"}), 403

    conversation = Conversation(user_id=user_id)
    db.session.add(conversation)
    db.session.commit()

    msg_user = Message(conversation_id=conversation.id, sender="user", content=message)
    db.session.add(msg_user)
    db.session.commit()

    history = format_history(conversation.id)
    try:
        reply = call_anthropic_api(history)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

    msg_bot = Message(conversation_id=conversation.id, sender="bot", content=reply)
    db.session.add(msg_bot)

    user.api_usage += 1
    db.session.commit()

    return jsonify({"reply": reply, "conversation_id": conversation.id})

@bp.route("/history/<int:user_id>", methods=["GET"])
def get_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "No se encuentra el usuario"}), 404

    result = []
    for convo in user.conversations:
        result.append({
            "conversation_id": convo.id,
            "created_at": convo.created_at.isoformat(),
            "messages": [
                {"sender": m.sender, "content": m.content, "timestamp": m.timestamp.isoformat()}
                for m in convo.messages
            ],
        })
    return jsonify(result)

@bp.route("/conversation/<int:conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    convo = Conversation.query.get(conversation_id)
    if not convo:
        return jsonify({"error": "No se encuentra la conversación"}), 404

    return jsonify([
        {"sender": m.sender, "content": m.content, "timestamp": m.timestamp.isoformat()}
        for m in convo.messages
    ])

@bp.route("/api_usage", methods=["GET"])
def api_usage():
    """Devuelve el contador de llamadas a Anthropic de esta sesión."""
    return jsonify({"api_calls": get_api_call_count()})