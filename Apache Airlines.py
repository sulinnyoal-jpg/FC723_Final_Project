# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:20:37 2026

@author: sulin
"""
import datetime
import random
import sqlite3
import string 

class BookingSystem:
    def __init__(self, days_until_flight = 30):
        #Set up the seating chart when a BookingSystem is created
        self.seating_chart = {
            '1A': 'F', '2A': 'F', '3A': 'F', '4A': 'F', '77A': 'F', '78A': 'F', '79A': 'F', '80A': 'F',
            '1B': 'F', '2B': 'F', '3B': 'F', '4B': 'F', '77B': 'F', '78B': 'F', '79B': 'F', '80B': 'F',
            '1C': 'F', '2C': 'F', '3C': 'F', '4C': 'F', '77C': 'F', '78C': 'F', '79C': 'F', '80C': 'F',
            '1D': 'F', '2D': 'F', '3D': 'F', '4D': 'F', '79D': 'F', '80D': 'F',
            '1E': 'F', '2E': 'F', '3E': 'F', '4E': 'F', '79E': 'F', '80E': 'F',
            '1F': 'F', '2F': 'F', '3F': 'F', '4F': 'F', '79F': 'F', '80F': 'F'
        }
        #Hold date of departure from user
        self.flight_date = datetime.date.today() + datetime.timedelta(days=days_until_flight)
        #Create a connection to an SQLite Database file
        self.conn = sqlite3.connect("airline_bookings.db")
        self.init_database()
        self.sync_seating_chart_from_db()
    
    def init_database(self):
        #Create relational database to store customer data
        cursor = self.conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS passenger_database(
                           seat_number TEXT PRIMARY KEY,
                           booking_reference TEXT UNIQUE NOT NULL,
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL,
                           passport_number TEXT NOT NULL,
                           has_insurance INTEGER NOT NULL,
                           booking_date TEXT NOT NULL
                           )
                       """)
        self.conn.commit()
        
    def sync_seating_chart_from_db(self):
        #Ensure that seating chart mirrors the database entries when initialized
        cursor = self.conn.cursor()
        #Get seat number and booking reference from passanger's records
        cursor.execute("SELECT seat_number, booking_reference FROM passenger_database")
        for seat, reference in cursor.fetchall():
            #Check is seat exists and assign reference
            if seat in self.seating_chart:
                self.seating_chart[seat] = reference
                
    def menu(self):
        #Return the text for the main menu as one string
        menu_functionalities = ("-------------Menu-------------\n"
                                "1.Check availability of seat\n"
                                "2.Book a seat\n"
                                "3.Free a seat\n"
                                "4.Show booking status\n"
                                "5.Exit Program\n"
                                "-------------------------------")
        return menu_functionalities
    
    #Generating reference algorithm
    def generate_booking_reference(self):
        #define 36 possible characters (All uppercacse letters, 0-9)
        char_set = string.ascii_uppercase + string.digits
        cursor = self.conn.cursor()
        
        while True:
            #randomly select 8 characters 
            canidate_ref = "".join(random.choice(char_set) for char in range(8))
            
            #check database table records for uniqueness
            #if there is no same existing reference, None will be returned
            cursor.execute("SELECT 1 FROM passenger_database WHERE booking_reference =?",(canidate_ref,))
            
            #return reference if no duplicate is found
            if cursor.fetchone() is None:
                return canidate_ref

    def is_valid_seat(self, seat):
        #Check whether a seat number actually exists in the seating chart
        return seat in self.seating_chart

    def get_seat_input(self, prompt):
        #Return a formatted version of 
        return input(prompt).strip().upper()

    def check_availability(self):
        #Look up a seat and tell the user to check 
        #its availability and whether it exists
        seat = self.get_seat_input("Enter the seat you want: ")

        # .get() returns None automatically if the seat isn't a key in
        # the dictionary, so this doubles as our "does it exist?" check.
        status = self.seating_chart.get(seat)

        if status is None:
            print("The seat does not exist")
        elif status == "F":
            print(f"Seat {seat} is free.")
        else:
            print(f"Seat {seat} is already booked under reference:{status}.")

    def book_a_seat(self):
        #Ask for a seat number.
        seat = self.get_seat_input("Enter the seat you want to book: ")
        
        #Check for seat existance and availability 
        if not self.is_valid_seat(seat):
            print("The seat does not exist")
            return

        if self.seating_chart[seat] != "F":
            print(f"Seat {seat} is not available.")
            return
        
        #Ask user for their information
        print("\n----Passenger Details----")
        first_name = input("First Name:").strip()
        last_name = input("Last Name:").strip()
        passport_num = input("Passport Number:").strip()
        #Ask whether the passenger is taking out the travel insurance
        has_insurance = input("Add travel insurance? (Y/N):").strip().upper() == "Y"

        #Book a seat, after checking it exists and is currently free.
        confirm_seat = input(f"Do you want to book seat {seat}? (Y/N): ").strip().upper()
        if confirm_seat == "Y":
            #generate unique reference code
            unique_ref = self.generate_booking_reference()
            # Only update the dictionary after the user has confirmed
            self.seating_chart[seat] = unique_ref
            
            #save passanger details to database table
            cursor = self.conn.cursor()
            cursor.execute("""
                           INSERT INTO passenger_database (seat_number, booking_reference, first_name, last_name, passport_number, has_insurance, booking_date)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           """,
                           (seat, unique_ref, first_name, last_name, passport_num, 1 if has_insurance else 0, str(datetime.date.today()))
            )
            self.conn.commit()
            
            print(f"Seat {seat} booked.The reference is:{unique_ref}")
        else:
            print("Booking not confirmed.")
    
    #Check whether the reason for refund is valid 
    def check_valid_refund(self,seat,reason):
        #Valid return if cancellation initiated by airline
        if reason == "airline":
            return True 
        
        #lookup database for conditional checks
        cursor = self.conn.cursor()
        cursor.execute("SELECT has_insurance FROM passenger_database WHERE seat_number = ?",
                       (seat,))
        row = cursor.fetchone()
        #check if passanger seat exists
        if row is not None:
            #check if passsanger has insurance
            if row[0] == 1:
                has_insurance = True
            else:
                has_insurance = False
        else:
            has_insurance = False
            
        #valid refund if cancellation unexpected for insured travellers
        if reason == "weather":
            return has_insurance
        
        #checks for a week's notice
        if reason == "customer":
            #Calculate gap between day of departure and cancellation
            days_left = (self.flight_date - datetime.date.today()).days
            return days_left >= 7
        
        return False

    def cancel_booking(self):
        #Ask for seat number
        seat = self.get_seat_input("Enter the seat you want to free: ")
        
        #Check whether seat exists,and it's booked
        if not self.is_valid_seat(seat):
            print("The seat does not exist")
            return

        if self.seating_chart[seat] == "F":
            print("Seat is currently not booked.")
            return

        confirm_cancellation = input(f"Do you want to cancel this booking for seat {seat}? (Y/N): ").strip().upper()
        if confirm_cancellation != "Y":
            print("Booking has not been cancelled")
            return
        
        #ask reason for cancellation
        print("Reason for cancellation:")
        print("1. Cancelled by customer")
        print("2. Cancelled by airline")
        print("3. Unexpected cancellation(weather)")
        reason_choice = input("Choose 1-3: ").strip()
        
        #link key to values to check for valid reason
        reason_map = {"1": "customer", "2": "airline", "3": "weather"}
        reason = reason_map.get(reason_choice)
        
        if reason is None:
            print("Invalid reason selected.Cancellation invalid.")
            return
        
        #Issue refund
        refunded = self.check_valid_refund(seat,reason)
        
        #Remove booking details from database table
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM passenger_database WHERE seat_number = ?",(seat,))
        self.conn.commit()
        
        #Change status of seat
        self.seating_chart[seat] = "F"
        
        print("Booking cancelled")
        if refunded:
            print("Refund approved.")
        else:
            print("Refund denied.")

    def show_booking_status(self):
        # Each list contains only the seat numbers 
        #where the status matches what we're looking for.
        booked_seats = [seat for seat, status in self.seating_chart.items() if status != "F"]
        free_seats = [seat for seat, status in self.seating_chart.items() if status == "F"]

        print("\n---- Seating Chart Status Summary ----")
        print("Total seats:", len(self.seating_chart))
        print(f"Booked: {len(booked_seats)}")
        print(f"Remaining: {len(free_seats)}")
        print(f"Booked seats: {booked_seats}")
        print(f"Available seats: {free_seats}")

        # Let the user find information of one specific seat 
        check_specific_seat = input("Press 'Y' to look up a specific seat: ")
        if check_specific_seat == "Y":
            seat = self.get_seat_input("Enter seat number: ")
            if self.is_valid_seat(seat):
                print(f"Seat {seat} reference: {self.seating_chart[seat]}")
                
                #gets information from database table
                cursor = self.conn.cursor()
                cursor.execute("SELECT first_name, last_name, passport_number FROM passenger_database WHERE seat_number = ?",(seat,),)
                row = cursor.fetchone()
                
                if row:
                    print(f"Passenger: {row[0]} {row[1]} | Passport: {row[2]}")
                else:
                    print("Seat is empty.")
            else:
                print("Invalid seat name")
    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    system = BookingSystem()

    # Main program loop: keep showing the menu and handling the user's
    # choice until they choose option 5 to exit.
    while True:
        print(system.menu())
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            system.check_availability()
        elif choice == "2":
            system.book_a_seat()
        elif choice == "3":
            system.cancel_booking()
        elif choice == "4":
            system.show_booking_status()
        elif choice == "5":
            system.close_connection()
            print("Program Exited")
            break  # exits the while loop, ending the program
        else:
            print("Invalid Option. Choose from 1-5.")