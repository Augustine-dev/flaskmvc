import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, delete_user, get_all_users_json, get_all_users, initialize,
                             log_hours, confirm_hours, get_leaderboard, get_student_accolades )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
'''
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')
'''

#New create user function
@user_cli.command("create", help="Create a user with user_type")
@click.argument("username")
@click.argument("password")
@click.argument("user_type", default="student")
def create_user_command(username, password, user_type):
    user = create_user(username, password, user_type)
    print(f'{user_type.capitalize()}{user.username} created!')

#Delete user function
@user_cli.command("delete", help="Delete a user by ID")
@click.argument("user_id", type=int)
def delete_user_command(user_id):
    success = delete_user(user_id)
    if success:
        print(f'User {user_id} deleted!')
    else:
        print("User not found.")

@user_cli.command
# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

#Group for student commands
student_cli = AppGroup('student', help='Student incentive commands')

@student_cli.command("acolades", help="View accolades for student")
@click.argument("student_id", type = int)
def view_accolades(student_id):
    print(get_student_accolades(student_id))

@student_cli.command("leaderboard", help="View leaderboard")
def leaderboard():
    print(get_leaderboard())

app.cli.add_command(student_cli)

#Group for staff commands
staff_cli = AppGroup('staff', help='Staff incentive commands')

@staff_cli.command("log", help="Log hours for student")
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("hours", type=int)
def log_command(student_id, staff_id, hours):
    log = log_hours(student_id, staff_id, hours)
    print(f"Logged {hours} hours for student {student_id}, log id={log.id}")

@staff_cli.command("confirm", help="Confirm or reject student hours")
@click.argument("log_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("confirm", type=bool)
def confirm_command(log_id, staff_id, confirm):
    log = log_hours(log_id, staff_id, confirm)
    if log:
        print(f"Log {log.id} confirmed={log.confirmed}")
    else:
        print("Invalid log or staff ID")

app.cli.add_command(staff_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)