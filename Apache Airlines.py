# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:20:37 2026

@author: sulin
"""
class BookingSystem:
    def __init__(self):
        #Set up the seating chart when a BookingSystem is created
        self.seating_chart = {
            '1A': 'F', '2A': 'F', '3A': 'F', '4A': 'F', '77A': 'F', '78A': 'F', '79A': 'F', '80A': 'F',
            '1B': 'F', '2B': 'F', '3B': 'F', '4B': 'F', '77B': 'F', '78B': 'F', '79B': 'F', '80B': 'F',
            '1C': 'F', '2C': 'F', '3C': 'F', '4C': 'F', '77C': 'F', '78C': 'F', '79C': 'F', '80C': 'F',
            '1D': 'F', '2D': 'F', '3D': 'F', '4D': 'F', '79D': 'F', '80D': 'F',
            '1E': 'F', '2E': 'F', '3E': 'F', '4E': 'F', '79E': 'F', '80E': 'F',
            '1F': 'F', '2F': 'F', '3F': 'F', '4F': 'F', '79F': 'F', '80F': 'F'
        }

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
            print(f"Seat {seat} is already booked.")

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

        #Book a seat, after checking it exists and is currently free.
        confirm_seat = input(f"Do you want to book seat {seat}? (Y/N): ")
        if confirm_seat == "Y":
            # Only update the dictionary after the user has confirmed
            self.seating_chart[seat] = "R"
            print(f"Seat {seat} booked.")
        else:
            print("Booking not confirmed.")

    def cancel_booking(self):
        #Ask for seat number
        seat = self.get_seat_input("Enter the seat you want to free: ")
        
        #Check whether seat exists,and it's booked
        if not self.is_valid_seat(seat):
            print("The seat does not exist")
            return

        if self.seating_chart[seat] != "R":
            print("Seat is currently not booked.")
            return

        confirm_cancellation = input(f"Do you want to cancel this booking for seat {seat}? (Y/N): ")
        if confirm_cancellation == "Y":
            #Change status of seat once cancellation is confirmed
            self.seating_chart[seat] = "F"
            print("Booking cancelled")
        else:
            print("Booking has not been cancelled")

    def show_booking_status(self):
        # Each list contains only the seat numbers 
        #where the status matches what we're looking for.
        booked_seats = [seat for seat, status in self.seating_chart.items() if status == "R"]
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
                print(f"Seat {seat} status: {self.seating_chart[seat]}")
            else:
                print("Invalid seat name")


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
            print("Program Exited")
            break  # exits the while loop, ending the program
        else:
            print("Invalid Option. Choose from 1-5.")