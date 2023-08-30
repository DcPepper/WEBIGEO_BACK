import unittest
import requests
import os
import json

class ApiTest(unittest.TestCase):
    
    def setUp(self):
        self.country = requests.get("http://localhost:8000/country/").text
        self.quiz = requests.get("http://localhost:8000/quiz/").text
        self.record = json.loads(requests.get("http://localhost:8000/record/").text)
        
    def test_points(self):
        wrong_point_request = {
            'time': '1', 
            'user': 'DcPepper', 
            'device': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0', 
            'quiz': 'http://localhost:8000/quiz/1/', 
            'points': -1
            }

        r = requests.post(url= "http://localhost:8000/record/", data=wrong_point_request)
        #Test d'un score négatif: résultat attendu= 400
        self.assertEqual(r.status_code, 400)

        wrong_point_request["points"] = 25
        r = requests.post(url= "http://localhost:8000/record/", data=wrong_point_request)
        #Test d'un score > nombre de questions: résultat attendu= 400
        self.assertEqual(r.status_code, 400)
        
        wrong_point_request["points"] = 1
        r = requests.post(url= "http://localhost:8000/record/", data=wrong_point_request)
        #Test d'un score > nombre de questions: résultat attendu= 400
        self.assertEqual(r.status_code, 201)
    
    def test_time(self):
        wrong_time_request = {
            'time': '-1', 
            'user': 'DcPepper', 
            'device': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0', 
            'quiz': 'http://localhost:8000/quiz/1/', 
            'points': 10
            }
        r = requests.post(url= "http://localhost:8000/record/", data=wrong_time_request)
        #Test d'un temps < 0: résultat attendu= 400
        self.assertEqual(r.status_code, 400)





if __name__ == "__main__":
    
    unittest.main()