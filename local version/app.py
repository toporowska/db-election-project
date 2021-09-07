import psycopg2
import getpass
import sshtunnel 
from time import sleep

##################### user authentication functions #####################
def check(log,pas,cursor):
    cursor.callproc('log_in', (log,pas))
    type = cursor.fetchone() 
    type = type[0]
     
    return type 

def logging_in(cursor):
    ans = input("What do you want to do?: \n 1) Log in \n 2) Exit\n" )
    while ans != "2":
        if ans == "1":
            user = input("Username:")
            password = getpass.getpass("Password:")
            
            type = check(user,password,cursor)
            if type == "commitee" or type == "voter":
                return type, user
            print('\n',type, '\n')
        else:
            print("I don't understand \n")
        ans = input("What do you want to do?: \n 1) Log in \n 2) Exit\n" )   
            
    return 0, 0


##################### Commitee action/helper functions #####################
def add_voter(cursor,name,surname,index):
    
    cursor.callproc('new_voter', (index,name,surname))
    odp = cursor.fetchone()
    return odp[0]

def add_election(cursor,election_name,num_positions,deadline,begin_date,end_date):
    cursor.callproc('new_election', (election_name,num_positions,deadline,begin_date,end_date))
    odp = cursor.fetchone()
    return odp[0]

def publish_results(cursor):
    print("Results of which election do you want to publish?")
    election = show_election(cursor,'publishable')  
    if len(election) == 0:
        return "No election found"
    number = int(input(""))
    while number-1 not in range(len(election)):
        print("Please choose a number between 1 and {}".format(len(election)))
        number = int(input(""))
    election_name = election[number-1]
    
    cursor.execute("SELECT publish('{}'); ".format(election_name))
    
    return "Published results of: {} ".format(election_name)

def show_voters(cursor):
    cursor.execute('''SELECT * FROM voter;''')
    voters = cursor.fetchall()
    for i in range(len(voters)):
        print(i+1,")", voters[i])
    return 0

def find_voter(cursor,name,surname):
    cursor.execute('''SELECT index_number FROM voter WHERE name = '{}' AND surname = '{}';'''.format(name,surname))
    index = cursor.fetchall()
    
    if len(index) == 0:
        return "No such person in the database"
      
    return index[0][0]

def show_election(cursor,type = "all"):
    if type == "detailed":
        cursor.execute('''SELECT * FROM election;''')
        election = cursor.fetchall()
        opisy = ["election name","number of positions","nomination deadline","beggining","end","published"]
        election = [str(elem).replace('datetime.date',' ').strip("()") for elem in election]
        
        print(opisy)
        for i in range(len(election)):
            print(i+1,")", election[i])
    else:
        if type == 'publishable':
            cursor.execute('''SELECT name FROM election WHERE published = 'F' AND end_date < NOW();''')
        elif type == "all" :
            cursor.execute('''SELECT name FROM election;''')
        elif type == "votable":
            cursor.execute('''SELECT name FROM election WHERE begin_date < NOW() AND end_date > NOW();''')
        elif type == "published":
            cursor.execute('''SELECT name FROM election WHERE published = 'T';''')
        elif type == "collecting nominations":
            cursor.execute('''SELECT name FROM election WHERE nomination_deadline > NOW();''')
        election = cursor.fetchall()
        election = [elem[0] for elem in election]    
        
        for i in range(len(election)):
            print(i+1,")", election[i])
        
    return election

# other functions
def other(cursor):
    ans = input("\n Other options: \n 1. Show voters \n 2. Show elections \n 3. Show candidates \n 4. Show election results \n 5. Previous site \n")
    if ans == '1':
        print("Registered voters: \n")
        show_voters(cursor)
    elif ans == '2':
        print("Registered elections: \n")
        show_election(cursor,"detailed")
    elif ans == '3':
        print("Please pick election:")
        election = show_election(cursor)
        
        if len(election) == 0:
            return "Sorry, no election available"
        number = int(input(""))
        
        while number-1 not in range(len(election)):
            print("Please pick a number from 1 to {}".format(len(election)))
            number = int(input(""))
        
        election_name = election[number-1]
        print("Registered candidates: \n")
        candidates = show_candidates(cursor,election_name)
        if len(candidates) == 0:
            print("There are no candidates registered for this election\n")
    elif ans == '4':
        results = show_results(cursor)
        print("\n")
        for result in results:
            print(result)
        print("\n")
    elif ans == '5':
        return 0
    else:
        print("I don't understand")
        other(cursor)

# to prevent errors from wrong date format
def fetchdate(mess):
    ans = "y"
    
    while ans != "n":
        string = input(mess)
        if len(string) > 3:
            sep = string[2]
        else:
            sep = "-"
        lst = string.split(sep)
        if len(lst) != 3:
            print("Wrong date format. Please use format: dd-mm-yyyy:")
        else:
            num = [el.isnumeric() for el in lst]
            if False in num:
                print("A character detected. Please use only numbers.")
            else:
                num = [int(el) for el in lst]
                if num[0] not in range(1,32):
                    print("Day {} out of scale".format(num[0]))
                elif num[1] not in range(1,13):
                    print("Month {} out of scale".format(num[1]))
                else:
                    return "-".join(lst)
        
        ans = input("Do you want to try again? (y/n) \n")
        
    return "error"
    
##################### commitee menu function #####################

