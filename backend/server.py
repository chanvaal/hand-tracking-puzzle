import cv2
import mediapipe as mp
import asyncio
import websockets
import json

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

async def handler(websocket):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        fingertip = None

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            index_tip = hand.landmark[8]

            fingertip = {
                "x": index_tip.x,
                "y": index_tip.y
            }

        await websocket.send(json.dumps({
            "finger": fingertip
        }))

        await asyncio.sleep(0.03)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()