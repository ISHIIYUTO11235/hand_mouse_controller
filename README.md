# hand_mouse_controller

Google MediaPipe を用いたハンドジェスチャによる**マウス操作アプリ**。デジタルボードゲームを実際にプレイできるレベルの操作性を確認したうえで公開しています。

## 概要

カメラに映した手のジェスチャだけでカーソル移動・クリック・スクロールを行えます。親指を基点としたピンチ操作で各種マウス動作にマッピングしており、物理マウスに近い感覚で扱えるよう設計しました。

## 操作方法

| 動作 | ジェスチャ |
|------|-----------|
| カーソル移動 | 親指を基点に手を動かす |
| 左クリック | 人差し指 + 親指をピンチ |
| 右クリック | 中指 + 親指をピンチ |
| スクロール | 薬指 + 親指をピンチして上下に移動 |
| 非アクティブ（マウスを浮かせる相当） | 小指 + 親指をピンチ |
| 終了 | カメラ画面をフォーカスして `Q` キー |

## 工夫した点

- **顔検出による安全機構**：ユーザーの顔がカメラに認識されているときのみマウス操作が有効。視線を外す・フレームから外れると自動で非アクティブになり、誤操作を防止。
- **奥行きに応じた感度調整**：手がカメラから遠いほど感度が上がる仕組みで、大きな移動と細かい操作を両立。
- **「マウスを浮かせる」概念の再現**：小指ピンチで一時的に操作を切り、物理マウスの持ち上げと同じ感覚で位置をリセットできる。

## 使用技術

- **言語**: Python（**3.10系**推奨）
- **ハンドトラッキング**: Google MediaPipe
- **マウス制御**: OSレベルのカーソル/クリック操作

## セットアップ・既知の問題（必読）

1. **Python 3.10 必須**：MediaPipe の都合上、3.10系でないと動作しません。仮想環境の利用を推奨します。
2. **日本語パス非対応**：MediaPipe の特性（バグ）により、**非ASCII文字（日本語）を含むパス**では動作しません。Windowsのユーザー名が日本語の場合は、フォルダを **Cドライブ直下**（例：`C:\hand_mouse_v4`）に配置してください。
3. **実行方法**：単一 `.exe` へのビルドができなかったため、`hand_mouse_v4` フォルダごとダウンロードし、中の `hand_mouse_v4.exe` を起動してください（exeをフォルダから分離しないこと）。ビルド済みファイルは容量が大きくアップロードできなかったため、本リポジトリにはコードのみを置いています。


# hand_mouse_controller
Hand Mouse Controller
This application allows you to control the mouse cursor using your hand gestures, powered by Google MediaPipe. I have tested it by playing digital board games and found the performance to be smooth enough for regular gameplay, so I am releasing it to the public.
The built file was too large to upload, so I'll just leave the code. Mediapipe won't work unless you're using Python 3.10, so please create a virtual environment.
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
ビルドしたファイルはファイルが多すぎてアップロードできなかったのでコードだけおいていきます。python3.10あたりじゃないとmediapipeはうごかないので仮想環境をうまく作ってください。
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

