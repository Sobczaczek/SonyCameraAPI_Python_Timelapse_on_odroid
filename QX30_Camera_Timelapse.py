# @autor Dawid Sobczak
# @date 2022-06-03
# @brief Timelapse with live photo to master download using SonyAPI
#    	 by pySony library
#
# Tested on:
# Sony DSC-QX30

# IMPORTS ==============================================================================================================
from __future__ import print_function
from pysony import SonyAPI, ControlPoint

from datetime import datetime

import requests
import urllib.request

import base64, hashlib
import time
import json
import six
import sys
import os
import shutil

# VARIABLES ============================================================================================================
# local path:
localPath = './static'
# pendrive path:
penSavePath = "/media/odroid/KINGSTON/sony_timelapse/saved"
# path (you can change it)
saveFilePath = penSavePath


# FUNCTIONS ============================================================================================================
# Convert file name (delete odd characters and spaces) -----------------------------------------------------------------
def convertFileName(s):
    # empty string
    str1 = ""
    for c in s:
        if c == " ":
            str1 += "_"
        elif c == ".":
            str1 += "_"
        elif c == ":":
            str1 += "_"
        else:
            str1 += c
    return str1


# Status logger for file -----------------------------------------------------------------------------------------------
def saveStatus(s):
    # open file in append mode
    log = open('/media/odroid/KINGSTON/sony_timelapse/log.txt', 'a')
    separator = "----------------------------------------------------------------------------------------------------\n"
    # log separatos
    log.write(separator)
    # save text
    log.write(s)
    # close file
    log.close()


# Convert list to string -----------------------------------------------------------------------------------------------
def list2string(list_variable):
    # empty string
    str1 = ""
    # iterate through list
    for element in list_variable:
        # create output string
        str1 += element
    return str1


# Eliminate extra slash from photo URL (probably json.dumps for this #TODO) --------------------------------------------
def eliminateSlash(s):
    # prepare empty string
    str1 = ""
    # iterate through string
    for c in s:
        # eliminate extra slash char
        if c != "\\":
            str1 += c
    return str1


# Split list into n sublists (for delete content purposes) ------------------------------------------------------------
def splitList(l, n):
    listOfSublists = []
    for i in range(0, len(l), n):
        listOfSublists.append(l[i:i + n])
    return listOfSublists


