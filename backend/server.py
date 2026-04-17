import asyncio
import json
import cv2
import mediapipe as mp
import websockets
import math
import time

mp_hands = mp.solutions.hands
mp.drawing = mp.solutions.drawing_utils

hands = mp.hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

INDEX_TIP = 8
INDEX_MCP = 5
THUMB_TIP = 4
MIDDLE_TIP = 12
WRIST = 0

def dist(a, b):
    """Euclidean distance between two (x, y) tuples."""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def is_finger_up(lm, tip_id, mcp_id):
    """Return True if fingertip is above its MCP knuckle (extended finger)."""
    return lm[tip_id].y < lm[mcp_id].y

def detect_gesture(landmarks, frame_w, frame_h):