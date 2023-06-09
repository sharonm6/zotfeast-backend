import onnxruntime
import numpy as np

session = onnxruntime.InferenceSession('model/model.onnx')
threshold = 0.6

def get_recommendation(schedule, time, dist, task, duration):
    schedule_list = [int(digit) for digit in schedule]
    user_input = schedule_list + [time, dist, task, duration]

    input_data = [user_input]
    print(input_data)
    input_name = session.get_inputs()[0].name
    inputs = {input_name: input_data}

    prediction = session.run(None, inputs)[0][0][0]
    recommendation = 0 if prediction < threshold else 1 

    print(f'{prediction} --> {recommendation}')

    return recommendation

if __name__ == '__main__':
    rec = get_recommendation('11111000000000000000000001000010', 15, 0.5, 1, .7)
    print(rec)