# Camera authentication ------------------------------------------------------------------------------------------------
def authenticate(camera):
    # 64 _ASCII_ character == 256 bit equivalant
    AUTH_CONST_STRING = "35fc6c85705f5b37eb0f31f60c8412644fb2755ff55701e04a82d671c4b5d998"
    METHODS_TO_ENABLE = "\
	avContent/deleteContent:\
	avContent/getContentCount:\
	avContent/getContentList:\
	avContent/getSchemeList:\
	avContent/getSourceList:\
	avContent/pauseStreaming:\
	avContent/requestToNotifyStreamingStatus:\
	avContent/seekStreamingPosition:\
	avContent/setStreamingContent:\
	avContent/startStreaming:\
	avContent/stopStreaming:\
	camera/actFormatStorage:\
	camera/actHalfPressShutter:\
	camera/actTakePicture:\
	camera/actTrackingFocus:\
	camera/actWhiteBalanceOnePushCustom:\
	camera/actZoom:\
	camera/awaitTakePicture:\
	camera/cancelHalfPressShutter:\
	camera/cancelTouchAFPosition:\
	camera/cancelTrackingFocus:\
	camera/getApplicationInfo:\
	camera/getAudioRecording:\
	camera/getAutoPowerOff:\
	camera/getAvailableApiList:\
	camera/getAvailableAudioRecording:\
	camera/getAvailableAutoPowerOff:\
	camera/getAvailableBeepMode:\
	camera/getAvailableCameraFunction:\
	camera/getAvailableColorSetting:\
	camera/getAvailableContShootingMode:\
	camera/getAvailableContShootingSpeed:\
	camera/getAvailableExposureCompensation:\
	camera/getAvailableExposureMode:\
	camera/getAvailableFlashMode:\
	camera/getAvailableFlipSetting:\
	camera/getAvailableFNumber:\
	camera/getAvailableFocusMode:\
	camera/getAvailableInfraredRemoteControl:\
	camera/getAvailableIntervalTime:\
	camera/getAvailableIsoSpeedRate:\
	camera/getAvailableLiveviewSize:\
	camera/getAvailableLoopRecTime:\
	camera/getAvailableMovieFileFormat:\
	camera/getAvailableMovieQuality:\
	camera/getAvailablePostviewImageSize:\
	camera/getAvailableSceneSelection:\
	camera/getAvailableSelfTimer:\
	camera/getAvailableShootMode:\
	camera/getAvailableShutterSpeed:\
	camera/getAvailableSteadyMode:\
	camera/getAvailableStillQuality:\
	camera/getAvailableStillSize:\
	camera/getAvailableTrackingFocus:\
	camera/getAvailableTvColorSystem:\
	camera/getAvailableViewAngle:\
	camera/getAvailableWhiteBalance:\
	camera/getAvailableWindNoiseReduction:\
	camera/getAvailableZoomSetting:\
	camera/getBeepMode:\
	camera/getCameraFunction:\
	camera/getColorSetting:\
	camera/getContShootingMode:\
	camera/getContShootingSpeed:\
	camera/getEvent:\
	camera/getExposureCompensation:\
	camera/getExposureMode:\
	camera/getFlashMode:\
	camera/getFlipSetting:\
	camera/getFNumber:\
	camera/getFocusMode:\
	camera/getInfraredRemoteControl:\
	camera/getIntervalTime:\
	camera/getIsoSpeedRate:\
	camera/getLiveviewFrameInfo:\
	camera/getLiveviewSize:\
	camera/getLoopRecTime:\
	camera/getMethodTypes:\
	camera/getMovieFileFormat:\
	camera/getMovieQuality:\
	camera/getPostviewImageSize:\
	camera/getSceneSelection:\
	camera/getSelfTimer:\
	camera/getShootMode:\
	camera/getShutterSpeed:\
	camera/getSteadyMode:\
	camera/getStillQuality:\
	camera/getStillSize:\
	camera/getStorageInformation:\
	camera/getSupportedAudioRecording:\
	camera/getSupportedAutoPowerOff:\
	camera/getSupportedBeepMode:\
	camera/getSupportedCameraFunction:\
	camera/getSupportedColorSetting:\
	camera/getSupportedContShootingMode:\
	camera/getSupportedContShootingSpeed:\
	camera/getSupportedExposureCompensation:\
	camera/getSupportedExposureMode:\
	camera/getSupportedFlashMode:\
	camera/getSupportedFlipSetting:\
	camera/getSupportedFNumber:\
	camera/getSupportedFocusMode:\
	camera/getSupportedInfraredRemoteControl:\
	camera/getSupportedIntervalTime:\
	camera/getSupportedIsoSpeedRate:\
	camera/getSupportedLiveviewSize:\
	camera/getSupportedLoopRecTime:\
	camera/getSupportedMovieFileFormat:\
	camera/getSupportedMovieQuality:\
	camera/getSupportedPostviewImageSize:\
	camera/getSupportedProgramShift:\
	camera/getSupportedSceneSelection:\
	camera/getSupportedSelfTimer:\
	camera/getSupportedShootMode:\
	camera/getSupportedShutterSpeed:\
	camera/getSupportedSteadyMode:\
	camera/getSupportedStillQuality:\
	camera/getSupportedStillSize:\
	camera/getSupportedTrackingFocus:\
	camera/getSupportedTvColorSystem:\
	camera/getSupportedViewAngle:\
	camera/getSupportedWhiteBalance:\
	camera/getSupportedWindNoiseReduction:\
	camera/getSupportedZoomSetting:\
	camera/getTouchAFPosition:\
	camera/getTrackingFocus:\
	camera/getTvColorSystem:\
	camera/getVersions:\
	camera/getViewAngle:\
	camera/getWhiteBalance:\
	camera/getWindNoiseReduction:\
	camera/getZoomSetting:\
	camera/liveview:\
	camera/setAudioRecording:\
	camera/setAutoPowerOff:\
	camera/setBeepMode:\
	camera/setCameraFunction:\
	camera/setColorSetting:\
	camera/setContShootingMode:\
	camera/setContShootingSpeed:\
	camera/setExposureCompensation:\
	camera/setExposureMode:\
	camera/setFlashMode:\
	camera/setFlipSetting:\
	camera/setFNumber:\
	camera/setFocusMode:\
	camera/setInfraredRemoteControl:\
	camera/setIntervalTime:\
	camera/setIsoSpeedRate:\
	camera/setLiveviewFrameInfo:\
	camera/setLiveviewSize:\
	camera/setLoopRecTime:\
	camera/setMovieFileFormat:\
	camera/setMovieQuality:\
	camera/setPostviewImageSize:\
	camera/setProgramShift:\
	camera/setSceneSelection:\
	camera/setSelfTimer:\
	camera/setShootMode:\
	camera/setShutterSpeed:\
	camera/setSteadyMode:\
	camera/setStillQuality:\
	camera/setStillSize:\
	camera/setTouchAFPosition:\
	camera/setTrackingFocus:\
	camera/setTvColorSystem:\
	camera/setViewAngle:\
	camera/setWhiteBalance:\
	camera/setWindNoiseReduction:\
	camera/setZoomSetting:\
	camera/startAudioRec:\
	camera/startContShooting:\
	camera/startIntervalStillRec:\
	camera/startLiveview:\
	camera/startLiveviewWithSize:\
	camera/startLoopRec:\
	camera/startMovieRec:\
	camera/startRecMode:\
	camera/stopAudioRec:\
	camera/stopContShooting:\
	camera/stopIntervalStillRec:\
	camera/stopLiveview:\
	camera/stopLoopRec:\
	camera/stopMovieRec:\
	camera/stopRecMode:\
	system/setCurrentTime"

    # request random nonce from camera
    resp = camera.actEnableMethods([{"methods": "", "developerName": "", \
                                     "developerID": "", "sg": ""}])
    print(resp)
    dg = resp['result'][0]['dg']

    # append nonce to AUTH string and hash
    h = hashlib.sha256()
    h.update(bytes(AUTH_CONST_STRING + dg, encoding='utf8'))
    sg = base64.b64encode(h.digest()).decode("UTF-8")

    # Pass credentials to camera, which will eval with secret method/values
    resp = camera.actEnableMethods([{"methods": METHODS_TO_ENABLE, \
                                     "developerName": "Rubber Duck Paradise", \
                                     "developerID": "22222222-2222-2222-2222-222222222222", "sg": sg}])
    print("Authenicated:", resp)


