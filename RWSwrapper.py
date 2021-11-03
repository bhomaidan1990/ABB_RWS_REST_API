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
from math import pi as PI
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

    def getJointtarget(self, mechUnit='ROB_L'):
        """
        Function: getJointtarget, to get the robot robtarget.
        ---
        Parameters:
        @param: mechUnit, string, 'ROB_L' or 'ROB_R'.
        ---
        @return: jointtarget, list of joint values, jointtarget.
        Angles in Radian to confront with ROS, and the joints order is: [1, 2, 7, 3, 4, 5, 6] to follow ABB
        """
        URI = self.REST_URI+"/rw/motionsystem/mechunits/"+mechUnit+"/jointtarget"

        resp = self.session.get(URI)
        if(resp.status_code != 200):
            print("Exit with Request Error Code: ", resp.status_code)
            return False
        tree = ET.fromstring(resp.content)

        for child in tree[1].iter('*'):
        	if   child.attrib == {'class': 'rax_1'}:
        		rax_1 = round((PI/180) * float(child.text), 4)
        	elif child.attrib == {'class': 'rax_2'}:
        		rax_2 =round( (PI/180) * float(child.text), 4)
        	elif child.attrib == {'class': 'rax_3'}:
        		rax_3 =round( (PI/180) * float(child.text), 4)
        	elif child.attrib == {'class': 'rax_4'}:
        		rax_4 =round( (PI/180) * float(child.text), 4)
        	elif child.attrib == {'class': 'rax_5'}:
        		rax_5 =round( (PI/180) * float(child.text), 4)
        	elif child.attrib == {'class': 'rax_6'}:
        		rax_6 =round( (PI/180) * float(child.text), 4)
        	elif child.attrib == {'class': 'eax_a'}:
        		eax_a =round( (PI/180) * float(child.text), 4)

        jointtarget = [rax_1, rax_2, eax_a,rax_3, rax_4, rax_5, rax_6]#, [eax_a, '9E+09', '9E+09', '9E+09', '9E+09', '9E+09']] # eax_b, eax_c, eax_d, eax_e, eax_f]]
        return jointtarget

    def getRobtarget(self, mechUnit='ROB_L'):
        """
        Function: getRobtarget, to get the robot robtarget.
        ---
        Parameters:
        @param: mechUnit, string, 'ROB_L' or 'ROB_R'.
        ---
        @return: robtarget, list of lists, robtarget.
        """
        URI = self.REST_URI+"/rw/motionsystem/mechunits/"+mechUnit+"/robtarget"

        resp = self.session.get(URI)
        if(resp.status_code != 200):
            print("Exit with Request Error Code: ", resp.status_code)
            return False

        tree = ET.fromstring(resp.content)

        for child in tree[1].iter('*'):
            if child.attrib == {'class': 'x'}:
                x = float(child.text)
            elif child.attrib == {'class': 'y'}:
                y = float(child.text)
            elif child.attrib == {'class': 'z'}:
                z = float(child.text)
            elif child.attrib == {'class': 'q1'}:
                q1 = float(child.text)
            elif child.attrib == {'class': 'q2'}:
                q2 = float(child.text)
            elif child.attrib == {'class': 'q3'}:
                q3 = float(child.text)
            elif child.attrib == {'class': 'q4'}:
                q4 = float(child.text)
            elif child.attrib == {'class': 'cf1'}:
                cf11 = float(child.text)
            elif child.attrib == {'class': 'cf4'}:
                cf14 = float(child.text)
            elif child.attrib == {'class': 'cf6'}:
                cf16 = float(child.text)
            elif child.attrib == {'class': 'cfx'}:
                cf1x = float(child.text)
            elif child.attrib == {'class': 'eax_a'}:
                eax_a = float(child.text)

        robtarget = [[x, y, z], [q1, q2, q3, q4], [cf11, cf14, cf16, cf1x], [eax_a, '9E+09', '9E+09', '9E+09', '9E+09', '9E+09']] # eax_b, eax_c, eax_d, eax_e, eax_f]]
		
        return robtarget
# =============================================================
# # Usage Example:

# rws = RWSwrapper()

# print(rws.getJointtarget())
# print(rws.getJointtarget('ROB_R'))
# Set the Flexpendant to "Manual Mode", and Set motors to "ON"

# if(rws.connect()):
# 	rws.activateLeadThrough("ROB_R") # ROB_L

# print(rws.getLeadThroughStatus("ROB_R")) # ROB_L

# # rws.deactivateLeadThrough("ROB_R")

# ROB_L_HOME = [0.0, -2.2688, 2.356, 0.5238, -0.0, 0.6994, -0.0004]
# ROB_R_HOME = [-0.0002, -2.2689, -2.3562, 0.5238, -0.0, 0.699, -0.0003]