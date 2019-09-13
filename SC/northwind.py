"""
Run the whole file in python to get answer from
Part 2-4
"""

import sqlite3

conn = sqlite3.connect('northwind_small (1).sqlite3')
curs = conn.cursor()

# Pylint issues, will come back
print(
    'Table names for northwind',
    curs.execute("""SELECT name FROM sqlite_master
                WHERE type='table' ORDER BY name;""").fetchall(), '\n')


def get_query(query, info_str, curs):
    curs.execute(query)
    print(info_str, curs.fetchall(), '\n')


# What are the ten most expensive items (per unit price) in the db?
# Select product names and order by price limit 10

query = "SELECT ProductName FROM Product ORDER BY UnitPrice DESC LIMIT 10"
get_query(query, 'Ten most expensive items', curs)


# What is the avg age of an employee at time of hiring?

query = "SELECT AVG(HireDate - BirthDate) FROM Employee"
get_query(query, 'Average age of each hiree', curs)


# How does the average age of employee at hire vary by city?

query = """SELECT AVG(HireDate - BirthDate), City FROM Employee
        GROUP BY City"""
get_query(query, 'Average age of each hiree by city', curs)

# Part 3 #

# What are the ten most expensive items AND their suppliers?

query = """SELECT ProductName, CompanyName FROM Product 
        INNER JOIN Supplier ON SupplierId = Supplier.Id
        ORDER BY UnitPrice DESC LIMIT 10"""
get_query(query, 'Ten most expensive items and Suppliers', curs)


# What is the largest category by number of unique products in it?

query = """SELECT CategoryName FROM Category
        INNER JOIN Product ON Category.Id = CategoryId
        GROUP BY Category.Id ORDER BY COUNT(DISTINCT(Product.Id))
        DESC LIMIT 1"""
get_query(query, 'The largest category by number of unique products', curs)


# Who is the employee with the most territories?

query = """SELECT FirstName, LastName FROM Employee
        INNER JOIN EmployeeTerritory ON
        Employee.Id = EmployeeTerritory.EmployeeId
        GROUP BY Employee.Id ORDEr BY COUNT(DISTINCT(TerritoryId))
        DESC LIMIT 1"""
get_query(query, 'Employee with the most territories', curs)

# Part 4 ###

# What is the type of relationship between the Employee and Territory tables?

print("""Part4.1 ANSWER: The tables are not directly linked but linked
through an intermediary table 'Employee Territory'.
The relationship though is ONE to MANY as it is
how many territories per employee. \n""")


# What is a situation where a document store like MongoDB is appropriate, and
# what is a situation where it is not?

print("""Part4.2 ANSWER: MongoDB is used when files/documents
are unstructured such as lacking proper rows and columns(dictionaries)
or is organized in a different manner such as graphs or images.
Mongo is not best when the files are in a structured table layout and/or
simply do not need to be scaled.""")


# What is NEWSQL?

print("""Part4.3 ANSWER: NewSQL is trying to go a step above NoSQL and
keep ACID guarantees. ACID is Atomicity, Consistency, Isolation, and
Durability; key concepts that database transactions need to keep in
the event of an error/malfunction. It is not practical for NoSQL to
have these guarantees due to its flexibility.""")