# Delete content from camera memory ------------------------------------------------------------------------------------
def deleteContent(camera):
    # Function algorithm:
    # [1]
    # [2]
    # [3]
    # [4]

    # Get camera current function
    cameraMode = camera.getCameraFunction()['result'][0]
    print("Camera is now in %s mode." % cameraMode)

    # Check if camera is not 'Remote Shooting'
    if cameraMode != "Remote Shooting":
        # Set camera in 'Remote Shooting' mode
        camera.setCameraFunction("Remote Shooting")
        print("Camera function is now set to 'Remote Shooting'")
        # Wait some time for mode to change (wait for lens to extend)
        time.sleep(5)

    # Check actual camera storage information
    print("Checking camera storage information...")
    storageInformation = camera.getStorageInformation()['result'][0]
    # Get number of recordable images
    numberOfRecordableImages = storageInformation[0]['numberOfRecordableImages']
    # Get name of storage (SID)
    storageID = storageInformation[0]['storageID']

    print("Number of recordable images: ", numberOfRecordableImages)
    print("Storage identification name: ", storageID)
    print("Camera storage information complete!")

    # Set camera in 'Contents Transfer' mode
    camera.setCameraFunction('Contents Transfer')
    print("Camera function is now set to 'Contents Transfer'")
    # Wait some time for mode change (wait for lens to fold)
    time.sleep(5)

    # Get camera storage scheme list
    print("Getting camera scheme list...")
    storageScheme = camera.getSchemeList()['result'][0]
    print("Camera scheme list information complete!")

    # Get camera source list
    print("Getting camera source list...")
    mainSource = camera.getSourceList(storageScheme)['result'][0]
    mainSource = mainSource[0]['source']
    print(mainSource)
    print("Camera source list information complete!")

    # Get content count of main catalog
    print("Getting camera content count of main catalog...")
    contentCountParam = [{'uri': mainSource, 'view': 'date'}]
    mainCatalogContentCount = int(camera.getContentCount(contentCountParam)['result'][0]['count'])
    print("Main content count:", mainCatalogContentCount)

    # Get main catalog content list
    mainCatalogContentListParam = [{'uri': mainSource, 'stldx': 0, 'cnt': \
        mainCatalogContentCount, 'view': 'date', 'sort': ''}]

    mainCatalogContentList = camera.getContentList(mainCatalogContentListParam)['result'][0]
    # dumps json | list -> string
    mainCatalogContentList = json.dumps(mainCatalogContentList)
    # parse json | string -> list
    mainCatalogContentList = json.loads(mainCatalogContentList)

    print("")
    print("Main catalog contents list:")
    print(mainCatalogContentList)
    print("")

    # Get main catalog content URIs and make list out of them
    iterator0 = 0  # iterator == 0
    mainCatalogContentURIs = []  # empty list

    for Folder in mainCatalogContentList:
        # append URI to list from main catalog contents list
        mainCatalogContentURIs.append(mainCatalogContentList[iterator0]['uri'])
        # increase iterator
        iterator0 += 1

    print("")
    print("Main catalog URIs list: ", mainCatalogContentURIs)
    print("")

    # Repeat it for every content (catalog aka folder) in mainCatalogContentURIs
    iterator1 = 0  # iterator == 0
    allContentURIs = []  # empty list

    for Catalog in mainCatalogContentURIs:
        print("")
        print("Catalog URI: ", iterator1)
        print("Catalog: ", Catalog)

        # param for .getContentCount()
        catalogContentCountParam = [{'uri': Catalog, 'view': 'date'}]

        # .getContentCount()
        catalogContentCount = camera.getContentCount(catalogContentCountParam) \
            ['result'][0]['count']
        print("Liczba elementow w katalogu: ", catalogContentCount)

        # lista elementow katalogu
        catalogContentListParam = [{'uri': Catalog, 'stldx': 0, 'cnt': \
            catalogContentCount, 'view': 'date', 'sort': ''}]

        catalogContentList = camera.getContentList(catalogContentListParam)['result'][0]

        # dumps json | list -> string
        catalogContentList = json.dumps(catalogContentList)
        # parse json | string -> list
        catalogContentList = json.loads(catalogContentList)

        print("")
        print("Lista elementow w katalogu:")
        print(catalogContentList)

        # wyciagamy tylko uri zdjec z katalogu
        iterator2 = 0
        for Content in catalogContentList:
            allContentURIs.append(catalogContentList[iterator2]['uri'])
            iterator2 += 1

        iterator1 += 1

    print("")
    print("Lista calego contentu na karcie: ")
    print(allContentURIs)

    # create list of sublists
    URIsSublists = splitList(allContentURIs, 50)
    print(URIsSublists)

    # execute delete
    for uri_list in URIsSublists:
        # delete
        deleteAllContentParam = [{'uri': uri_list}]
        # print response
        # if corect - camera should return only id
        print(camera.deleteContent(deleteAllContentParam))
        # sleep
        time.sleep(20.0)


