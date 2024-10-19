README

**Getting Started**
Welcome to the Repair Ticket Management System! To begin using the system, follow these steps:

Register: First, you need to create an account by registering in the system.
Login: After registering, you can log in with your credentials to access the dashboard and other sections.
System Overview
The system consists of several key sections: Dashboard, Users, Clients, Items, and Repair Orders. Each section serves a specific purpose in managing repair tickets and related data.

Dashboard
The Dashboard provides an overview of statistics related to repair tickets. You can quickly see the status of tickets, such as how many are pending, in progress, or completed. It's the central hub for tracking repair activity.

Users
In the Users section, you can manage user accounts. The following actions are available:

Activate/Deactivate Users: Enable or disable access for users.
Edit/Delete Users: Update user information or delete accounts.
Change User Role: You can change a user's role to either "Technician" or "Salesperson" from the user edit screen.
Clients
In the Clients section, you can manage client records. The following actions are available:

Add New Client: Create a new client by providing details such as name, email, phone, and address.
Edit/Delete Client: Update or remove existing client records.
Items (Brands and Models)
In the Items section, you can manage the brands and models of equipment. The following actions are available:

Add New Brand: Create new brands that will be associated with models.
Add New Model: Add models under specific brands.
Edit/Delete Models and Brands: Manage existing models and brands.
Repair Orders (Tickets)
This is the most complex and important section of the system. Repair orders allow you to manage repair tickets, assign technicians, and track the status of repairs. Here's how the process works:

Create a Repair Ticket:

When creating a ticket, the system first asks you to either select an existing client or add a new client.
You can search for an existing client using their RIF, email address, or phone number.
If a match is found in the database, the process continues; if not, you'll be redirected to a form to create a new client.
When adding a new client, you'll be required to provide details like name, RIF, email, and phone number. The system has several validation rules:
The RIF must start with either J, B, or G and be followed by at least 7 digits.
The email must be in a valid format.
Select Brand:

After selecting the client, the next step is to select the brand of the equipment being repaired.
Select or Add Model:

In the third step, you'll select the model of the equipment.
If the model doesn't exist, you can add a new one. When adding a new model, you can also add a new brand if needed.
Add Equipment Details:

After selecting the model, you'll be prompted to provide the serial number of the equipment and a description of the problem.
Ticket Creation:

Once all the information is provided, the ticket will be created, and you'll be able to view the ticket details.
Assigning a Technician
Once a ticket is created, an admin can assign a technician to handle the repair:

Go to the Repair Orders section.
Find the ticket and click the Assign Technician button.
Choose a technician and update the status of the repair (e.g., Pending, In Progress, Completed).
Save the assignment, and the technician will now be responsible for the repair.
Validation and Error Handling
The system includes several validation checks to ensure data accuracy, such as:

RIF validation: The RIF must follow specific patterns depending on the type of client (e.g., J, V, or G followed by numbers).
Email validation: The email field must contain a valid email format.
