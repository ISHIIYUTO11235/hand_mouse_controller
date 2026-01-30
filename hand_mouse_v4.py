import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np

# --- 設定 ---
CAM_WIDTH, CAM_HEIGHT = 640, 480

# 感度設定
BASE_SENSITIVITY = 1.0       
REF_HAND_SIZE = 150          

# 判定距離
BASE_CLICK_DIST = 40         
MIN_CLICK_DIST = 10          
SCROLL_SENSITIVITY = 5

# ★スムージング設定（新しい設定）★
# alpha（0.0〜1.0）: 1.0に近いほど「反応優先」、0.0に近いほど「滑らかさ優先（遅延あり）」
MIN_ALPHA = 0.15  # 最も遠い時の反応速度（かなり滑らか＝遅延強め）
MAX_ALPHA = 0.8   # 最も近い時の反応速度（ほぼ生の動き＝キビキビ）

# 安全装置解除
pyautogui.FAILSAFE = False

# --- MediaPipe初期化 ---
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(min_detection_confidence=0.6)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# --- 変数 ---
# 前回の「スムージング適用後」の座標
prev_smooth_x, prev_smooth_y = 0, 0
is_first_frame = True
is_dragging = False
is_right_clicking = False
is_paused = False 

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

# ==================================================
# ★ 新機能：距離に応じたスムージング係数を計算する関数 ★
# ==================================================
def get_dynamic_smoothing_alpha(scale):
    """
    手の距離(scale)に応じて、指数移動平均の係数(alpha)を決定する。
    scaleが小さい（遠い）ほどalphaを小さくして、ブレを強力に抑制する。
    """
    # 線形補間を使って滑らかに変化させる
    # scaleが 0.5 (遠い) 以下なら MIN_ALPHA
    # scaleが 1.2 (近い) 以上なら MAX_ALPHA
    # その間は滑らかにつなぐ
    alpha = np.interp(scale, [0.5, 1.2], [MIN_ALPHA, MAX_ALPHA])
    return alpha

