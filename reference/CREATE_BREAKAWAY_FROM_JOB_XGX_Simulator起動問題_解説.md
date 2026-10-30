# `CREATE_BREAKAWAY_FROM_JOB` で XG-X Simulator が起動できた理由

## 1. 今回の現象

Python から KEYENCE XG-X Simulator を起動するため、最初は次のような
シンプルなコードを使用しました。

``` python
import subprocess


SIMULATOR = (
    r"C:\Program Files (x86)\KEYENCE"
    r"\XG-X VisionEditor H1X\sim\XG-X Simulator.exe"
)

BOOT_FILE = (
    r"C:\Users\fumih\Desktop"
    r"\basler_camera_test\XG_SimBoot.dat"
)


subprocess.Popen(
    [
        SIMULATOR,
        BOOT_FILE,
    ]
)
```

このコードでは、実行方法によって結果が異なりました。

  実行方法                           結果
  ---------------------------------- --------------
  Pythonファイルをダブルクリック     起動できる
  VS Code右上の「Run Python File」   起動できる
  VS CodeでF5（デバッグ実行）        起動できない

つまり、Pythonコードや実行ファイルのパスそのものには問題がなく、 **VS
CodeのF5によるデバッグ実行時だけ問題が発生していました。**

------------------------------------------------------------------------

## 2. 最終的に解決したコード

`subprocess.Popen()` に次のオプションを追加すると、 VS
CodeのF5からも正常にXG-X Simulatorを起動できました。

``` python
creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB,
```

完成したコードは次のとおりです。

``` python
import subprocess


SIMULATOR = (
    r"C:\Program Files (x86)\KEYENCE"
    r"\XG-X VisionEditor H1X\sim\XG-X Simulator.exe"
)

BOOT_FILE = (
    r"C:\Users\fumih\Desktop"
    r"\basler_camera_test\XG_SimBoot.dat"
)


subprocess.Popen(
    [
        SIMULATOR,
        BOOT_FILE,
    ],
    # Allow the simulator to run correctly from the VS Code debugger
    creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB,
)
```

------------------------------------------------------------------------

## 3. `creationflags` とは

`creationflags` は、Windowsで新しいプロセスを作成するときの動作を
指定する `subprocess.Popen()` のオプションです。

Pythonの `subprocess` はWindowsでは内部的にWindowsのプロセス生成機能を
利用します。

例えば、次のようなフラグがあります。

-   `CREATE_NEW_CONSOLE`
-   `CREATE_NO_WINDOW`
-   `DETACHED_PROCESS`
-   `CREATE_BREAKAWAY_FROM_JOB`

今回使用したのは、

``` python
subprocess.CREATE_BREAKAWAY_FROM_JOB
```

です。

Python公式ドキュメントでは、このフラグは新しいプロセスを
**Job（ジョブ）に関連付けないためのフラグ**として説明されています。

------------------------------------------------------------------------

## 4. Windowsの「Job」とは

ここでいう Job は、一般的な「仕事」という意味ではなく、 Windowsの **Job
Object（ジョブ オブジェクト）** という仕組みです。

Job Objectを使うと、複数のプロセスをひとまとまりとして管理できます。

イメージとしては次のようになります。

``` text
Job
├─ Process A
├─ Process B
└─ Process C
```

Jobには、関連付けられたプロセスに対して、

-   プロセスの管理
-   リソース制限
-   優先度などの制限
-   プロセスツリーの監視
-   一括終了

などを行う仕組みがあります。

Microsoftの公式ドキュメントによると、Jobに所属しているプロセスが
新しい子プロセスを作成すると、**通常はその子プロセスも同じJobに
関連付けられます。**

つまり、

``` text
親プロセス
    │
    └─ 子プロセス
```

という単純な関係だけでなく、

``` text
Job
├─ 親プロセス
└─ 子プロセス
```

という管理関係が生まれる場合があります。

------------------------------------------------------------------------

## 5. 今回のF5実行で起きていたと考えられること

今回の検証では、次のことを確認しました。

### 通常実行

``` text
VS Code
    ↓
Run Python File
    ↓
Python
    ↓
subprocess.Popen()
    ↓
XG-X Simulator
    ↓
正常起動
```

### F5デバッグ実行

``` text
VS Code
    ↓
Python Debugger
    ↓
Python
    ↓
subprocess.Popen()
    ↓
XG-X Simulator
    ↓
起動しない
```

さらに、通常実行とF5実行について、

-   使用しているPython
-   `VIRTUAL_ENV`
-   `PATH`
-   `PYTHONPATH`
-   `PYTHONHOME`

を比較しましたが、実質的な違いは見つかりませんでした。

また、

-   `cwd` の指定
-   `shell=True`
-   `cmd /c`
-   `DETACHED_PROCESS`
-   `launch.json`
-   `"subProcess": false`

なども本質的な解決にはなりませんでした。

最終的に、

``` python
creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB
```

を指定したときだけ、F5でも正常起動しました。

------------------------------------------------------------------------

## 6. なぜ `CREATE_BREAKAWAY_FROM_JOB` で解決したのか

