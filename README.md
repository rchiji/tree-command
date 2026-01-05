# tree-command

拡張子ごとにファイルをグループ化し、**大量のファイルは中略して表示するツリー表示ツール**。  
中略部分は、例えば以下のようになる:

... (304 .tif files total)


## 使い方

```powershell
tree2 C:\path\to\dir --threshold 50 --head 3 --tail 2
```

## オプション

 - --threshold / -t  
 1つの拡張子グループに含まれるファイル数がこの数を超えると中略（デフォルト: 10）
 - --head  
 中略時に先頭に表示する件数（デフォルト: 3）
 - --tail  
 中略時に末尾に表示する件数（デフォルト: 2）
 - --level / -L  
 表示する最大階層。
 --level 1 ならルート直下だけ、--level 2 ならサブディレクトリ1段階まで。
デフォルトは 0（無制限）。
 - --no-hidden  
 隠しファイル・ディレクトリを非表示にします。
デフォルトでは 表示 されます。


## Windows への簡単インストール方法

1. 任意の場所にフォルダを作成（例: C:\Users\\\<username>\bin）

2. このフォルダに tree2.py をコピー

3. 同じフォルダに tree2.bat を作成し、内容を以下のようにする:

```
@echo off
python "%~dp0tree2.py" %*
```

4. 環境変数 PATH に C:\Users\\\<username>\bin を追加
（コントロールパネル → システム → 詳細設定 → 環境変数。pathの項目に追加）

5. 新しい PowerShell を開いて動作確認:
```
tree2 --help
```

![alt text](image-1.png)

## 表示例

```
tree2 Images
```
```
Images/
├── raw/
│   ├── F001_ch0_raw.tif
│   ├── F001_ch1_raw.tif
│   ├── F001_ch2_raw.tif
│       ... (1520 .tif files total)
│   ├── F304_ch3_raw.tif
│   └── F304_ch4_raw.tif
├── Thumbs.db
```

## 注意

罫線（├──, └──, │）が文字化けする場合は PowerShell を使用したほうがいいかも


# LINUXへの導入例

```
mkdir -p ~/.local/bin
curl -L https://raw.githubusercontent.com/rchiji/tree-command/main/tree2.py -o ~/.local/bin/tree2
chmod +x ~/.local/bin/tree2
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```
shellを再起動して（.bashrcを読み込み直して）、`tree2 --help`が通れば成功。（`~/.local/bin/tree2 --help`と呼んでも良い。）


CMD を使う場合は chcp 65001 で UTF-8 に切り替えると改善することがある。


