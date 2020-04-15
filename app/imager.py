import base64
import requests
import json
import pandas as pd
from PIL import Image, ImageDraw
from io import BytesIO
import matplotlib.pyplot as plt

# data = data_original[1:-1]

# data = [[50.80583, -0.427663], [50.805829, -0.427636], [50.805832, -0.427572], [50.805851, -0.427537], [50.805899, -0.427489], [50.805928, -0.427482]]

# data = [[10, -100], [15, -20], [20, 40], [20, 60], [15, 80], [15, 100]]

def normalise_data(data):
    sizing = 1000
    data = data[1:-1]
    df = pd.DataFrame(data)
    # print(df)
    df_x, df_y = df[0], df[1]
    df_x_diff, df_y_diff = df_x.max()-df_x.min(), df_y.max()-df_y.min()

    if df_x_diff < df_y_diff:
        x_y_diff = df_x_diff / df_y_diff
        weight = (sizing-(sizing*x_y_diff))/2
        # weight = 0
        norm_x = ((df_x-df_x.min())/(df_x.max()-df_x.min()))*sizing*x_y_diff
        norm_x = norm_x.add(weight)
        norm_y = ((df_y-df_y.min())/(df_y.max()-df_y.min()))*sizing
    else:
        x_y_diff = df_y_diff / df_x_diff
        weight = (sizing-x_y_diff)/2
        norm_x = ((df_x-df_x.min())/(df_x.max()-df_x.min()))*sizing
        norm_y = ((df_y-df_y.min())/(df_y.max()-df_y.min()))*sizing*x_y_diff
        norm_y = norm_y.add(weight)

    norm_df = pd.concat([norm_x,norm_y], axis=1)
    norm_data = norm_df.values.tolist()

    print(x_y_diff)

    # normalised_df = ((df-df.min())/(df.max()-df.min()))*255
    # normalised_data = normalised_df.values.tolist()
    
    return norm_data

def draw_route(data):
    sizing = 1000
    img = Image.new('RGBA', (sizing, sizing))
    draw_img = ImageDraw.Draw(img)
     
    for i in range(len(data)):
        j = i + 1
        x1 = data[i][0]
        y1 = data[i][1]
        try:
            x2 = data[j][0]
            y2 = data[j][1]
        except:
            x2 = data[i][0]
            y2 = data[i][1]
        # draw_img.line((x1,y1,x2,y2), width=2, fill=(25,25,112))
        draw_img.line((x1,y1,x2,y2), width=5, fill=(255,255,255))
             
    # img.save('my_png.png')

    img = img.rotate(90)
    # img.show()

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return(img_str)


api_key = 'a2bfa0b4f13fb01cec47fd7fa307ff8f'

def post_image_str(api_key, image_str):
    session = requests.Session()
    base_url = "https://api.imgbb.com/1/upload"
    payload = {
            "key": api_key,
            "image": image_str
        }
    res = requests.post(base_url, payload)

    image_url = res.json()['data']['url']
    print(image_url)

    return(image_url)

def post_image_file(api_key, file):
    session = requests.Session()
    base_url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": api_key,
        "image": base64.b64encode(file.read())
        }
    res = requests.post(base_url, payload)

    image_url = res.json()['data']['url']
    print('done uploading')
    # print(image_url)
    # print(res.json())
    return(image_url)

def post_image(api_key):
    session = requests.Session()
    with open("cat.png", "rb") as file:
        base_url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read())
        }
        res = requests.post(base_url, payload)

    image_url = res.json()['data']['url']
    print(image_url)
    print(res.json())
    return(image_url)

def draw_elevation(xaxis, yaxis, y2axis):
    # plt.figure(figsize=(9,6))
    plt.figure(figsize=(14,2))
    plt.plot(xaxis,yaxis,color = 'deepskyblue', lw = 0.1, alpha = 0.8)
    plt.fill_between(xaxis, yaxis, y2axis, color="skyblue", alpha=0.6)
    plt.axis('off')

    buffered = BytesIO()
    plt.savefig(buffered, format='png', transparent=True, bbox_inches='tight', pad_inches=0, dpi=300)
    img_str = base64.b64encode(buffered.getvalue())
    plt.close()
    return(img_str)



# xs = [0,1,2,3,4,5,6]
# ys = [0,10,20,13,14,25,16]
# y2s = [0,0,0,0,0,0,0]

# if __name__ == '__main__':
# #     normalised_route = normalise_data(data)
# #     my_image_string = draw_route(normalised_route)
#     my_image_string = draw_elevation(xs, ys, y2s)
#     my_image_url = post_image_str(api_key, my_image_string)
#     # print(my_image_url)



	# RESIZE ELEVATION IMAGE

	# elevation_image = Image.open('app/static/temp/elevation_image_raw.png')

	# basewidth = 1000
	# wpercent = (basewidth/float(elevation_image.size[0]))
	# hsize = int((float(elevation_image.size[1])*float(wpercent)))
	# elevation_image = elevation_image.resize((basewidth,hsize), Image.ANTIALIAS)

	# crop_area = (111,0,955,hsize)
	# elevation_image = elevation_image.crop(crop_area)

	# basewidth = 1000
	# wpercent = (basewidth/float(elevation_image.size[0]))
	# elevation_image = elevation_image.resize((basewidth,hsize), Image.ANTIALIAS)