import cloudinary
import cloudinary.uploader
from src.conf.config import cloud_init
from src.schemas.transform import TransformModel
from sqlalchemy.orm import Session
from src.repository.photos import get_photo
from src.conf.config import settings


async def get_transform_url(photo_id: int, transforms: TransformModel, db: Session):
    photo = await get_photo(photo_id, db)
    if photo:
        cloud_init()
        param_dict = dict()
        for i in transforms:
            if i[1]:
                param_dict[i[0]] = i[1]

        r = cloudinary.uploader.upload(photo.image_url, public_id='PhotoShareApp/user', overwrite=True)
        height = int(
            photo.image_url.split('/')[6].split(',')[1].replace('h_', '') if 'height' not in param_dict else param_dict[
                'height'])
        width = int(
            photo.image_url.split('/')[6].split(',')[2].replace('w_', '') if 'width' not in param_dict else param_dict[
                'width'])
        angle = param_dict['angle'] if 'angle' in param_dict else 0
        src_url = cloudinary.CloudinaryImage('PhotoShareApp/user').build_url(
            transformation=[{'height': height, 'width': width, 'crop': param_dict['crop']},
                            {'effect': f"blur:{param_dict['blur']}"},
                            {'angle': angle},
                            {'opacity': param_dict['opacity']}],

            version=r.get('version'))
        print(src_url)
        return src_url
    return None