def commitee(cursor):

    ans = 0 
    
    while ans != "5":
        ans = input("\n What do you want to do? \n 1. Add a voter \n 2. Add election \n 3. Publish results \n 4. Other options \n 5. Exit\n")
        
        if ans == "1":
            print("Please enter voters data")
            name = input("name: ")
            surname = input("surname: ")
            index = input("Index number: ")
            
            while not index.isnumeric():
                index = input("Index number must be a number! Please enter a valid index number: ")
                
            while not int(index) > 0:
                index = input("Index number must be a positive number! Please enter a valid index number:")    
            
            print("\n",add_voter(cursor,name,surname,index))

        elif ans == "2":
            print("Please enter election details")
            election_name = input("election name: ")
            num_positions = input("number of positions: ")
            while not num_positions.isnumeric():
                num_positions = input("Number of positions must be a number! Please enter a valid number of positions: ")
                
            deadline = fetchdate("Nomination deadline (dd-mm-yyyy): ")
            if deadline != "error":
                begin_date = fetchdate("When to begin voting (dd-mm-yyyy): ")   
                if begin_date != "error":
                    end_date = fetchdate("when to end voting (dd-mm-yyyy): ")
                    if end_date != "error":
                        print("\n",add_election(cursor,election_name,num_positions,deadline,begin_date,end_date))
            
        elif ans == "3":
            print("\n",publish_results(cursor))
            
        elif ans == "4":
            other(cursor)

        elif ans != "5":
            print("I don't understand\n")
        

    print("Ok, bye!")
    
    return 0


##################### Voter action/helper functions #####################

def show_candidates(cursor,election):
    cursor.execute('''SELECT name, surname FROM voter WHERE index_number IN (SELECT index_number FROM candidate WHERE election_name = '{}');'''.format(election))
    candidates = cursor.fetchall()
    candidates = [(elem[0],elem[1]) for elem in candidates]    
    
    for i in range(len(candidates)):
        print(i+1,")", str(candidates[i]).strip("()").replace(',','').replace("'",""))
    
    return candidates
    
def add_candidate(cursor,name,surname):

    index = find_voter(cursor,name,surname)
    if isinstance(index,str):
        return index
        
    print("To which election do you want to nominate someone?")
    election = show_election(cursor,"collecting nominations")
    if len(election) == 0:
        return "No available elections"
    number = int(input(""))
    
    while number-1 not in range(len(election)):
        print("Please pick a number from 1 to {}".format(len(election)))
        number = int(input(""))
        
    election_name = election[number-1]
    
    cursor.callproc('new_candidate', (election_name,index))
    odp = cursor.fetchone()
    
    return odp[0]

def vote(cursor,idx):
    print("\n In which election do you want to vote?")
    election = show_election(cursor,"votable")
    
    if len(election) == 0:
        return "No available elections"
    number = int(input(""))
    
    while number-1 not in range(len(election)):
        print("Please pick a number from 1 to {}".format(len(election)))
        number = int(input(""))
        
    election_name = election[number-1]
    
    print("\n Who do you want to vote for?")
    candidates = show_candidates(cursor,election_name)
    if len(candidates) == 0:
        return "No candidates in this election"
    number = int(input(""))
    
    while number-1 not in range(len(candidates)):
        print("Please pick a number from 1 to {}".format(len(candidates)))
        number = int(input(""))
    
    candidate_idx = int(find_voter(cursor,candidates[number-1][0],candidates[number-1][1]))
    
    cursor.callproc('vote', (election_name,idx,candidate_idx))
    odp = cursor.fetchall()
    
    return odp[0][0]

def show_results(cursor):
    print("Results of which election are you interested in?")
    election = show_election(cursor,"published")
    if len(election) == 0:
        return ["No results were found",""]
    number = int(input(""))
    
    while number-1 not in range(len(election)):
        print("Please pick a number from 1 to {}".format(len(election)))
        number = int(input(""))
    
    election_name = election[number-1]
    
    cursor.execute("SELECT results('{}'); ".format(election_name))
    odp = cursor.fetchall()
    if len(odp) == 0:
        return ["Nobody voted in this election",""]
    
    return [str(elem).strip("'()',").replace(',',' ') for elem in odp]


##################### voter menu function #################

def voter(cursor,idx):

    ans = 0
    
    while ans != "4":
        ans = input("\nWhat do you want to do? \n 1. Nominate a candidate \n 2. Vote \n 3. See results \n 4. Exit\n")

        if ans == "1":
            print("\n Please enter candidate data \n")
            name = input("name: ")
            surname = input("surname: ")
            print(add_candidate(cursor,name,surname),"\n")

        elif ans == "2":
            print("\n",vote(cursor,idx),"\n")

        elif ans == "3":
            results = show_results(cursor)
            print("\n")
            for result in results:
                print(result)
            print("\n")

        elif ans != "4":
            print("\n I don't understand \n")
        
    print("Ok, bye!")
    
    return 0


##################### main app function ######################

def main():
    #establishing the connection
    user = input("Username: ")
    password = getpass.getpass("Password: ")    

    conn = psycopg2.connect(
    database="election", user=user, password=password, host='127.0.0.1', port= '5432'
    )
    conn.autocommit = True

    #Creating a cursor
    cursor = conn.cursor()

    type, number = logging_in(cursor)
    if type == 0:
        conn.close()
        return 0


    if type == 'commitee':
        commitee(cursor)
    elif type == 'voter':
        voter(cursor,number)
    
    conn.close()
    return 0
    

main()