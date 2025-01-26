from flask import Blueprint, request, jsonify
import database.user as user
import utils.error.error as error

user_route = Blueprint("user", __name__, url_prefix='/api/user')

def handle_user_request(data, required_fields, user_action):
    error_response, fields = error.validate_and_extract_fields(data, required_fields)
    if error_response:
        return error_response

    result = user_action(fields)
    return result

@user_route.route('/signup', methods=['POST'])
def add_user():
    try:
        data = request.json
        required_fields = ['email', 'name', 'password', 'birth_date', 'phone_address', 'gender', 'job']

        def action(fields):
            result = user.add_user(fields['email'], fields['name'], fields['password'], fields['birth_date'], fields['phone_address'], fields['gender'], fields['job'])
            if not result:
                return jsonify({"msg": "User already exists"}), 400
            return jsonify({"msg": "User Added Successfully"}), 200

        return handle_user_request(data, required_fields, action)

    except Exception as e:
        return error.handle_error(e)

@user_route.route('/signin', methods=['POST'])
def login_user():
    try:
        data = request.json
        required_fields = ['email', 'password']

        def action(fields):
            access_token, refresh_token = user.login_user(fields['email'], fields['password'])
            if not access_token or not refresh_token:
                return jsonify({"msg": "User does not exist"}), 400
            return jsonify({"msg": "User Login Successfully", 'Access_Token': access_token, "Refresh_Token": refresh_token}), 200

        return handle_user_request(data, required_fields, action)

    except Exception as e:
        return error.handle_error(e)

# @user_route.route('/me', methods=['POST'])
# def select_user():
#     try:
#         data = request.json
#         data = request.json
#         required_fields = ['email']

#         def action(fields):
#             access_token, refresh_token = user.login_user(fields['email'], fields['password'])
#             if not access_token or not refresh_token:
#                 return jsonify({"msg": "User does not exist"}), 400
#             return jsonify({"msg": "User Login Successfully", 'Access_Token': access_token, "Refresh_Token": refresh_token}), 200

#         return handle_user_request(data, required_fields, action)

#     except Exception as e:
#         return error.handle_error(e)

@user_route.route('/password', methods=['POST'])
def change_password():
    try:
        data = request.json
        required_fields = ['email', 'current_password', 'new_password', 'confirm_password']

        def action(fields):
            result = user.change_password(fields['email'], fields['current_password'], fields['new_password'], fields['confirm_password'])
            if not result:
                return jsonify({"msg": "Invalid credentials"}), 400
            return jsonify({"msg": "Change to Password Successfully"}), 200

        return handle_user_request(data, required_fields, action)

    except Exception as e:
        return error.handle_error(e)

@user_route.route('/name', methods=['POST'])
def change_name():
    try:
        data = request.json
        required_fields = ['email', 'password', 'name']

        def action(fields):
            result = user.change_name(fields['email'], fields['password'], fields['name'])
            if not result:
                return jsonify({"msg": "Invalid credentials"}), 400
            return jsonify({"msg": "Change to Name Successfully"}), 200

        return handle_user_request(data, required_fields, action)

    except Exception as e:
        return error.handle_error(e)
    
@user_route.route('/gender', methods=['POST'])
def change_gender():
    try:
        data = request.json
        required_fields = ['email', 'password', 'gender']

        def action(fields):
            result = user.change_gender(fields['email'], fields['password'], fields['gender'])
            if not result:
                return jsonify({"msg": "Invalid credentials"}), 400
            return jsonify({"msg": "Change to Gender Successfully"}), 200

        return handle_user_request(data, required_fields, action)

    except Exception as e:
        return error.handle_error(e)

@user_route.route('/job', methods=['POST'])
def change_job():
    try:
        data = request.json
        required_fields = ['email', 'password', 'job']

        def action(fields):
            result = user.change_job(fields['email'], fields['password'], fields['job'])
            if not result:
                return jsonify({"msg": "Invalid credentials"}), 400
            return jsonify({"msg": "Change to Job Successfully"}), 200

        return handle_user_request(data, required_fields, action)

    except Exception as e:
        return error.handle_error(e)