# Camera timelapse -----------------------------------------------------------------------------------------------------
def timelapse(camera):
    log_data2 = ""
    # Start timer
    startTime = time.time()
    # Check camera current mode
    cameraMode = camera.getCameraFunction()['result'][0]
    print("Camera is now in %s mode." % cameraMode)

    # Check if camera is not in 'Remote Shooting' mode
    if cameraMode != "Remote Shooting":
        # Set camera in 'Remote Shooting' mode
        camera.setCameraFunction("Remote Shooting")
        print("Camera function is now set to 'Remote Shooting'")
        # Wait some time for mode change
        time.sleep(5)

    # Act timelapse
    while True:
        print("Taking picture...")
        photo = camera.actTakePicture()
        print("Picture made!")

        # Convert URL from list to string
        imageURL = list2string(photo['result'][0])
        # or use json.loads (?)

        # Delete extra slashes from URL
        imageURL = eliminateSlash(imageURL)

        # Create local file
        date_time = datetime.fromtimestamp(int(time.time()))

        # imageLocal = './static/saved/' + str(int(time.time())) + '.jpg' # time name in sec
        # imageLocal = './static/saved/' + str(date_time) + '.jpg'	 # date name format
        fileName = convertFileName(str(date_time)) + ".jpg"
        print(fileName)

        # file name location
        # imageLocal = os.path.join("/home/odroid/Timelapse_budowa/static" + "/saved/", fileName)
        imageLocal = os.path.join(saveFilePath, fileName)

        # Retrive data from URL
        urllib.request.urlretrieve(imageURL, imageLocal)
        print("Image saved!")
        log_data2 = "Picture made and saved in: \n"
        log_data2 += str(imageLocal) + "\n"

        # Move file to pendrive
        # time.sleep(2)
        # shutil.copy("/home/odroid/Timelapse_budowa/static/saved/"+fileName, penSavePath+fileName)
        # shutil.copyfile("/home/odroid/Timelapse_budowa/static/saved/"+fileName,
        # "/media/odroid/KINGSTON/sony_timelapse/" + fileName)
        # time.sleep(2)
        # remove image from local dir
        # print("Image saved on USB stick!")
        # os.remove("/home/odroid/Timelapse_budowa/static/saved/"+fileName)

        # Request memory status
        memoryInfo = camera.getStorageInformation()['result'][0]
        print("Memory information:")
        print(memoryInfo)

        # Check number of recordable images
        numberOfRecordableImages = memoryInfo[0]['numberOfRecordableImages']
        print(type(numberOfRecordableImages))
        log_data2 += "Number of recordable images: \n"
        log_data2 += str(numberOfRecordableImages) + '\n'

        # if less than 200
        if numberOfRecordableImages <= 200:
            # Act delete function
            log_data2 += "Deleting files!\n"
            deleteContent(camera)
            # Check camera current mode
            cameraMode = camera.getCameraFunction()['result'][0]
            print("Camera is now in %s mode." % cameraMode)

            # Check if camera is not in 'Remote Shooting' mode
            if cameraMode != "Remote Shooting":
                # Set camera in 'Remote Shooting' mode
                camera.setCameraFunction("Remote Shooting")
                print("Camera function is now set to 'Remote Shooting'")
            # Wait some time for mode change
            time.sleep(5)
            log_data2 += "Deletion complete!\n"

        # logger
        saveStatus(log_data2)
        # Sleep....
        # time.sleep(120.0 - ((time.time() - startTime) % 120)) # 2min
        time.sleep(900.0 - ((time.time() - startTime) % 900))  # 15min


