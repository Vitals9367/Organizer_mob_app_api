import uuid
from app.main import db
from app.main.model.user import User

from werkzeug import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, ContainerSasPermissions
from datetime import datetime, timedelta

#Azure storage connection string
connect_str = "string"

account_name = "organizerapi"
account_key = "key"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_name = 'pictures'
container_client = blob_service_client.get_container_client(container_name)

def get_img_url_with_blob_sas_token(blob_name):
    blob_sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=3)
    )
    blob_url_with_blob_sas_token = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{blob_sas_token}"
    return blob_url_with_blob_sas_token

#Checking allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Returning user image by username

def get_user_image(username):

    user = User.query.filter_by(username=username).first();

    if user:
        if user.image_name:
            
            blob = BlobClient.from_connection_string(
                conn_str=connect_str, container_name=container_name, blob_name=user.image_name)
            exists = blob.exists()

            if exists:
                response = {
                    "status" : "success",
                    "url": get_img_url_with_blob_sas_token(user.image_name)
                }
                return response

            response = {
                "status": "success",
                "url": get_img_url_with_blob_sas_token("person.png")
            }
            return response

        response = {
            "status": "success",
            "url": get_img_url_with_blob_sas_token("person.png")
        }
        return response

    else:
        response = {
            'status': 'fail',
            'message':'User not found',
        }
        return response, 404

#Uploading user image
def upload_user_image(username, request):

    user = User.query.filter_by(username=username).first()

    if not user:
        response = {
            'status': 'fail',
            'message': 'User not found',
        }
        return response, 404

    if 'file' not in request.files:
        response = {
            'status': 'fail',
            'message': 'No file part',
        }
        return response, 404

    file = request.files['file']
    name = secure_filename(file.filename)

    if not allowed_file(name):
        response = {
        'status': 'fail',
        'message': 'Wrong file format',
        }
        return response, 404

    if user.image_name:

        blob = BlobClient.from_connection_string(
            conn_str=connect_str, container_name=container_name, blob_name=user.image_name)
        exists = blob.exists()

        if exists:
            blob_client = container_client.get_blob_client(user.image_name)
            blob_client.delete_blob()

    genereted_string = uuid.uuid4().hex

    user.image_name = genereted_string

    blob_client = container_client.get_blob_client(user.image_name)

    blob_client.upload_blob(file)

    db.session.commit()

    response = {
        'status': 'success',
        'url': get_img_url_with_blob_sas_token(user.image_name),
    }
    return response, 200
