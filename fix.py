import re
import sys

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replacement 1: delete image logic
content = re.sub(
    r'if image_filename:\s*image_path\s*=\s*os\.path\.join\(app\.config\[\'UPLOAD_FOLDER\'\], image_filename\)\s*if os\.path\.exists\(image_path\):\s*try:\s*os\.remove\(image_path\)\s*except Exception as e:\s*db\.rollback\(\)',
    '''if image_filename and not image_filename.startswith("data:image"):
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    db.rollback()''',
    content
)

old_save = """        if 'camera_image' in request.form and request.form['camera_image']:
            img_data = request.form['camera_image'].split(",")[1]
            filename = f"camera_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(img_data))
        else:
            image    = request.files['image']
            if image and image.filename:
                orig_filename = secure_filename(image.filename)
                base, ext = os.path.splitext(orig_filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{base}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
            else:
                filename = \"\""""

new_save = """        if 'camera_image' in request.form and request.form['camera_image']:
            filename = request.form['camera_image']
        else:
            image = request.files.get('image')
            if image and image.filename:
                import base64
                img_data = base64.b64encode(image.read()).decode('utf-8')
                mime_type = image.mimetype or 'image/png'
                filename = f"data:{mime_type};base64,{img_data}"
            else:
                filename = \"\""""

content = content.replace(old_save, new_save)

old_edit_save = """        filename = item['image']
        if 'camera_image' in request.form and request.form['camera_image']:
            img_data = request.form['camera_image'].split(",")[1]
            filename = f"camera_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(img_data))
            # Delete old image
            if item['image']:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], item['image'])
                if os.path.exists(old_path):
                    os.remove(old_path)
        else:
            image = request.files.get('image')
            if image and image.filename:
                orig_filename = secure_filename(image.filename)
                base, ext = os.path.splitext(orig_filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{base}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                # Delete old image
                if item['image']:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], item['image'])
                    if os.path.exists(old_path):
                        os.remove(old_path)"""

new_edit_save = """        filename = item['image']
        if 'camera_image' in request.form and request.form['camera_image']:
            filename = request.form['camera_image']
        else:
            image = request.files.get('image')
            if image and image.filename:
                import base64
                img_data = base64.b64encode(image.read()).decode('utf-8')
                mime_type = image.mimetype or 'image/png'
                filename = f"data:{mime_type};base64,{img_data}"
                
        # Don't delete old images on edit if they are base64, 
        # and on Vercel old files won't exist anyway.
"""

content = content.replace(old_edit_save, new_edit_save)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modified app.py")
