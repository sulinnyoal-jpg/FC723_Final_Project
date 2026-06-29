# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 14:20:37 2026

@author: sulin
"""

#menu option
"""
def menu():
    menu_functionalities = ("1.Check availability of seat/n"
                            "2.Book a seat/n"
                            "3.Free a seat/n"
                            "4.Show booking status"
                            "5.Exit Program")
    return menu_functionalities
"""

seating_check = {
    '1A': 'F', '2A': 'F', '3A': 'F', '4A': 'F', '77A': 'F', '78A': 'F', '79A': 'F', '80A': 'F', 
    '1B': 'F', '2B': 'F', '3B': 'F', '4B': 'F', '77B': 'F', '78B': 'F', '79B': 'F', '80B': 'F', 
    '1C': 'F', '2C': 'F', '3C': 'F', '4C': 'F', '77C': 'F', '78C': 'F', '79C': 'F', '80C': 'F', 
    '1D': 'F', '2D': 'F', '3D': 'F', '4D': 'F', '79D': 'F', '80D': 'F', 
    '1E': 'F', '2E': 'F', '3E': 'F', '4E': 'F', '79E': 'F', '80E': 'F', 
    '1F': 'F', '2F': 'F', '3F': 'F', '4F': 'F', '79F': 'F', '80F': 'F'
}

#check available
free_seat = False
book_seat = input("Enter the seat you want:") 
for seat , status in seating_check.items():
    if seat == book_seat and status == "F":
        free_seat = True

#book a seat
if free_seat == True:
    confirm_seat = input("Do you want to book this seat (Y/N)")
    if confirm_seat == "Y":
        seating_check[book_seat] = "R"

#free a seat
if free_seat == False:
    confirm_cancellation = input("Do you want to cancel this booking (Y/N)")
    if confirm_cancellation == "Y":
        seating_check[book_seat] = "F"
        print("Booking cancelled")
print("Booking has not been cancelled")

#show booking status
if book_seat in seating_check.keys():
    print(seating_check[book_seat])