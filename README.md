# hand_mouse_controller
Hand Mouse Controller
This application allows you to control the mouse cursor using your hand gestures, powered by Google MediaPipe. I have tested it by playing digital board games and found the performance to be smooth enough for regular gameplay, so I am releasing it to the public.

⚠️ Installation & Known Issues (Please Read)
1. Directory Path Limitation
Due to a characteristic (or bug) of MediaPipe, this application will not work if placed in a directory path containing Japanese characters (non-ASCII characters).

Fix: If your Windows username contains Japanese characters, please place the application folder directly under the C: drive (e.g., C:\hand_mouse_v4).

2. Execution
Due to a bug involving MediaPipe and Python during the build process, I was unable to compile this into a single standalone .exe file.

How to Run: Please download the entire hand_mouse_v4 folder and launch hand_mouse_v4.exe located inside. Do not separate the exe from the folder.

🎮 Controls
Cursor Movement: Your Thumb acts as the reference point (cursor).

Left Click: Pinch Index Finger + Thumb.

Right Click: Pinch Middle Finger + Thumb.

Mouse Wheel (Scroll): Pinch Ring Finger + Thumb and move your hand up or down.

Inactive Mode (Lift Mouse): Pinch Pinky + Thumb.

This stops cursor movement, similar to lifting a physical mouse off the desk.

⚙️ Features & Mechanics
Face Detection Safety: Mouse control is only active when the user's face is recognized by the camera. If you look away or leave the frame, the mouse becomes inactive.

Depth Sensitivity: The application recognizes depth. The further your hand is from the camera, the higher the mouse sensitivity becomes.

❌ How to Exit
To close the application, ensure the camera window is in focus and press the [Q] key.

手でマウス操作ができます。googleのmediapipeを使用していて、それらの特性（というかバグ）で日本語下のディレクトリでは動かないのでユーザー名が日本語の人はCドライブ直下などに配置して使ってください。
それとmedeapipeとpythonのバグでビルドする際に一つの.exeファイルにどうしてもまとめられなかったのでhand_mouse_v4ごとダウンロードして中のhand_mouse_v4.exeを起動してください。
ユーザーの顔が認識されなければマウス操作は非アクティブになります。これを使ってボードゲームをしてみましたが、普通にプレイできるレベルまで持ってこれたので公開したいと思います。
親指が基点（カーソル）
人差し指と親指をくっつけると左クリック
中指と親指をくっつけると右クリック
薬指と親指をくっつけた状態で上下に動かすとマウスホイールを動かしているのと同じ状態
小指と親指をくっつけた状態は非アクティブとなり、マウスを話しているような状態になります。

奥行を認識していて、手をカメラから離せば離すほど感度が高くなります。
アプリケーションはカメラ画面にフォーカスして[Q]キーを押すことで終了できます。

