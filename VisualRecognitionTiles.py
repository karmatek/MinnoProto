"""This module breaks image to tiles and runs it trhough watson visual recognition,
and shows result in a original picure with red color tile"""

import json
import math
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
from PIL import Image
def analyzeImage(image):
    visual_recognition = VisualRecognitionV3(
        # The release date of the version of the API you want to use.
        '2018-03-19',
        # visual-recognition's API key
        iam_api_key='cdH1cuZP6Oik4LWWBS5fqEBGo957ZSpjwvGWleVBICOW')

    # Load image for testing
    #testImage = Image.open("C:/Users/veeti/PycharmProjects/IAT/testdata/moles/mole2.jpg")
    # testImage=Image.open("C:/Users/veeti/PycharmProjects/IAT/testdata/fruitbowl.jpg")

    testImage = image

    # get image size information,Image size, in pixels. The size is given as a 2-tuple (width, height).
    imageSize = testImage.size

    # divide image to tiles and run through watson visual recognition
    tileWidth = 100
    tileHeight = 100
    # calculate amount of tiles in each direction
    tilesInWidthDirection = imageSize[0] // tileWidth
    tilesInHeightDirection = imageSize[1] // tileHeight
    print("tilesInWidthDirection: %d tilesInHeightDirection: %d " % (tilesInWidthDirection, tilesInHeightDirection))

    # copy=testImage.copy()
    """make a new image with white backround, after each tile analyzing 
    the result is indicated with new tile filled with red, and intensity of red 
    is showing the score
    """
    copy = Image.new("RGB", (imageSize), (255, 255, 255))
    score = 0.0

    # Crops piece of original image, saves it to temponary file  and sends it to watson visual recognition to analyze
    for testImageRow in range(0, tilesInHeightDirection):
        for testImageCol in range(0, tilesInWidthDirection):
            croppedTestImage = testImage.crop((testImageCol * tileWidth, testImageRow * tileHeight,
                                           testImageCol * tileWidth + tileWidth,
                                           testImageRow * tileHeight + tileHeight))
            croppedTestImage.save("C:/Users/veeti/PycharmProjects/IAT/testdata/tempCroppedImage.jpg")

            croppedTestImage.save("C:/Users/veeti/PycharmProjects/IAT/testdata/tempCroppedImage.jpg")
            print("running at row %d col %d" % (testImageRow, testImageCol))

            # sends image to watson, receives data and saves it to res variable
            with open("C:/Users/veeti/PycharmProjects/IAT/testdata/tempCroppedImage.jpg", 'rb') as images_file:
                res = visual_recognition.classify(images_file,
                                              threshold='0.1', classifier_ids='DefaultCustomModel_1433648033')
                temp = json.dumps(res)
                print(temp)

                # tries to find word "score from test result, and saves its location to startIndex variable
                startIndex = (temp.find("score"))

                # score is usually somewhere about 130+ letters from start
                if (startIndex > 10):
                    print(startIndex)
                    # after score value there is either "," or "}" mark find one of those, saves its location,
                    # and reads score value between "score" word and "," or "}" mark
                    endIndex = temp.find("}", startIndex + 8)
                    if endIndex < 0 or endIndex > 170:
                        endIndex = temp.find(",", startIndex + 8)
                    print(endIndex)
                    stringScore = temp[(startIndex + 8):endIndex]  # parse score value
                    score = float(stringScore)  # cast score value from string to float
                    print(score)

                # if score is above 0.1 (= 10 %) show it in the picture
                if (score > 0.1):
                    # make score exponential for visual purpose
                    expScore = (score / 2)
                    expScore = math.pow(expScore, (1 / 5))
                    print(expScore)

                    """make new image which is size of tile and color it red, which intensity is 
                    showing the score, then paste this "tileImage" to the white image (which was 
                    at the begining), image is pasted at the position of the sample tile.
                    """
                    redBoxImage = Image.new("RGB", (tileWidth, tileHeight), (int(255 * score)))
                    copy.paste(redBoxImage, (testImageCol * tileWidth, testImageRow * tileHeight))

                    score = 0


    # copy.show()
    # mask original image with the white image (with result tiles), (0,3) sets the transparency of the top layer
    #blend = Image.blend(testImage, copy, 0.3)
    #blend.show()
    return copy

