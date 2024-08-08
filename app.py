from flask import Flask, render_template, request, redirect, url_for, flash,session
import pickle
import os

from classes import TicketFactory,Ticket,Client,Observer,Admin,ServiceEngineer

from classes import BasicTicket,AdditionalInfoDecorator

app = Flask(__name__)

app.secret_key = '1234'

USER_DATA_FILE = 'user_data.pkl'

CLIENT_DATA_FILE = 'client_data.pkl'

TICKET_DATA_FILE = 'ticket_data.pkl'

ADMIN_DATA_FILE = 'admin_data.pkl'


if not os.path.exists(ADMIN_DATA_FILE):
    with open(ADMIN_DATA_FILE, 'wb') as file:
        pickle.dump([], file)

if not os.path.exists(TICKET_DATA_FILE):
    with open(TICKET_DATA_FILE, 'wb') as file:
        pickle.dump([], file)

if not os.path.exists(CLIENT_DATA_FILE):
    with open(CLIENT_DATA_FILE, 'wb') as file:
        pickle.dump([], file)

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'wb') as file:
        pickle.dump([], file)

def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as file:
        pickle.dump(user_data, file)

def load_user_data():
    with open(USER_DATA_FILE, 'rb') as file:
        return pickle.load(file)
        
def save_client_data(client_data):
    with open(CLIENT_DATA_FILE, 'wb') as file:
        pickle.dump(client_data, file)

def load_client_data():
    with open(CLIENT_DATA_FILE, 'rb') as file:
        return pickle.load(file)

def save_ticket_data(ticket_data):
    with open(TICKET_DATA_FILE, 'wb') as file:
        pickle.dump(ticket_data, file)

def load_ticket_data():
    with open(TICKET_DATA_FILE, 'rb') as file:
        return pickle.load(file)
    
def get_ticket_by_id(ticket_id):
    ticket_data = load_ticket_data()

    for ticket in ticket_data:
        if str(ticket.id) == str(ticket_id):
            return ticket
    return None

def save_admin_data(admin_data):
    with open(ADMIN_DATA_FILE, 'wb') as file:
        pickle.dump(admin_data, file)

def load_admin_data():
    with open(ADMIN_DATA_FILE, 'rb') as file:
        return pickle.load(file)
    
def update_ticket_in_data(updated_ticket):
    ticket_data = load_ticket_data()

    index_to_update = None
    for i, ticket in enumerate(ticket_data):
        if ticket.id == updated_ticket.id:
            index_to_update = i
            break

    if index_to_update is not None:
        ticket_data[index_to_update] = updated_ticket

        save_ticket_data(ticket_data)
    else:
        print(f"Ticket with ID {updated_ticket.id} not found.")

def update_engineer_assigned_tickets(engineer_id, updated_tickets):
    engineer_assigned_tickets_file = f'engineer_assigned_tickets_{engineer_id}.pkl'

    with open(engineer_assigned_tickets_file, 'wb') as file:
        pickle.dump(updated_tickets, file)

@app.route('/')
def index():
    return render_template('common_login.html')

@app.route('/client')
def client_index():
    return render_template('client_index.html')

@app.route('/client_signup', methods=['GET', 'POST'])
def client_signup():
    if request.method == 'POST':
        client_name = request.form['name']
        client_dept = request.form['dept']
        client_hostel = request.form['hostel']
        client_room_no = request.form['room_no']
        client_hostel_no = request.form['hostel_no']
        client_mobile_no = request.form['mobile_no']
        client_password = request.form['password']

        client_data = load_client_data()
        new_client = Client(client_name, client_dept, client_hostel, client_room_no, client_hostel_no, client_mobile_no, client_password)
        client_data.append(new_client)
        save_client_data(client_data)

        flash(f'Successfully signed up! Your ID is: {new_client.id}', 'success')
        return redirect(url_for('client_login'))

    return render_template('client_signup.html')

@app.route('/client_login', methods=['GET', 'POST'])
def client_login():
    if request.method == 'POST':
        client_id = request.form['id']
        client_password = request.form['password']

        client_data = load_client_data()
        for client in client_data:
            if str(client.id) == client_id and client.password == client_password:
                session['client_id'] = client_id
                flash(f'Welcome, {client.name}!', 'success')
                return redirect(url_for('client_dashboard'))

        flash('Invalid ID or password. Please try again.', 'error')

    return render_template('client_login.html')

@app.route('/client_dashboard')
def client_dashboard():
    return render_template('client_dashboard.html', tickets=load_ticket_data())

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        ticket_service = request.form['service']
        ticket_date = request.form['o_date']
        ticket_location = request.form['location']
        ticket_client = request.form['client']
        ticket_time = request.form['time']
        ticket_summary = request.form['summary']

        client_id = session['client_id']
        client_data = load_client_data()
        client_log = None
        for client in client_data:
            if str(client.id) == client_id:
                client_log = client
                break
        new_ticket = client_log.raise_ticket(ticket_service, ticket_date, ticket_location, ticket_client, ticket_time, ticket_summary)

        if new_ticket:
            ticket_data = load_ticket_data()
            ticket_data.append(new_ticket)
            save_ticket_data(ticket_data)   

            flash('Ticket created successfully!', 'success')
            return redirect(url_for('client_dashboard'))
        else:
            flash('Invalid service type.', 'error')

    return render_template('create_ticket.html')

@app.route('/view_tickets')
def view_tickets():
    tickets = load_ticket_data()

    basic_tickets = [BasicTicket(ticket.id, ticket.department,ticket.status, ticket.summary) for ticket in tickets]

    return render_template('view_tickets.html', basic_tickets=basic_tickets)

