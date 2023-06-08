import onnxruntime
import numpy as np

session = onnxruntime.InferenceSession('../../model/model.onnx')

def get_recommendation(schedule, time, dist, task, duration):
    schedule_list = [int(digit) for digit in schedule]
    user_input = schedule_list + [time, dist, task, duration]

    input_data = [user_input]
    input_name = session.get_inputs()[0].name
    inputs = {input_name: input_data}

    outputs = session.run(None, inputs)
    recommendation = np.round(outputs[0][0])

    return recommendation

if __name__ == '__main__':
    get_recommendation('1'*32, 30, 9, 1, 1.7)