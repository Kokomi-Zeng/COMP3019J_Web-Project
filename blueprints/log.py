from flask import Blueprint, request, jsonify
from models import User
import logging
import os

bp = Blueprint('log', __name__, url_prefix='/log')
def setup_logging():
    # create the directory for logging
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    log_file_path = os.path.join(root_dir, 'logs')

    os.makedirs(log_file_path, exist_ok=True)

    # create a logger
    logger = logging.getLogger('my_app_logger')
    logger.setLevel(logging.INFO)

    # create a file handler to write the log file
    log_file_path = os.path.join(log_file_path, 'app.log')
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(phone)s  - %(log_content)s')
    file_handler.setFormatter(formatter)

    # add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

@bp.route("/get_log", methods=["GET"])
def get_log():
    phone = request.args.get('phone')
    log_type = request.args.get('type')
    user = User.query.filter_by(phone=phone).first()

    if user and user.user_type == '2':
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        log_file_path = os.path.join(root_dir, 'logs', 'app.log')

        filtered_logs = []
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                # filter by log type
                if log_type in line or not log_type:
                    filtered_logs.append(line.strip())

        # get the last 200 log records after filtering
        logs = filtered_logs[-200:]

        # log example: "2023-12-05 09:55:17,012 - WARNING - qwetwqt - Incorrect phone or password."
        # log_time, log_type, phone, log_content
        logs = [log.split(' - ') for log in logs]
        logs = [{'log_time': log[0], 'log_type': log[1], 'phone': log[2], 'log_content': log[3]} for log in logs]

        return jsonify(logs)

    return jsonify({"success": False, "message": "Unauthorized access"})
