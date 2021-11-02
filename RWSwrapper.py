#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
| author:
| Belal HMEDAN, LIG lab/ Marven Team, France, 2021.
| RWSwrapper API.
'''
import requests
import xml.etree.ElementTree as ET
import time
from requests import auth
'''
 * This the main class distributed in this package.
 * It is the implementation of a REST Client for using ABB Robot Web Services 1.0 API for the robot Yumi.
 * <br/>The reference for this API is found on ABB's website @see <a href="https://developercenter.robotstudio.com/api/rwsApi/">here</a>.
 * It implements most of the methods useful for controlling Yumi via RWS.
 * <br/> For better explanation <a href="https://developercenter.robotstudio.com/api/RWS">REST API 2.0</a>
 * 
 * <br/>It is used as follows:
 * <br/><code>
 * import something
 *
 * <br/> class 
 * <br/>
 * </code><br/>
'''

class RWSwrapper:
    """
    
    """
    def __init__(self):

        self.REST_URI = "http://192.168.125.1"
        self.username = "Default User"
        self.password = "robotics"
        self.session  = requests.Session()
        self.auth = auth.HTTPDigestAuth(self.username, self.password)
        self.session.auth = self.auth
        self.rmmp_session = None
        self.rmmp_session_t = None
        # self.cookies = None
        # self.getCookies()

    # def getCookies(self):
    #     """
        
    #     """
    #     resp = self.session.get(self.REST_URI)

    #     if(resp.status_code > 203):
    #         print("Error: getCookies Exit with Request Error Code: ", resp.status_code)
    #     else:
    #         self.cookies = resp.cookies

    def getResponse(self, URI, keyword=None, payload=None):
        """
        
        """
        URI = self.REST_URI + URI
        if(payload is not None):
            resp = self.session.get(URI, params=payload)
        else:
            resp = self.session.get(URI)

        if(resp.status_code > 203):
            print("Error: getResponse Exit with Request Error Code: ", resp.status_code)
            return None

        if(keyword is not None):
            
            xml = ET.fromstring(resp.content)
            k = {'class': keyword}
            status = ''
            for child in xml[1].iter('*'):
                if child.attrib==k:
                    status = child.text
            return status
        elif(resp.status_code==204):
            print("Warning: getResponse with empty body response!")
            return None
        return None

    def postResponse(self, URI, header=None, payload=None, action=None):
        """
        
        """
        URI = self.REST_URI + URI

        if action is not None:
            URI=URI+'?action='+action

        if (header is not None):
            if(payload is not None):
                resp = self.session.post(URI, headers=header, data=payload)
            else:
                resp = self.session.post(URI, headers=header)
        else:
            if(payload is not None):
                resp = self.session.post(URI, data=payload, timeout=10)
            else:
                resp = self.session.post(URI)

        # if(resp.status_code > 203):
        #     print("postResponse Exit with Request Error Code: ", resp.status_code)

        return resp.status_code

    def userID(self):
        """

        """
        status = self.getResponse(URI="/users/rmmp", keyword='userid')
        return status

    def getOperationMode(self):
        """
        MANR - AUTO
        """
        status = self.getResponse(URI='/rw/panel/opmode', keyword='opmode')
        return status

    def registerTheUser(self):
        """
        
        """
        # TODO to implement a dynamic registeration with { local | remote }
        payload = {"username" : self.username, "application" : "Belal_API", "location" : "anything", "ulocale" : "local"}
        resp = self.postResponse(URI="/users", payload=payload)
        if(resp<204):
            print("Successful connection ", resp)
            return True
        else:
            print("Connection Failed! ", resp)
        return False

    def requestRMMP(self, timeout=9):
        """
        Request Manual Mode Privileges (RMMP)
        """        
        payload={"privilege" : "modify"}
        

        t1=time.time()
        while (int(time.time() - t1) < timeout):
            self.postResponse("/users/rmmp", payload=payload)
            status = self.getResponse(URI='/users/rmmp/poll', keyword='status')

            if status=="GRANTED":
                print("Successful Request of Manual Mode Privileges (RMMP)")
                return True

            elif status!="PENDING":
                raise Exception("User did not grant remote access")

            time.sleep(0.25)
        # raise Exception("Timeout: User did not grant remote access within {} seconds!".format(timeout))
        print("Error: Request Timeout!")
        return False

    def grantRMMP(self, privilege="modify"):
        """
        Request Manual Mode Privileges (RMMP)
        privilege {modify | exec | deny}
        """
        uID = self.userID()
        payload={"uid" : uID, "privilege" : privilege}
        resp = self.postResponse("/users/rmmp", payload=payload, action="set")
        if(resp==204):
            print("RMMP Granted ", resp)
            return True
        else:
            print("RMMP Denied! ", resp)
        return False

    def connect(self):
        """
        
        """
        self.registerTheUser()
        if(self.requestRMMP):
            if(self.grantRMMP()):
                print("Successful connection")
                return True
            else:
                print("Connection Failed, RMMP wasn't Granted!")
        else:
            print("Connection Failed, RMMP request failed")
        return False

    def getLeadThroughStatus(self, mechUnit="ROB_L"):
        """
        ROB_L, ROB_R
        """
        URI = "/rw/motionsystem/mechunits/{}?resource=lead-through".format(mechUnit)
        status = self.getResponse(URI=URI, keyword="status")
        return status

    def activateLeadThrough(self, mechUnit="ROB_L"):
        """
        ROB_L, ROB_R
        """
        if(self.connect()):
            payload = {'status': 'active'}
            URI = "/rw/motionsystem/mechunits/"+mechUnit
            print(URI)
            resp = self.postResponse(URI=URI, payload=payload, action="set-lead-through")
            print(resp)
            if resp == 204:
                print('Mechanical Unit {} in Lead Through Mode'.format(mechUnit))
                return True
        else:
            print('Could not set LeadThrough Mode!')
            return False
    
    def deactivateLeadThrough(self, mechUnit="ROB_L"):
        """
        ROB_L, ROB_R
        """
        if(self.connect()):
            self.requestMastership()
            payload = {'status': 'inactive'}
            URI = "/rw/motionsystem/mechunits/"+mechUnit
            print(URI)
            resp = self.postResponse(URI=URI, payload=payload, action="set-lead-through")
            print(resp)
            if resp == 204:
                print('Lead Through Mode for Mechanical Unit {} has been deactivated!'.format(mechUnit))
                return True
        else:
            print('Could not set LeadThrough Mode')
            return False
# =============================================================
# # Usage Example:

# rws = RWSwrapper()

# Set the Flexpendant to "Manual Mode", and Set motors to "ON"

# if(rws.connect()):
# 	rws.activateLeadThrough("ROB_R") # ROB_L

# print(rws.getLeadThroughStatus("ROB_R")) # ROB_L

# # rws.deactivateLeadThrough("ROB_R")