# Main -----------------------------------------------------------------------------------------------------------------
def main():
    # logger file preparation
    date_log = datetime.fromtimestamp(int(time.time()))
    log_data = "\nScript started execution\n"
    log_data = str(date_log) + "\n"

    # Scan for camera
    print("Scanning for available WiFi camera...")
    log_data += "Scanning for available WiFi camera...\n"
    search = ControlPoint()
    cameras = search.discover(5)

    print("Scanning complete!")
    log_data += "Scanning complete!\n"
    print("List of available cameras: %s" % cameras)
    log_data += "List of available cameras: %s\n" % cameras

    # Connect to Camera
    print("Connecting to Camera...")
    if len(cameras):
        camera = SonyAPI(QX_ADDR=cameras[0])
        print("Connected!")
        log_data += "Connected to camera!\n"
    else:
        print("ERROR: Could not find any device!")
        log_data += "Error with connecting... restarting!\n"
        # exit with ERROR: 2
        sys.exit(2)

    # Authenticate Camera
    print("Authenticating connected camera...")
    authenticate(camera)

    # Prepare folders v2
    # if not os.path.exists(saveFilePath):
    #   os.makedirs(saveFilePath)
    #
    # if not os.path.exists(saveFilePath + "/saved"):
    #    os.makedirs(saveFilePath + "/saved")

    # Prepare folders
    while not os.path.exists(saveFilePath):
        # stay until path is found (example: pendrive mounted)
        print("Waiting")
        log_data += "Waiting for mount...\n"

    # Timelapse
    print("Activating timelapse...")
    log_data += "Activating timelapse...\n"
    # save status
    saveStatus(log_data)
    timelapse(camera)


# TESTS ----------------------------------------------------------------------------------------------------------------
def test():
    # Scan for camera
    print("Scanning for available WiFi camera...")
    search = ControlPoint()
    cameras = search.discover(5)

    print("Scanning complete!")
    print("List of available cameras: %s" % cameras)

    # Connect to Camera
    print("Connecting to Camera...")
    if len(cameras):
        camera = SonyAPI(QX_ADDR=cameras[0])
        print("Connected!")
    else:
        print("ERROR: Could not find any device!")
        # exit with ERROR: 2
        sys.exit(2)

    camera.setCameraFunction("Remote Shooting")
    time.sleep(10)
    print(authenticate(camera))


# main =================================================================================================================
if __name__ == "__main__":
    main()
