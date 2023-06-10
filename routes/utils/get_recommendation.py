import onnxruntime
import numpy as np

session = onnxruntime.InferenceSession('model/model.onnx')
threshold = 0.6

def get_recommendation(schedule, time, dist, task, duration):
    schedule_list = [int(digit) for digit in schedule]

    nEvents = sum(schedule_list[time:min(time+5, len(schedule_list))])

    user_input = [nEvents, dist, task, duration]

    input_data = [user_input]
    input_name = session.get_inputs()[0].name
    inputs = {input_name: input_data}

    prediction = session.run(None, inputs)[0][0][0]
    recommendation = 0 if prediction < threshold else 1 

    # print(f'{prediction} --> {recommendation}')
    return recommendation


if __name__ == '__main__':
    rec = get_recommendation('11111000000000000000000001000010', 15, 0.5, 1, .7)
    # print(rec)

    rec = get_recommendation('00000000000000000000000000000000', 15, 0.5, 1, .7)
    # print(rec)

    rec = get_recommendation('11111111111111111111111111111111', 12, 10, 1, .7)
    # print(rec)


    """
    Unit Tests
        - If schedule completely busy, then no
        - If schedule completely free, then yes
        - If schedule partially free and duration, then yes
        - If schedule partially free and no duration, then no
        - If schedule partially busy and distance is short, then yes
        - If schedule partially busy and distance is long, then no
    """