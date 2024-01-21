from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')

def index():
    return "Hello World"

class Main:
    @app.route('/get-employee-details', methods = ['GET'])
    def get_subscription_details():
        # Fecthes the subscriber_id
        subscriber_id = request.args.get('subscriber_id')
        # With the subsciber ID make a call to backend to fetch the employee details
        # Temporary code whcih mockes the data that is recieved from benefits
        with open('data/employee-read-data.json', 'r') as employeewriteData:
            data = json.load(employeewriteData)
        
        # Writing the data into a json file
        file_path = 'data/employee-write-data.json'
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        # Fetching and storing the data to fetch employees name 
        with open('data/employee-write-data.json', 'r') as testData :
            employeeData = json.load(testData)

        employeeName = employeeData[0]['EmployeeName']['FirstName']

        message =  "Hey " + employeeName + " Which Life Event do you want to Perfrom today? Marriage or Death"
    
        return{
            "status_code" : 200,
            "message" : message
        }


    @app.route('/get-life-event-type')

    def get_type_of_life_event():
        # Need to use STT
        life_event_type  = request.data.decode("utf-8")

        if life_event_type not in ["marriage", "death"]:
            return {
                "status_code" : 400,
                "message" :"Please Provide a Valid Life Event"
            }
        else:
            return {
                "status_code" : 200,
                "life_event_type" : life_event_type,
            }
        
    
    @app.route('/marriage')

    def marriage_life_event():
        dictQuestions = {
            1 : "Congrats on your marriage, Can you please provide the event date",
            2:  "Can you provide your dependent name",
            3:  "Can you provide your dependent ssn",
            4:  "Can you provide your dependent date of birth",
            5:  "Do you want to add more dependents",
            6:  "For which coverage do you want to make a change",
            7:  "Do you want to add more coverage",
            8:  "Can i check out"
        }

        user_id = int(request.args.get('user_id'))
        completed_question_id  = int(request.args.get('question_id'))
        next_question_id = completed_question_id + 1

        if completed_question_id == 0:
            data  =  {'life_event_type' : 'marriage'}
            # create a json file with {user_id}.json
            file_path = f"data/{user_id}.json"
            with open(file_path, 'w') as json_file:
                json.dump(data,json_file, indent = 4) 
            return {
                "status_code" : 200,
                "question_name" : dictQuestions[next_question_id],
                "question_number": next_question_id
            }
        
        if completed_question_id == 1:
            # Need to use STT
            event_date = request.data.decode("utf-8")
            data = {
                "event_date" : event_date
            }
            file_path = f"data/{user_id}.json"
            with open(file_path, 'w') as json_file:
                json.dump(data,json_file, indent = 4)  
            return {
                "status_code" : 200,
                "question_name" : dictQuestions[next_question_id],
                "question_number": next_question_id
            }
        
        if completed_question_id == 2:
            # get the dependent name
            dependent_name = request.data.decode("utf-8")
            file_path = f"data/{user_id}.json"

            with open(file_path, 'r') as json_file:
                employeeData = json.load(json_file)
            
            if 'dependents' not in employeeData.keys():
                employeeData['dependents'] = []
            
            data = {
                "id" : len(employeeData['dependents']) + 1,
                "dependent_name": dependent_name
            }
            employeeData['dependents'].append(data)

            with open(file_path, 'w') as file:
                json.dump(employeeData,file, indent = 4)

            return {
                "status_code" : 200,
                "dependent_id": data["id"],
                "question_name" : dictQuestions[next_question_id],
                "question_number": next_question_id
            }
        
        if completed_question_id == 3:
            file_path = f"data/{user_id}.json"
            dependent_id = int(request.args.get('dependent_id'))
            dependent_ssn = request.data.decode("utf-8")

            with open(file_path, 'r') as json_file:
                employeeData = json.load(json_file)
            
            for values in employeeData['dependents']:
                if values['id'] == dependent_id:
                    values['dependent_ssn'] = dependent_ssn
                    break
                

            with open(file_path, 'w') as file:
                json.dump(employeeData,file, indent = 4)


            return{
                "status_code" : 200,
                "dependent_id": dependent_id,
                "question_name" : dictQuestions[next_question_id],
                "question_number": next_question_id
            }
        
        if completed_question_id == 4:
            file_path = f"data/{user_id}.json"
            dependent_id = int(request.args.get('dependent_id'))
            dependent_date_of_birth = request.data.decode("utf-8")

            with open(file_path, 'r') as json_file:
                employeeData = json.load(json_file)
            
            for values in employeeData['dependents']:
                if values['id'] == dependent_id:
                    values['dependent_date_of_birth'] = dependent_date_of_birth
                    break

            with open(file_path, 'w') as file:
                json.dump(employeeData,file, indent = 4)

            return{
                "status_code" : 200,
                "dependent_id": dependent_id,
                "question_name" : dictQuestions[next_question_id],
                "question_number": next_question_id
            }
        
        if completed_question_id == 5:
            coverage_details = ['Vision', 'Medical', 'Dental']
            response =  request.data.decode("utf-8")
            if response == "Yes":
                return{
                "status_code" : 200,
                "question_name" : dictQuestions[2],
                "question_number": 2
                }
            return{
                "status_code" : 200,
                "question_name" : f"{dictQuestions[next_question_id]}{coverage_details}",
                "question_number": next_question_id
            }
    
        if completed_question_id == 6:
            file_path = f"data/{user_id}.json"
            coverage =  request.data.decode("utf-8")
            with open(file_path, 'r') as json_file:
                employeeData = json.load(json_file)
            if 'coverages' not in employeeData.keys():
                employeeData['coverages'] = [] 
            data = {
                "id" : len(employeeData['coverages']) + 1,
                "coverage_name": coverage
                }
            employeeData['coverages'].append(data)

            with open(file_path, 'w') as file:
                json.dump(employeeData,file, indent = 4)
            return{
                "coverage_id": data["id"],
                "status_code" : 200,
                "question" : dictQuestions[next_question_id],
                "question_number" : next_question_id
            }
        
        if completed_question_id == 7:
            response =  request.data.decode("utf-8")
            if response == "Yes":
                return {
                    "status_code" : 200,
                    "question" : dictQuestions[6],
                    "question_number" : 6
                }
            return{
                "status_code" : 200,
                "question" : dictQuestions[next_question_id],
                "question_number" : next_question_id

            }

        if completed_question_id ==8:
            file_path = f"data/{user_id}.json"
            with open(file_path, 'r') as json_file:
                employeeData = json.load(json_file)
            response =  request.data.decode("utf-8")

            if response == "Yes":
                employeeData['checkout'] = True
                with open(file_path, 'w') as file:
                    json.dump(employeeData,file, indent = 4)
                return {
                    'message': "Your Life Event Has been Completed",
                    'status_code' : 200
                }
            return{
                'status_code' : 400,
                'message': "Please refresh the page to start again"
            }




            

        
    if __name__ == "__main__":
        app.run(port=8000, debug=True)