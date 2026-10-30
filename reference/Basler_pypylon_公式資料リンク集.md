# Basler pypylon 公式資料リンク集

Basler製カメラをPythonから操作する際に参照する公式資料をまとめる。

## 使用環境

``` text
Camera: Basler acA1920-25um
Interface: USB 3.0
pylon Software Suite: 26.08
pypylon: 26.9
OpenCV: opencv-python
```

------------------------------------------------------------------------

## 1. pypylon 公式ドキュメント

### Basler Product Documentation - pypylon Introduction

https://docs.baslerweb.com/pypylon-introduction

日本語版：

https://ja.docs.baslerweb.com/pypylon-introduction

pypylonはBasler pylon C++ APIの公式Pythonバインディング。
PythonからBaslerカメラを制御し、画像を取得するための基本資料として使用する。

------------------------------------------------------------------------

## 2. pypylon 公式GitHub

### basler/pypylon

https://github.com/basler/pypylon

主な用途：

-   pypylonのインストール方法
-   最新APIの確認
-   サンプルコード
-   変更履歴
-   Programmer's Guide
-   Issueの確認

pypylonはバージョンによって推奨APIが変更される場合があるため、
古いWeb記事より公式GitHubを優先して確認する。

------------------------------------------------------------------------

## 3. pypylon Programmer's Guide

https://github.com/basler/pypylon/tree/master/docs/programmers_guide

カメラ接続、パラメータ操作、画像取得など、
Pythonアプリケーションを作成するときの詳しい基準資料。

------------------------------------------------------------------------

## 4. pypylon 公式サンプル

https://github.com/basler/pypylon/tree/master/samples

シンプルな実装例を確認したい場合に使用する。
特に画像取得処理の基本形を確認するときに便利。

------------------------------------------------------------------------

## 5. pypylon-samples

https://github.com/basler/pypylon-samples

Basler公式のサンプル集。 PythonスクリプトだけでなくJupyter
Notebookのサンプルも含まれる。

主な内容：

-   カメラ列挙・基本設定
-   Grab Strategy
-   複数カメラ
-   ハードウェアトリガー
-   USBカメラ
-   OpenCV連携
-   Exposure Sequencer
-   HDR
-   Serial Communication

画像検査アプリを開発するときに参考になる。

なお、サンプル集には最新のpypylon APIやコーディングスタイルを
常に反映しているとは限らない旨の注意書きがある。
最新の記述方法はpypylon本体のREADMEや変更履歴も確認する。

------------------------------------------------------------------------

## 6. OpenCVとの連携

### Basler公式 - Integration with OpenCV

https://docs.baslerweb.com/pypylon-integration-with-opencv

日本語版：

https://ja.docs.baslerweb.com/pypylon-integration-with-opencv

基本的な流れ：

``` text
Basler Camera
      ↓
   pypylon
      ↓
 NumPy Array
      ↓
   OpenCV
      ↓
表示・保存・画像処理
```

pypylonで取得した画像はNumPy配列として扱えるため、
OpenCVとの連携が容易。

今回のサンプルでも、

``` python
image = grab_result.Array
```

で画像を取得し、

``` python
cv2.imshow("Basler Camera", image)
cv2.imwrite("image.png", image)
```

のようにOpenCVへ渡している。

------------------------------------------------------------------------

## 7. pypylon 26.6以降のAPI記述

pypylon 26.6では変更が導入されているため、
古いサンプルコードを使用するときは注意する。

以前の記述例：

``` python
camera.Gain = 42
```

現在推奨されている記述：

``` python
camera.Gain.Value = 42
```

パラメータAPIでは、例えば以下のような操作も可能。

``` python
camera.ExposureTime.SetToMaximum()
camera.PixelFormat.TrySetValue("Mono8")
```

今回使用しているのは `pypylon 26.9` なので、
今後は新しいAPIスタイルを基本とする。

------------------------------------------------------------------------

## 8. 今後特に参照しそうな項目

acA1920-25umを画像検査用途で使用する場合、
特に以下を確認する可能性が高い。

``` text
Exposure Time
Gain
Pixel Format
ROI
Grab Strategy
Hardware Trigger
Software Trigger
Continuous Acquisition
Image Saving
OpenCV Integration
```

特にハードウェアトリガーについては、
pypylon-samplesにUSBカメラ向けサンプルが用意されている。

------------------------------------------------------------------------

## 9. 資料を確認する優先順位

``` text
1. Basler Product Documentation
        ↓
2. basler/pypylon 公式GitHub
        ↓
3. pypylon Programmer's Guide
        ↓
4. basler/pypylon-samples
        ↓
5. その他のWeb記事
```

第三者の記事よりBasler公式資料を優先する。

------------------------------------------------------------------------

## 10. 今回作成した最小サンプル

``` text
capture_image.py
    1枚撮像
    PNG保存
    OpenCV表示

capture_video.py
    連続撮像
    OpenCVライブ表示
    ESCキーで終了
```

これらを最小サンプルとして残し、
今後のカメラ制御プログラム作成時のベースとして使用する。

------------------------------------------------------------------------

## まとめ

PythonからBaslerカメラを使用するときの中心となるライブラリは
Basler公式の `pypylon`。

``` text
Basler Camera
      ↓
pylon
      ↓
pypylon
      ↓
NumPy
      ↓
OpenCV
```

カメラ固有の制御はpypylonに任せ、
取得後の画像表示・保存・画像処理は通常のOpenCVとして扱える。

APIの使用方法を確認するときは、
まずBasler公式pypylonドキュメントと公式GitHubを参照する。
