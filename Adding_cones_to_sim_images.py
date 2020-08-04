
widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
]
cones_major = [file for file in glob.glob('../keras-retinanet/datasets/cones/real/*.png')]
for back_image_file in progressbar.progressbar(sim_df['image'].unique(), widgets=widgets):
    back_image = Image.open('../keras-retinanet' + back_image_file[1:])
    back_image = back_image.convert('RGBA')
    back_im_shape = back_image.size
    num_cones = random.randint(1,5)
    cones = random.choices(cones_major,k=num_cones)
    coordinates = []
    for index in range(num_cones):
        cone_img = Image.open(cones[index])
        cone_img = cone_img.convert('RGBA')
        cone_shape = cone_img.size
        max_cone_width = random.randint(17, 30)
        angle = random.randint(-25,25)
        wpercent = (max_cone_width/float(cone_img.size[0]))
        hsize = int((float(cone_img.size[1])*float(wpercent)))
        cone_img = cone_img.resize((max_cone_width,hsize), Image.ANTIALIAS)
        rot = cone_img.rotate(angle, expand=1)
        cone_shape = rot.size
        x,y = (int((back_im_shape[0] - cone_shape[0]) * np.random.uniform()),
                int((back_im_shape[1] - cone_shape[1])* np.random.uniform()) #// 2 *(np.random.uniform() + 1))
                )
        back_image.paste(rot, (x,y), rot)
        back_image = back_image.convert("RGB")
        back_image.save('../keras-retinanet' + back_image_file[1:])
        cone_annotation = {'image':back_image_file,'x1':x,'y1':y,'x2':x+cone_shape[0], 'y2':y+cone_shape[1],'class':'trafficcone'}
        sim_df = sim_df.append(cone_annotation, ignore_index=True)