今回の実験結果から考えると、F5でデバッグ実行したPythonから XG-X
Simulatorを起動したとき、Simulatorが親側のJob環境の影響を
受けていた可能性が高いと考えられます。

通常の `Popen()` では、

``` text
VS Code / デバッグ環境
        │
        └─ Python
              │
              └─ XG-X Simulator
```

というプロセスツリーの中で、XG-X Simulatorも親側のJobに
関連付けられる可能性があります。

そこで、

``` python
creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB
```

を指定すると、新しく作成するXG-X SimulatorをそのJobから **break
away（離脱）**させるようWindowsに要求します。

イメージとしては、

``` text
VS Code / デバッグ環境
        │
        └─ Python
              │
              └─ XG-X Simulator
                    ↑
              Jobから切り離して起動
```

となります。

その結果、XG-X SimulatorがVS Codeのデバッグ実行環境側のJobの
影響を受けにくくなり、正常に起動できたと考えられます。

------------------------------------------------------------------------

## 7. 「原因が完全に証明された」わけではない点に注意

今回確実に確認できた事実は、

``` text
通常のPopen()                         → F5では起動しない
CREATE_BREAKAWAY_FROM_JOB付きPopen() → F5でも起動する
```

ということです。

したがって、

**WindowsのJobへの関連付けが今回の現象に関係していた可能性は非常に高い**

と考えられます。

ただし、XG-X Simulator内部の処理内容は確認していないため、

> XG-X Simulator内部のこの処理がJobによって失敗した

というところまで特定できたわけではありません。

そのため、技術的には

> F5デバッグ実行時のプロセス管理環境とXG-X Simulatorの組み合わせで
> 問題が発生し、`CREATE_BREAKAWAY_FROM_JOB` によってその影響を
> 回避できた

と理解するのが安全です。

------------------------------------------------------------------------

## 8. 仮想環境（venv）が原因ではなかった

途中ではPythonの仮想環境が原因である可能性も疑いました。

しかし、右上の「Run Python File」で正常起動したときも、

``` text
Python:
C:\Users\fumih\Desktop\basler_camera_test\.venv\Scripts\python.exe
```

が使用されていました。

さらに、

``` text
VIRTUAL_ENV:
C:\Users\fumih\Desktop\basler_camera_test\.venv
```

も設定されていました。

つまり、

``` text
venv + 通常実行 → 起動できる
venv + F5       → 起動できない
```

だったため、**venvそのものが原因ではありませんでした。**

これは今後、Basler用の `pypylon` やOpenCVを入れた仮想環境を
そのまま使用できるという意味でも重要です。

------------------------------------------------------------------------

## 9. `DETACHED_PROCESS` との違い

似た名前のオプションとして、

``` python
subprocess.DETACHED_PROCESS
```

があります。

これは主に、

**新しいプロセスが親プロセスのコンソールを継承しない**

ためのフラグです。

一方、

``` python
subprocess.CREATE_BREAKAWAY_FROM_JOB
```

は、

**新しいプロセスをJobに関連付けない**

ためのフラグです。

今回問題になっていたのは単なるコンソールの継承ではなく、
Jobによるプロセス管理側だったと考えられるため、
`CREATE_BREAKAWAY_FROM_JOB` が有効でした。

------------------------------------------------------------------------

## 10. 今回のポイント

今回のトラブルから得られた重要なポイントは次のとおりです。

``` text
Popen()で外部GUIアプリを起動できない
        ↓
パスや引数だけが原因とは限らない
        ↓
実行元のプロセス管理環境が影響する場合がある
        ↓
WindowsではJob Objectの影響も考えられる
        ↓
CREATE_BREAKAWAY_FROM_JOB が有効な場合がある
```

特に、

``` text
ダブルクリックでは動く
通常実行では動く
F5デバッグ実行だけ動かない
```

という場合は、Pythonコードそのものだけでなく、
**デバッガーや親プロセスの実行環境の違い**を疑う価値があります。

------------------------------------------------------------------------

## 11. 今回の最終コード

今後の基準コードは次の形とします。

``` python
import subprocess


SIMULATOR = (
    r"C:\Program Files (x86)\KEYENCE"
    r"\XG-X VisionEditor H1X\sim\XG-X Simulator.exe"
)

BOOT_FILE = (
    r"C:\Users\fumih\Desktop"
    r"\basler_camera_test\XG_SimBoot.dat"
)


subprocess.Popen(
    [
        SIMULATOR,
        BOOT_FILE,
    ],
    # Allow the simulator to run correctly from the VS Code debugger
    creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB,
)
```

この形なら、

``` text
.py ダブルクリック
VS CodeのRun Python File
VS CodeのF5デバッグ実行
```

のいずれでもXG-X Simulatorを起動できることを確認済みです。

------------------------------------------------------------------------

## 参考資料

-   Python `subprocess` 公式ドキュメント\
    https://docs.python.org/ja/3/library/subprocess.html

-   Microsoft Learn - Job Objects\
    https://learn.microsoft.com/ja-jp/windows/win32/procthread/job-objects
