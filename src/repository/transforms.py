import cloudinary
import cloudinary.uploader
from src.conf.config import cloud_init
from src.schemas.transform import TransformModel
from sqlalchemy.orm import Session
from src.repository.photos import get_photo
import qrcode
from src.database.models import User, Photo
import io


async def get_transform_url(photo_id: int, transforms: TransformModel, current_user: User, db: Session):
    photo = await get_photo(photo_id, db)
    if photo:
        cloud_init()
        param_dict = dict()
        for i in transforms:
            if i[1]:
                param_dict[i[0]] = i[1]

        r = cloudinary.uploader.upload(photo.image_url, public_id=f'PhotoShareApp/transform/{current_user.username}',
                                       overwrite=True)
        height = int(
            photo.image_url.split('/')[6].split(',')[1].replace('h_', '') if 'height' not in param_dict else param_dict[
                'height'])
        width = int(
            photo.image_url.split('/')[6].split(',')[2].replace('w_', '') if 'width' not in param_dict else param_dict[
                'width'])
        angle = param_dict['angle'] if 'angle' in param_dict else 0
        src_url = cloudinary.CloudinaryImage(f'PhotoShareApp/transform/{current_user.username}').build_url(
            transformation=[{'height': height, 'width': width, 'crop': param_dict['crop']},
                            {'effect': f"blur:{param_dict['blur']}"},
                            {'angle': angle},
                            {'opacity': param_dict['opacity']}],

            version=r.get('version'))

        new_photo = Photo(image_url=src_url, title=photo.title, description=photo.description, user_id=photo.user_id)
        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)
        return src_url
    return None


async def get_qr_code(photo_id: int, current_user: User, db: Session):
    photo = await get_photo(photo_id, db)
    if photo:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(photo.image_url)
        img = qr.make_image()
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        cloud_init()
        r_qr = cloudinary.uploader.upload(img_byte_arr, public_id=f'PhotoShareApp/qrcode/{current_user.username}',
                                          overwrite=True)
        qr_url = cloudinary.CloudinaryImage(f'PhotoShareApp/qrcode/{current_user.username}').build_url(height=250,
                                                                                                       width=250,
                                                                                                       version=r_qr.get(
                                                                                                           'version'))
        return qr_url
    return None
