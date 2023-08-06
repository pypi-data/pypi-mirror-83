import sys
import socket
import requests
from visualone import utils
import random
import string
import json
import glob
import time


samples_s3_folder = 'pypi_samples'
inference_samples_s3_folder = 'pypi_toinfer'


class client():
        
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.object_id = ''
                        
    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, oid):
        clients = utils.get_client(self.public_key)
        if len(clients) == 0: raise Exception("Invalid api_public_key!")
        if len(clients) > 1: raise Exception("Invalid client. Contact Visual One team at contact@visualone.tech")  
        if not clients[0]['private_key'] == self.private_key: raise Exception("Invalid api_private_key!")
        self._object_id = clients[0]['objectId']    
                       
        
        
    def train(self, path_to_positive_samples, path_to_negative_samples, confidence_threshold):
               
        config = utils.get_config('pypi')[0]
           
        event_id = 'pypi_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        
        print("Creating the event... event_id = {}".format(event_id)) 
        
        # Upload the positive samples into s3
        positive_samples = glob.glob(path_to_positive_samples + "/*.jpg") + glob.glob(path_to_positive_samples + "/*.png")
        n_positive = 0
        for positive_sample in positive_samples:
            n_positive += 1
            utils.upload_to_s3(positive_sample,
                               samples_s3_folder, 
                               "{}_positive_{}.jpg".format(event_id, str(n_positive)))        
        
        print("Found {} positive samples.".format(str(n_positive)))
        
        # Upload the negative samples into s3
        negative_samples = glob.glob(path_to_negative_samples + "/*.jpg") + glob.glob(path_to_negative_samples + "/*.png")
        n_negative = 0
        for negative_sample in negative_samples:
            n_negative += 1
            utils.upload_to_s3(negative_sample, 
                               samples_s3_folder, 
                               "{}_negative_{}.jpg".format(event_id, str(n_negative)))              
        
        print("Found {} negative samples.".format(str(n_negative)))
        
        print("Started model training...")
        payload = {
            "event_id": event_id,
            "camera_id": 'nil',
            "event_name": 'nil',
            "conf_threshold": confidence_threshold,
            "n_positive": n_positive,
            "n_negative": n_negative,
            "client_id": self.object_id,
            "samples_s3_bucket": 'vo-fsl-demo2',
            "samples_s3_folder": samples_s3_folder
        }
                
        # Create the event 
        resp = requests.post(config['event_manager_endpoint'] + '/create_event', json = payload)
        
        resp_json = json.loads(resp.content)
        
        return resp_json
    
        
    def predict(self, event_id, image_file):
        
        config = utils.get_config('pypi')[0]
        
        utils.upload_to_s3(image_file, 
                           inference_samples_s3_folder, 
                           "{}.jpg".format(event_id))              
        
        payload = {
            "event_id": event_id,
            "event_name": 'nil',
            "image_name": "{}.jpg".format(event_id),
            "timestamp": round(time.time()*1000),
            "update_model": False,
            "force_late_infer": True,
            "inference_samples_s3_bucket": 'vo-fsl-demo2',
            "inference_samples_s3_folder": inference_samples_s3_folder
        }
        
        print("Applying the model...")
        
        resp_json = {}
        try:
            resp = requests.post(config['event_predictor_endpoint'], json = payload)
        
            resp_json = json.loads(resp.content)
            
        except:
            return 'An error occured.'
        
        result = {}
        result['prediction'] = resp_json['prediction']
        result['confidence'] = resp_json['confidence']
        result['event_id'] = resp_json['event_id']
        result['latency'] = resp_json['latency']
        
        return result
            
            
            
            


