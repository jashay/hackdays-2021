import boto3
import base64

def preprocess_image(img_dir):
    encoded_string = base64.b64encode(img_dir)
    base_64_binary = base64.decodebytes(encoded_string)
    return base_64_binary

def detect_labels(img):

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={"Bytes":img},
        MaxLabels=20)

    print('Detected labels for test')
    print()
    ret = []
    for label in response['Labels']:
        if label['Name'] not in ["Food", "Vegetable", "Fruit", "Food", "Plant", 'Snake', 'Nut', 'Produce', 'Grain', 'Leaf', 'Seed']:
            print ("Label: " + label['Name'])
            ret.append(label['Name'])
            print ("Confidence: " + str(label['Confidence']))
            print ("Instances:")
            for instance in label['Instances']:
                print ("  Bounding box")
                print ("    Top: " + str(instance['BoundingBox']['Top']))
                print ("    Left: " + str(instance['BoundingBox']['Left']))
                print ("    Width: " +  str(instance['BoundingBox']['Width']))
                print ("    Height: " +  str(instance['BoundingBox']['Height']))
                print ("  Confidence: " + str(instance['Confidence']))
                print()

            print ("Parents:")
            for parent in label['Parents']:
                print ("   " + parent['Name'])
            print(label)
            print ("----------")
            print ()

    return (len(response['Labels']), ret)



def get_labels(img):
    label_count=detect_labels(preprocess_image(img))
    print("Labels detected: " + str(label_count[0]))
    return label_count[1]
