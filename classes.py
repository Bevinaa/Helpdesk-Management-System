from abc import ABC,abstractmethod

import os

import pickle

from datetime import datetime  

def save_ticket_data(ticket_data):
    with open('ticket_data.pkl', 'wb') as file:
        pickle.dump(ticket_data, file)

def load_ticket_data():
    with open('ticket_data.pkl', 'rb') as file:
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

class Observer:
    def update(self):
        pass

class TicketComponent(ABC):
    @abstractmethod
    def get_info(self):
        pass

class BasicTicket(TicketComponent):
    def __init__(self, id, dept, status, summary):
        self.id = id
        self.department = dept
        self.status = status
        self.summary = summary

    def get_info(self):
        return f"Ticket ID: {self.id}, Department: {self.department}, Status: {self.status}, Summary: {self.summary}"

class TicketDecorator(TicketComponent):
    def __init__(self, ticket):
        self._ticket = ticket

    def get_info(self):
        return self._ticket.get_info()

class AdditionalInfoDecorator(TicketDecorator):
    def __init__(self, ticket, additional_info):
        super().__init__(ticket)
        self.additional_info = additional_info

    def get_info(self):
        return f"{super().get_info()}, Additional Info: {self.additional_info}"

class TicketStatus(ABC):
    @abstractmethod
    def process(self):
        pass

class OpenStatus(TicketStatus):
    def __init__(self):
        self.status = "Open"
    
    def get_status(self):
        return self.status
    
    def process(self):
        return "Ticket is open. Assigning an engineer..."

class AssignedStatus(TicketStatus):
    def __init__(self):
        self.status = "Assigned"
    
    def get_status(self):
        return self.status
    
    def process(self):
        return "Ticket is assigned. Performing the service..."

class ClosedStatus(TicketStatus):
    def __init__(self):
        self.status = "Closed"
    
    def get_status(self):
        return self.status
    
    def process(self):
        return "Ticket is closed. No further processing..."

class Ticket:
    ticket_id = 0

    def __init__(self, service, o_date, location, client, time, summary, status, engg=None, c_date=None):
        Ticket.ticket_id += 1
        self.id = Ticket.ticket_id
        self.department = service
        self.open_date = o_date
        self.location = location
        self.client = client
        self.preferred_time = time
        self.status = OpenStatus()
        self.summary = summary
        self.assigned_engineer = engg
        self.completion_date = c_date
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)
        self.notify_observers()

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def assign_engineer(self, engineer):
        self.assigned_engineer = engineer

    def get_status(self):
        return self.status.get_status()

    def set_status(self, status):
        if status == "Open":
            self.status = OpenStatus()
        elif status == "Assigned":
            self.status = AssignedStatus()
        elif status == "Closed":
            self.status = ClosedStatus()
        else:
            raise ValueError("Invalid status") 

    def process(self):
        self.status.process()

class TicketFactory:
    @staticmethod
    def create_ticket(service, o_date, location, client, time, summary):
        status = OpenStatus()
        if service == "Network":
            return NetworkTicket(service, o_date, location, client, time, summary, status)
        elif service == "Electrical":
            return ElectricalTicket(service, o_date, location, client, time, summary, status)
        elif service == "Internet/Ethernet":
            return InternetEthernetTicket(service, o_date, location, client, time, summary, status)
        elif service == "Wifi/LAN":
            return WifiLANTicket(service, o_date, location, client, time, summary, status)
        elif service == "Facilities":
            return FacilitiesTicket(service, o_date, location, client, time, summary, status)
        else:
            return False


class NetworkTicket(Ticket, AdditionalInfoDecorator):
    def __init__(self, service, o_date, location, client, time, summary, status):
        Ticket.__init__(self, service, o_date, location, client, time, summary, status)
        AdditionalInfoDecorator.__init__(self, self, [self.location, self.preferred_time, self.client, self.open_date])

    def check_status(self):
        return f"Checking status for Ticket ID {self.id}..."


