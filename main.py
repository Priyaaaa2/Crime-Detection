import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLOWorld
from moviepy.editor import ImageSequenceClip
import os
import json
from datetime import datetime
import ipfs_convertion, pushHash

def main():
    object1 = ['knife','gun']

    cap = cv2.VideoCapture(0)  # Use video path instead of camera
    model = YOLOWorld("models/your-model-for-detection")  # Assuming YOLO instead of YOLOWorld

    object_list = ['a','b', 'c', 'd'] # Make a list of objects to be detected using your model
    model.set_classes(object_list)  # Uncomment if YOLO supports setting custom classes

    image_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detected_object = []
        frame = cv2.flip(frame, 1)

        results = model(frame)

        for result in results:
            boxes = result.boxes
            for box in boxes:
                label = model.names[int(box.cls)]
                detected_object.append(label)

                im_array = result.plot()  # plot BGR numpy array
                frame = im_array

            if object1[0] in detected_object or object1[1] in detected_object:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_frames.append(frame_rgb)

        cv2.namedWindow('yolov8', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('yolov8', 640, 480)
        cv2.imshow("yolov8", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Check if there are any frames to process
    if image_frames:
        # Generate a unique filename based on the object detected
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{object1}_{timestamp}.mp4"
        output_path = os.path.join('detected_videos', output_filename)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create video clip
        clip = ImageSequenceClip(image_frames, fps=10)
        clip.write_videofile(output_path, codec='libx264') 

        # Save path to JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), 'output_path.json')

        # Read existing data from JSON file
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
        else:
            data = {"video_paths": []}

        # Create a new entry with hash as None and isHashed as False
        new_entry = {
            "path": output_path,
            "hash": None,
            "isHashed": False,
            "dynamoDBstatus": False
        }

        # Append new entry
        data["video_paths"].append(new_entry)

        # Write updated data to JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=12)

        print(f"Video saved as {output_path}")
    else:
        print("No frames with detected objects to create a video.")
    
    ipfs_convertion.main()
    pushHash.main()

if __name__ == "__main__":
    main()