@app.route('/view_additional_info/<ticket_id>')
def view_additional_info(ticket_id):
    ticket = get_ticket_by_id(ticket_id)

    if ticket:
        basic_ticket = BasicTicket(ticket.id, ticket.department, ticket.status, ticket.summary)
        if not isinstance(ticket, AdditionalInfoDecorator):
            decorated_ticket = AdditionalInfoDecorator(basic_ticket, ticket.additional_info)
        else:
            decorated_ticket = basic_ticket

        return render_template('view_additional_info.html', ticket=decorated_ticket)

    flash('Ticket not found.', 'error')
    return redirect(url_for('client_dashboard'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    admin = Admin()

    admin_data = load_admin_data()

    if admin not in admin_data:
        admin_data.append(admin)
        save_admin_data(admin_data)

    if request.method == 'POST':
        admin_id = request.form['id']
        admin_password = request.form['password']

        admin_data = load_admin_data()

        for admin in admin_data:
            if admin.id == int(admin_id) and admin.password == admin_password:
                session['admin_id'] = admin_id
                flash(f'Welcome, Admin!', 'success')
                return redirect(url_for('admin_dashboard'))

        flash('Invalid ID or password. Please try again.', 'error')

    return render_template('admin_login.html')
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Admin not logged in.', 'error')
        return redirect(url_for('admin_login'))

    return render_template('admin_dashboard.html')

@app.route('/admin_tickets')
def admin_tickets():
    tickets = load_ticket_data()
    return render_template('admin_tickets.html', tickets=tickets)

@app.route('/admin_engineers')
def admin_engineers():
    engineers = load_user_data()
    return render_template('admin_engineers.html', engineers=engineers)

@app.route('/assign_tickets', methods=['GET', 'POST'])
def assign_tickets():
    tickets = load_ticket_data()
    engineers = load_user_data()
    
    if request.method == 'POST':
        selected_ticket_id = request.form['ticket_id']
        selected_engineer_id = request.form['engineer_id']
        
        ticket = next((t for t in tickets if t.id == int(selected_ticket_id)), None)
        engineer = next((e for e in engineers if e.id == int(selected_engineer_id)), None)
        print(ticket,engineer)
        
        if ticket and engineer:
            log = Admin()
            log.assign_ticket(ticket, engineer)
            flash('Ticket assigned successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid ticket or engineer ID.', 'error')

    return render_template('assign_tickets.html', tickets=tickets, engineers=engineers)
@app.route('/engineer')
def engineer_index():
    return render_template('engineer_index.html')

@app.route('/engineer_signup', methods=['GET', 'POST'])
def engineer_signup():
    if request.method == 'POST':
        user_name = request.form['name']
        user_dept = request.form['dept']

        user_data = load_user_data()
        new_engineer = ServiceEngineer(user_name, user_dept)
        user_data.append(new_engineer)
        save_user_data(user_data)

        flash(f'Successfully signed up! Your ID is: {new_engineer.id}', 'success')
        return redirect(url_for('engineer_login'))
    
    return render_template('engineer_signup.html')

@app.route('/engineer_login', methods=['GET', 'POST'])
def engineer_login():
    if request.method == 'POST':
        user_id = request.form['id']

        user_data = load_user_data()
        for user in user_data:
            if user.id == int(user_id):
                session['engineer_id'] = user.id
                return redirect(url_for('engineer_dashboard'))

        return 'User not found. Please check your credentials.'

    return render_template('engineer_login.html')

@app.route('/engineer_dashboard')
def engineer_dashboard():
    engineer_id = session.get('engineer_id')
    
    if engineer_id is not None:
        return render_template('engineer_dashboard.html')
    else:
        flash('Engineer not logged in.', 'error')
        return redirect(url_for('engineer_login'))

@app.route('/view_assigned_tickets')
def view_assigned_tickets():
    engineer_id = session.get('engineer_id')
    if engineer_id:
        engineer_assigned_tickets_file = f'engineer_assigned_tickets_{engineer_id}.pkl'
        
        if os.path.exists(engineer_assigned_tickets_file):
            with open(engineer_assigned_tickets_file, 'rb') as file:
                assigned_tickets = pickle.load(file)
                
            return render_template('view_assigned_tickets.html', assigned_tickets=assigned_tickets)
        else:
            flash('No assigned tickets.', 'info')
    else:
        flash('Engineer not logged in.', 'error')
    
    return redirect(url_for('engineer_login'))

@app.route('/close_ticket/<ticket_id>', methods=['POST'])
def close_ticket(ticket_id):
    ticket = get_ticket_by_id(ticket_id)

    if ticket:
        ticket.set_status("Closed")

        update_ticket_in_data(ticket)

        engineer_id = session.get('engineer_id')

        if engineer_id:
            engineer_assigned_tickets_file = f'engineer_assigned_tickets_{engineer_id}.pkl'
            print("engineer")

            if os.path.exists(engineer_assigned_tickets_file):
                with open(engineer_assigned_tickets_file, 'rb') as file:
                    assigned_tickets = pickle.load(file)

                updated_assigned_tickets = [t for t in assigned_tickets if t['ticket_id'] != int(ticket_id)]

                update_engineer_assigned_tickets(engineer_id, updated_assigned_tickets)

        flash(f'Ticket {ticket_id} closed successfully!', 'success')
    else:
        flash('Ticket not found.', 'error')

    return redirect(url_for('engineer_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
    
