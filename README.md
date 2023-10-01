# Overview

The purpose of this project is to be an exploration of Mongo DB and interacting with it using Python.

I used VS Code as my editor and the Python language. I used pymongo to connect to a cloud database and tkinter to make the UI. The basic functionality of the program is that you can store records of radio stations in the database. The interface allows you to search for them and then modify or delete them. You can also use the map display to pin a location and save it.

My purpose for writing this software is to familiarize myself with MongoDB and using a library to do so. MongoDB queries are significanly different that a typical SQL query.

[Software Demo Video](https://youtu.be/m91MxceOKH4)

# Cloud Database

This project connects to an Atlas MongoDB.

The database is relatively simple. There are two collections (tables), frequencies and users. Each collection has documents to store information about radio stations and user credientials.

# Development Environment

I use VS Code on a Mac as my development platform.

I used Python with the PyMongo and tkinter libraries to create this application.

# Useful Websites


- [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/index.html)
- [MongoDB Resources](https://www.mongodb.com/docs/drivers/pymongo/)

# Future Work

This project still has a way to go before it's complete. A few items I need to address are:

- Logging in is still less than ideal.  Destroying the TopLevel widget causes complications that I haven't figured out.
- I need to be able to click on a queries record and have to smap widget center on it. This shouldn't be too hard.
