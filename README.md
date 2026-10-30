# basler_camera_control

BaslerカメラをPythonから操作するためのプロジェクトです。

Baslerカメラからの静止画・連続画像の取得に加え、 KEYENCE XG-X
VisionEditor Simulatorで使用する2M画像フォーマットへの変換や、 XG-X
Simulatorの起動・GUI操作を行います。

## 主な機能

-   Baslerカメラから静止画を取得
-   Baslerカメラから連続画像を取得
-   取得画像をOpenCVで表示・保存
-   Basler画像をKEYENCE XG-X用2M画像フォーマットへ変換
-   XG-X VisionEditor SimulatorをPythonから起動
-   XG-X Simulatorのウィンドウ位置・サイズを設定
-   PyGetWindowでXG-X Simulatorを前面化
-   PyAutoGUIでXG-X Simulatorへキー入力

今後、PyAutoGUIなどを使用して画面状態を確認しながら操作する
RPA的な自動化への発展も想定しています。

------------------------------------------------------------------------

## 動作環境

-   Windows
-   Python
-   Basler pylon Software Suite
-   Basler USB3 Vision Camera
-   KEYENCE XG-X VisionEditor Simulator

本プロジェクトではBaslerカメラの制御に `pypylon` を使用します。

------------------------------------------------------------------------

## セットアップ

### 1. 仮想環境の作成

プロジェクトフォルダで次のコマンドを実行します。

``` bash
python -m venv .venv
```

### 2. 仮想環境の有効化

Windowsの場合：

``` bash
.venv\Scripts\activate
```

### 3. 必要なPythonパッケージのインストール

``` bash
pip install -r requirements.txt
```

`requirements.txt` には次のパッケージを登録しています。

``` text
opencv-python
pypylon
pyautogui
PyGetWindow
```

------------------------------------------------------------------------

## ファイル構成

``` text
basler_camera_control/
├─ capture_image.py
├─ capture_video.py
├─ capture_image_keyence_2m_format.py
├─ launch_xgx_simulator.py
├─ XG_SimBoot.dat
├─ requirements.txt
└─ README.md
```

### capture_image.py

Baslerカメラから静止画を1枚取得します。

取得した画像はPNG形式で保存し、OpenCVのウィンドウにも表示します。

### capture_video.py

Baslerカメラから画像を連続取得してOpenCVで表示します。

`ESC` キーを押すと終了します。

### capture_image_keyence_2m_format.py

Baslerカメラで取得した画像を、 KEYENCE
XG-Xで使用できる2M画像フォーマットへ変換します。

現在の変換内容は次のとおりです。

``` text
Basler画像
1920 x 1080
    ↓
左右を中央基準でクロップ
1920 → 1600
    ↓
上下に黒帯を60 pixelずつ追加
    ↓
1600 x 1200
    ↓
BMP形式で保存
```

リサイズは行わず、中央部分をクロップして使用します。

### launch_xgx_simulator.py

KEYENCE XG-X VisionEditor Simulatorを起動します。

`XG_SimBoot.dat` は、Pythonファイルと同じプロジェクトフォルダから
自動的に絶対パスを取得します。

Simulator起動後は対象ウィンドウが表示されるまで待機し、
ウィンドウ位置・サイズを設定して前面化した後、`T` キーを送信します。

ウィンドウが一定時間内に見つからない場合は、
タイムアウトエラーとして処理を終了します。

------------------------------------------------------------------------

## XG_SimBoot.datについて

`launch_xgx_simulator.py` を使用する場合は、 `XG_SimBoot.dat`
をプロジェクトフォルダへ配置してください。

``` text
basler_camera_control/
├─ launch_xgx_simulator.py
└─ XG_SimBoot.dat
```

`XG_SimBoot.dat` が見つからない場合、
プログラムは処理を停止して保存元フォルダを表示します。

``` text
"C:\ProgramData\KEYENCE\XG-H7N\Vision Editor"
```

使用する `XG_SimBoot.dat` をこのフォルダから
プロジェクトフォルダへコピーして使用します。

------------------------------------------------------------------------

## XG-X Simulatorのウィンドウ操作

現在はPyGetWindowとPyAutoGUIを使用しています。

PyGetWindow：

``` python
windows = gw.getWindowsWithTitle("Baslerテスト")
window = windows[0]
window.activate()
```

PyAutoGUI：

``` python
pyautogui.press("t")
```

この構成により、Windows APIを直接操作するコードを大量に記述せず、
比較的シンプルなPythonコードでGUI操作を行えます。

将来的には、

``` text
画面を確認
    ↓
特定の表示を検出
    ↓
状態を判断
    ↓
キー入力・クリック
```

といったRPA的な処理への拡張を想定しています。

------------------------------------------------------------------------

## 使用ライブラリ

### pypylon

Basler pylon SDKをPythonから使用するためのライブラリです。

カメラ接続、撮像、連続取得などに使用します。

### OpenCV

取得画像の表示・保存・画像変換に使用します。

Pythonでは次の名前でインポートします。

``` python
import cv2
```

### PyAutoGUI

キーボード入力やマウス操作など、 GUIの自動操作に使用します。

現在はXG-X Simulatorへ `T` キーを送信するために使用しています。

### PyGetWindow

Windows上のウィンドウ検索・位置変更・サイズ変更・前面化に使用します。

------------------------------------------------------------------------

## 注意事項

### Basler pylon Software Suite

`pypylon` を使用する前に、 Basler pylon Software
Suiteおよびカメラドライバが
正常にインストールされていることを確認してください。

### XG-X Simulator

XG-X Simulatorの実行ファイルは、
現在の環境では次の場所を使用しています。

``` text
C:\Program Files (x86)\KEYENCE\XG-X VisionEditor H1X\sim\XG-X Simulator.exe
```

環境によってインストール先が異なる場合は、 `launch_xgx_simulator.py`
の設定を変更してください。

### GUI自動操作

PyAutoGUIによるキー入力は、
対象ウィンドウの状態によって結果が変わる可能性があります。

そのため `launch_xgx_simulator.py` では、
PyGetWindowを使用して対象のXG-X Simulatorウィンドウを検索し、
前面化してからキー入力を行います。

------------------------------------------------------------------------

## 今後の拡張候補

-   Baslerカメラの露光時間設定
-   Gain設定
-   撮像条件の設定ファイル化
-   画像保存先の設定
-   XG-X Simulatorとの連続テスト
-   PyAutoGUIによるマウス操作
-   画面上の特定画像の検出
-   XG-X Simulatorの状態判定
-   GUI操作の自動化
-   OpenCVを利用した画面状態判定

------------------------------------------------------------------------

## 方針

本プロジェクトでは、必要以上に複雑な構成にせず、
シンプルで読みやすいPythonコードを優先します。

``` text
KISS
Keep It Simple
```

まず確実に動く小さな処理を作り、
必要になった機能を順番に追加していく方針です。