class ElectricalTicket(Ticket, AdditionalInfoDecorator):
    def __init__(self, service, o_date, location, client, time, summary, status):
        Ticket.__init__(self, service, o_date, location, client, time, summary, status)
        AdditionalInfoDecorator.__init__(self, self, [self.location, self.preferred_time, self.client, self.open_date])

    def check_status(self):
        return f"Checking status for Ticket ID {self.id}..."


class InternetEthernetTicket(Ticket, AdditionalInfoDecorator):
    def __init__(self, service, o_date, location, client, time, summary, status):
        Ticket.__init__(self, service, o_date, location, client, time, summary, status)
        AdditionalInfoDecorator.__init__(self, self, [self.location, self.preferred_time, self.client, self.open_date])

    def check_status(self):
        return f"Checking status for Ticket ID {self.id}..."


class WifiLANTicket(Ticket, AdditionalInfoDecorator):
    def __init__(self, service, o_date, location, client, time, summary, status):
        Ticket.__init__(self, service, o_date, location, client, time, summary, status)
        AdditionalInfoDecorator.__init__(self, self, [self.location, self.preferred_time, self.client, self.open_date])

    def check_status(self):
        print(f"Checking status for Ticket ID {self.id}...")


class FacilitiesTicket(Ticket, AdditionalInfoDecorator):
    def __init__(self, service, o_date, location, client, time, summary, status):
        Ticket.__init__(self, service, o_date, location, client, time, summary, status)
        AdditionalInfoDecorator.__init__(self, self, [self.location, self.preferred_time, self.client, self.open_date])

    def check_status(self):
        return f"Checking status for Ticket ID {self.id}..."

class Client(Observer):
    client_id = 0
    def __init__(self,name,dept,hostel,room_no,hostel_no,mobile_no,password):
        Client.client_id += 1
        self.id = Client.client_id
        self.name = name
        self.dept = dept
        self.hostel = hostel
        self.room_no = room_no
        self.hostel_no = hostel_no
        self.mobile_no = mobile_no
        self.password = password

    def update(self, ticket):
        print(f"Client {self.name}: Received update for Ticket ID {ticket.id}. Status: {ticket.status}")

    def raise_ticket(self,ticket_service, ticket_date, ticket_location, ticket_client, ticket_time, ticket_summary):
        new_ticket = TicketFactory.create_ticket(
            ticket_service, ticket_date, ticket_location, ticket_client, ticket_time, ticket_summary
        )
        new_ticket.attach(self)
        return new_ticket
          
class Admin:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Admin, cls).__new__(cls)
            cls._instance.id = 1234
            cls._instance.password = "1234"
            cls._instance.all_tickets = []
            cls._instance.engineers = []
            cls._instance.reports_generated = []
        return cls._instance
    
    def assign_ticket(self, ticket,engineer):
        ticket.set_status("Assigned")
        update_ticket_in_data(ticket)
        self.save_assigned_tickets(ticket,engineer)

    def save_assigned_tickets(self,ticket,engineer):
        engineer_assigned_tickets_file = f'engineer_assigned_tickets_{engineer.id}.pkl'
        
        if not os.path.exists(engineer_assigned_tickets_file):
            with open(engineer_assigned_tickets_file, 'wb') as file:
                pickle.dump([], file)

        with open(engineer_assigned_tickets_file, 'rb') as file:
            assigned_tickets = pickle.load(file)

        assigned_tickets.append({
            'ticket_id': ticket.id,
            'status': ticket.status.get_status(),
            'assignment_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        with open(engineer_assigned_tickets_file, 'wb') as file:
            pickle.dump(assigned_tickets, file)

class ServiceEngineer(Observer):
    last_assigned_id = 0

    def __init__(self, name, dept):
        ServiceEngineer.last_assigned_id += 1
        self.id = ServiceEngineer.last_assigned_id
        self.name = name
        self.dept = dept
        self.assigned_tickets = []


    def close_ticket(self,ticket):
        ticket.set_status("Closed")
        update_ticket_in_data(ticket)

    def update(self, ticket):
        return f"Engineer {self.name}: Received update for Ticket ID {ticket.id}. Status: {ticket.status}"