print("=== AIマウス v6 (距離可変スムージング搭載) ===")
print("遠距離：感度超アップ ＆ 手ブレ補正MAX")
print("近距離：感度ノーマル ＆ 反応速度MAX")
print("'q'キーで終了")

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_H, img_W, _ = img.shape

    # 1. 顔認識
    face_results = face_detection.process(img_rgb)
    if not face_results.detections:
        cv2.rectangle(img, (0, 0), (img_W, img_H), (0, 0, 0, 150), cv2.FILLED)
        cv2.putText(img, "NO FACE - PAUSED", (50, img_H // 2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # 手が見えなくなったら初期化フラグを立てる（復帰時の飛び防止）
        is_first_frame = True
    else:
        # 2. 手認識
        hand_results = hands.process(img_rgb)
        
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                def to_px(lm):
                    return int(lm.x * CAM_WIDTH), int(lm.y * CAM_HEIGHT)

                wrist = hand_landmarks.landmark[0]
                middle_mcp = hand_landmarks.landmark[9]
                
                thumb = hand_landmarks.landmark[4]
                index = hand_landmarks.landmark[8]
                middle = hand_landmarks.landmark[12]
                ring = hand_landmarks.landmark[16]
                pinky = hand_landmarks.landmark[20]

                # 生の座標を取得
                wx, wy = to_px(wrist)
                mmx, mmy = to_px(middle_mcp)
                raw_tx, raw_ty = to_px(thumb) # 親指（生データ）
                ix, iy = to_px(index)
                mx, my = to_px(middle)
                rx, ry = to_px(ring)
                px, py = to_px(pinky)

                # --- 距離・感度・判定エリア計算 ---
                current_hand_size = math.hypot(wx - mmx, wy - mmy)
                if current_hand_size < 10: current_hand_size = 10
                scale = current_hand_size / REF_HAND_SIZE

                # 感度 (遠いと急激に速く)
                dynamic_sensitivity = BASE_SENSITIVITY * ((1.0 / scale) ** 2)
                dynamic_sensitivity = np.clip(dynamic_sensitivity, 0.5, 12.0) # 上限を少し緩和

                # 判定距離 (遠いと狭く)
                dynamic_click_dist = BASE_CLICK_DIST * scale
                if dynamic_click_dist < MIN_CLICK_DIST:
                    dynamic_click_dist = MIN_CLICK_DIST

                # ==================================================
                # ★ スムージング処理の適用 ★
                # ==================================================
                if is_first_frame:
                    prev_smooth_x, prev_smooth_y = raw_tx, raw_ty
                    is_first_frame = False

                # 1. 現在の距離に応じた「滑らかさ係数(alpha)」を取得
                alpha = get_dynamic_smoothing_alpha(scale)

                # 2. 指数移動平均 (Exponential Moving Average) で座標を安定化
                # 新しい座標 = alpha * 生座標 + (1-alpha) * 前回の座標
                curr_smooth_x = alpha * raw_tx + (1 - alpha) * prev_smooth_x
                curr_smooth_y = alpha * raw_ty + (1 - alpha) * prev_smooth_y

                # 3. 移動量の計算には「安定化した座標」を使う
                delta_x = curr_smooth_x - prev_smooth_x
                delta_y = curr_smooth_y - prev_smooth_y
                
                # 次回のために保存
                prev_smooth_x, prev_smooth_y = curr_smooth_x, curr_smooth_y

                # デバッグ表示
                info_text = f"Scale:{scale:.2f} Sens:{dynamic_sensitivity:.1f} Alpha:{alpha:.2f}"
                cv2.putText(img, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                # ==================================================

                # --- クラッチ判定 (小指 + 親指) ---
                # 判定には「生の座標」または「補正後の座標」のどちらを使うか？
                # ここでは判定ミスを防ぐため、相対関係が崩れない「生座標(raw)」同士で距離を見るのが無難
                dist_pinky = math.hypot(raw_tx - px, raw_ty - py)
                
                if dist_pinky < (dynamic_click_dist * 1.2):
                    is_paused = True
                    cv2.circle(img, (px, py), 15, (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, "CLUTCH PAUSED", (int(curr_smooth_x), int(curr_smooth_y) - 40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                else:
                    is_paused = False
                    cv2.circle(img, (px, py), 8, (0, 255, 0), 2)

                # --- アクション ---
                if not is_paused:
                    # スクロール (薬指)
                    dist_ring = math.hypot(raw_tx - rx, raw_ty - ry)
                    if dist_ring < dynamic_click_dist:
                        scroll_amount = int(-delta_y * SCROLL_SENSITIVITY)
                        if abs(scroll_amount) > 0:
                            pyautogui.scroll(scroll_amount)
                        cv2.circle(img, (rx, ry), int(dynamic_click_dist/2), (0, 165, 255), cv2.FILLED)
                    
                    else:
                        # カーソル移動
                        move_x = delta_x * dynamic_sensitivity
                        move_y = delta_y * dynamic_sensitivity
                        
                        # 微小な動きをカットしてさらに震え防止（オプション）
                        if abs(move_x) < 0.5: move_x = 0
                        if abs(move_y) < 0.5: move_y = 0

                        pyautogui.moveRel(move_x, move_y, _pause=False)
                        
                        # 描画は安定化した座標で行うと見やすい
                        cv2.circle(img, (int(curr_smooth_x), int(curr_smooth_y)), 5, (255, 0, 255), cv2.FILLED)

                        # 左クリック (人差し指)
                        dist_index = math.hypot(raw_tx - ix, raw_ty - iy)
                        if dist_index < dynamic_click_dist:
                            cv2.circle(img, (ix, iy), int(dynamic_click_dist/2), (0, 255, 0), cv2.FILLED)
                            if not is_dragging:
                                pyautogui.mouseDown()
                                is_dragging = True
                        else:
                            if is_dragging:
                                pyautogui.mouseUp()
                                is_dragging = False

                        # 右クリック (中指)
                        dist_middle = math.hypot(raw_tx - mx, raw_ty - my)
                        if dist_middle < dynamic_click_dist:
                            cv2.circle(img, (mx, my), int(dynamic_click_dist/2), (255, 0, 0), cv2.FILLED)
                            if not is_right_clicking:
                                pyautogui.rightClick()
                                is_right_clicking = True
                        else:
                            is_right_clicking = False
        else:
            is_first_frame = True

    cv2.imshow("AI Mouse v6 (Dynamic Smoothing)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()