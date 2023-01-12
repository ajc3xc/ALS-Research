import boto3

s3 = boto3.client('s3', region_name = 'us-east-2', aws_access_key_id = 'AKIAXPCCGXHHET6LYOPI', aws_secret_access_key = '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')

def createBucket(bucketName):
    bucket = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint':'us-east-2'})

def printBucket():
    bucket_response = s3.list_buckets()
    buckets = bucket_response['Buckets']
    for bucket in buckets:
        print(buckets)

def deleteBucket(bucketName):
    response = s3.delete_bucket(Bucket=bucketName)

def keepBucket(bucketName):
    bucket_response = s3.list_buckets()
    buckets = bucket_response['Buckets']
    hasName = False;
    for bucket in buckets:
        if bucket['Name'] == bucketName: hasName = True;
    if hasName==False: createBucket(bucketName)


def upload_file(fName, Bucket, Key):
    s3.upload_file(\
    Filename = fName,\
    Bucket=Bucket,\
    Key=Key)

def upload_public(fName, bucket, key):
    s3.upload_file(Filename = fName,\
    Bucket=bucket, Key=key,\
    ExtraArgs={'ACL':'public-read'})

def print_objects(bucket, pre):
    response = s3.list_objects(Bucket=bucket,\
    Prefix=pre)
    print(response)

def print_object(bucket, pre):
    response = s3.head_object(\
    Bucket=bucket, Pre = pre)
    print(response)

def remove(bucket, key): s3.delete_object(Bucket=bucket, Key=key)


#----------------------------------------Chapter 2---------------------------------------------------#


def make_public(): s3.put_object_acl(Bucket=Bucket, Key=Key, ACL='public-read')
#can use ExtraArgs instead

def get_url():
    url = "https://{}.{}".format(Bucket, Key);
    return url;

def make_public():
    s3.put_object_acl(Bucket=Bucket, Key = obj['Key'], ACL = '')

def get_obj():
    obj = s3.get_object(Bucket=Bucket, Key=Key)
    return obj

def create_temp_url(time):
    share_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        ExpiresIn=time,
        Params={'Bucket':Bucket, 'Key':Key})

def getUrls(path):
    files = []
    f = open(path, "r")
    for l in f:
        files.append(repr(l))
    f.close()
    return files

def down_file():
    s3.download_file(Filename=Filename, Bucket=Bucket, Key=Key)

comm = r"""
#--------------------------------vars & output-------------------------------------#
Filename = r"C:\Users\13144\Downloads\answers.txt"
Bucket = "ajc123private"
Key = "answers.txt"
keys = ['answers.txt', "Datacamp - internet importing.png", "Lab5.png",
        "Screenshot 2022-06-04 Completed Courses.png",
        "PreLab2.txt",
        "answers.txt"]

#workaround
File1 = r"C:\Users\13144\Downloads\answers.txt"
File2 = r"C:\Users\13144\Pictures\Datacamp - internet importing.png"
File3 = r"C:\Users\13144\Pictures\Lab5.png"
File4 =         r"C:\Users\13144\Pictures\Screenshot 2022-06-04 Completed Courses.png"
File5 =         r"C:\Users\13144\Desktop\PreLab2.txt"
File6 =         r"C:\Users\13144\Downloads\answers.txt"
files = [File1, File2, File3, File4, File5, File6]
keepBucket('ajc123private')

#upload, show data in files, delete
for x in range(len(files)):
    upload_file(files[x], Bucket, keys[x])
    print_objects(Bucket, keys[x])
    print("")
"""











