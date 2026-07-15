from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, School, Round, Score, UsedQuestion
import json
import os
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-please-change')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)

# Load questions
with open('questions.json', 'r') as f:
    QUESTIONS = json.load(f)

# ---------- Global State ----------
current_state = {
    "round_id": None,
    "round_name": "No Round Selected",
    "question_id": None,
    "question_text": "Load a question to start",
    "options": [],
    "current_school": None,
    "scores": {},
    "schools": [],
    "timestamp": datetime.now().isoformat(),
    "question_number": None,
    "is_dead": False
}

# ---------- Timer State (no thread) ----------
timer_state = {
    'running': False,
    'start_time': None,
    'max_time': 15,
    'time_left': 15,
    'round_name': ''
}

# ---------- Helper Functions ----------
def get_question_for_admin(q_id):
    for q in QUESTIONS:
        if q['id'] == q_id:
            return q
    return None

def get_round_scores_dict(round_id):
    scores = Score.query.filter_by(round_id=round_id).all()
    agg = {}
    for s in scores:
        if s.school_id not in agg:
            agg[s.school_id] = 0
        agg[s.school_id] += s.points
    return agg

def update_projector_state(round_id, question_id, turn_index, scores_dict, is_dead=False):
    global current_state, timer_state
    current_state["timestamp"] = datetime.now().isoformat()
    current_state["is_dead"] = is_dead
    
    if round_id:
        round_obj = Round.query.get(round_id)
        if round_obj:
            current_state["round_id"] = round_id
            current_state["round_name"] = round_obj.name
            school_ids = round_obj.school_ids
            schools = School.query.filter(School.id.in_(school_ids)).all()
            current_state["schools"] = [{"id": s.id, "name": s.name} for s in schools]
            
            # Set timer max time based on round
            if 'Round 4' in round_obj.name or 'Round 5' in round_obj.name:
                timer_state['max_time'] = 10
            else:
                timer_state['max_time'] = 15
            if not timer_state['running']:
                timer_state['time_left'] = timer_state['max_time']
                timer_state['start_time'] = None
            timer_state['round_name'] = round_obj.name
        else:
            current_state["schools"] = []
    else:
        current_state["schools"] = []

    if question_id:
        q = get_question_for_admin(question_id)
        if q:
            current_state["question_id"] = q["id"]
            current_state["question_text"] = q["question"]
            current_state["options"] = q["options"]
            current_state["question_number"] = q["id"]
        else:
            current_state["question_text"] = "Question not found"
            current_state["options"] = []
    else:
        current_state["question_text"] = "No question loaded"
        current_state["options"] = []

    if turn_index is not None and current_state["schools"]:
        if turn_index < len(current_state["schools"]):
            current_state["current_school"] = current_state["schools"][turn_index]
        else:
            current_state["current_school"] = None
    else:
        current_state["current_school"] = None

    current_state["scores"] = scores_dict or {}

# ---------- Routes ----------
@app.route('/')
def serve_admin():
    return app.send_static_file('admin.html')

@app.route('/admin')
def serve_admin_alt():
    return app.send_static_file('admin.html')

@app.route('/projector')
def serve_projector():
    return app.send_static_file('projector.html')

@app.route('/boss')
def serve_boss():
    return app.send_static_file('boss.html')

@app.route('/result/<result_id>')
def boss_view(result_id):
    return app.send_static_file('boss.html')

# ---------- API Routes ----------
@app.route('/api/rounds', methods=['GET'])
def get_rounds():
    rounds = Round.query.all()
    result = []
    for r in rounds:
        schools = School.query.filter(School.id.in_(r.school_ids)).all()
        result.append({
            'id': r.id,
            'name': r.name,
            'schools': [{'id': s.id, 'name': s.name} for s in schools]
        })
    return jsonify(result)

@app.route('/api/question/<int:q_id>', methods=['GET'])
def get_question(q_id):
    q = get_question_for_admin(q_id)
    if not q:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify(q)

@app.route('/api/check_question_used', methods=['POST'])
def check_question_used():
    data = request.json
    round_id = data.get('round_id')
    question_id = data.get('question_id')
    used = UsedQuestion.query.filter_by(
        round_id=round_id, 
        question_id=question_id
    ).first()
    return jsonify({'used': used is not None})

@app.route('/api/score', methods=['POST'])
def add_score():
    data = request.json
    round_id = data.get('round_id')
    school_id = data.get('school_id')
    question_id = data.get('question_id')
    points = data.get('points')
    score_type = data.get('type', 'primary')

    if not all([round_id, school_id, question_id, points is not None]):
        return jsonify({'error': 'Missing fields'}), 400

    new_score = Score(
        round_id=round_id,
        school_id=school_id,
        question_id=question_id,
        points=points,
        type=score_type
    )
    db.session.add(new_score)
    db.session.commit()
    
    used = UsedQuestion.query.filter_by(
        round_id=round_id,
        question_id=question_id
    ).first()
    if not used:
        used = UsedQuestion(round_id=round_id, question_id=question_id)
        db.session.add(used)
        db.session.commit()
    
    scores = get_round_scores_dict(round_id)
    update_projector_state(
        round_id, 
        data.get('current_q_id'), 
        data.get('turn_index'), 
        scores,
        data.get('is_dead', False)
    )
    
    return jsonify({'success': True, 'id': new_score.id})

@app.route('/api/scores/round/<int:round_id>', methods=['GET'])
def get_round_scores(round_id):
    return jsonify(get_round_scores_dict(round_id))

@app.route('/api/scores/all', methods=['GET'])
def get_all_scores():
    scores = Score.query.all()
    agg = {}
    for s in scores:
        if s.school_id not in agg:
            agg[s.school_id] = 0
        agg[s.school_id] += s.points
    schools = School.query.all()
    name_map = {s.id: s.name for s in schools}
    result = [{'school_id': sid, 'name': name_map.get(sid, 'Unknown'), 'total': pts} for sid, pts in agg.items()]
    result.sort(key=lambda x: x['total'], reverse=True)
    return jsonify(result)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(current_state)

@app.route('/api/update_state', methods=['POST'])
def update_state():
    data = request.json
    round_id = data.get('round_id')
    question_id = data.get('question_id')
    turn_index = data.get('turn_index')
    is_dead = data.get('is_dead', False)
    scores = get_round_scores_dict(round_id) if round_id else {}
    update_projector_state(round_id, question_id, turn_index, scores, is_dead)
    return jsonify({'success': True})

@app.route('/api/round_questions_count/<int:round_id>', methods=['GET'])
def get_round_questions_count(round_id):
    count = UsedQuestion.query.filter_by(round_id=round_id).count()
    return jsonify({'count': count})

@app.route('/api/reset_round/<int:round_id>', methods=['POST'])
def reset_round(round_id):
    Score.query.filter_by(round_id=round_id).delete()
    UsedQuestion.query.filter_by(round_id=round_id).delete()
    db.session.commit()
    scores = get_round_scores_dict(round_id)
    update_projector_state(
        round_id, 
        current_state.get('question_id'), 
        0, 
        scores,
        False
    )
    return jsonify({'success': True})

# ---------- Timer Endpoints (no thread) ----------
@app.route('/api/timer/start', methods=['POST'])
def timer_start():
    global timer_state
    if timer_state['time_left'] <= 0:
        timer_state['time_left'] = timer_state['max_time']
    timer_state['running'] = True
    timer_state['start_time'] = time.time()
    return jsonify(timer_state)

@app.route('/api/timer/stop', methods=['POST'])
def timer_stop():
    global timer_state
    timer_state['running'] = False
    timer_state['start_time'] = None
    return jsonify(timer_state)

@app.route('/api/timer/reset', methods=['POST'])
def timer_reset():
    global timer_state
    timer_state['running'] = False
    timer_state['time_left'] = timer_state['max_time']
    timer_state['start_time'] = None
    return jsonify(timer_state)

@app.route('/api/timer/state', methods=['GET'])
def get_timer_state():
    global timer_state
    if timer_state['running'] and timer_state['start_time'] is not None:
        elapsed = time.time() - timer_state['start_time']
        remaining = timer_state['max_time'] - elapsed
        if remaining <= 0:
            timer_state['running'] = False
            timer_state['time_left'] = 0
            timer_state['start_time'] = None
        else:
            timer_state['time_left'] = int(remaining) + 1
    return jsonify({
        'running': timer_state['running'],
        'time_left': timer_state['time_left'],
        'max_time': timer_state['max_time'],
        'round_name': timer_state['round_name']
    })

@app.route('/api/timer/set', methods=['POST'])
def timer_set():
    data = request.json
    global timer_state
    timer_state['max_time'] = data.get('seconds', 15)
    if not timer_state['running']:
        timer_state['time_left'] = timer_state['max_time']
        timer_state['start_time'] = None
    return jsonify(timer_state)

# ---------- Reset DB (protected, no shell needed) ----------
RESET_TOKEN = os.environ.get('RESET_TOKEN', 'megatek2024')

@app.route('/reset-db')
def reset_database():
    token = request.args.get('token')
    if token != RESET_TOKEN:
        return "Unauthorized – provide ?token=YOUR_TOKEN", 401

    db.drop_all()
    db.create_all()
    init_db()
    return "Database reset successfully! New school names are applied."

# ---------- Init DB ----------
def init_db():
    if School.query.count() == 0:
        # 14 SCHOOLS (updated list)
        school_names = [
            "Methodist Primary School, Gberigbe",
            "Ayangbure Primary School, Ikorodu",
            "Salvation Army Pry. School, Ikorodu",
            "Temidire Primary School Ikorodu",
            "Oga Primary School, Ikorodu",
            "Anglican Primary School, Ikorodu",
            "Aga Primary School, Ikorodu",
            "J. I. Primary School, Ikorodu",
            "Muslim Primary School, Ikorodu",
            "Ijomu Muslim Primary School, Ikorodu",
            "Community Primary School, Mowo-Nla",
            "African Bethel Pry. School, Ikorodu",
            "Etunrenren Primary School, Ikorodu",
            "Holy Trinity Primary School, Ikorodu"
        ]
        for name in school_names:
            db.session.add(School(name=name))
        db.session.commit()

        # ROUNDS: 1-5 for R1, 6-10 for R2, 11-14 for R3
        rounds_config = [
            ("Round 1", [1,2,3,4,5]),
            ("Round 2", [6,7,8,9,10]),
            ("Round 3", [11,12,13,14]),
            ("Round 4 (Finals)", []),
            ("Round 5 (Finals)", []),
            ("Tiebreaker", [])
        ]
        for name, ids in rounds_config:
            db.session.add(Round(name=name, school_ids=ids))
        db.session.commit()

# ---- Runs on app startup ----
with app.app_context():
    db.create_all()
    init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)